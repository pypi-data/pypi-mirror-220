import abc
from functools import partial
import math

import sympy as sp
from sympy.core.cache import cacheit

from pystencils.astnodes import Block, Conditional
from pystencils.typing import TypedSymbol, create_type
from pystencils.integer_functions import div_ceil, div_floor
from pystencils.slicing import normalize_slice
from pystencils.sympyextensions import is_integer_sequence, prod


class ThreadIndexingSymbol(TypedSymbol):
    def __new__(cls, *args, **kwds):
        obj = ThreadIndexingSymbol.__xnew_cached_(cls, *args, **kwds)
        return obj

    def __new_stage2__(cls, name, dtype, *args, **kwargs):
        obj = super(ThreadIndexingSymbol, cls).__xnew__(cls, name, dtype, *args, **kwargs)
        return obj

    __xnew__ = staticmethod(__new_stage2__)
    __xnew_cached_ = staticmethod(cacheit(__new_stage2__))


BLOCK_IDX = [ThreadIndexingSymbol("blockIdx." + coord, create_type("int32")) for coord in ('x', 'y', 'z')]
THREAD_IDX = [ThreadIndexingSymbol("threadIdx." + coord, create_type("int32")) for coord in ('x', 'y', 'z')]
BLOCK_DIM = [ThreadIndexingSymbol("blockDim." + coord, create_type("int32")) for coord in ('x', 'y', 'z')]
GRID_DIM = [ThreadIndexingSymbol("gridDim." + coord, create_type("int32")) for coord in ('x', 'y', 'z')]


class AbstractIndexing(abc.ABC):
    """
    Abstract base class for all Indexing classes. An Indexing class defines how a multidimensional
    field is mapped to GPU's block and grid system. It calculates indices based on GPU's thread and block indices
    and computes the number of blocks and threads a kernel is started with. The Indexing class is created with
    a pystencils field, a slice to iterate over, and further optional parameters that must have default values.
    """

    @property
    @abc.abstractmethod
    def coordinates(self):
        """Returns a sequence of coordinate expressions for (x,y,z) depending on symbolic GPU block and thread indices.
        These symbolic indices can be obtained with the method `index_variables` """

    @property
    def index_variables(self):
        """Sympy symbols for GPU's block and thread indices, and block and grid dimensions. """
        return BLOCK_IDX + THREAD_IDX + BLOCK_DIM + GRID_DIM

    @abc.abstractmethod
    def call_parameters(self, arr_shape):
        """Determine grid and block size for kernel call.

        Args:
            arr_shape: the numeric (not symbolic) shape of the array
        Returns:
            dict with keys 'blocks' and 'threads' with tuple values for number of (x,y,z) threads and blocks
            the kernel should be started with
        """

    @abc.abstractmethod
    def guard(self, kernel_content, arr_shape):
        """In some indexing schemes not all threads of a block execute the kernel content.

        This function can return a Conditional ast node, defining this execution guard.

        Args:
            kernel_content: the actual kernel contents which can e.g. be put into the Conditional node as true block
            arr_shape: the numeric or symbolic shape of the field

        Returns:
            ast node, which is put inside the kernel function
        """

    @abc.abstractmethod
    def max_threads_per_block(self):
        """Return maximal number of threads per block for launch bounds. If this cannot be determined without
        knowing the array shape return None for unknown """

    @abc.abstractmethod
    def symbolic_parameters(self):
        """Set of symbols required in call_parameters code"""


# -------------------------------------------- Implementations ---------------------------------------------------------


