# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE
from __future__ import annotations

import collections
import itertools
import numbers
import os
import re
import sys
from collections.abc import Collection, Iterable, Mapping, Sequence, Sized

import packaging.version

import awkward as ak
from awkward._nplikes import nplike_of, ufuncs
from awkward._nplikes.jax import Jax
from awkward._nplikes.numpy import Numpy
from awkward._nplikes.numpylike import NumpyMetadata
from awkward.typing import TypeVar

np = NumpyMetadata.instance()

win = os.name == "nt"
bits32 = np.iinfo(np.intp).bits == 32

# matches include/awkward/common.h
kMaxInt8 = 127  # 2**7  - 1
kMaxUInt8 = 255  # 2**8  - 1
kMaxInt32 = 2147483647  # 2**31 - 1
kMaxUInt32 = 4294967295  # 2**32 - 1
kMaxInt64 = 9223372036854775806  # 2**63 - 2: see below
kSliceNone = kMaxInt64 + 1  # for Slice::none()
kMaxLevels = 48


def parse_version(version):
    return packaging.version.parse(version)


def numpy_at_least(version):
    import numpy  # noqa: TID251

    return parse_version(numpy.__version__) >= parse_version(version)


def in_module(obj, modulename: str) -> bool:
    m = type(obj).__module__
    return m == modulename or m.startswith(modulename + ".")


def is_file_path(x) -> bool:
    try:
        return os.path.isfile(x)
    except ValueError:
        return False


def is_sized_iterable(obj) -> bool:
    return isinstance(obj, Iterable) and isinstance(obj, Sized)


def is_integer(x) -> bool:
    return isinstance(x, numbers.Integral) and not isinstance(x, bool)


def is_non_string_like_iterable(obj) -> bool:
    return not isinstance(obj, (str, bytes)) and isinstance(obj, Iterable)


def is_non_string_like_sequence(obj) -> bool:
    return not isinstance(obj, (str, bytes)) and isinstance(obj, Sequence)


def tobytes(array):
    if hasattr(array, "tobytes"):
        return array.tobytes()
    else:
        return array.tostring()


native_byteorder = "<" if sys.byteorder == "little" else ">"


def native_to_byteorder(array, byteorder: str):
    """
    Args:
        array: nplike array
        byteorder (`"<"` or `">"`): desired byteorder

    Return a copy of array. Swap the byteorder if `byteorder` does not match
    `ak._util.native_byteorder`. This function is _not_ idempotent; no metadata
    from `array` exists to determine its current byteorder.
    """
    assert byteorder in "<>"
    if byteorder != native_byteorder:
        return array.byteswap(inplace=False)
    else:
        return array


def identifier_hash(str):
    import base64
    import struct

    return (
        base64.encodebytes(struct.pack("q", hash(str)))
        .rstrip(b"=\n")
        .replace(b"+", b"")
        .replace(b"/", b"")
        .decode("ascii")
    )


# FIXME: introduce sentinel type for this
class _Unset:
    def __repr__(self):
        return f"{__name__}.unset"


unset = _Unset()


# Sentinel object for catching pass-through values
class Unspecified:
    pass


def regularize_path(path):
    """
    Converts pathlib Paths into plain string paths (for all versions of Python).
    """
    is_path = False

    if isinstance(path, getattr(os, "PathLike", ())):
        is_path = True
        path = os.fspath(path)

    elif hasattr(path, "__fspath__"):
        is_path = True
        path = path.__fspath__()

    elif path.__class__.__module__ == "pathlib":
        import pathlib

        if isinstance(path, pathlib.Path):
            is_path = True
            path = str(path)

    return is_path, path


def overlay_behavior(behavior: dict | None) -> collections.abc.Mapping:
    """
    Args:
        behavior: behavior dictionary, or None

    Return a ChainMap object that overlays the given behavior
    on top of the global #ak.behavior
    """
    if behavior is None:
        return ak.behavior
    return collections.ChainMap(behavior, ak.behavior)


