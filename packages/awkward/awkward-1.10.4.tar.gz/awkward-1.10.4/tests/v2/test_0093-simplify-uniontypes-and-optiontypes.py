# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

to_list = ak._v2.operations.to_list


def test_numpyarray_merge():
    emptyarray = ak._v2.contents.EmptyArray()

    np1 = np.arange(2 * 7 * 5).reshape(2, 7, 5)
    np2 = np.arange(3 * 7 * 5).reshape(3, 7, 5)
    ak1 = ak._v2.contents.NumpyArray(np1)
    ak2 = ak._v2.contents.NumpyArray(np2)
    assert to_list(ak1.merge(ak2)) == to_list(np.concatenate([np1, np2]))
    assert to_list(ak1[1:, :-1, ::-1].merge(ak2[1:, :-1, ::-1])) == to_list(
        np.concatenate([np1[1:, :-1, ::-1], np2[1:, :-1, ::-1]])
    )
    assert ak1.typetracer.merge(ak2).form == ak1.merge(ak2).form
    assert (
        ak1[1:, :-1, ::-1].typetracer.merge(ak2[1:, :-1, ::-1]).form
        == ak1[1:, :-1, ::-1].merge(ak2[1:, :-1, ::-1]).form
    )

    for x in [
        np.bool_,
        np.int8,
        np.int16,
        np.int32,
        np.int64,
        np.uint8,
        np.uint16,
        np.uint32,
        np.uint64,
        np.float32,
        np.float64,
    ]:
        for y in [
            np.bool_,
            np.int8,
            np.int16,
            np.int32,
            np.int64,
            np.uint8,
            np.uint16,
            np.uint32,
            np.uint64,
            np.float32,
            np.float64,
        ]:
            z = np.concatenate(
                [np.array([1, 2, 3], dtype=x), np.array([4, 5], dtype=y)]
            ).dtype.type
            one = ak._v2.contents.NumpyArray(np.array([1, 2, 3], dtype=x))
            two = ak._v2.contents.NumpyArray(np.array([4, 5], dtype=y))
            three = one.merge(two)
            assert np.asarray(three).dtype == np.dtype(z), "{} {} {} {}".format(
                x, y, z, np.asarray(three).dtype.type
            )
            assert to_list(three) == to_list(
                np.concatenate([np.asarray(one), np.asarray(two)])
            )
            assert to_list(one.merge(emptyarray)) == to_list(one)
            assert to_list(emptyarray.merge(one)) == to_list(one)

            assert one.typetracer.merge(two).form == one.merge(two).form
            assert one.typetracer.merge(emptyarray).form == one.merge(emptyarray).form
            assert emptyarray.typetracer.merge(one).form == emptyarray.merge(one).form


def test_regulararray_merge():
    emptyarray = ak._v2.contents.EmptyArray()

    np1 = np.arange(2 * 7 * 5).reshape(2, 7, 5)
    np2 = np.arange(3 * 7 * 5).reshape(3, 7, 5)
    ak1 = ak._v2.operations.from_iter(np1, highlevel=False)
    ak2 = ak._v2.operations.from_iter(np2, highlevel=False)

    assert to_list(ak1.merge(ak2)) == to_list(np.concatenate([np1, np2]))
    assert to_list(ak1.merge(emptyarray)) == to_list(ak1)
    assert to_list(emptyarray.merge(ak1)) == to_list(ak1)

    assert ak1.typetracer.merge(ak2).form == ak1.merge(ak2).form
    assert ak1.typetracer.merge(emptyarray).form == ak1.merge(emptyarray).form
    assert emptyarray.typetracer.merge(ak1).form == emptyarray.merge(ak1).form