class BlockIndexing(AbstractIndexing):
    """Generic indexing scheme that maps sub-blocks of an array to GPU blocks.

    Args:
        field: pystencils field (common to all Indexing classes)
        iteration_slice: slice that defines rectangular subarea which is iterated over
        permute_block_size_dependent_on_layout: if True the block_size is permuted such that the fastest coordinate
                                                gets the largest amount of threads
        compile_time_block_size: compile in concrete block size, otherwise the gpu variable 'blockDim' is used
        maximum_block_size: maximum block size that is possible for the GPU. Set to 'auto' to let cupy define the
                            maximum block size from the device properties
        device_number: device number of the used GPU. By default, the zeroth device is used.
    """

    def __init__(self, field, iteration_slice,
                 block_size=(16, 16, 1), permute_block_size_dependent_on_layout=True, compile_time_block_size=False,
                 maximum_block_size=(1024, 1024, 64), device_number=None):
        if field.spatial_dimensions > 3:
            raise NotImplementedError("This indexing scheme supports at most 3 spatial dimensions")

        if permute_block_size_dependent_on_layout:
            block_size = self.permute_block_size_according_to_layout(block_size, field.layout)

        self._block_size = block_size
        if maximum_block_size == 'auto':
            assert device_number is not None, 'If "maximum_block_size" is set to "auto" a device number must be stated'
            # Get device limits
            import cupy as cp
            # See https://github.com/cupy/cupy/issues/7676
            if cp.cuda.runtime.is_hip:
                maximum_block_size = tuple(cp.cuda.runtime.deviceGetAttribute(i, device_number) for i in range(26, 29))
            else:
                da = cp.cuda.Device(device_number).attributes
                maximum_block_size = tuple(da[f"MaxBlockDim{c}"] for c in ["X", "Y", "Z"])

        self._maximum_block_size = maximum_block_size
        self._iterationSlice = normalize_slice(iteration_slice, field.spatial_shape)
        self._dim = field.spatial_dimensions
        self._symbolic_shape = [e if isinstance(e, sp.Basic) else None for e in field.spatial_shape]
        self._compile_time_block_size = compile_time_block_size
        self._device_number = device_number

    @property
    def cuda_indices(self):
        block_size = self._block_size if self._compile_time_block_size else BLOCK_DIM
        indices = [block_index * bs + thread_idx
                   for block_index, bs, thread_idx in zip(BLOCK_IDX, block_size, THREAD_IDX)]

        return indices[:self._dim]

    @property
    def coordinates(self):
        offsets = _get_start_from_slice(self._iterationSlice)
        coordinates = [c + off for c, off in zip(self.cuda_indices, offsets)]

        return coordinates[:self._dim]

    def call_parameters(self, arr_shape):
        substitution_dict = {sym: value for sym, value in zip(self._symbolic_shape, arr_shape) if sym is not None}

        widths = [end - start for start, end in zip(_get_start_from_slice(self._iterationSlice),
                                                    _get_end_from_slice(self._iterationSlice, arr_shape))]
        widths = sp.Matrix(widths).subs(substitution_dict)
        extend_bs = (1,) * (3 - len(self._block_size))
        block_size = self._block_size + extend_bs
        if not self._compile_time_block_size:
            assert len(block_size) == 3
            adapted_block_size = []
            for i in range(len(widths)):
                factor = div_floor(prod(block_size[:i]), prod(adapted_block_size))
                adapted_block_size.append(sp.Min(block_size[i] * factor, widths[i]))
            extend_adapted_bs = (1,) * (3 - len(adapted_block_size))
            block_size = tuple(adapted_block_size) + extend_adapted_bs

        block_size = tuple(sp.Min(bs, max_bs) for bs, max_bs in zip(block_size, self._maximum_block_size))
        grid = tuple(div_ceil(length, block_size) for length, block_size in zip(widths, block_size))
        extend_gr = (1,) * (3 - len(grid))

        return {'block': block_size,
                'grid': grid + extend_gr}

    def guard(self, kernel_content, arr_shape):
        arr_shape = arr_shape[:self._dim]
        end = _get_end_from_slice(self._iterationSlice, arr_shape)

        conditions = [c < e for c, e in zip(self.coordinates, end)]
        for cuda_index, iter_slice in zip(self.cuda_indices, self._iterationSlice):
            if isinstance(iter_slice, slice) and iter_slice.step > 1:
                conditions.append(sp.Eq(sp.Mod(cuda_index, iter_slice.step), 0))

        condition = conditions[0]
        for c in conditions[1:]:
            condition = sp.And(condition, c)
        return Block([Conditional(condition, kernel_content)])

    def iteration_space(self, arr_shape):
        return _iteration_space(self._iterationSlice, arr_shape)

    def limit_block_size_by_register_restriction(self, block_size, required_registers_per_thread):
        """Shrinks the block_size if there are too many registers used per block.
        This is not done automatically, since the required_registers_per_thread are not known before compilation.
        They can be obtained by ``func.num_regs`` from a cupy function.
        Args:
            block_size: used block size that is target for limiting
            required_registers_per_thread: needed registers per thread
        returns: smaller block_size if too many registers are used.
        """
        import cupy as cp

        # See https://github.com/cupy/cupy/issues/7676
        if cp.cuda.runtime.is_hip:
            max_registers_per_block = cp.cuda.runtime.deviceGetAttribute(71, self._device_number)
        else:
            device = cp.cuda.Device(self._device_number)
            da = device.attributes
            max_registers_per_block = da.get("MaxRegistersPerBlock")

        result = list(block_size)
        while True:
            required_registers = math.prod(result) * required_registers_per_thread
            if required_registers <= max_registers_per_block:
                return result
            else:
                largest_list_entry_idx = max(range(len(result)), key=lambda e: result[e])
                assert result[largest_list_entry_idx] >= 2
                result[largest_list_entry_idx] //= 2

    @staticmethod
    def permute_block_size_according_to_layout(block_size, layout):
        """Returns modified block_size such that the fastest coordinate gets the biggest block dimension"""
        if not is_integer_sequence(block_size):
            return block_size
        sorted_block_size = list(sorted(block_size, reverse=True))
        while len(sorted_block_size) > len(layout):
            sorted_block_size[0] *= sorted_block_size[-1]
            sorted_block_size = sorted_block_size[:-1]

        result = list(block_size)
        for l, bs in zip(reversed(layout), sorted_block_size):
            result[l] = bs
        return tuple(result[:len(layout)])

    def max_threads_per_block(self):
        if is_integer_sequence(self._block_size):
            return prod(self._block_size)
        else:
            return None

    def symbolic_parameters(self):
        return set(b for b in self._block_size if isinstance(b, sp.Symbol))