def arrayclass(layout, behavior):
    behavior = overlay_behavior(behavior)
    arr = layout.parameter("__array__")
    if isinstance(arr, str):
        cls = behavior.get(arr)
        if isinstance(cls, type) and issubclass(cls, ak.highlevel.Array):
            return cls
    deeprec = layout.purelist_parameter("__record__")
    if isinstance(deeprec, str):
        cls = behavior.get(("*", deeprec))
        if isinstance(cls, type) and issubclass(cls, ak.highlevel.Array):
            return cls
    return ak.highlevel.Array


def custom_cast(obj, behavior):
    behavior = overlay_behavior(behavior)
    for key, fcn in behavior.items():
        if (
            isinstance(key, tuple)
            and len(key) == 2
            and key[0] == "__cast__"
            and isinstance(obj, key[1])
        ):
            return fcn
    return None


def custom_broadcast(layout, behavior):
    behavior = overlay_behavior(behavior)
    custom = layout.parameter("__array__")
    if not isinstance(custom, str):
        custom = layout.parameter("__record__")
    if not isinstance(custom, str):
        custom = layout.purelist_parameter("__record__")
    if isinstance(custom, str):
        for key, fcn in behavior.items():
            if (
                isinstance(key, tuple)
                and len(key) == 2
                and key[0] == "__broadcast__"
                and key[1] == custom
            ):
                return fcn
    return None


def custom_ufunc(ufunc, layout, behavior):
    behavior = overlay_behavior(behavior)
    custom = layout.parameter("__array__")
    if not isinstance(custom, str):
        custom = layout.parameter("__record__")
    if isinstance(custom, str):
        for key, fcn in behavior.items():
            if (
                isinstance(key, tuple)
                and len(key) == 2
                and (key[0] is ufunc or key[0] is ufuncs.ufunc)
                and key[1] == custom
            ):
                return fcn
    return None


def numba_array_typer(layouttype, behavior):
    behavior = overlay_behavior(behavior)
    arr = layouttype.parameters.get("__array__")
    if isinstance(arr, str):
        typer = behavior.get(("__numba_typer__", arr))
        if callable(typer):
            return typer
    deeprec = layouttype.parameters.get("__record__")
    if isinstance(deeprec, str):
        typer = behavior.get(("__numba_typer__", "*", deeprec))
        if callable(typer):
            return typer
    return None


def numba_array_lower(layouttype, behavior):
    behavior = overlay_behavior(behavior)
    arr = layouttype.parameters.get("__array__")
    if isinstance(arr, str):
        lower = behavior.get(("__numba_lower__", arr))
        if callable(lower):
            return lower
    deeprec = layouttype.parameters.get("__record__")
    if isinstance(deeprec, str):
        lower = behavior.get(("__numba_lower__", "*", deeprec))
        if callable(lower):
            return lower
    return None


def recordclass(layout, behavior):
    behavior = overlay_behavior(behavior)
    rec = layout.parameter("__record__")
    if isinstance(rec, str):
        cls = behavior.get(rec)
        if isinstance(cls, type) and issubclass(cls, ak.highlevel.Record):
            return cls
    return ak.highlevel.Record


def reducer_recordclass(reducer, layout, behavior):
    behavior = overlay_behavior(behavior)
    rec = layout.parameter("__record__")
    if isinstance(rec, str):
        return behavior.get((reducer.highlevel_function(), rec))


def typestrs(behavior):
    behavior = overlay_behavior(behavior)
    out = {}
    for key, typestr in behavior.items():
        if (
            isinstance(key, tuple)
            and len(key) == 2
            and key[0] == "__typestr__"
            and isinstance(key[1], str)
            and isinstance(typestr, str)
        ):
            out[key[1]] = typestr
    return out


def gettypestr(parameters, typestrs):
    if parameters is not None:
        record = parameters.get("__record__")
        if record is not None:
            typestr = typestrs.get(record)
            if typestr is not None:
                return typestr
        array = parameters.get("__array__")
        if array is not None:
            typestr = typestrs.get(array)
            if typestr is not None:
                return typestr
    return None