def test_listarray_merge():
    emptyarray = ak._v2.contents.EmptyArray()

    content1 = ak._v2.contents.NumpyArray(np.array([1.1, 2.2, 3.3, 4.4, 5.5]))
    content2 = ak._v2.contents.NumpyArray(np.array([1, 2, 3, 4, 5, 6, 7]))

    for (dtype1, Index1, ListArray1), (dtype2, Index2, ListArray2) in [
        (
            (np.int32, ak._v2.index.Index32, ak._v2.contents.ListArray),
            (np.int32, ak._v2.index.Index32, ak._v2.contents.ListArray),
        ),
        (
            (np.int32, ak._v2.index.Index32, ak._v2.contents.ListArray),
            (np.uint32, ak._v2.index.IndexU32, ak._v2.contents.ListArray),
        ),
        (
            (np.int32, ak._v2.index.Index32, ak._v2.contents.ListArray),
            (np.int64, ak._v2.index.Index64, ak._v2.contents.ListArray),
        ),
        (
            (np.uint32, ak._v2.index.IndexU32, ak._v2.contents.ListArray),
            (np.int32, ak._v2.index.Index32, ak._v2.contents.ListArray),
        ),
        (
            (np.uint32, ak._v2.index.IndexU32, ak._v2.contents.ListArray),
            (np.uint32, ak._v2.index.IndexU32, ak._v2.contents.ListArray),
        ),
        (
            (np.uint32, ak._v2.index.IndexU32, ak._v2.contents.ListArray),
            (np.int64, ak._v2.index.Index64, ak._v2.contents.ListArray),
        ),
        (
            (np.int64, ak._v2.index.Index64, ak._v2.contents.ListArray),
            (np.int32, ak._v2.index.Index32, ak._v2.contents.ListArray),
        ),
        (
            (np.int64, ak._v2.index.Index64, ak._v2.contents.ListArray),
            (np.uint32, ak._v2.index.IndexU32, ak._v2.contents.ListArray),
        ),
        (
            (np.int64, ak._v2.index.Index64, ak._v2.contents.ListArray),
            (np.int64, ak._v2.index.Index64, ak._v2.contents.ListArray),
        ),
    ]:
        starts1 = Index1(np.array([0, 3, 3], dtype=dtype1))
        stops1 = Index1(np.array([3, 3, 5], dtype=dtype1))
        starts2 = Index2(np.array([2, 99, 0], dtype=dtype2))
        stops2 = Index2(np.array([6, 99, 3], dtype=dtype2))
        array1 = ListArray1(starts1, stops1, content1)
        array2 = ListArray2(starts2, stops2, content2)
        assert to_list(array1) == [[1.1, 2.2, 3.3], [], [4.4, 5.5]]
        assert to_list(array2) == [[3, 4, 5, 6], [], [1, 2, 3]]

        assert to_list(array1.merge(array2)) == [
            [1.1, 2.2, 3.3],
            [],
            [4.4, 5.5],
            [3, 4, 5, 6],
            [],
            [1, 2, 3],
        ]
        assert to_list(array2.merge(array1)) == [
            [3, 4, 5, 6],
            [],
            [1, 2, 3],
            [1.1, 2.2, 3.3],
            [],
            [4.4, 5.5],
        ]
        assert to_list(array1.merge(emptyarray)) == to_list(array1)
        assert to_list(emptyarray.merge(array1)) == to_list(array1)

        assert array1.typetracer.merge(array2).form == array1.merge(array2).form
        assert array2.typetracer.merge(array1).form == array2.merge(array1).form
        assert array1.typetracer.merge(emptyarray).form == array1.merge(emptyarray).form
        assert emptyarray.typetracer.merge(array1).form == emptyarray.merge(array1).form

    regulararray = ak._v2.contents.RegularArray(content2, 2, zeros_length=0)
    assert to_list(regulararray) == [[1, 2], [3, 4], [5, 6]]
    assert to_list(regulararray.merge(emptyarray)) == to_list(regulararray)
    assert to_list(emptyarray.merge(regulararray)) == to_list(regulararray)

    for (dtype1, Index1, ListArray1) in [
        (np.int32, ak._v2.index.Index32, ak._v2.contents.ListArray),
        (np.uint32, ak._v2.index.IndexU32, ak._v2.contents.ListArray),
        (np.int64, ak._v2.index.Index64, ak._v2.contents.ListArray),
    ]:
        starts1 = Index1(np.array([0, 3, 3], dtype=dtype1))
        stops1 = Index1(np.array([3, 3, 5], dtype=dtype1))
        array1 = ListArray1(starts1, stops1, content1)

        assert to_list(array1.merge(regulararray)) == [
            [1.1, 2.2, 3.3],
            [],
            [4.4, 5.5],
            [1, 2],
            [3, 4],
            [5, 6],
        ]
        assert to_list(regulararray.merge(array1)) == [
            [1, 2],
            [3, 4],
            [5, 6],
            [1.1, 2.2, 3.3],
            [],
            [4.4, 5.5],
        ]


def test_listoffsetarray_merge():
    emptyarray = ak._v2.contents.EmptyArray()

    content1 = ak._v2.contents.NumpyArray(np.array([1.1, 2.2, 3.3, 4.4, 5.5]))
    content2 = ak._v2.contents.NumpyArray(np.array([1, 2, 3, 4, 5, 6, 7]))

    for (dtype1, Index1, ListOffsetArray1), (dtype2, Index2, ListOffsetArray2) in [
        (
            (np.int32, ak._v2.index.Index32, ak._v2.contents.ListOffsetArray),
            (np.int32, ak._v2.index.Index32, ak._v2.contents.ListOffsetArray),
        ),
        (
            (np.int32, ak._v2.index.Index32, ak._v2.contents.ListOffsetArray),
            (np.uint32, ak._v2.index.IndexU32, ak._v2.contents.ListOffsetArray),
        ),
        (
            (np.int32, ak._v2.index.Index32, ak._v2.contents.ListOffsetArray),
            (np.int64, ak._v2.index.Index64, ak._v2.contents.ListOffsetArray),
        ),
        (
            (np.uint32, ak._v2.index.IndexU32, ak._v2.contents.ListOffsetArray),
            (np.int32, ak._v2.index.Index32, ak._v2.contents.ListOffsetArray),
        ),
        (
            (np.uint32, ak._v2.index.IndexU32, ak._v2.contents.ListOffsetArray),
            (np.uint32, ak._v2.index.IndexU32, ak._v2.contents.ListOffsetArray),
        ),
        (
            (np.uint32, ak._v2.index.IndexU32, ak._v2.contents.ListOffsetArray),
            (np.int64, ak._v2.index.Index64, ak._v2.contents.ListOffsetArray),
        ),
        (
            (np.int64, ak._v2.index.Index64, ak._v2.contents.ListOffsetArray),
            (np.int32, ak._v2.index.Index32, ak._v2.contents.ListOffsetArray),
        ),
        (
            (np.int64, ak._v2.index.Index64, ak._v2.contents.ListOffsetArray),
            (np.uint32, ak._v2.index.IndexU32, ak._v2.contents.ListOffsetArray),
        ),
        (
            (np.int64, ak._v2.index.Index64, ak._v2.contents.ListOffsetArray),
            (np.int64, ak._v2.index.Index64, ak._v2.contents.ListOffsetArray),
        ),
    ]:
        offsets1 = Index1(np.array([0, 3, 3, 5], dtype=dtype1))
        offsets2 = Index2(np.array([1, 3, 3, 3, 5], dtype=dtype2))
        array1 = ListOffsetArray1(offsets1, content1)
        array2 = ListOffsetArray2(offsets2, content2)
        assert to_list(array1) == [[1.1, 2.2, 3.3], [], [4.4, 5.5]]
        assert to_list(array2) == [[2, 3], [], [], [4, 5]]

        assert to_list(array1.merge(array2)) == [
            [1.1, 2.2, 3.3],
            [],
            [4.4, 5.5],
            [2, 3],
            [],
            [],
            [4, 5],
        ]
        assert to_list(array2.merge(array1)) == [
            [2, 3],
            [],
            [],
            [4, 5],
            [1.1, 2.2, 3.3],
            [],
            [4.4, 5.5],
        ]
        assert to_list(array1.merge(emptyarray)) == to_list(array1)
        assert to_list(emptyarray.merge(array1)) == to_list(array1)

        assert array1.typetracer.merge(array2).form == array1.merge(array2).form
        assert array2.typetracer.merge(array1).form == array2.merge(array1).form
        assert array1.typetracer.merge(emptyarray).form == array1.merge(emptyarray).form
        assert emptyarray.typetracer.merge(array1).form == emptyarray.merge(array1).form

    regulararray = ak._v2.contents.RegularArray(content2, 2, zeros_length=0)
    assert to_list(regulararray) == [[1, 2], [3, 4], [5, 6]]

    for (dtype1, Index1, ListArray1) in [
        (np.int32, ak._v2.index.Index32, ak._v2.contents.ListArray),
        (np.uint32, ak._v2.index.IndexU32, ak._v2.contents.ListArray),
        (np.int64, ak._v2.index.Index64, ak._v2.contents.ListArray),
    ]:
        starts1 = Index1(np.array([0, 3, 3], dtype=dtype1))
        stops1 = Index1(np.array([3, 3, 5], dtype=dtype1))
        array1 = ListArray1(starts1, stops1, content1)

        assert to_list(array1.merge(regulararray)) == [
            [1.1, 2.2, 3.3],
            [],
            [4.4, 5.5],
            [1, 2],
            [3, 4],
            [5, 6],
        ]
        assert to_list(regulararray.merge(array1)) == [
            [1, 2],
            [3, 4],
            [5, 6],
            [1.1, 2.2, 3.3],
            [],
            [4.4, 5.5],
        ]

        assert (
            array1.typetracer.merge(regulararray).form
            == array1.merge(regulararray).form
        )
        assert (
            regulararray.typetracer.merge(array1).form
            == regulararray.merge(array1).form
        )


