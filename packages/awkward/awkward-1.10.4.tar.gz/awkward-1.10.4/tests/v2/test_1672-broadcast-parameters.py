# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import pytest  # noqa: F401
import awkward as ak  # noqa: F401


numpy = ak.nplike.Numpy.instance()


@pytest.mark.skip("string broadcasting is broken")
def test_broadcast_strings_1d():
    this = ak._v2.Array(["one", "two", "one", "nine"])
    that = ak._v2.with_parameter(
        ak._v2.Array(["two", "one", "four", "three"]), "reason", "because!"
    )
    this_next, that_next = ak._v2.operations.ak_broadcast_arrays.broadcast_arrays(
        this, that
    )

    assert this.layout.parameters == this_next.layout.parameters
    assert that.layout.parameters == that_next.layout.parameters


@pytest.mark.skip("string broadcasting is broken")
def test_broadcast_strings_1d_right_broadcast():
    this = ak._v2.Array(["one", "two", "one", "nine"])
    that = ak._v2.operations.ak_to_regular.to_regular(
        ak._v2.with_parameter(ak._v2.Array(["two"]), "reason", "because!"), axis=1
    )
    this_next, that_next = ak._v2.operations.ak_broadcast_arrays.broadcast_arrays(
        this, that
    )

    assert this.layout.parameters == this_next.layout.parameters
    assert that.layout.parameters == that_next.layout.parameters


@pytest.mark.skip("string broadcasting is broken")
def test_broadcast_strings_2d():
    this = ak._v2.Array([["one", "two", "one"], ["nine"]])
    that = ak._v2.to_regular(
        ak._v2.with_parameter(ak._v2.Array([["two"], ["three"]]), "reason", "because!"),
        axis=1,
    )
    this_next, that_next = ak._v2.operations.ak_broadcast_arrays.broadcast_arrays(
        this, that
    )

    assert this.layout.parameters == this_next.layout.parameters
    assert that.layout.parameters == that_next.layout.parameters

    assert this.layout.content.parameters == this_next.layout.content.parameters
    assert that.layout.content.parameters == that_next.layout.content.parameters


@pytest.mark.skip("string broadcasting is broken")
def test_broadcast_string_int():
    this = ak._v2.Array(["one", "two", "one", "nine"])
    that = ak._v2.contents.NumpyArray(
        numpy.array([1, 2, 1, 9], dtype="int32"), parameters={"kind": "integer"}
    )
    this_next, that_next = ak._v2.operations.ak_broadcast_arrays.broadcast_arrays(
        this, that
    )

    assert this.layout.parameters == this_next.layout.parameters
    assert that.layout.parameters == that_next.layout.parameters


def test_broadcast_float_int():
    this = ak._v2.contents.NumpyArray(
        numpy.array([1.0, 2.0, 3.0, 4.0], dtype="float64"), parameters={"name": "this"}
    )
    that = ak._v2.contents.NumpyArray(
        numpy.array([1, 2, 1, 9], dtype="int32"), parameters={"name": "that"}
    )
    this_next, that_next = ak._v2.operations.ak_broadcast_arrays.broadcast_arrays(
        this, that, highlevel=False
    )

    assert this.parameters == this_next.parameters
    assert that.parameters == that_next.parameters


def test_broadcast_float_int_option():
    this = ak._v2.contents.NumpyArray(numpy.arange(4), parameters={"name": "this"})
    that = ak._v2.contents.ByteMaskedArray(
        ak._v2.index.Index8(numpy.array([0, 1, 0, 1])),
        ak._v2.contents.NumpyArray(
            numpy.arange(4),
        ),
        valid_when=True,
        parameters={"name": "that"},
    )
    this_next, that_next = ak._v2.operations.ak_broadcast_arrays.broadcast_arrays(
        this, that, highlevel=False
    )

    assert this.parameters == this_next.parameters
    assert that.parameters == that_next.parameters