def numba_record_typer(layouttype, behavior):
    behavior = overlay_behavior(behavior)
    rec = layouttype.parameters.get("__record__")
    if isinstance(rec, str):
        typer = behavior.get(("__numba_typer__", rec))
        if callable(typer):
            return typer
    return None


def numba_record_lower(layouttype, behavior):
    behavior = overlay_behavior(behavior)
    rec = layouttype.parameters.get("__record__")
    if isinstance(rec, str):
        lower = behavior.get(("__numba_lower__", rec))
        if callable(lower):
            return lower
    return None


def overload(behavior, signature):
    if not any(s is None for s in signature):
        behavior = overlay_behavior(behavior)
        for key, custom in behavior.items():
            if (
                isinstance(key, tuple)
                and len(key) == len(signature)
                and key[0] == signature[0]
                and all(
                    k == s
                    or (
                        isinstance(k, type) and isinstance(s, type) and issubclass(s, k)
                    )
                    for k, s in zip(key[1:], signature[1:])
                )
            ):
                return custom


def numba_attrs(layouttype, behavior):
    behavior = overlay_behavior(behavior)
    rec = layouttype.parameters.get("__record__")
    if isinstance(rec, str):
        for key, typer in behavior.items():
            if (
                isinstance(key, tuple)
                and len(key) == 3
                and key[0] == "__numba_typer__"
                and key[1] == rec
            ):
                lower = behavior["__numba_lower__", key[1], key[2]]
                yield key[2], typer, lower


def numba_methods(layouttype, behavior):
    behavior = overlay_behavior(behavior)
    rec = layouttype.parameters.get("__record__")
    if isinstance(rec, str):
        for key, typer in behavior.items():
            if (
                isinstance(key, tuple)
                and len(key) == 4
                and key[0] == "__numba_typer__"
                and key[1] == rec
                and key[3] == ()
            ):
                lower = behavior["__numba_lower__", key[1], key[2], ()]
                yield key[2], typer, lower


def numba_unaryops(unaryop, left, behavior):
    behavior = overlay_behavior(behavior)
    done = False

    if isinstance(left, ak._connect.numba.layout.ContentType):
        left = left.parameters.get("__record__")
        if not isinstance(left, str):
            done = True

    if not done:
        for key, typer in behavior.items():
            if (
                isinstance(key, tuple)
                and len(key) == 3
                and key[0] == "__numba_typer__"
                and key[1] == unaryop
                and key[2] == left
            ):
                lower = behavior["__numba_lower__", key[1], key[2]]
                yield typer, lower


def numba_binops(binop, left, right, behavior):
    behavior = overlay_behavior(behavior)
    done = False

    if isinstance(left, ak._connect.numba.layout.ContentType):
        left = left.parameters.get("__record__")
        if not isinstance(left, str):
            done = True

    if isinstance(right, ak._connect.numba.layout.ContentType):
        right = right.parameters.get("__record__")
        if not isinstance(right, str):
            done = True

    if not done:
        for key, typer in behavior.items():
            if (
                isinstance(key, tuple)
                and len(key) == 4
                and key[0] == "__numba_typer__"
                and key[1] == left
                and key[2] == binop
                and key[3] == right
            ):
                lower = behavior["__numba_lower__", key[1], key[2], key[3]]
                yield typer, lower


def behavior_of(*arrays, **kwargs):
    behavior = kwargs.get("behavior")
    if behavior is not None:
        # An explicit 'behavior' always wins.
        return behavior

    copied = False
    highs = (
        ak.highlevel.Array,
        ak.highlevel.Record,
        ak.highlevel.ArrayBuilder,
    )
    for x in arrays[::-1]:
        if isinstance(x, highs) and x.behavior is not None:
            if behavior is None:
                behavior = x.behavior
            elif behavior is x.behavior:
                pass
            elif not copied:
                behavior = dict(behavior)
                behavior.update(x.behavior)
                copied = True
            else:
                behavior.update(x.behavior)
    return behavior


