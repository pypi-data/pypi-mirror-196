# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE
from __future__ import annotations

import copy
import json
import math

import awkward as ak
from awkward._nplikes.numpy import Numpy
from awkward._nplikes.numpylike import IndexType, NumpyMetadata
from awkward._nplikes.shape import unknown_length
from awkward._nplikes.typetracer import MaybeNone, TypeTracer
from awkward._util import unset
from awkward.contents.bytemaskedarray import ByteMaskedArray
from awkward.contents.content import Content
from awkward.forms.bitmaskedform import BitMaskedForm
from awkward.forms.form import _type_parameters_equal
from awkward.index import Index
from awkward.typing import TYPE_CHECKING, Final, Self, SupportsIndex, final

if TYPE_CHECKING:
    from awkward._slicing import SliceItem

np = NumpyMetadata.instance()
numpy = Numpy.instance()


@final
class BitMaskedArray(Content):
    """
    Like #ak.contents.ByteMaskedArray, BitMaskedArray implements an
    #ak.types.OptionType with two buffers, `mask` and `content`.
    However, the boolean `mask` values are packed into a bitmap.

    BitMaskedArray has an additional parameter, `lsb_order`; if True,
    the position of each bit is in
    [Least-Significant Bit order](https://en.wikipedia.org/wiki/Bit_numbering)
    (LSB):

        is_valid[j] = bool(mask[j // 8] & (1 << (j % 8))) == valid_when

    If False, the position of each bit is in Most-Significant Bit order
    (MSB):

        is_valid[j] = bool(mask[j // 8] & (128 >> (j % 8))) == valid_when

    If the logical size of the buffer is not a multiple of 8, the `mask`
    has to be padded. Thus, an explicit `length` is also part of the
    class's definition.

    This is equivalent to *all* of Apache Arrow's array types because they all
    [use bitmaps](https://arrow.apache.org/docs/format/Columnar.html#validity-bitmaps)
    to mask their data, with `valid_when=True` and `lsb_order=True`.

    To illustrate how the constructor arguments are interpreted, the following is a
    simplified implementation of `__init__`, `__len__`, and `__getitem__`:

        class BitMaskedArray(Content):
            def __init__(self, mask, content, valid_when, length, lsb_order):
                assert isinstance(mask, IndexU8)
                assert isinstance(content, Content)
                assert isinstance(valid_when, bool)
                assert isinstance(length, int) and length >= 0
                assert isinstance(lsb_order, bool)
                assert len(mask) <= len(content)
                self.mask = mask
                self.content = content
                self.valid_when = valid_when
                self.length = length
                self.lsb_order = lsb_order

            def __len__(self):
                return self.length

            def __getitem__(self, where):
                if isinstance(where, int):
                    if where < 0:
                        where += len(self)
                    assert 0 <= where < len(self)
                    if self.lsb_order:
                        bit = bool(self.mask[where // 8] & (1 << (where % 8)))
                    else:
                        bit = bool(self.mask[where // 8] & (128 >> (where % 8)))
                    if bit == self.valid_when:
                        return self.content[where]
                    else:
                        return None

                elif isinstance(where, slice) and where.step is None:
                    # In general, slices must convert BitMaskedArray to ByteMaskedArray.
                    bytemask = np.unpackbits(
                        self.mask, bitorder=("little" if self.lsb_order else "big")
                    ).view(bool)
                    return ByteMaskedArray(
                        bytemask[where.start : where.stop],
                        self.content[where.start : where.stop],
                        valid_when=self.valid_when,
                    )

                elif isinstance(where, str):
                    return BitMaskedArray(
                        self.mask,
                        self.content[where],
                        valid_when=self.valid_when,
                        length=self.length,
                        lsb_order=self.lsb_order,
                    )

                else:
                    raise AssertionError(where)
    """

    is_option = True

    def __init__(
        self, mask, content, valid_when, length, lsb_order, *, parameters=None
    ):
        if not (isinstance(mask, Index) and mask.dtype == np.dtype(np.uint8)):
            raise ak._errors.wrap_error(
                TypeError(
                    "{} 'mask' must be an Index with dtype=uint8, not {}".format(
                        type(self).__name__, repr(mask)
                    )
                )
            )
        if not isinstance(content, Content):
            raise ak._errors.wrap_error(
                TypeError(
                    "{} 'content' must be a Content subtype, not {}".format(
                        type(self).__name__, repr(content)
                    )
                )
            )
        if content.is_union or content.is_indexed or content.is_option:
            raise ak._errors.wrap_error(
                TypeError(
                    "{0} cannot contain a union-type, option-type, or indexed 'content' ({1}); try {0}.simplified instead".format(
                        type(self).__name__, type(content).__name__
                    )
                )
            )
        if not isinstance(valid_when, bool):
            raise ak._errors.wrap_error(
                TypeError(
                    "{} 'valid_when' must be boolean, not {}".format(
                        type(self).__name__, repr(valid_when)
                    )
                )
            )
        if length is not unknown_length:
            if not (ak._util.is_integer(length) and length >= 0):
                raise ak._errors.wrap_error(
                    TypeError(
                        "{} 'length' must be a non-negative integer, not {}".format(
                            type(self).__name__, length
                        )
                    )
                )
        if not isinstance(lsb_order, bool):
            raise ak._errors.wrap_error(
                TypeError(
                    "{} 'lsb_order' must be boolean, not {}".format(
                        type(self).__name__, repr(lsb_order)
                    )
                )
            )
        if (
            not (length is unknown_length or mask.length is unknown_length)
            and length > mask.length * 8
        ):
            raise ak._errors.wrap_error(
                ValueError(
                    "{} 'length' ({}) must be <= len(mask) * 8 ({})".format(
                        type(self).__name__, length, mask.length * 8
                    )
                )
            )
        if (
            not (length is unknown_length or content.length is unknown_length)
            and length > content.length * 8
        ):
            raise ak._errors.wrap_error(
                ValueError(
                    "{} 'length' ({}) must be <= len(content) ({})".format(
                        type(self).__name__, length, content.length
                    )
                )
            )

        assert mask.nplike is content.backend.index_nplike

        self._mask = mask
        self._content = content
        self._valid_when = valid_when
        self._length = length
        self._lsb_order = lsb_order
        self._init(parameters, content.backend)

    @property
    def mask(self):
        return self._mask

    @property
    def content(self):
        return self._content

    @property
    def valid_when(self):
        return self._valid_when

    @property
    def lsb_order(self):
        return self._lsb_order

    form_cls: Final = BitMaskedForm

    def copy(
        self,
        mask=unset,
        content=unset,
        valid_when=unset,
        length=unset,
        lsb_order=unset,
        *,
        parameters=unset,
    ):
        return BitMaskedArray(
            self._mask if mask is unset else mask,
            self._content if content is unset else content,
            self._valid_when if valid_when is unset else valid_when,
            self._length if length is unset else length,
            self._lsb_order if lsb_order is unset else lsb_order,
            parameters=self._parameters if parameters is unset else parameters,
        )

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        return self.copy(
            mask=copy.deepcopy(self._mask, memo),
            content=copy.deepcopy(self._content, memo),
            parameters=copy.deepcopy(self._parameters, memo),
        )

    @classmethod
    def simplified(
        cls,
        mask,
        content,
        valid_when,
        length,
        lsb_order,
        *,
        parameters=None,
    ):
        if content.is_union or content.is_indexed or content.is_option:
            backend = content.backend
            index = ak.index.Index64.empty(mask.length * 8, backend.index_nplike)
            Content._selfless_handle_error(
                backend[
                    "awkward_BitMaskedArray_to_IndexedOptionArray",
                    index.dtype.type,
                    mask.dtype.type,
                ](
                    index.raw(backend.nplike),
                    mask.data,
                    mask.length,
                    valid_when,
                    lsb_order,
                ),
            )
            if content.is_union:
                return content._union_of_optionarrays(index[0:length], parameters)
            else:
                return ak.contents.IndexedOptionArray.simplified(
                    index[0:length], content, parameters=parameters
                )
        else:
            return cls(
                mask,
                content,
                valid_when,
                length,
                lsb_order,
                parameters=parameters,
            )

    def _form_with_key(self, getkey):
        form_key = getkey(self)
        return self.form_cls(
            self._mask.form,
            self._content._form_with_key(getkey),
            self._valid_when,
            self._lsb_order,
            parameters=self._parameters,
            form_key=form_key,
        )

    def _to_buffers(self, form, getkey, container, backend, byteorder):
        assert isinstance(form, self.form_cls)
        key = getkey(self, form, "mask")
        container[key] = ak._util.native_to_byteorder(
            self._mask.raw(backend.index_nplike), byteorder
        )
        self._content._to_buffers(form.content, getkey, container, backend, byteorder)

    def _to_typetracer(self, forget_length: bool) -> Self:
        tt = TypeTracer.instance()
        return BitMaskedArray(
            self._mask.to_nplike(tt),
            self._content._to_typetracer(False),
            self._valid_when,
            unknown_length if forget_length else self.length,
            self._lsb_order,
            parameters=self._parameters,
        )

    def _touch_data(self, recursive):
        if not self._backend.index_nplike.known_data:
            self._mask.data.touch_data()
        if recursive:
            self._content._touch_data(recursive)

    def _touch_shape(self, recursive):
        if not self._backend.index_nplike.known_data:
            self._mask.data.touch_shape()
        if recursive:
            self._content._touch_shape(recursive)

    @property
    def length(self):
        return self._length

    def __repr__(self):
        return self._repr("", "", "")

    def _repr(self, indent, pre, post):
        out = [indent, pre, "<BitMaskedArray valid_when="]
        out.append(repr(json.dumps(self._valid_when)))
        out.append(" lsb_order=")
        out.append(repr(json.dumps(self._lsb_order)))
        out.append(" len=")
        out.append(repr(str(self.length)))
        out.append(">")
        out.extend(self._repr_extra(indent + "    "))
        out.append("\n")
        out.append(self._mask._repr(indent + "    ", "<mask>", "</mask>\n"))
        out.append(self._content._repr(indent + "    ", "<content>", "</content>\n"))
        out.append(indent + "</BitMaskedArray>")
        out.append(post)
        return "".join(out)

    def to_IndexedOptionArray64(self):
        index = ak.index.Index64.empty(
            self._mask.length * 8, self._backend.index_nplike
        )
        assert (
            index.nplike is self._backend.nplike
            and self._mask.nplike is self._backend.nplike
        )
        self._handle_error(
            self._backend[
                "awkward_BitMaskedArray_to_IndexedOptionArray",
                index.dtype.type,
                self._mask.dtype.type,
            ](
                index.raw(self._backend.nplike),
                self._mask.data,
                self._mask.length,
                self._valid_when,
                self._lsb_order,
            ),
        )
        return ak.contents.IndexedOptionArray(
            index[0 : self._length], self._content, parameters=self._parameters
        )

    def to_ByteMaskedArray(self):
        bytemask = ak.index.Index8.empty(
            self._mask.length * 8, self._backend.index_nplike
        )
        assert (
            bytemask.nplike is self._backend.nplike
            and self._mask.nplike is self._backend.nplike
        )
        self._handle_error(
            self._backend[
                "awkward_BitMaskedArray_to_ByteMaskedArray",
                bytemask.dtype.type,
                self._mask.dtype.type,
            ](
                bytemask.data,
                self._mask.data,
                self._mask.length,
                False,  # this differs from the kernel call in 'bytemask'
                self._lsb_order,
            )
        )
        return ByteMaskedArray(
            bytemask[: self._length],
            self._content,
            self._valid_when,
            parameters=self._parameters,
        )

    def to_BitMaskedArray(self, valid_when, lsb_order):
        if lsb_order == self._lsb_order:
            if valid_when == self._valid_when:
                return self
            else:
                return BitMaskedArray(
                    ak.index.IndexU8(
                        self._backend.index_nplike.logical_not(self._mask.data)
                    ),
                    self._content,
                    valid_when,
                    self._length,
                    lsb_order,
                    parameters=self._parameters,
                )

        else:
            bit_order = "little" if lsb_order else "big"
            bytemask = self.backend.index_nplike.unpackbits(
                self._mask.data, bitorder=bit_order
            )
            bitmask = self.backend.index_nplike.packbits(bytemask, bitorder=bit_order)

            if valid_when != self._valid_when:
                bitmask = ~bitmask

            return BitMaskedArray(
                ak.index.IndexU8(bitmask),
                self._content,
                valid_when,
                self._length,
                lsb_order,
                parameters=self._parameters,
            )

    def mask_as_bool(self, valid_when=None):
        if valid_when is None:
            valid_when = self._valid_when

        bytemask = ak.index.Index8.empty(
            self._mask.length * 8, self._backend.index_nplike
        )
        assert (
            bytemask.nplike is self._backend.nplike
            and self._mask.nplike is self._backend.nplike
        )
        self._handle_error(
            self._backend[
                "awkward_BitMaskedArray_to_ByteMaskedArray",
                bytemask.dtype.type,
                self._mask.dtype.type,
            ](
                bytemask.data,
                self._mask.data,
                self._mask.length,
                0 if valid_when == self._valid_when else 1,
                self._lsb_order,
            )
        )
        return bytemask.data[: self._length].view(np.bool_)

    def _getitem_nothing(self):
        return self._content._getitem_range(0, 0)

    def _getitem_at(self, where: IndexType):
        if not self._backend.nplike.known_data:
            self._touch_data(recursive=False)
            return MaybeNone(self._content._getitem_at(where))

        if where < 0:
            where += self.length
        if not (0 <= where < self.length) and self._backend.nplike.known_data:
            raise ak._errors.index_error(self, where)
        if self._lsb_order:
            bit = bool(self._mask[where // 8] & (1 << (where % 8)))
        else:
            bit = bool(self._mask[where // 8] & (128 >> (where % 8)))
        if bit == self._valid_when:
            return self._content._getitem_at(where)
        else:
            return None

    def _getitem_range(self, start: IndexType, stop: IndexType) -> Content:
        return self.to_ByteMaskedArray()._getitem_range(start, stop)

    def _getitem_field(
        self, where: str | SupportsIndex, only_fields: tuple[str, ...] = ()
    ) -> Content:
        return BitMaskedArray.simplified(
            self._mask,
            self._content._getitem_field(where, only_fields),
            self._valid_when,
            self._length,
            self._lsb_order,
            parameters=None,
        )

    def _getitem_fields(
        self, where: list[str | SupportsIndex], only_fields: tuple[str, ...] = ()
    ) -> Content:
        return BitMaskedArray.simplified(
            self._mask,
            self._content._getitem_fields(where, only_fields),
            self._valid_when,
            self._length,
            self._lsb_order,
            parameters=None,
        )

    def _carry(self, carry: Index, allow_lazy: bool) -> Content:
        assert isinstance(carry, ak.index.Index)
        return self.to_ByteMaskedArray()._carry(carry, allow_lazy)

    def _getitem_next_jagged(self, slicestarts, slicestops, slicecontent, tail):
        return self.to_ByteMaskedArray()._getitem_next_jagged(
            slicestarts, slicestops, slicecontent, tail
        )

    def _getitem_next(
        self,
        head: SliceItem | tuple,
        tail: tuple[SliceItem, ...],
        advanced: Index | None,
    ) -> Content:
        if head == ():
            return self

        elif isinstance(
            head, (int, slice, ak.index.Index64, ak.contents.ListOffsetArray)
        ):
            return self.to_ByteMaskedArray()._getitem_next(head, tail, advanced)

        elif isinstance(head, str):
            return self._getitem_next_field(head, tail, advanced)

        elif isinstance(head, list):
            return self._getitem_next_fields(head, tail, advanced)

        elif head is np.newaxis:
            return self._getitem_next_newaxis(tail, advanced)

        elif head is Ellipsis:
            return self._getitem_next_ellipsis(tail, advanced)

        elif isinstance(head, ak.contents.IndexedOptionArray):
            return self._getitem_next_missing(head, tail, advanced)

        else:
            raise ak._errors.wrap_error(AssertionError(repr(head)))

    def project(self, mask=None):
        return self.to_ByteMaskedArray().project(mask)

    def _offsets_and_flattened(self, axis, depth):
        return self.to_ByteMaskedArray._offsets_and_flattened(axis, depth)

    def _mergeable_next(self, other, mergebool):
        # Is the other content is an identity, or a union?
        if other.is_identity_like or other.is_union:
            return True
        # We can only combine option types whose array-record parameters agree
        elif other.is_option or other.is_indexed:
            return self._content._mergeable_next(
                other.content, mergebool
            ) and _type_parameters_equal(self._parameters, other._parameters)
        else:
            return self._content._mergeable_next(other, mergebool)

    def _reverse_merge(self, other):
        return self.to_IndexedOptionArray64()._reverse_merge(other)

    def _mergemany(self, others):
        if len(others) == 0:
            return self

        out = self.to_IndexedOptionArray64()._mergemany(others)

        if all(
            isinstance(x, BitMaskedArray)
            and x._valid_when == self._valid_when
            and x._lsb_order == self._lsb_order
            for x in others
        ):
            return out.to_BitMaskedArray(self._valid_when, self._lsb_order)
        else:
            return out

    def _fill_none(self, value: Content) -> Content:
        return self.to_IndexedOptionArray64()._fill_none(value)

    def _local_index(self, axis, depth):
        return self.to_ByteMaskedArray()._local_index(axis, depth)

    def _numbers_to_type(self, name, including_unknown):
        return self.to_ByteMaskedArray()._numbers_to_type(name, including_unknown)

    def _is_unique(self, negaxis, starts, parents, outlength):
        if self._mask.length == 0:
            return True
        return self.to_IndexedOptionArray64()._is_unique(
            negaxis, starts, parents, outlength
        )

    def _unique(self, negaxis, starts, parents, outlength):
        if self._mask.length == 0:
            return self
        out = self.to_IndexedOptionArray64()._unique(
            negaxis, starts, parents, outlength
        )
        if negaxis is None:
            return out
        else:
            return out._content

    def _argsort_next(
        self, negaxis, starts, shifts, parents, outlength, ascending, stable
    ):
        return self.to_IndexedOptionArray64()._argsort_next(
            negaxis, starts, shifts, parents, outlength, ascending, stable
        )

    def _sort_next(self, negaxis, starts, parents, outlength, ascending, stable):
        return self.to_IndexedOptionArray64()._sort_next(
            negaxis, starts, parents, outlength, ascending, stable
        )

    def _combinations(self, n, replacement, recordlookup, parameters, axis, depth):
        return self.to_ByteMaskedArray()._combinations(
            n, replacement, recordlookup, parameters, axis, depth
        )

    def _reduce_next(
        self,
        reducer,
        negaxis,
        starts,
        shifts,
        parents,
        outlength,
        mask,
        keepdims,
        behavior,
    ):
        return self.to_ByteMaskedArray()._reduce_next(
            reducer,
            negaxis,
            starts,
            shifts,
            parents,
            outlength,
            mask,
            keepdims,
            behavior,
        )

    def _validity_error(self, path):
        if self.mask.length * 8 < self.length:
            return f"at {path} ({type(self)!r}): len(mask) * 8 < length"
        elif self._content.length < self.length:
            return f"at {path} ({type(self)!r}): len(content) < length"
        else:
            return self._content._validity_error(path + ".content")

    def _nbytes_part(self):
        return self.mask._nbytes_part() + self.content._nbytes_part()

    def _pad_none(self, target, axis, depth, clip):
        return self.to_ByteMaskedArray()._pad_none(target, axis, depth, clip)

    def _to_arrow(self, pyarrow, mask_node, validbytes, length, options):
        return self.to_ByteMaskedArray()._to_arrow(
            pyarrow, mask_node, validbytes, length, options
        )

    def _to_backend_array(self, allow_missing, backend):
        return self.to_ByteMaskedArray()._to_backend_array(allow_missing, backend)

    def _remove_structure(self, backend, options):
        branch, depth = self.branch_depth
        if branch or options["drop_nones"] or depth > 1:
            return self.project()._remove_structure(backend, options)
        else:
            return [self]

    def _drop_none(self):
        return self.to_ByteMaskedArray()._drop_none()

    def _recursively_apply(
        self, action, behavior, depth, depth_context, lateral_context, options
    ):
        if self._backend.nplike.known_data:
            content = self._content[0 : self._length]
        else:
            content = self._content

        if options["return_array"]:
            if options["return_simplified"]:
                make = BitMaskedArray.simplified
            else:
                make = BitMaskedArray

            def continuation():
                return make(
                    self._mask,
                    content._recursively_apply(
                        action,
                        behavior,
                        depth,
                        copy.copy(depth_context),
                        lateral_context,
                        options,
                    ),
                    self._valid_when,
                    self._length,
                    self._lsb_order,
                    parameters=self._parameters if options["keep_parameters"] else None,
                )

        else:

            def continuation():
                content._recursively_apply(
                    action,
                    behavior,
                    depth,
                    copy.copy(depth_context),
                    lateral_context,
                    options,
                )

        result = action(
            self,
            depth=depth,
            depth_context=depth_context,
            lateral_context=lateral_context,
            continuation=continuation,
            behavior=behavior,
            backend=self._backend,
            options=options,
        )

        if isinstance(result, Content):
            return result
        elif result is None:
            return continuation()
        else:
            raise ak._errors.wrap_error(AssertionError(result))

    def to_packed(self) -> Self:
        if self._content.is_record:
            next = self.to_IndexedOptionArray64()

            content = next._content.to_packed()
            if content.length > self._length:
                content = content[: self._length]

            return ak.contents.IndexedOptionArray(
                next._index, content, parameters=next._parameters
            )

        else:
            excess_length = int(math.ceil(self._length / 8.0))
            if self._mask.length == excess_length:
                mask = self._mask
            else:
                mask = self._mask[:excess_length]

            content = self._content.to_packed()
            if content.length > self._length:
                content = content[: self._length]

            return BitMaskedArray(
                mask,
                content,
                self._valid_when,
                self._length,
                self._lsb_order,
                parameters=self._parameters,
            )

    def _to_list(self, behavior, json_conversions):
        if not self._backend.nplike.known_data:
            raise ak._errors.wrap_error(
                TypeError("cannot convert typetracer arrays to Python lists")
            )

        out = self._to_list_custom(behavior, json_conversions)
        if out is not None:
            return out

        mask = self.mask_as_bool(valid_when=True)[: self._length]
        out = self._content._getitem_range(0, self._length)._to_list(
            behavior, json_conversions
        )

        for i, isvalid in enumerate(mask):
            if not isvalid:
                out[i] = None

        return out

    def _to_backend(self, backend: ak._backends.Backend) -> Self:
        content = self._content.to_backend(backend)
        mask = self._mask.to_nplike(backend.index_nplike)
        return BitMaskedArray(
            mask,
            content,
            valid_when=self._valid_when,
            length=len(self),
            lsb_order=self._lsb_order,
            parameters=self._parameters,
        )

    def _is_equal_to(self, other, index_dtype, numpyarray):
        return (
            self.valid_when == other.valid_when
            and self.lsb_order == other.lsb_order
            and self.mask.is_equal_to(other.mask, index_dtype, numpyarray)
            and self.content.is_equal_to(other.content, index_dtype, numpyarray)
        )
