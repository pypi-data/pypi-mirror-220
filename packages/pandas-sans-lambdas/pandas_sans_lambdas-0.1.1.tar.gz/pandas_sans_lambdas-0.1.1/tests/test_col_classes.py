"""Test core Col functionality."""

# %% Imports
from contextlib import nullcontext as does_not_raise

import pandas as pd
import pytest

from pandas_sans_lambdas.helpers import BaseCol, CallCol, Col, _is_col_test, _decide_if_call

# %% Data
df = pd.DataFrame(dict(a=[1,2,3], b=[4,5,6]))
df2 = pd.DataFrame({tuple([1,2,3]): [1,2,3]})

# %% Test _is_col_test
@pytest.mark.parametrize(
    "obj,expectation",
    [
        (Col("a"), True),
        (1, False),
        (df["a"], False),
        (None, False),
    ],
)
def test_is_col_test(obj, expectation):
    """Test _is_col_test."""
    assert _is_col_test(obj) == expectation


@pytest.mark.parametrize(
    "args,expectation",
    [
        ((1,), does_not_raise()),
        ((df["a"],), does_not_raise()),
        ((Col("a"),), does_not_raise()),
        (tuple(), pytest.raises(TypeError)),
        ((1,2), pytest.raises(TypeError)),
        ((Col("a"),Col("b")), pytest.raises(TypeError)),
    ],
)
def test_is_col_test_errors(args, expectation):
    """Test _is_col_test errors."""
    with expectation:
        _is_col_test(*args)

# %% Test _decide_if_call
@pytest.mark.parametrize(
    "obj1,obj2,expectation",
    [
        (Col("a"), df, pd.Series),
    ],
)
def test_decide_if_call(obj1, obj2, expectation):
    """Test _decide_if_call."""
    assert isinstance(_decide_if_call(obj1, obj2), expectation)

@pytest.mark.parametrize(
    "arg1,arg2,expectation",
    [
        (Col("a"), df, does_not_raise()),
        (Col((1, 2, 3)), df2, does_not_raise()),
        (Col("ABC"), df, pytest.raises(KeyError)),
        (Col("a"), df["a"], pytest.raises(KeyError)),
        (Col("a"), 1, pytest.raises(TypeError)),
    ],
)
def test_decide_if_call_errors(arg1, arg2, expectation):
    """Test _decide_if_call errors."""
    with expectation:
        _decide_if_call(arg1, arg2)

# %% Test Col.__getitem__
@pytest.mark.parametrize(
    "obj,indexer,df,expectation",
    [
        (Col("b"), slice(1), df, [4]),
        (Col("b"), slice(1,3), df, [5, 6]),
        (Col("b"), slice(0), df, []),
    ],
)
def test_col_getitem(obj, indexer, df, expectation):
    """Test Col.__getitem__."""
    output = obj(df)[indexer]
    assert output.to_list() == expectation
    assert isinstance(output, pd.Series)

# %% Test Col.__call__
@pytest.mark.parametrize(
    "column,df",
    [
        ("a", df),
    ],
)
def test_col_call(column, df):
    """Test Col.__call__."""
    assert (Col(column)(df) == df[column]).all()

@pytest.mark.parametrize(
    "column,df,expectation",
    [
        ("a", df, does_not_raise()),
        ("a", 10, pytest.raises(TypeError)),
        ("c", df, pytest.raises(KeyError)),
    ],
)
def test_col_call_errors(column, df, expectation):
    """Test Col.__call__ errors."""
    with expectation:
        Col(column)(df)

# %% Test CallCol.__call__
@pytest.mark.parametrize(
    "fn,df",
    [
        (lambda DF: pd.Series([1,2,3]), df),
        (lambda DF: DF["a"], df),
        (lambda DF: DF.max(axis=1), df),
    ],
)
def test_callcol_call(fn, df):
    """Test CallCol.__call__."""
    assert (CallCol(fn)(df) == fn(df)).all()

@pytest.mark.parametrize(
    "fn,df,expectation",
    [
        (lambda DF: 123,                        df, does_not_raise()),
        (lambda DF: DF["a"],                    df, does_not_raise()),
        (lambda DF1,  DF2: DF1["a"] + DF2["a"], df, pytest.raises(TypeError)),
        (lambda: 123,                           df, pytest.raises(TypeError)),
        ("hello",                               df, pytest.raises(TypeError)),
        (lambda DF: DF["a"],               "hello", pytest.raises(TypeError)),
    ],
)
def test_callcol_call_errors(fn, df, expectation):
    """Test CallCol.__call__ errors."""
    with expectation:
        CallCol(fn)(df)

# %% Test BaseCol
def test_basecol():
    """Test BaseCol."""
    assert BaseCol()._is_col