def wrap(content, behavior=None, highlevel=True, like=None, allow_other=False):
    assert (
        content is None
        or isinstance(content, (ak.contents.Content, ak.record.Record))
        or allow_other
    )
    assert behavior is None or isinstance(behavior, Mapping)
    assert isinstance(highlevel, bool)
    if highlevel:
        if like is not None and behavior is None:
            behavior = behavior_of(like)

        if isinstance(content, ak.contents.Content):
            return ak.highlevel.Array(content, behavior=behavior)
        elif isinstance(content, ak.record.Record):
            return ak.highlevel.Record(content, behavior=behavior)

    return content


def union_to_record(unionarray, anonymous):
    nplike = nplike_of(unionarray)

    contents = []
    for layout in unionarray.contents:
        if layout.is_indexed and not layout.is_option:
            contents.append(layout.project())
        elif layout.is_union:
            contents.append(union_to_record(layout, anonymous))
        elif layout.is_option:
            contents.append(
                ak.operations.fill_none(layout, np.nan, axis=0, highlevel=False)
            )
        else:
            contents.append(layout)

    if not any(isinstance(x, ak.contents.RecordArray) for x in contents):
        return ak.contents.UnionArray(
            unionarray.tags,
            unionarray.index,
            contents,
            parameters=unionarray.parameters,
        )

    else:
        seen = set()
        all_names = []
        for layout in contents:
            if isinstance(layout, ak.contents.RecordArray):
                for field in layout.fields:
                    if field not in seen:
                        seen.add(field)
                        all_names.append(field)
            else:
                if anonymous not in seen:
                    seen.add(anonymous)
                    all_names.append(anonymous)

        missingarray = ak.contents.IndexedOptionArray(
            ak.index.Index64(nplike.full(len(unionarray), -1, dtype=np.int64)),
            ak.contents.EmptyArray(),
        )

        all_fields = []
        for name in all_names:
            union_contents = []
            for layout in contents:
                if isinstance(layout, ak.contents.RecordArray):
                    for field in layout.fields:
                        if name == field:
                            union_contents.append(layout._getitem_field(field))
                            break
                    else:
                        union_contents.append(missingarray)
                else:
                    if name == anonymous:
                        union_contents.append(layout)
                    else:
                        union_contents.append(missingarray)

            all_fields.append(
                ak.contents.UnionArray.simplified(
                    unionarray.tags,
                    unionarray.index,
                    union_contents,
                    parameters=unionarray.parameters,
                )
            )

        return ak.contents.RecordArray(all_fields, all_names, unionarray.length)


def direct_Content_subclass(node):
    if node is None:
        return None
    else:
        mro = type(node).mro()
        return mro[mro.index(ak.contents.Content) - 1]


def direct_Content_subclass_name(node):
    out = direct_Content_subclass(node)
    if out is None:
        return None
    else:
        return out.__name__


def expand_braces(text, seen=None):
    if seen is None:
        seen = set()

    spans = [m.span() for m in expand_braces.regex.finditer(text)][::-1]
    alts = [text[start + 1 : stop - 1].split(",") for start, stop in spans]

    if len(spans) == 0:
        if text not in seen:
            yield text
        seen.add(text)

    else:
        for combo in itertools.product(*alts):
            replaced = list(text)
            for (start, stop), replacement in zip(spans, combo):
                replaced[start:stop] = replacement
            yield from expand_braces("".join(replaced), seen)


expand_braces.regex = re.compile(r"\{[^\{\}]*\}")