def test_recordarray_merge():
    emptyarray = ak._v2.contents.EmptyArray()

    arrayr1 = ak._v2.operations.from_iter(
        [{"x": 0, "y": []}, {"x": 1, "y": [1, 1]}, {"x": 2, "y": [2, 2]}],
        highlevel=False,
    )
    arrayr2 = ak._v2.operations.from_iter(
        [
            {"x": 2.2, "y": [2.2, 2.2]},
            {"x": 1.1, "y": [1.1, 1.1]},
            {"x": 0.0, "y": [0.0, 0.0]},
        ],
        highlevel=False,
    )
    arrayr3 = ak._v2.operations.from_iter(
        [{"x": 0, "y": 0.0}, {"x": 1, "y": 1.1}, {"x": 2, "y": 2.2}],
        highlevel=False,
    )
    arrayr4 = ak._v2.operations.from_iter(
        [{"y": [], "x": 0}, {"y": [1, 1], "x": 1}, {"y": [2, 2], "x": 2}],
        highlevel=False,
    )
    arrayr5 = ak._v2.operations.from_iter(
        [
            {"x": 0, "y": [], "z": 0},
            {"x": 1, "y": [1, 1], "z": 1},
            {"x": 2, "y": [2, 2], "z": 2},
        ],
        highlevel=False,
    )
    arrayr6 = ak._v2.operations.from_iter(
        [
            {"z": 0, "x": 0, "y": []},
            {"z": 1, "x": 1, "y": [1, 1]},
            {"z": 2, "x": 2, "y": [2, 2]},
        ],
        highlevel=False,
    )
    arrayr7 = ak._v2.operations.from_iter(
        [{"x": 0}, {"x": 1}, {"x": 2}], highlevel=False
    )

    arrayt1 = ak._v2.operations.from_iter(
        [(0, []), (1, [1.1]), (2, [2, 2])], highlevel=False
    )
    arrayt2 = ak._v2.operations.from_iter(
        [(2.2, [2.2, 2.2]), (1.1, [1.1, 1.1]), (0.0, [0.0, 0.0])], highlevel=False
    )
    arrayt3 = ak._v2.operations.from_iter(
        [(0, 0.0), (1, 1.1), (2, 2.2)], highlevel=False
    )
    arrayt4 = ak._v2.operations.from_iter(
        [([], 0), ([1.1], 1), ([2.2, 2.2], 2)], highlevel=False
    )
    arrayt5 = ak._v2.operations.from_iter(
        [(0, [], 0), (1, [1], 1), (2, [2, 2], 2)], highlevel=False
    )
    arrayt6 = ak._v2.operations.from_iter(
        [(0, 0, []), (1, 1, [1]), (2, 2, [2, 2])], highlevel=False
    )
    arrayt7 = ak._v2.operations.from_iter([(0,), (1,), (2,)], highlevel=False)

    assert arrayr1.mergeable(arrayr2)
    assert arrayr2.mergeable(arrayr1)
    assert not arrayr1.mergeable(arrayr3)
    assert arrayr1.mergeable(arrayr4)
    assert arrayr4.mergeable(arrayr1)
    assert not arrayr1.mergeable(arrayr5)
    assert not arrayr1.mergeable(arrayr6)
    assert arrayr5.mergeable(arrayr6)
    assert arrayr6.mergeable(arrayr5)
    assert not arrayr1.mergeable(arrayr7)

    assert arrayt1.mergeable(arrayt2)
    assert arrayt2.mergeable(arrayt1)
    assert not arrayt1.mergeable(arrayt3)
    assert not arrayt1.mergeable(arrayt4)
    assert not arrayt1.mergeable(arrayt5)
    assert not arrayt1.mergeable(arrayt6)
    assert not arrayt5.mergeable(arrayt6)
    assert not arrayt1.mergeable(arrayt7)

    assert to_list(arrayr1.merge(arrayr2)) == [
        {"x": 0.0, "y": []},
        {"x": 1.0, "y": [1.0, 1.0]},
        {"x": 2.0, "y": [2.0, 2.0]},
        {"x": 2.2, "y": [2.2, 2.2]},
        {"x": 1.1, "y": [1.1, 1.1]},
        {"x": 0.0, "y": [0.0, 0.0]},
    ]
    assert to_list(arrayr2.merge(arrayr1)) == [
        {"x": 2.2, "y": [2.2, 2.2]},
        {"x": 1.1, "y": [1.1, 1.1]},
        {"x": 0.0, "y": [0.0, 0.0]},
        {"x": 0.0, "y": []},
        {"x": 1.0, "y": [1.0, 1.0]},
        {"x": 2.0, "y": [2.0, 2.0]},
    ]

    assert to_list(arrayr1.merge(arrayr4)) == [
        {"x": 0, "y": []},
        {"x": 1, "y": [1, 1]},
        {"x": 2, "y": [2, 2]},
        {"x": 0, "y": []},
        {"x": 1, "y": [1, 1]},
        {"x": 2, "y": [2, 2]},
    ]
    assert to_list(arrayr4.merge(arrayr1)) == [
        {"x": 0, "y": []},
        {"x": 1, "y": [1, 1]},
        {"x": 2, "y": [2, 2]},
        {"x": 0, "y": []},
        {"x": 1, "y": [1, 1]},
        {"x": 2, "y": [2, 2]},
    ]

    assert to_list(arrayr5.merge(arrayr6)) == [
        {"x": 0, "y": [], "z": 0},
        {"x": 1, "y": [1, 1], "z": 1},
        {"x": 2, "y": [2, 2], "z": 2},
        {"x": 0, "y": [], "z": 0},
        {"x": 1, "y": [1, 1], "z": 1},
        {"x": 2, "y": [2, 2], "z": 2},
    ]
    assert to_list(arrayr6.merge(arrayr5)) == [
        {"x": 0, "y": [], "z": 0},
        {"x": 1, "y": [1, 1], "z": 1},
        {"x": 2, "y": [2, 2], "z": 2},
        {"x": 0, "y": [], "z": 0},
        {"x": 1, "y": [1, 1], "z": 1},
        {"x": 2, "y": [2, 2], "z": 2},
    ]

    assert to_list(arrayt1.merge(arrayt2)) == [
        (0.0, []),
        (1.0, [1.1]),
        (2.0, [2.0, 2.0]),
        (2.2, [2.2, 2.2]),
        (1.1, [1.1, 1.1]),
        (0.0, [0.0, 0.0]),
    ]
    assert to_list(arrayt2.merge(arrayt1)) == [
        (2.2, [2.2, 2.2]),
        (1.1, [1.1, 1.1]),
        (0.0, [0.0, 0.0]),
        (0.0, []),
        (1.0, [1.1]),
        (2.0, [2.0, 2.0]),
    ]

    assert arrayr1.typetracer.merge(arrayr2).form == arrayr1.merge(arrayr2).form
    assert arrayr2.typetracer.merge(arrayr1).form == arrayr2.merge(arrayr1).form
    assert arrayr1.typetracer.merge(arrayr4).form == arrayr1.merge(arrayr4).form
    assert arrayr4.typetracer.merge(arrayr1).form == arrayr4.merge(arrayr1).form
    assert arrayr5.typetracer.merge(arrayr6).form == arrayr5.merge(arrayr6).form
    assert arrayr6.typetracer.merge(arrayr5).form == arrayr6.merge(arrayr5).form
    assert arrayt1.typetracer.merge(arrayt2).form == arrayt1.merge(arrayt2).form
    assert arrayt2.typetracer.merge(arrayt1).form == arrayt2.merge(arrayt1).form

    assert to_list(arrayr1.merge(emptyarray)) == to_list(arrayr1)
    assert to_list(arrayr2.merge(emptyarray)) == to_list(arrayr2)
    assert to_list(arrayr3.merge(emptyarray)) == to_list(arrayr3)
    assert to_list(arrayr4.merge(emptyarray)) == to_list(arrayr4)
    assert to_list(arrayr5.merge(emptyarray)) == to_list(arrayr5)
    assert to_list(arrayr6.merge(emptyarray)) == to_list(arrayr6)
    assert to_list(arrayr7.merge(emptyarray)) == to_list(arrayr7)

    assert to_list(emptyarray.merge(arrayr1)) == to_list(arrayr1)
    assert to_list(emptyarray.merge(arrayr2)) == to_list(arrayr2)
    assert to_list(emptyarray.merge(arrayr3)) == to_list(arrayr3)
    assert to_list(emptyarray.merge(arrayr4)) == to_list(arrayr4)
    assert to_list(emptyarray.merge(arrayr5)) == to_list(arrayr5)
    assert to_list(emptyarray.merge(arrayr6)) == to_list(arrayr6)
    assert to_list(emptyarray.merge(arrayr7)) == to_list(arrayr7)

    assert to_list(arrayt1.merge(emptyarray)) == to_list(arrayt1)
    assert to_list(arrayt2.merge(emptyarray)) == to_list(arrayt2)
    assert to_list(arrayt3.merge(emptyarray)) == to_list(arrayt3)
    assert to_list(arrayt4.merge(emptyarray)) == to_list(arrayt4)
    assert to_list(arrayt5.merge(emptyarray)) == to_list(arrayt5)
    assert to_list(arrayt6.merge(emptyarray)) == to_list(arrayt6)
    assert to_list(arrayt7.merge(emptyarray)) == to_list(arrayt7)

    assert to_list(emptyarray.merge(arrayt1)) == to_list(arrayt1)
    assert to_list(emptyarray.merge(arrayt2)) == to_list(arrayt2)
    assert to_list(emptyarray.merge(arrayt3)) == to_list(arrayt3)
    assert to_list(emptyarray.merge(arrayt4)) == to_list(arrayt4)
    assert to_list(emptyarray.merge(arrayt5)) == to_list(arrayt5)
    assert to_list(emptyarray.merge(arrayt6)) == to_list(arrayt6)
    assert to_list(emptyarray.merge(arrayt7)) == to_list(arrayt7)

    assert arrayr1.typetracer.merge(emptyarray).form == arrayr1.merge(emptyarray).form
    assert arrayr2.typetracer.merge(emptyarray).form == arrayr2.merge(emptyarray).form
    assert arrayr3.typetracer.merge(emptyarray).form == arrayr3.merge(emptyarray).form
    assert arrayr4.typetracer.merge(emptyarray).form == arrayr4.merge(emptyarray).form
    assert arrayr5.typetracer.merge(emptyarray).form == arrayr5.merge(emptyarray).form
    assert arrayr6.typetracer.merge(emptyarray).form == arrayr6.merge(emptyarray).form
    assert arrayr7.typetracer.merge(emptyarray).form == arrayr7.merge(emptyarray).form

    assert emptyarray.typetracer.merge(arrayr1).form == emptyarray.merge(arrayr1).form
    assert emptyarray.typetracer.merge(arrayr2).form == emptyarray.merge(arrayr2).form
    assert emptyarray.typetracer.merge(arrayr3).form == emptyarray.merge(arrayr3).form
    assert emptyarray.typetracer.merge(arrayr4).form == emptyarray.merge(arrayr4).form
    assert emptyarray.typetracer.merge(arrayr5).form == emptyarray.merge(arrayr5).form
    assert emptyarray.typetracer.merge(arrayr6).form == emptyarray.merge(arrayr6).form
    assert emptyarray.typetracer.merge(arrayr7).form == emptyarray.merge(arrayr7).form

    assert arrayt1.typetracer.merge(emptyarray).form == arrayt1.merge(emptyarray).form
    assert arrayt2.typetracer.merge(emptyarray).form == arrayt2.merge(emptyarray).form
    assert arrayt3.typetracer.merge(emptyarray).form == arrayt3.merge(emptyarray).form
    assert arrayt4.typetracer.merge(emptyarray).form == arrayt4.merge(emptyarray).form
    assert arrayt5.typetracer.merge(emptyarray).form == arrayt5.merge(emptyarray).form
    assert arrayt6.typetracer.merge(emptyarray).form == arrayt6.merge(emptyarray).form
    assert arrayt7.typetracer.merge(emptyarray).form == arrayt7.merge(emptyarray).form

    assert emptyarray.typetracer.merge(arrayt1).form == emptyarray.merge(arrayt1).form
    assert emptyarray.typetracer.merge(arrayt2).form == emptyarray.merge(arrayt2).form
    assert emptyarray.typetracer.merge(arrayt3).form == emptyarray.merge(arrayt3).form
    assert emptyarray.typetracer.merge(arrayt4).form == emptyarray.merge(arrayt4).form
    assert emptyarray.typetracer.merge(arrayt5).form == emptyarray.merge(arrayt5).form
    assert emptyarray.typetracer.merge(arrayt6).form == emptyarray.merge(arrayt6).form
    assert emptyarray.typetracer.merge(arrayt7).form == emptyarray.merge(arrayt7).form