class LineIndexing(AbstractIndexing):
    """
    Indexing scheme that assigns the innermost 'line' i.e. the elements which are adjacent in memory to a 1D GPU block.
    The fastest coordinate is indexed with thread_idx.x, the remaining coordinates are mapped to block_idx.{x,y,z}
    This indexing scheme supports up to 4 spatial dimensions, where the innermost dimensions is not larger than the
    maximum amount of threads allowed in a GPU block (which depends on device).
    """

    def __init__(self, field, iteration_slice):
        available_indices = [THREAD_IDX[0]] + BLOCK_IDX
        if field.spatial_dimensions > 4:
            raise NotImplementedError("This indexing scheme supports at most 4 spatial dimensions")

        coordinates = available_indices[:field.spatial_dimensions]

        fastest_coordinate = field.layout[-1]
        coordinates[0], coordinates[fastest_coordinate] = coordinates[fastest_coordinate], coordinates[0]

        self._coordinates = coordinates
        self._iterationSlice = normalize_slice(iteration_slice, field.spatial_shape)
        self._symbolicShape = [e if isinstance(e, sp.Basic) else None for e in field.spatial_shape]

    @property
    def coordinates(self):
        return [i + offset for i, offset in zip(self._coordinates, _get_start_from_slice(self._iterationSlice))]

    def call_parameters(self, arr_shape):
        substitution_dict = {sym: value for sym, value in zip(self._symbolicShape, arr_shape) if sym is not None}

        widths = [end - start for start, end in zip(_get_start_from_slice(self._iterationSlice),
                                                    _get_end_from_slice(self._iterationSlice, arr_shape))]
        widths = sp.Matrix(widths).subs(substitution_dict)

        def get_shape_of_cuda_idx(cuda_idx):
            if cuda_idx not in self._coordinates:
                return 1
            else:
                idx = self._coordinates.index(cuda_idx)
                return widths[idx]

        return {'block': tuple([get_shape_of_cuda_idx(idx) for idx in THREAD_IDX]),
                'grid': tuple([get_shape_of_cuda_idx(idx) for idx in BLOCK_IDX])}

    def guard(self, kernel_content, arr_shape):
        return kernel_content

    def max_threads_per_block(self):
        return None

    def symbolic_parameters(self):
        return set()

    def iteration_space(self, arr_shape):
        return _iteration_space(self._iterationSlice, arr_shape)


# -------------------------------------- Helper functions --------------------------------------------------------------

def _get_start_from_slice(iteration_slice):
    res = []
    for slice_component in iteration_slice:
        if type(slice_component) is slice:
            res.append(slice_component.start if slice_component.start is not None else 0)
        else:
            assert isinstance(slice_component, int)
            res.append(slice_component)
    return res


def _get_end_from_slice(iteration_slice, arr_shape):
    iter_slice = normalize_slice(iteration_slice, arr_shape)
    res = []
    for slice_component in iter_slice:
        if type(slice_component) is slice:
            res.append(slice_component.stop)
        else:
            assert isinstance(slice_component, int)
            res.append(slice_component + 1)
    return res


def _get_steps_from_slice(iteration_slice):
    res = []
    for slice_component in iteration_slice:
        if type(slice_component) is slice:
            res.append(slice_component.step)
        else:
            res.append(1)
    return res


def _iteration_space(iteration_slice, arr_shape):
    starts = _get_start_from_slice(iteration_slice)
    ends = _get_end_from_slice(iteration_slice, arr_shape)
    steps = _get_steps_from_slice(iteration_slice)
    return [slice(start, end, step) for start, end, step in zip(starts, ends, steps)]


def indexing_creator_from_params(gpu_indexing, gpu_indexing_params):
    if isinstance(gpu_indexing, str):
        if gpu_indexing == 'block':
            indexing_creator = BlockIndexing
        elif gpu_indexing == 'line':
            indexing_creator = LineIndexing
        else:
            raise ValueError(f"Unknown GPU indexing {gpu_indexing}. Valid values are 'block' and 'line'")
        if gpu_indexing_params:
            indexing_creator = partial(indexing_creator, **gpu_indexing_params)
        return indexing_creator
    else:
        return gpu_indexing