def from_arraylib(array, regulararray, recordarray, highlevel, behavior):
    np = NumpyMetadata.instance()
    # overshadows global NumPy import for nplike-safety
    numpy = Numpy.instance()

    def recurse(array, mask=None):
        nplike = nplike_of(array)

        if Jax.is_tracer(array):
            raise ak._errors.wrap_error(
                TypeError("Jax tracers cannot be used with `ak.from_arraylib`")
            )

        if regulararray and len(array.shape) > 1:
            new_shape = (-1,) + array.shape[2:]
            return ak.contents.RegularArray(
                recurse(nplike.reshape(array, new_shape), mask),
                array.shape[1],
                array.shape[0],
            )

        if len(array.shape) == 0:
            array = nplike.reshape(array, (1,))

        if array.dtype.kind == "S":
            assert nplike is numpy
            asbytes = array.reshape(-1)
            itemsize = asbytes.dtype.itemsize
            starts = numpy.arange(0, len(asbytes) * itemsize, itemsize, dtype=np.int64)
            stops = numpy.add(starts, numpy.char.str_len(asbytes))
            data = ak.contents.ListArray(
                ak.index.Index64(starts),
                ak.index.Index64(stops),
                ak.contents.NumpyArray(
                    asbytes.view("u1"),
                    parameters={"__array__": "byte"},
                    backend=ak._backends.NumpyBackend.instance(),
                ),
                parameters={"__array__": "bytestring"},
            )
            for i in range(len(array.shape) - 1, 0, -1):
                data = ak.contents.RegularArray(
                    data, array.shape[i], array.shape[i - 1]
                )

        elif array.dtype.kind == "U":
            assert nplike is numpy
            asbytes = numpy.char.encode(array.reshape(-1), "utf-8", "surrogateescape")
            itemsize = asbytes.dtype.itemsize
            starts = numpy.arange(0, len(asbytes) * itemsize, itemsize, dtype=np.int64)
            stops = numpy.add(starts, numpy.char.str_len(asbytes))
            data = ak.contents.ListArray(
                ak.index.Index64(starts),
                ak.index.Index64(stops),
                ak.contents.NumpyArray(
                    asbytes.view("u1"),
                    parameters={"__array__": "char"},
                    backend=ak._backends.NumpyBackend.instance(),
                ),
                parameters={"__array__": "string"},
            )
            for i in range(len(array.shape) - 1, 0, -1):
                data = ak.contents.RegularArray(
                    data, array.shape[i], array.shape[i - 1]
                )

        else:
            data = ak.contents.NumpyArray(array)

        if mask is None:
            return data

        elif mask is False or (isinstance(mask, np.bool_) and not mask):
            # NumPy's MaskedArray with mask == False is an UnmaskedArray
            if len(array.shape) == 1:
                return ak.contents.UnmaskedArray(data)
            else:

                def attach(x):
                    if isinstance(x, ak.contents.NumpyArray):
                        return ak.contents.UnmaskedArray(x)
                    else:
                        return ak.contents.RegularArray(
                            attach(x.content), x.size, len(x)
                        )

                return attach(data.to_RegularArray())

        else:
            # NumPy's MaskedArray is a ByteMaskedArray with valid_when=False
            return ak.contents.ByteMaskedArray(
                ak.index.Index8(mask), data, valid_when=False
            )

    if array.dtype == np.dtype("O"):
        raise ak._errors.wrap_error(
            TypeError("Awkward Array does not support arrays with object dtypes.")
        )

    if isinstance(array, numpy.ma.MaskedArray):
        mask = numpy.ma.getmask(array)
        array = numpy.ma.getdata(array)
        if isinstance(mask, np.ndarray) and len(mask.shape) > 1:
            regulararray = True
            mask = mask.reshape(-1)
    else:
        mask = None

    if not recordarray or array.dtype.names is None:
        layout = recurse(array, mask)

    else:
        contents = []
        for name in array.dtype.names:
            contents.append(recurse(array[name], mask))
        layout = ak.contents.RecordArray(contents, array.dtype.names)

    return ak._util.wrap(layout, behavior, highlevel)