def test_indexedarray_merge():
    content1 = ak._v2.operations.from_iter(
        [[1.1, 2.2, 3.3], [], [4.4, 5.5]], highlevel=False
    )
    content2 = ak._v2.operations.from_iter([[1, 2], [], [3, 4]], highlevel=False)
    index1 = ak._v2.index.Index64(np.array([2, 0, -1, 0, 1, 2], dtype=np.int64))
    indexedarray1 = ak._v2.contents.IndexedOptionArray(index1, content1)

    assert to_list(indexedarray1) == [
        [4.4, 5.5],
        [1.1, 2.2, 3.3],
        None,
        [1.1, 2.2, 3.3],
        [],
        [4.4, 5.5],
    ]

    assert to_list(indexedarray1.merge(content2)) == [
        [4.4, 5.5],
        [1.1, 2.2, 3.3],
        None,
        [1.1, 2.2, 3.3],
        [],
        [4.4, 5.5],
        [1.0, 2.0],
        [],
        [3.0, 4.0],
    ]
    assert to_list(content2.merge(indexedarray1)) == [
        [1.0, 2.0],
        [],
        [3.0, 4.0],
        [4.4, 5.5],
        [1.1, 2.2, 3.3],
        None,
        [1.1, 2.2, 3.3],
        [],
        [4.4, 5.5],
    ]
    assert to_list(indexedarray1.merge(indexedarray1)) == [
        [4.4, 5.5],
        [1.1, 2.2, 3.3],
        None,
        [1.1, 2.2, 3.3],
        [],
        [4.4, 5.5],
        [4.4, 5.5],
        [1.1, 2.2, 3.3],
        None,
        [1.1, 2.2, 3.3],
        [],
        [4.4, 5.5],
    ]

    assert (
        indexedarray1.typetracer.merge(content2).form
        == indexedarray1.merge(content2).form
    )
    assert (
        content2.typetracer.merge(indexedarray1).form
        == content2.merge(indexedarray1).form
    )
    assert (
        indexedarray1.typetracer.merge(indexedarray1).form
        == indexedarray1.merge(indexedarray1).form
    )