def test_broadcast_float_int_union():
    this = ak._v2.contents.NumpyArray(numpy.arange(4), parameters={"name": "this"})
    that_1 = ak._v2.contents.ByteMaskedArray(
        ak._v2.index.Index8(numpy.array([0, 1, 0, 1], dtype="int8")),
        ak._v2.contents.NumpyArray(
            numpy.arange(4),
        ),
        valid_when=True,
        parameters={"name": "that"},
    )
    that_2 = ak._v2.contents.ByteMaskedArray(
        ak._v2.index.Index8(numpy.array([0, 1, 0, 1], dtype="int8")),
        ak._v2.contents.NumpyArray(
            numpy.arange(4, dtype="complex"),
        ),
        valid_when=True,
        parameters={"name": "other"},
    )
    that = ak._v2.contents.UnionArray(
        ak._v2.index.Index8(numpy.array([0, 1, 0, 1], dtype="int8")),
        ak._v2.index.Index32(numpy.array([0, 0, 1, 1], dtype="int32")),
        [that_1, that_2],
    )
    this_next, that_next = ak._v2.operations.ak_broadcast_arrays.broadcast_arrays(
        this, that, highlevel=False
    )

    assert this.parameters == this_next.parameters
    assert that.parameters == that_next.parameters


def test_broadcast_float_int_2d():
    this = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index64(numpy.array([0, 3, 4], dtype="int64")),
        ak._v2.contents.NumpyArray(numpy.array([1.0, 2.0, 3.0, 4.0], dtype="float64")),
        parameters={"name": "this"},
    )
    that = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index64(numpy.array([0, 3, 4], dtype="int64")),
        ak._v2.contents.NumpyArray(numpy.array([1, 2, 1, 9], dtype="int64")),
        parameters={"name": "that"},
    )
    this_next, that_next = ak._v2.operations.ak_broadcast_arrays.broadcast_arrays(
        this, that, highlevel=False
    )

    assert this.parameters == this_next.parameters
    assert that.parameters == that_next.parameters

    assert this.content.parameters == this_next.content.parameters
    assert that.content.parameters == that_next.content.parameters


def test_broadcast_float_int_2d_right_broadcast():
    this = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index64(numpy.array([0, 3, 4], dtype="int64")),
        ak._v2.contents.NumpyArray(numpy.array([1.0, 2.0, 3.0, 4.0], dtype="float64")),
        parameters={"name": "this"},
    )
    that = ak._v2.contents.RegularArray(
        ak._v2.contents.NumpyArray(numpy.array([1, 9], dtype="int64")),
        size=1,
        parameters={"name": "that"},
    )
    this_next, that_next = ak._v2.operations.ak_broadcast_arrays.broadcast_arrays(
        this, that, highlevel=False
    )

    assert this.parameters == this_next.parameters
    assert that.parameters == that_next.parameters

    assert this.content.parameters == this_next.content.parameters
    assert that.content.parameters == that_next.content.parameters


def test_broadcast_float_int_2d_regular():
    this = ak._v2.contents.RegularArray(
        ak._v2.contents.NumpyArray(numpy.array([1.0, 2.0, 3.0, 4.0], dtype="float64")),
        size=2,
        parameters={"name": "this"},
    )
    that = ak._v2.contents.RegularArray(
        ak._v2.contents.NumpyArray(numpy.array([1, 9], dtype="int64")),
        size=1,
        parameters={"name": "that"},
    )
    this_next, that_next = ak._v2.operations.ak_broadcast_arrays.broadcast_arrays(
        this, that, highlevel=False
    )

    assert this.parameters == this_next.parameters
    assert that.parameters == that_next.parameters

    assert this.content.parameters == this_next.content.parameters
    assert that.content.parameters == that_next.content.parameters


def test_broadcast_string_self():
    this = ak._v2.Array(["one", "two", "one", "nine"])
    that = this

    this_next, that_next = ak._v2.operations.ak_broadcast_arrays.broadcast_arrays(
        this, that
    )

    assert this.layout.parameters == this_next.layout.parameters
    assert that.layout.parameters == that_next.layout.parameters


def test_transform_float_int_2d_same():
    this = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index64(numpy.array([0, 3, 4], dtype="int64")),
        ak._v2.contents.NumpyArray(numpy.array([1.0, 2.0, 3.0, 4.0], dtype="float64")),
        parameters={"name": "this"},
    )
    that = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index64(numpy.array([0, 3, 4], dtype="int64")),
        ak._v2.contents.NumpyArray(numpy.array([1, 2, 1, 9], dtype="int64")),
        parameters={"name": "this"},
    )
    this_next, that_next = ak._v2.operations.ak_transform.transform(
        lambda *a, **k: None, this, that, highlevel=False
    )

    assert this_next.parameters == that_next.parameters
    assert this_next.parameters != {}