def maybe_posaxis(layout, axis, depth):
    if isinstance(layout, ak.record.Record):
        if axis == 0:
            raise ak._errors.wrap_error(
                np.AxisError("Record type at axis=0 is a scalar, not an array")
            )
        return maybe_posaxis(layout._array, axis, depth)

    if axis >= 0:
        return axis

    else:
        is_branching, additional_depth = layout.branch_depth
        if not is_branching:
            return axis + depth + additional_depth - 1
        else:
            return None


try:
    import numpy  # noqa: TID251

    NDArrayOperatorsMixin = numpy.lib.mixins.NDArrayOperatorsMixin

except AttributeError:
    from numpy.core import umath as um  # noqa: TID251

    def _disables_array_ufunc(obj):
        try:
            return obj.__array_ufunc__ is None
        except AttributeError:
            return False

    def _binary_method(ufunc, name):
        def func(self, other):
            if _disables_array_ufunc(other):
                return NotImplemented
            return ufunc(self, other)

        func.__name__ = f"__{name}__"
        return func

    def _reflected_binary_method(ufunc, name):
        def func(self, other):
            if _disables_array_ufunc(other):
                return NotImplemented
            return ufunc(other, self)

        func.__name__ = f"__r{name}__"
        return func

    def _inplace_binary_method(ufunc, name):
        def func(self, other):
            return ufunc(self, other, out=(self,))

        func.__name__ = f"__i{name}__"
        return func

    def _numeric_methods(ufunc, name):
        return (
            _binary_method(ufunc, name),
            _reflected_binary_method(ufunc, name),
            _inplace_binary_method(ufunc, name),
        )

    def _unary_method(ufunc, name):
        def func(self):
            return ufunc(self)

        func.__name__ = f"__{name}__"
        return func

    class NDArrayOperatorsMixin:
        __lt__ = _binary_method(um.less, "lt")
        __le__ = _binary_method(um.less_equal, "le")
        __eq__ = _binary_method(um.equal, "eq")
        __ne__ = _binary_method(um.not_equal, "ne")
        __gt__ = _binary_method(um.greater, "gt")
        __ge__ = _binary_method(um.greater_equal, "ge")

        __add__, __radd__, __iadd__ = _numeric_methods(um.add, "add")
        __sub__, __rsub__, __isub__ = _numeric_methods(um.subtract, "sub")
        __mul__, __rmul__, __imul__ = _numeric_methods(um.multiply, "mul")
        __matmul__, __rmatmul__, __imatmul__ = _numeric_methods(um.matmul, "matmul")
        __truediv__, __rtruediv__, __itruediv__ = _numeric_methods(
            um.true_divide, "truediv"
        )
        __floordiv__, __rfloordiv__, __ifloordiv__ = _numeric_methods(
            um.floor_divide, "floordiv"
        )
        __mod__, __rmod__, __imod__ = _numeric_methods(um.remainder, "mod")
        if hasattr(um, "divmod"):
            __divmod__ = _binary_method(um.divmod, "divmod")
            __rdivmod__ = _reflected_binary_method(um.divmod, "divmod")
        __pow__, __rpow__, __ipow__ = _numeric_methods(um.power, "pow")
        __lshift__, __rlshift__, __ilshift__ = _numeric_methods(um.left_shift, "lshift")
        __rshift__, __rrshift__, __irshift__ = _numeric_methods(
            um.right_shift, "rshift"
        )
        __and__, __rand__, __iand__ = _numeric_methods(um.bitwise_and, "and")
        __xor__, __rxor__, __ixor__ = _numeric_methods(um.bitwise_xor, "xor")
        __or__, __ror__, __ior__ = _numeric_methods(um.bitwise_or, "or")

        __neg__ = _unary_method(um.negative, "neg")
        if hasattr(um, "positive"):
            __pos__ = _unary_method(um.positive, "pos")
        __abs__ = _unary_method(um.absolute, "abs")
        __invert__ = _unary_method(um.invert, "invert")


T = TypeVar("T")


def unique_list(items: Collection[T]) -> list[T]:
    seen = set()
    result = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result