def test_unionarray_merge():
    emptyarray = ak._v2.contents.EmptyArray()

    one = ak._v2.operations.from_iter([0.0, 1.1, 2.2, [], [1], [2, 2]], highlevel=False)
    two = ak._v2.operations.from_iter(
        [{"x": 1, "y": 1.1}, 999, 123, {"x": 2, "y": 2.2}], highlevel=False
    )
    three = ak._v2.operations.from_iter(["one", "two", "three"], highlevel=False)

    assert to_list(one.merge(two)) == [
        0.0,
        1.1,
        2.2,
        [],
        [1],
        [2, 2],
        {"x": 1, "y": 1.1},
        999,
        123,
        {"x": 2, "y": 2.2},
    ]
    assert to_list(two.merge(one)) == [
        {"x": 1, "y": 1.1},
        999,
        123,
        {"x": 2, "y": 2.2},
        0.0,
        1.1,
        2.2,
        [],
        [1],
        [2, 2],
    ]

    assert to_list(one.merge(emptyarray)) == [0.0, 1.1, 2.2, [], [1], [2, 2]]
    assert to_list(emptyarray.merge(one)) == [0.0, 1.1, 2.2, [], [1], [2, 2]]

    assert to_list(one.merge(three)) == [
        0.0,
        1.1,
        2.2,
        [],
        [1],
        [2, 2],
        "one",
        "two",
        "three",
    ]
    assert to_list(two.merge(three)) == [
        {"x": 1, "y": 1.1},
        999,
        123,
        {"x": 2, "y": 2.2},
        "one",
        "two",
        "three",
    ]
    assert to_list(three.merge(one)) == [
        "one",
        "two",
        "three",
        0.0,
        1.1,
        2.2,
        [],
        [1],
        [2, 2],
    ]
    assert to_list(three.merge(two)) == [
        "one",
        "two",
        "three",
        {"x": 1, "y": 1.1},
        999,
        123,
        {"x": 2, "y": 2.2},
    ]

    assert one.typetracer.merge(two).form == one.merge(two).form
    assert two.typetracer.merge(one).form == two.merge(one).form
    assert one.typetracer.merge(emptyarray).form == one.merge(emptyarray).form
    assert emptyarray.typetracer.merge(one).form == emptyarray.merge(one).form
    assert one.typetracer.merge(three).form == one.merge(three).form
    assert two.typetracer.merge(three).form == two.merge(three).form
    assert three.typetracer.merge(one).form == three.merge(one).form
    assert three.typetracer.merge(two).form == three.merge(two).form