def test_transform_float_int_2d_different_one_to_one():
    this = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index64(numpy.array([0, 3, 4], dtype="int64")),
        ak._v2.contents.NumpyArray(numpy.array([1.0, 2.0, 3.0, 4.0], dtype="float64")),
        parameters={"name": "this"},
    )
    that = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index64(numpy.array([0, 3, 4], dtype="int64")),
        ak._v2.contents.NumpyArray(numpy.array([1, 2, 1, 9], dtype="int64")),
        parameters={"name": "that"},
    )
    this_next, that_next = ak._v2.operations.ak_transform.transform(
        lambda *a, **k: None,
        this,
        that,
        highlevel=False,
        broadcast_parameters_rule="one_to_one",
    )

    assert this_next.parameters == this.parameters
    assert that_next.parameters == that.parameters


def test_transform_float_int_2d_different_intersect():
    this = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index64(numpy.array([0, 3, 4], dtype="int64")),
        ak._v2.contents.NumpyArray(numpy.array([1.0, 2.0, 3.0, 4.0], dtype="float64")),
        parameters={
            "name": "this",
            "key": "value",
            "parent": {"child": 1},
            "pets": [{"name": "fido"}],
        },
    )
    that = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index64(numpy.array([0, 3, 4], dtype="int64")),
        ak._v2.contents.NumpyArray(numpy.array([1, 2, 1, 9], dtype="int64")),
        parameters={
            "name": "that",
            "key": "value",
            "parent": {"child": 2},
            "pets": [{"name": "fido"}],
        },
    )
    this_next, that_next = ak._v2.operations.ak_transform.transform(
        lambda *a, **k: None,
        this,
        that,
        highlevel=False,
        broadcast_parameters_rule="intersect",
    )

    assert this_next.parameters == that_next.parameters
    assert that_next.parameters == {"key": "value", "pets": [{"name": "fido"}]}


def test_transform_float_int_2d_one_to_one_error():
    this = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index64(numpy.array([0, 3, 4], dtype="int64")),
        ak._v2.contents.NumpyArray(numpy.array([1.0, 2.0, 3.0, 4.0], dtype="float64")),
        parameters={"name": "this"},
    )
    that = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index64(numpy.array([0, 3, 4], dtype="int64")),
        ak._v2.contents.NumpyArray(numpy.array([1, 2, 1, 9], dtype="int64")),
        parameters={"name": "that"},
    )

    def apply(arrays, **kwargs):
        layout = ak._v2.operations.ak_to_layout.to_layout(arrays[0])
        if isinstance(layout, ak._v2.contents.NumpyArray):
            return layout

    with pytest.raises(ValueError):
        ak._v2.operations.ak_transform.transform(
            apply, this, that, highlevel=False, broadcast_parameters_rule="one_to_one"
        )


def test_transform_string_self_one_to_one():
    this = ak._v2.Array(["one", "two", "one", "nine"])
    that = this

    def apply(arrays, **kwargs):
        layout = ak._v2.operations.ak_to_layout.to_layout(arrays[0])
        if layout.parameter("__array__") is not None:
            return arrays

    this_next, that_next = ak._v2.operations.ak_transform.transform(
        apply, this, that, broadcast_parameters_rule="one_to_one"
    )

    assert this.layout.parameters == this_next.layout.parameters
    assert that.layout.parameters == that_next.layout.parameters


@pytest.mark.parametrize("rule", ["all_or_nothing", "intersect", "one_to_one"])
def test_transform_string_self_intersect(rule):
    this = ak._v2.Array(["one", "two", "one", "nine"])
    that = this

    def apply(arrays, **kwargs):
        layout = ak._v2.operations.ak_to_layout.to_layout(arrays[0])
        if layout.parameter("__array__") is not None:
            return arrays

    this_next, that_next = ak._v2.operations.ak_transform.transform(
        apply, this, that, broadcast_parameters_rule=rule
    )

    assert this.layout.parameters == this_next.layout.parameters
    assert that.layout.parameters == that_next.layout.parameters