def test_merge_parameters():
    one = ak._v2.operations.from_iter(
        [[121, 117, 99, 107, 121], [115, 116, 117, 102, 102]], highlevel=False
    )
    two = ak._v2.operations.from_iter(["good", "stuff"], highlevel=False)

    assert to_list(ak._v2.operations.concatenate([one, two])) == [
        [121, 117, 99, 107, 121],
        [115, 116, 117, 102, 102],
        "good",
        "stuff",
    ]
    assert to_list(ak._v2.operations.concatenate([two, one])) == [
        "good",
        "stuff",
        [121, 117, 99, 107, 121],
        [115, 116, 117, 102, 102],
    ]

    assert (
        ak._v2.operations.concatenate([one, two], highlevel=False).typetracer.form
        == ak._v2.operations.concatenate([one, two], highlevel=False).form
    )
    assert (
        ak._v2.operations.concatenate([two, one], highlevel=False).typetracer.form
        == ak._v2.operations.concatenate([two, one], highlevel=False).form
    )


def test_mask_as_bool():
    array = ak._v2.operations.from_iter(
        ["one", "two", None, "three", None, None, "four"], highlevel=False
    )
    index2 = ak._v2.index.Index64(np.array([2, 2, 1, 5, 0], dtype=np.int64))
    array2 = ak._v2.contents.IndexedArray(index2, array)
    assert np.asarray(array.mask_as_bool(valid_when=False).view(np.int8)).tolist() == [
        0,
        0,
        1,
        0,
        1,
        1,
        0,
    ]
    assert np.asarray(array2.mask_as_bool(valid_when=False).view(np.int8)).tolist() == [
        0,
        0,
        0,
        0,
        0,
    ]


def test_indexedarray_simplify():
    array = ak._v2.operations.from_iter(
        ["one", "two", None, "three", None, None, "four", "five"], highlevel=False
    )
    index2 = ak._v2.index.Index64(np.array([2, 2, 1, 6, 5], dtype=np.int64))

    array2 = ak._v2.contents.IndexedArray(index2, array)
    assert np.asarray(array.index).tolist() == [0, 1, -1, 2, -1, -1, 3, 4]
    assert (
        to_list(array2.simplify_optiontype())
        == to_list(array2)
        == [None, None, "two", "four", None]
    )

    assert (
        array2.typetracer.simplify_optiontype().form
        == array2.simplify_optiontype().form
    )


def test_indexedarray_simplify_more():
    content = ak._v2.contents.NumpyArray(
        np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9])
    )

    index1_32 = ak._v2.index.Index32(np.array([6, 5, 4, 3, 2, 1, 0], dtype=np.int32))
    index1_U32 = ak._v2.index.IndexU32(np.array([6, 5, 4, 3, 2, 1, 0], dtype=np.uint32))
    index1_64 = ak._v2.index.Index64(np.array([6, 5, 4, 3, 2, 1, 0], dtype=np.int64))
    index2_32 = ak._v2.index.Index32(np.array([0, 2, 4, 6], dtype=np.int32))
    index2_U32 = ak._v2.index.IndexU32(np.array([0, 2, 4, 6], dtype=np.uint32))
    index2_64 = ak._v2.index.Index64(np.array([0, 2, 4, 6], dtype=np.int64))

    array = ak._v2.contents.IndexedArray(
        index2_32, ak._v2.contents.IndexedArray(index1_32, content)
    )
    assert to_list(array) == [6.6, 4.4, 2.2, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(
        array.simplify_optiontype(), ak._v2.contents.indexedarray.IndexedArray
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedArray(
        index2_32, ak._v2.contents.IndexedArray(index1_U32, content)
    )
    assert to_list(array) == [6.6, 4.4, 2.2, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(
        array.simplify_optiontype(), ak._v2.contents.indexedarray.IndexedArray
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedArray(
        index2_32, ak._v2.contents.IndexedArray(index1_64, content)
    )
    assert to_list(array) == [6.6, 4.4, 2.2, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(
        array.simplify_optiontype(), ak._v2.contents.indexedarray.IndexedArray
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedArray(
        index2_U32, ak._v2.contents.IndexedArray(index1_32, content)
    )
    assert to_list(array) == [6.6, 4.4, 2.2, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(
        array.simplify_optiontype(), ak._v2.contents.indexedarray.IndexedArray
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedArray(
        index2_U32, ak._v2.contents.IndexedArray(index1_U32, content)
    )
    assert to_list(array) == [6.6, 4.4, 2.2, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(
        array.simplify_optiontype(), ak._v2.contents.indexedarray.IndexedArray
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedArray(
        index2_U32, ak._v2.contents.IndexedArray(index1_64, content)
    )
    assert to_list(array) == [6.6, 4.4, 2.2, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(
        array.simplify_optiontype(), ak._v2.contents.indexedarray.IndexedArray
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedArray(
        index2_64, ak._v2.contents.IndexedArray(index1_32, content)
    )
    assert to_list(array) == [6.6, 4.4, 2.2, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(
        array.simplify_optiontype(), ak._v2.contents.indexedarray.IndexedArray
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedArray(
        index2_64, ak._v2.contents.IndexedArray(index1_U32, content)
    )
    assert to_list(array) == [6.6, 4.4, 2.2, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(
        array.simplify_optiontype(), ak._v2.contents.indexedarray.IndexedArray
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedArray(
        index2_64, ak._v2.contents.IndexedArray(index1_64, content)
    )
    assert to_list(array) == [6.6, 4.4, 2.2, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(
        array.simplify_optiontype(), ak._v2.contents.indexedarray.IndexedArray
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    index1_32 = ak._v2.index.Index32(np.array([6, 5, -1, 3, -1, 1, 0], dtype=np.int32))
    index1_64 = ak._v2.index.Index64(np.array([6, 5, -1, 3, -1, 1, 0], dtype=np.int64))
    index2_32 = ak._v2.index.Index32(np.array([0, 2, 4, 6], dtype=np.int32))
    index2_U32 = ak._v2.index.IndexU32(np.array([0, 2, 4, 6], dtype=np.uint32))
    index2_64 = ak._v2.index.Index64(np.array([0, 2, 4, 6], dtype=np.int64))

    array = ak._v2.contents.IndexedArray(
        index2_32, ak._v2.contents.IndexedOptionArray(index1_32, content)
    )
    assert to_list(array) == [6.6, None, None, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, None, None, 0.0]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedArray(
        index2_32, ak._v2.contents.IndexedOptionArray(index1_64, content)
    )
    assert to_list(array) == [6.6, None, None, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, None, None, 0.0]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedArray(
        index2_U32, ak._v2.contents.IndexedOptionArray(index1_32, content)
    )
    assert to_list(array) == [6.6, None, None, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, None, None, 0.0]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedArray(
        index2_U32, ak._v2.contents.IndexedOptionArray(index1_64, content)
    )
    assert to_list(array) == [6.6, None, None, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, None, None, 0.0]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedArray(
        index2_64, ak._v2.contents.IndexedOptionArray(index1_32, content)
    )
    assert to_list(array) == [6.6, None, None, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, None, None, 0.0]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedArray(
        index2_64, ak._v2.contents.IndexedOptionArray(index1_64, content)
    )
    assert to_list(array) == [6.6, None, None, 0.0]
    assert to_list(array.simplify_optiontype()) == [6.6, None, None, 0.0]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    index1_32 = ak._v2.index.Index32(np.array([6, 5, 4, 3, 2, 1, 0], dtype=np.int32))
    index1_U32 = ak._v2.index.IndexU32(np.array([6, 5, 4, 3, 2, 1, 0], dtype=np.uint32))
    index1_64 = ak._v2.index.Index64(np.array([6, 5, 4, 3, 2, 1, 0], dtype=np.int64))
    index2_32 = ak._v2.index.Index32(np.array([0, -1, 4, -1], dtype=np.int32))
    index2_64 = ak._v2.index.Index64(np.array([0, -1, 4, -1], dtype=np.int64))

    array = ak._v2.contents.IndexedOptionArray(
        index2_32, ak._v2.contents.IndexedArray(index1_32, content)
    )
    assert to_list(array) == [6.6, None, 2.2, None]
    assert to_list(array.simplify_optiontype()) == [6.6, None, 2.2, None]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedOptionArray(
        index2_32, ak._v2.contents.IndexedArray(index1_U32, content)
    )
    assert to_list(array) == [6.6, None, 2.2, None]
    assert to_list(array.simplify_optiontype()) == [6.6, None, 2.2, None]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedOptionArray(
        index2_32, ak._v2.contents.IndexedArray(index1_64, content)
    )
    assert to_list(array) == [6.6, None, 2.2, None]
    assert to_list(array.simplify_optiontype()) == [6.6, None, 2.2, None]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedOptionArray(
        index2_64, ak._v2.contents.IndexedArray(index1_32, content)
    )
    assert to_list(array) == [6.6, None, 2.2, None]
    assert to_list(array.simplify_optiontype()) == [6.6, None, 2.2, None]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedOptionArray(
        index2_64, ak._v2.contents.IndexedArray(index1_U32, content)
    )
    assert to_list(array) == [6.6, None, 2.2, None]
    assert to_list(array.simplify_optiontype()) == [6.6, None, 2.2, None]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedOptionArray(
        index2_64, ak._v2.contents.IndexedArray(index1_64, content)
    )
    assert to_list(array) == [6.6, None, 2.2, None]
    assert to_list(array.simplify_optiontype()) == [6.6, None, 2.2, None]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    index1_32 = ak._v2.index.Index32(np.array([6, 5, -1, 3, -1, 1, 0], dtype=np.int32))
    index1_64 = ak._v2.index.Index64(np.array([6, 5, -1, 3, -1, 1, 0], dtype=np.int64))
    index2_32 = ak._v2.index.Index32(np.array([0, -1, 4, -1], dtype=np.int32))
    index2_64 = ak._v2.index.Index64(np.array([0, -1, 4, -1], dtype=np.int64))

    array = ak._v2.contents.IndexedOptionArray(
        index2_32, ak._v2.contents.IndexedOptionArray(index1_32, content)
    )
    assert to_list(array) == [6.6, None, None, None]
    assert to_list(array.simplify_optiontype()) == [6.6, None, None, None]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedOptionArray(
        index2_32, ak._v2.contents.IndexedOptionArray(index1_64, content)
    )
    assert to_list(array) == [6.6, None, None, None]
    assert to_list(array.simplify_optiontype()) == [6.6, None, None, None]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedOptionArray(
        index2_64, ak._v2.contents.IndexedOptionArray(index1_32, content)
    )
    assert to_list(array) == [6.6, None, None, None]
    assert to_list(array.simplify_optiontype()) == [6.6, None, None, None]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )

    array = ak._v2.contents.IndexedOptionArray(
        index2_64, ak._v2.contents.IndexedOptionArray(index1_64, content)
    )
    assert to_list(array) == [6.6, None, None, None]
    assert to_list(array.simplify_optiontype()) == [6.6, None, None, None]
    assert isinstance(
        array.simplify_optiontype(),
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert isinstance(
        array.simplify_optiontype().content, ak._v2.contents.numpyarray.NumpyArray
    )
    assert (
        array.typetracer.simplify_optiontype().form == array.simplify_optiontype().form
    )


def test_unionarray_simplify_one():
    one = ak._v2.operations.from_iter([5, 4, 3, 2, 1], highlevel=False)
    two = ak._v2.operations.from_iter([[], [1], [2, 2], [3, 3, 3]], highlevel=False)
    three = ak._v2.operations.from_iter([1.1, 2.2, 3.3], highlevel=False)
    tags = ak._v2.index.Index8(
        np.array([0, 0, 1, 2, 1, 0, 2, 1, 1, 0, 2, 0], dtype=np.int8)
    )
    index = ak._v2.index.Index64(
        np.array([0, 1, 0, 0, 1, 2, 1, 2, 3, 3, 2, 4], dtype=np.int64)
    )
    array = ak._v2.contents.UnionArray(tags, index, [one, two, three])

    assert to_list(array) == [
        5,
        4,
        [],
        1.1,
        [1],
        3,
        2.2,
        [2, 2],
        [3, 3, 3],
        2,
        3.3,
        1,
    ]
    assert to_list(array.simplify_uniontype(True, False)) == [
        5.0,
        4.0,
        [],
        1.1,
        [1],
        3.0,
        2.2,
        [2, 2],
        [3, 3, 3],
        2.0,
        3.3,
        1.0,
    ]
    assert len(array.contents) == 3
    assert len(array.simplify_uniontype(True, False).contents) == 2

    assert (
        array.typetracer.simplify_uniontype(True, False).form
        == array.simplify_uniontype(True, False).form
    )


def test_unionarray_simplify():
    one = ak._v2.operations.from_iter([5, 4, 3, 2, 1], highlevel=False)
    two = ak._v2.operations.from_iter([[], [1], [2, 2], [3, 3, 3]], highlevel=False)
    three = ak._v2.operations.from_iter([1.1, 2.2, 3.3], highlevel=False)

    tags2 = ak._v2.index.Index8(np.array([0, 1, 0, 1, 0, 0, 1], dtype=np.int8))
    index2 = ak._v2.index.Index32(np.array([0, 0, 1, 1, 2, 3, 2], dtype=np.int32))
    inner = ak._v2.contents.UnionArray(tags2, index2, [two, three])
    tags1 = ak._v2.index.Index8(
        np.array([0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0], dtype=np.int8)
    )
    index1 = ak._v2.index.Index64(
        np.array([0, 1, 0, 1, 2, 2, 3, 4, 5, 3, 6, 4], dtype=np.int64)
    )
    outer = ak._v2.contents.UnionArray(tags1, index1, [one, inner])
    assert to_list(outer) == [
        5,
        4,
        [],
        1.1,
        [1],
        3,
        2.2,
        [2, 2],
        [3, 3, 3],
        2,
        3.3,
        1,
    ]

    assert to_list(outer.simplify_uniontype(True, False)) == [
        5.0,
        4.0,
        [],
        1.1,
        [1],
        3.0,
        2.2,
        [2, 2],
        [3, 3, 3],
        2.0,
        3.3,
        1.0,
    ]
    assert isinstance(outer.content(1), ak._v2.contents.unionarray.UnionArray)
    assert isinstance(
        outer.simplify_uniontype(True, False).content(0),
        ak._v2.contents.numpyarray.NumpyArray,
    )
    assert isinstance(
        outer.simplify_uniontype(True, False).content(1),
        ak._v2.contents.listoffsetarray.ListOffsetArray,
    )
    assert len(outer.simplify_uniontype(True, False).contents) == 2
    assert (
        outer.typetracer.simplify_uniontype(True, False).form
        == outer.simplify_uniontype(True, False).form
    )

    tags2 = ak._v2.index.Index8(np.array([0, 1, 0, 1, 0, 0, 1], dtype=np.int8))
    index2 = ak._v2.index.Index64(np.array([0, 0, 1, 1, 2, 3, 2], dtype=np.int64))
    inner = ak._v2.contents.UnionArray(tags2, index2, [two, three])
    tags1 = ak._v2.index.Index8(
        np.array([1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1], dtype=np.int8)
    )
    index1 = ak._v2.index.Index32(
        np.array([0, 1, 0, 1, 2, 2, 3, 4, 5, 3, 6, 4], dtype=np.int32)
    )
    outer = ak._v2.contents.UnionArray(tags1, index1, [inner, one])
    assert to_list(outer) == [
        5,
        4,
        [],
        1.1,
        [1],
        3,
        2.2,
        [2, 2],
        [3, 3, 3],
        2,
        3.3,
        1,
    ]


def test_concatenate():
    one = ak._v2.highlevel.Array([1.1, 2.2, 3.3, 4.4, 5.5], check_valid=True).layout
    two = ak._v2.highlevel.Array([[], [1], [2, 2], [3, 3, 3]], check_valid=True).layout
    three = ak._v2.highlevel.Array(
        [True, False, False, True, True], check_valid=True
    ).layout

    assert to_list(ak._v2.operations.concatenate([one, two, three])) == [
        1.1,
        2.2,
        3.3,
        4.4,
        5.5,
        [],
        [1],
        [2, 2],
        [3, 3, 3],
        1.0,
        0.0,
        0.0,
        1.0,
        1.0,
    ]
    assert isinstance(
        ak._v2.operations.concatenate([one, two, three], highlevel=False),
        ak._v2.contents.unionarray.UnionArray,
    )
    assert (
        len(ak._v2.operations.concatenate([one, two, three], highlevel=False).contents)
        == 2
    )


def test_where():
    condition = ak._v2.highlevel.Array(
        [True, False, True, False, True],
        check_valid=True,
    )
    one = ak._v2.highlevel.Array([1.1, 2.2, 3.3, 4.4, 5.5], check_valid=True)
    two = ak._v2.highlevel.Array([False, False, False, True, True], check_valid=True)
    three = ak._v2.highlevel.Array(
        [[], [1], [2, 2], [3, 3, 3], [4, 4, 4, 4]], check_valid=True
    )

    assert to_list(ak._v2.operations.where(condition, one, two)) == [
        1.1,
        0.0,
        3.3,
        1.0,
        5.5,
    ]
    assert to_list(ak._v2.operations.where(condition, one, three)) == [
        1.1,
        [1],
        3.3,
        [3, 3, 3],
        5.5,
    ]
