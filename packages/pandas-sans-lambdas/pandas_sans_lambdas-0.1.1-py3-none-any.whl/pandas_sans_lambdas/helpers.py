"""Auto-generated dunder method col implementation"""

# %% Imports
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Callable

import pandas as pd
from pandas._libs import lib

# %% Classes and functions
def _is_col_test(obj):
    return hasattr(obj, "_is_col")

def _decide_if_call(obj, DF):
    return obj(DF) if _is_col_test(obj) else obj

class _AtIndexer:
    def __init__(self, func):
        self.func = func
    def __getitem__(self, *indexes):
        return CallCol(lambda DF: self.func(DF).at.__getitem__(*indexes))

class _IatIndexer:
    def __init__(self, func):
        self.func = func
    def __getitem__(self, *indexes):
        return CallCol(lambda DF: self.func(DF).iat.__getitem__(*indexes))

class _IlocIndexer:
    def __init__(self, func):
        self.func = func
    def __getitem__(self, *indexes):
        return CallCol(lambda DF: self.func(DF).iloc.__getitem__(*indexes))

class _LocIndexer:
    def __init__(self, func):
        self.func = func
    def __getitem__(self, *indexes):
        return CallCol(lambda DF: self.func(DF).loc.__getitem__(*indexes))

@dataclass
class _StrAccessor(object):
    _fn: Callable

    def capitalize(self):
        return CallCol(lambda DF: self._fn(DF).str.capitalize())

    def casefold(self):
        return CallCol(lambda DF: self._fn(DF).str.casefold())

    def cat(self, others = None, sep = None, na_rep = None, join = 'left'):
        return CallCol(lambda DF: self._fn(DF).str.cat(others=_decide_if_call(others, DF), sep=sep, na_rep=na_rep, join=join))

    def center(self, width, fillchar = ' '):
        return CallCol(lambda DF: self._fn(DF).str.center(width=width, fillchar=fillchar))

    def contains(self, pat, case = True, flags = 0, na = None, regex = True):
        return CallCol(lambda DF: self._fn(DF).str.contains(pat=pat, case=case, flags=flags, na=na, regex=regex))

    def count(self, pat, flags = 0):
        return CallCol(lambda DF: self._fn(DF).str.count(pat=pat, flags=flags))

    def decode(self, encoding, errors = 'strict'):
        return CallCol(lambda DF: self._fn(DF).str.decode(encoding=encoding, errors=errors))

    def encode(self, encoding, errors = 'strict'):
        return CallCol(lambda DF: self._fn(DF).str.encode(encoding=encoding, errors=errors))

    def endswith(self, pat, na = None):
        return CallCol(lambda DF: self._fn(DF).str.endswith(pat=pat, na=na))

    def extract(self, pat, flags = 0, expand = True):
        return CallCol(lambda DF: self._fn(DF).str.extract(pat=pat, flags=flags, expand=expand))

    def extractall(self, pat, flags = 0):
        return CallCol(lambda DF: self._fn(DF).str.extractall(pat=pat, flags=flags))

    def find(self, sub, start = 0, end = None):
        return CallCol(lambda DF: self._fn(DF).str.find(sub=sub, start=start, end=end))

    def findall(self, pat, flags = 0):
        return CallCol(lambda DF: self._fn(DF).str.findall(pat=pat, flags=flags))

    def fullmatch(self, pat, case = True, flags = 0, na = None):
        return CallCol(lambda DF: self._fn(DF).str.fullmatch(pat=pat, case=case, flags=flags, na=na))

    def get(self, i):
        return CallCol(lambda DF: self._fn(DF).str.get(i=i))

    def get_dummies(self, sep = '|'):
        return CallCol(lambda DF: self._fn(DF).str.get_dummies(sep=sep))

    def index(self, sub, start = 0, end = None):
        return CallCol(lambda DF: self._fn(DF).str.index(sub=sub, start=start, end=end))

    def isalnum(self):
        return CallCol(lambda DF: self._fn(DF).str.isalnum())

    def isalpha(self):
        return CallCol(lambda DF: self._fn(DF).str.isalpha())

    def isdecimal(self):
        return CallCol(lambda DF: self._fn(DF).str.isdecimal())

    def isdigit(self):
        return CallCol(lambda DF: self._fn(DF).str.isdigit())

    def islower(self):
        return CallCol(lambda DF: self._fn(DF).str.islower())

    def isnumeric(self):
        return CallCol(lambda DF: self._fn(DF).str.isnumeric())

    def isspace(self):
        return CallCol(lambda DF: self._fn(DF).str.isspace())

    def istitle(self):
        return CallCol(lambda DF: self._fn(DF).str.istitle())

    def isupper(self):
        return CallCol(lambda DF: self._fn(DF).str.isupper())

    def join(self, sep):
        return CallCol(lambda DF: self._fn(DF).str.join(sep=sep))

    def len(self):
        return CallCol(lambda DF: self._fn(DF).str.len())

    def ljust(self, width, fillchar = ' '):
        return CallCol(lambda DF: self._fn(DF).str.ljust(width=width, fillchar=fillchar))

    def lower(self):
        return CallCol(lambda DF: self._fn(DF).str.lower())

    def lstrip(self, to_strip = None):
        return CallCol(lambda DF: self._fn(DF).str.lstrip(to_strip=to_strip))

    def match(self, pat, case = True, flags = 0, na = None):
        return CallCol(lambda DF: self._fn(DF).str.match(pat=pat, case=case, flags=flags, na=na))

    def normalize(self, form):
        return CallCol(lambda DF: self._fn(DF).str.normalize(form=form))

    def pad(self, width, side = 'left', fillchar = ' '):
        return CallCol(lambda DF: self._fn(DF).str.pad(width=width, side=side, fillchar=fillchar))

    def partition(self, sep = ' ', expand = True):
        return CallCol(lambda DF: self._fn(DF).str.partition(sep=sep, expand=expand))

    def removeprefix(self, prefix):
        return CallCol(lambda DF: self._fn(DF).str.removeprefix(prefix=prefix))

    def removesuffix(self, suffix):
        return CallCol(lambda DF: self._fn(DF).str.removesuffix(suffix=suffix))

    def repeat(self, repeats):
        return CallCol(lambda DF: self._fn(DF).str.repeat(repeats=repeats))

    def replace(self, pat, repl, n = -1, case = None, flags = 0, regex = False):
        return CallCol(lambda DF: self._fn(DF).str.replace(pat=pat, repl=repl, n=n, case=case, flags=flags, regex=regex))

    def rfind(self, sub, start = 0, end = None):
        return CallCol(lambda DF: self._fn(DF).str.rfind(sub=sub, start=start, end=end))

    def rindex(self, sub, start = 0, end = None):
        return CallCol(lambda DF: self._fn(DF).str.rindex(sub=sub, start=start, end=end))

    def rjust(self, width, fillchar = ' '):
        return CallCol(lambda DF: self._fn(DF).str.rjust(width=width, fillchar=fillchar))

    def rpartition(self, sep = ' ', expand = True):
        return CallCol(lambda DF: self._fn(DF).str.rpartition(sep=sep, expand=expand))

    def rsplit(self, pat = None, n = -1, expand = False):
        return CallCol(lambda DF: self._fn(DF).str.rsplit(pat=pat, n=n, expand=expand))

    def rstrip(self, to_strip = None):
        return CallCol(lambda DF: self._fn(DF).str.rstrip(to_strip=to_strip))

    def slice(self, start = None, stop = None, step = None):
        return CallCol(lambda DF: self._fn(DF).str.slice(start=start, stop=stop, step=step))

    def slice_replace(self, start = None, stop = None, repl = None):
        return CallCol(lambda DF: self._fn(DF).str.slice_replace(start=start, stop=stop, repl=repl))

    def split(self, pat = None, n = -1, expand = False, regex = None):
        return CallCol(lambda DF: self._fn(DF).str.split(pat=pat, n=n, expand=expand, regex=regex))

    def startswith(self, pat, na = None):
        return CallCol(lambda DF: self._fn(DF).str.startswith(pat=pat, na=na))

    def strip(self, to_strip = None):
        return CallCol(lambda DF: self._fn(DF).str.strip(to_strip=to_strip))

    def swapcase(self):
        return CallCol(lambda DF: self._fn(DF).str.swapcase())

    def title(self):
        return CallCol(lambda DF: self._fn(DF).str.title())

    def translate(self, table):
        return CallCol(lambda DF: self._fn(DF).str.translate(table=table))

    def upper(self):
        return CallCol(lambda DF: self._fn(DF).str.upper())

    def wrap(self, width, **kwargs):
        return CallCol(lambda DF: self._fn(DF).str.wrap(width=width, kwargs=kwargs))

    def zfill(self, width):
        return CallCol(lambda DF: self._fn(DF).str.zfill(width=width))

@dataclass
class _CatAccessor(object):
    _fn: Callable

    @property
    def categories(self, DF):
        return self._fn(DF).cat.categories

    @property
    def codes(self, DF):
        return self._fn(DF).cat.codes

    @property
    def ordered(self, DF):
        return self._fn(DF).cat.ordered

    def add_categories(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).cat.add_categories(args=args, kwargs=kwargs))

    def as_ordered(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).cat.as_ordered(args=args, kwargs=kwargs))

    def as_unordered(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).cat.as_unordered(args=args, kwargs=kwargs))

    def remove_categories(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).cat.remove_categories(args=args, kwargs=kwargs))

    def remove_unused_categories(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).cat.remove_unused_categories(args=args, kwargs=kwargs))

    def rename_categories(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).cat.rename_categories(args=args, kwargs=kwargs))

    def reorder_categories(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).cat.reorder_categories(args=args, kwargs=kwargs))

    def set_categories(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).cat.set_categories(args=args, kwargs=kwargs))

@dataclass
class _DtAccessor(object):
    _fn: Callable

    @property
    def date(self, DF):
        return self._fn(DF).dt.date

    @property
    def day(self, DF):
        return self._fn(DF).dt.day

    @property
    def day_of_week(self, DF):
        return self._fn(DF).dt.day_of_week

    @property
    def day_of_year(self, DF):
        return self._fn(DF).dt.day_of_year

    @property
    def dayofweek(self, DF):
        return self._fn(DF).dt.dayofweek

    @property
    def dayofyear(self, DF):
        return self._fn(DF).dt.dayofyear

    @property
    def days_in_month(self, DF):
        return self._fn(DF).dt.days_in_month

    @property
    def daysinmonth(self, DF):
        return self._fn(DF).dt.daysinmonth

    @property
    def freq(self, DF):
        return self._fn(DF).dt.freq

    @property
    def hour(self, DF):
        return self._fn(DF).dt.hour

    @property
    def is_leap_year(self, DF):
        return self._fn(DF).dt.is_leap_year

    @property
    def is_month_end(self, DF):
        return self._fn(DF).dt.is_month_end

    @property
    def is_month_start(self, DF):
        return self._fn(DF).dt.is_month_start

    @property
    def is_quarter_end(self, DF):
        return self._fn(DF).dt.is_quarter_end

    @property
    def is_quarter_start(self, DF):
        return self._fn(DF).dt.is_quarter_start

    @property
    def is_year_end(self, DF):
        return self._fn(DF).dt.is_year_end

    @property
    def is_year_start(self, DF):
        return self._fn(DF).dt.is_year_start

    @property
    def microsecond(self, DF):
        return self._fn(DF).dt.microsecond

    @property
    def minute(self, DF):
        return self._fn(DF).dt.minute

    @property
    def month(self, DF):
        return self._fn(DF).dt.month

    @property
    def nanosecond(self, DF):
        return self._fn(DF).dt.nanosecond

    @property
    def quarter(self, DF):
        return self._fn(DF).dt.quarter

    @property
    def second(self, DF):
        return self._fn(DF).dt.second

    @property
    def time(self, DF):
        return self._fn(DF).dt.time

    @property
    def timetz(self, DF):
        return self._fn(DF).dt.timetz

    @property
    def tz(self, DF):
        return self._fn(DF).dt.tz

    @property
    def unit(self, DF):
        return self._fn(DF).dt.unit

    @property
    def weekday(self, DF):
        return self._fn(DF).dt.weekday

    @property
    def year(self, DF):
        return self._fn(DF).dt.year

    def as_unit(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).dt.as_unit(args=args, kwargs=kwargs))

    def ceil(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).dt.ceil(args=args, kwargs=kwargs))

    def day_name(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).dt.day_name(args=args, kwargs=kwargs))

    def floor(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).dt.floor(args=args, kwargs=kwargs))

    def isocalendar(self):
        return CallCol(lambda DF: self._fn(DF).dt.isocalendar())

    def month_name(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).dt.month_name(args=args, kwargs=kwargs))

    def normalize(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).dt.normalize(args=args, kwargs=kwargs))

    def round(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).dt.round(args=args, kwargs=kwargs))

    def strftime(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).dt.strftime(args=args, kwargs=kwargs))

    def to_period(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).dt.to_period(args=args, kwargs=kwargs))

    def to_pydatetime(self):
        return CallCol(lambda DF: self._fn(DF).dt.to_pydatetime())

    def tz_convert(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).dt.tz_convert(args=args, kwargs=kwargs))

    def tz_localize(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).dt.tz_localize(args=args, kwargs=kwargs))

@dataclass
class _SparseAccessor(object):
    _fn: Callable

    @property
    def density(self, DF):
        return self._fn(DF).sparse.density

    @property
    def fill_value(self, DF):
        return self._fn(DF).sparse.fill_value

    @property
    def npoints(self, DF):
        return self._fn(DF).sparse.npoints

    @property
    def sp_values(self, DF):
        return self._fn(DF).sparse.sp_values

    def to_coo(self, row_levels = (0,), column_levels = (1,), sort_labels = False):
        return CallCol(lambda DF: self._fn(DF).sparse.to_coo(row_levels=row_levels, column_levels=column_levels, sort_labels=sort_labels))

    def to_dense(self):
        return CallCol(lambda DF: self._fn(DF).sparse.to_dense())

@dataclass
class _PlotAccessor(object):
    _fn: Callable

    def area(self, x = None, y = None, stacked = True, **kwargs):
        return CallCol(lambda DF: self._fn(DF).plot.area(x=x, y=y, stacked=stacked, kwargs=kwargs))

    def bar(self, x = None, y = None, **kwargs):
        return CallCol(lambda DF: self._fn(DF).plot.bar(x=x, y=y, kwargs=kwargs))

    def barh(self, x = None, y = None, **kwargs):
        return CallCol(lambda DF: self._fn(DF).plot.barh(x=x, y=y, kwargs=kwargs))

    def box(self, by = None, **kwargs):
        return CallCol(lambda DF: self._fn(DF).plot.box(by=by, kwargs=kwargs))

    def density(self, bw_method = None, ind = None, **kwargs):
        return CallCol(lambda DF: self._fn(DF).plot.density(bw_method=bw_method, ind=ind, kwargs=kwargs))

    def hist(self, by = None, bins = 10, **kwargs):
        return CallCol(lambda DF: self._fn(DF).plot.hist(by=by, bins=bins, kwargs=kwargs))

    def kde(self, bw_method = None, ind = None, **kwargs):
        return CallCol(lambda DF: self._fn(DF).plot.kde(bw_method=bw_method, ind=ind, kwargs=kwargs))

    def line(self, x = None, y = None, **kwargs):
        return CallCol(lambda DF: self._fn(DF).plot.line(x=x, y=y, kwargs=kwargs))

    def pie(self, **kwargs):
        return CallCol(lambda DF: self._fn(DF).plot.pie(kwargs=kwargs))

    def __call__(self, *args, **kwargs):
        return CallCol(lambda DF: self._fn(DF).plot.__call__(args=args, kwargs=kwargs))

class BaseCol(object):
    _is_col = True

    @abstractmethod
    def __call__(self, df):
        pass

    def __getitem__(self, *indexes):
        return CallCol(lambda DF: self.__call__(DF).at.__getitem__(*indexes))

    @property
    def __annotations__(self, DF):
        return self.__call__(DF).__annotations__

    @property
    def __array_priority__(self, DF):
        return self.__call__(DF).__array_priority__

    @property
    def __dict__(self, DF):
        return self.__call__(DF).__dict__

    @property
    def __doc__(self, DF):
        return self.__call__(DF).__doc__

    @property
    def __hash__(self, DF):
        return self.__call__(DF).__hash__

    @property
    def __module__(self, DF):
        return self.__call__(DF).__module__

    @property
    def cat(self):
        return _CatAccessor(self.__call__)

    @property
    def dt(self):
        return _DtAccessor(self.__call__)

    @property
    def str(self):
        return _StrAccessor(self.__call__)

    @property
    def sparse(self):
        return _SparseAccessor(self.__call__)

    @property
    def plot(self):
        return _PlotAccessor(self.__call__)

    @property
    def T(self, DF):
        return self.__call__(DF).T

    @property
    def array(self, DF):
        return self.__call__(DF).array

    @property
    def attrs(self, DF):
        return self.__call__(DF).attrs

    @property
    def axes(self, DF):
        return self.__call__(DF).axes

    @property
    def dtype(self, DF):
        return self.__call__(DF).dtype

    @property
    def dtypes(self, DF):
        return self.__call__(DF).dtypes

    @property
    def empty(self, DF):
        return self.__call__(DF).empty

    @property
    def flags(self, DF):
        return self.__call__(DF).flags

    @property
    def hasnans(self, DF):
        return self.__call__(DF).hasnans

    @property
    def index(self, DF):
        return self.__call__(DF).index

    @property
    def is_monotonic_decreasing(self, DF):
        return self.__call__(DF).is_monotonic_decreasing

    @property
    def is_monotonic_increasing(self, DF):
        return self.__call__(DF).is_monotonic_increasing

    @property
    def is_unique(self, DF):
        return self.__call__(DF).is_unique

    @property
    def name(self, DF):
        return self.__call__(DF).name

    @property
    def nbytes(self, DF):
        return self.__call__(DF).nbytes

    @property
    def ndim(self, DF):
        return self.__call__(DF).ndim

    @property
    def shape(self, DF):
        return self.__call__(DF).shape

    @property
    def size(self, DF):
        return self.__call__(DF).size

    @property
    def values(self, DF):
        return self.__call__(DF).values

    @property
    def at(self):
        return _AtIndexer(self.__call__)

    @property
    def iat(self):
        return _IatIndexer(self.__call__)

    @property
    def iloc(self):
        return _IlocIndexer(self.__call__)

    @property
    def loc(self):
        return _LocIndexer(self.__call__)

    def __abs__(self):
        return CallCol(lambda DF: self.__call__(DF).__abs__())

    def __add__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__add__(other=_decide_if_call(other, DF)))

    def __and__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__and__(other=_decide_if_call(other, DF)))

    def __array__(self, dtype = None):
        return CallCol(lambda DF: self.__call__(DF).__array__(dtype=dtype))

    def __bool__(self):
        return CallCol(lambda DF: self.__call__(DF).__bool__())

    def __class__(self, data = None, index = None, dtype = None, name = None, copy = None, fastpath = False):
        return CallCol(lambda DF: self.__call__(DF).__class__(data=_decide_if_call(data, DF), index=index, dtype=dtype, name=name, copy=copy, fastpath=fastpath))

    def __contains__(self, key):
        return CallCol(lambda DF: self.__call__(DF).__contains__(key=key))

    def __divmod__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__divmod__(other=_decide_if_call(other, DF)))

    def __eq__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__eq__(other=_decide_if_call(other, DF)))

    def __float__(self):
        return CallCol(lambda DF: self.__call__(DF).__float__())

    def __floordiv__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__floordiv__(other=_decide_if_call(other, DF)))

    def __ge__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__ge__(other=_decide_if_call(other, DF)))

    def __gt__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__gt__(other=_decide_if_call(other, DF)))

    def __iadd__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__iadd__(other=_decide_if_call(other, DF)))

    def __iand__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__iand__(other=_decide_if_call(other, DF)))

    def __ifloordiv__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__ifloordiv__(other=_decide_if_call(other, DF)))

    def __imod__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__imod__(other=_decide_if_call(other, DF)))

    def __imul__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__imul__(other=_decide_if_call(other, DF)))

    def __int__(self):
        return CallCol(lambda DF: self.__call__(DF).__int__())

    def __invert__(self):
        return CallCol(lambda DF: self.__call__(DF).__invert__())

    def __ior__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__ior__(other=_decide_if_call(other, DF)))

    def __ipow__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__ipow__(other=_decide_if_call(other, DF)))

    def __isub__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__isub__(other=_decide_if_call(other, DF)))

    def __itruediv__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__itruediv__(other=_decide_if_call(other, DF)))

    def __ixor__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__ixor__(other=_decide_if_call(other, DF)))

    def __le__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__le__(other=_decide_if_call(other, DF)))

    def __len__(self):
        return CallCol(lambda DF: self.__call__(DF).__len__())

    def __lt__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__lt__(other=_decide_if_call(other, DF)))

    def __matmul__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__matmul__(other=_decide_if_call(other, DF)))

    def __mod__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__mod__(other=_decide_if_call(other, DF)))

    def __mul__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__mul__(other=_decide_if_call(other, DF)))

    def __ne__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__ne__(other=_decide_if_call(other, DF)))

    def __neg__(self):
        return CallCol(lambda DF: self.__call__(DF).__neg__())

    def __nonzero__(self):
        return CallCol(lambda DF: self.__call__(DF).__nonzero__())

    def __or__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__or__(other=_decide_if_call(other, DF)))

    def __pos__(self):
        return CallCol(lambda DF: self.__call__(DF).__pos__())

    def __pow__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__pow__(other=_decide_if_call(other, DF)))

    def __radd__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__radd__(other=_decide_if_call(other, DF)))

    def __rand__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__rand__(other=_decide_if_call(other, DF)))

    def __rdivmod__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__rdivmod__(other=_decide_if_call(other, DF)))

    def __rfloordiv__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__rfloordiv__(other=_decide_if_call(other, DF)))

    def __rmatmul__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__rmatmul__(other=_decide_if_call(other, DF)))

    def __rmod__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__rmod__(other=_decide_if_call(other, DF)))

    def __rmul__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__rmul__(other=_decide_if_call(other, DF)))

    def __ror__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__ror__(other=_decide_if_call(other, DF)))

    def __round__(self, decimals = 0):
        return CallCol(lambda DF: self.__call__(DF).__round__(decimals=decimals))

    def __rpow__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__rpow__(other=_decide_if_call(other, DF)))

    def __rsub__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__rsub__(other=_decide_if_call(other, DF)))

    def __rtruediv__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__rtruediv__(other=_decide_if_call(other, DF)))

    def __rxor__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__rxor__(other=_decide_if_call(other, DF)))

    def __sub__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__sub__(other=_decide_if_call(other, DF)))

    def __truediv__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__truediv__(other=_decide_if_call(other, DF)))

    def __xor__(self, other):
        return CallCol(lambda DF: self.__call__(DF).__xor__(other=_decide_if_call(other, DF)))

    def abs(self):
        return CallCol(lambda DF: self.__call__(DF).abs())

    def add(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).add(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def add_prefix(self, prefix, axis = None):
        return CallCol(lambda DF: self.__call__(DF).add_prefix(prefix=prefix, axis=axis))

    def add_suffix(self, suffix, axis = None):
        return CallCol(lambda DF: self.__call__(DF).add_suffix(suffix=suffix, axis=axis))

    def agg(self, func = None, axis = 0, *args, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).agg(func=func, axis=axis, args=args, kwargs=kwargs))

    def aggregate(self, func = None, axis = 0, *args, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).aggregate(func=func, axis=axis, args=args, kwargs=kwargs))

    def align(self, other, join = 'outer', axis = None, level = None, copy = None, fill_value = None, method = None, limit = None, fill_axis = 0, broadcast_axis = None):
        return CallCol(lambda DF: self.__call__(DF).align(other=_decide_if_call(other, DF), join=join, axis=axis, level=level, copy=copy, fill_value=fill_value, method=method, limit=limit, fill_axis=fill_axis, broadcast_axis=broadcast_axis))

    def all(self, axis = 0, bool_only = None, skipna = True, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).all(axis=axis, bool_only=bool_only, skipna=skipna, kwargs=kwargs))

    def any(self, axis = 0, bool_only = None, skipna = True, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).any(axis=axis, bool_only=bool_only, skipna=skipna, kwargs=kwargs))

    def apply(self, func, convert_dtype = True, args = (), **kwargs):
        return CallCol(lambda DF: self.__call__(DF).apply(func=func, convert_dtype=convert_dtype, args=args, kwargs=kwargs))

    def argmax(self, axis = None, skipna = True, *args, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).argmax(axis=axis, skipna=skipna, args=args, kwargs=kwargs))

    def argmin(self, axis = None, skipna = True, *args, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).argmin(axis=axis, skipna=skipna, args=args, kwargs=kwargs))

    def argsort(self, axis = 0, kind = 'quicksort', order = None):
        return CallCol(lambda DF: self.__call__(DF).argsort(axis=axis, kind=kind, order=order))

    def asfreq(self, freq, method = None, how = None, normalize = False, fill_value = None):
        return CallCol(lambda DF: self.__call__(DF).asfreq(freq=freq, method=method, how=how, normalize=normalize, fill_value=fill_value))

    def asof(self, where, subset = None):
        return CallCol(lambda DF: self.__call__(DF).asof(where=where, subset=subset))

    def astype(self, dtype, copy = None, errors = 'raise'):
        return CallCol(lambda DF: self.__call__(DF).astype(dtype=dtype, copy=copy, errors=errors))

    def at_time(self, time, asof = False, axis = None):
        return CallCol(lambda DF: self.__call__(DF).at_time(time=time, asof=asof, axis=axis))

    def autocorr(self, lag = 1):
        return CallCol(lambda DF: self.__call__(DF).autocorr(lag=lag))

    def backfill(self, axis = None, inplace = False, limit = None, downcast = None):
        return CallCol(lambda DF: self.__call__(DF).backfill(axis=axis, inplace=inplace, limit=limit, downcast=downcast))

    def between(self, left, right, inclusive = 'both'):
        return CallCol(lambda DF: self.__call__(DF).between(left=left, right=right, inclusive=inclusive))

    def between_time(self, start_time, end_time, inclusive = 'both', axis = None):
        return CallCol(lambda DF: self.__call__(DF).between_time(start_time=start_time, end_time=end_time, inclusive=inclusive, axis=axis))

    def bfill(self, axis = None, inplace = False, limit = None, downcast = None):
        return CallCol(lambda DF: self.__call__(DF).bfill(axis=axis, inplace=inplace, limit=limit, downcast=downcast))

    def bool(self):
        return CallCol(lambda DF: self.__call__(DF).bool())

    def clip(self, lower = None, upper = None, axis = None, inplace = False, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).clip(lower=lower, upper=upper, axis=axis, inplace=inplace, kwargs=kwargs))

    def combine(self, other, func, fill_value = None):
        return CallCol(lambda DF: self.__call__(DF).combine(other=_decide_if_call(other, DF), func=func, fill_value=fill_value))

    def combine_first(self, other):
        return CallCol(lambda DF: self.__call__(DF).combine_first(other=_decide_if_call(other, DF)))

    def compare(self, other, align_axis = 1, keep_shape = False, keep_equal = False, result_names = ('self', 'other')):
        return CallCol(lambda DF: self.__call__(DF).compare(other=_decide_if_call(other, DF), align_axis=align_axis, keep_shape=keep_shape, keep_equal=keep_equal, result_names=result_names))

    def convert_dtypes(self, infer_objects = True, convert_string = True, convert_integer = True, convert_boolean = True, convert_floating = True, dtype_backend = 'numpy_nullable'):
        return CallCol(lambda DF: self.__call__(DF).convert_dtypes(infer_objects=infer_objects, convert_string=convert_string, convert_integer=convert_integer, convert_boolean=convert_boolean, convert_floating=convert_floating, dtype_backend=dtype_backend))

    def copy(self, deep = True):
        return CallCol(lambda DF: self.__call__(DF).copy(deep=deep))

    def corr(self, other, method = 'pearson', min_periods = None):
        return CallCol(lambda DF: self.__call__(DF).corr(other=_decide_if_call(other, DF), method=method, min_periods=min_periods))

    def count(self):
        return CallCol(lambda DF: self.__call__(DF).count())

    def cov(self, other, min_periods = None, ddof = 1):
        return CallCol(lambda DF: self.__call__(DF).cov(other=_decide_if_call(other, DF), min_periods=min_periods, ddof=ddof))

    def cummax(self, axis = None, skipna = True, *args, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).cummax(axis=axis, skipna=skipna, args=args, kwargs=kwargs))

    def cummin(self, axis = None, skipna = True, *args, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).cummin(axis=axis, skipna=skipna, args=args, kwargs=kwargs))

    def cumprod(self, axis = None, skipna = True, *args, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).cumprod(axis=axis, skipna=skipna, args=args, kwargs=kwargs))

    def cumsum(self, axis = None, skipna = True, *args, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).cumsum(axis=axis, skipna=skipna, args=args, kwargs=kwargs))

    def describe(self, percentiles = None, include = None, exclude = None):
        return CallCol(lambda DF: self.__call__(DF).describe(percentiles=percentiles, include=include, exclude=exclude))

    def diff(self, periods = 1):
        return CallCol(lambda DF: self.__call__(DF).diff(periods=periods))

    def div(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).div(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def divide(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).divide(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def divmod(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).divmod(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def dot(self, other):
        return CallCol(lambda DF: self.__call__(DF).dot(other=_decide_if_call(other, DF)))

    def drop(self, labels = None, axis = 0, index = None, columns = None, level = None, inplace = False, errors = 'raise'):
        return CallCol(lambda DF: self.__call__(DF).drop(labels=labels, axis=axis, index=index, columns=columns, level=level, inplace=inplace, errors=errors))

    def drop_duplicates(self, keep = 'first', inplace = False, ignore_index = False):
        return CallCol(lambda DF: self.__call__(DF).drop_duplicates(keep=keep, inplace=inplace, ignore_index=ignore_index))

    def droplevel(self, level, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).droplevel(level=level, axis=axis))

    def dropna(self, axis = 0, inplace = False, how = None, ignore_index = False):
        return CallCol(lambda DF: self.__call__(DF).dropna(axis=axis, inplace=inplace, how=how, ignore_index=ignore_index))

    def duplicated(self, keep = 'first'):
        return CallCol(lambda DF: self.__call__(DF).duplicated(keep=keep))

    def eq(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).eq(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def equals(self, other):
        return CallCol(lambda DF: self.__call__(DF).equals(other=_decide_if_call(other, DF)))

    def ewm(self, com = None, span = None, halflife = None, alpha = None, min_periods = 0, adjust = True, ignore_na = False, axis = 0, times = None, method = 'single'):
        return CallCol(lambda DF: self.__call__(DF).ewm(com=com, span=span, halflife=halflife, alpha=alpha, min_periods=min_periods, adjust=adjust, ignore_na=ignore_na, axis=axis, times=_decide_if_call(times, DF), method=method))

    def expanding(self, min_periods = 1, axis = 0, method = 'single'):
        return CallCol(lambda DF: self.__call__(DF).expanding(min_periods=min_periods, axis=axis, method=method))

    def explode(self, ignore_index = False):
        return CallCol(lambda DF: self.__call__(DF).explode(ignore_index=ignore_index))

    def factorize(self, sort = False, use_na_sentinel = True):
        return CallCol(lambda DF: self.__call__(DF).factorize(sort=sort, use_na_sentinel=use_na_sentinel))

    def ffill(self, axis = None, inplace = False, limit = None, downcast = None):
        return CallCol(lambda DF: self.__call__(DF).ffill(axis=axis, inplace=inplace, limit=limit, downcast=downcast))

    def fillna(self, value = None, method = None, axis = None, inplace = False, limit = None, downcast = None):
        return CallCol(lambda DF: self.__call__(DF).fillna(value=_decide_if_call(value, DF), method=method, axis=axis, inplace=inplace, limit=limit, downcast=downcast))

    def filter(self, items = None, like = None, regex = None, axis = None):
        return CallCol(lambda DF: self.__call__(DF).filter(items=items, like=like, regex=regex, axis=axis))

    def first(self, offset):
        return CallCol(lambda DF: self.__call__(DF).first(offset=offset))

    def first_valid_index(self):
        return CallCol(lambda DF: self.__call__(DF).first_valid_index())

    def floordiv(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).floordiv(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def ge(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).ge(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def get(self, key, default = None):
        return CallCol(lambda DF: self.__call__(DF).get(key=key, default=default))

    def groupby(self, by = None, axis = 0, level = None, as_index = True, sort = True, group_keys = True, observed = False, dropna = True):
        return CallCol(lambda DF: self.__call__(DF).groupby(by=by, axis=axis, level=level, as_index=as_index, sort=sort, group_keys=group_keys, observed=observed, dropna=dropna))

    def gt(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).gt(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def head(self, n = 5):
        return CallCol(lambda DF: self.__call__(DF).head(n=n))

    def hist(self, by = None, ax = None, grid = True, xlabelsize = None, xrot = None, ylabelsize = None, yrot = None, figsize = None, bins = 10, backend = None, legend = False, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).hist(by=by, ax=ax, grid=grid, xlabelsize=xlabelsize, xrot=xrot, ylabelsize=ylabelsize, yrot=yrot, figsize=figsize, bins=bins, backend=backend, legend=legend, kwargs=kwargs))

    def idxmax(self, axis = 0, skipna = True, *args, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).idxmax(axis=axis, skipna=skipna, args=args, kwargs=kwargs))

    def idxmin(self, axis = 0, skipna = True, *args, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).idxmin(axis=axis, skipna=skipna, args=args, kwargs=kwargs))

    def infer_objects(self, copy = None):
        return CallCol(lambda DF: self.__call__(DF).infer_objects(copy=copy))

    def info(self, verbose = None, buf = None, max_cols = None, memory_usage = None, show_counts = True):
        return CallCol(lambda DF: self.__call__(DF).info(verbose=verbose, buf=buf, max_cols=max_cols, memory_usage=memory_usage, show_counts=show_counts))

    def interpolate(self, method = 'linear', axis = 0, limit = None, inplace = False, limit_direction = None, limit_area = None, downcast = None, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).interpolate(method=method, axis=axis, limit=limit, inplace=inplace, limit_direction=limit_direction, limit_area=limit_area, downcast=downcast, kwargs=kwargs))

    def isin(self, values):
        return CallCol(lambda DF: self.__call__(DF).isin(values=values))

    def isna(self):
        return CallCol(lambda DF: self.__call__(DF).isna())

    def isnull(self):
        return CallCol(lambda DF: self.__call__(DF).isnull())

    def item(self):
        return CallCol(lambda DF: self.__call__(DF).item())

    def items(self):
        return CallCol(lambda DF: self.__call__(DF).items())

    def keys(self):
        return CallCol(lambda DF: self.__call__(DF).keys())

    def kurt(self, axis = 0, skipna = True, numeric_only = False, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).kurt(axis=axis, skipna=skipna, numeric_only=numeric_only, kwargs=kwargs))

    def kurtosis(self, axis = 0, skipna = True, numeric_only = False, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).kurtosis(axis=axis, skipna=skipna, numeric_only=numeric_only, kwargs=kwargs))

    def last(self, offset):
        return CallCol(lambda DF: self.__call__(DF).last(offset=offset))

    def last_valid_index(self):
        return CallCol(lambda DF: self.__call__(DF).last_valid_index())

    def le(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).le(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def lt(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).lt(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def map(self, arg, na_action = None):
        return CallCol(lambda DF: self.__call__(DF).map(arg=_decide_if_call(arg, DF), na_action=na_action))

    def mask(self, cond, other = lib.no_default, inplace = False, axis = None, level = None):
        return CallCol(lambda DF: self.__call__(DF).mask(cond=_decide_if_call(cond, DF), other=_decide_if_call(other, DF), inplace=inplace, axis=axis, level=level))

    def max(self, axis = 0, skipna = True, numeric_only = False, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).max(axis=axis, skipna=skipna, numeric_only=numeric_only, kwargs=kwargs))

    def mean(self, axis = 0, skipna = True, numeric_only = False, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).mean(axis=axis, skipna=skipna, numeric_only=numeric_only, kwargs=kwargs))

    def median(self, axis = 0, skipna = True, numeric_only = False, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).median(axis=axis, skipna=skipna, numeric_only=numeric_only, kwargs=kwargs))

    def memory_usage(self, index = True, deep = False):
        return CallCol(lambda DF: self.__call__(DF).memory_usage(index=index, deep=deep))

    def min(self, axis = 0, skipna = True, numeric_only = False, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).min(axis=axis, skipna=skipna, numeric_only=numeric_only, kwargs=kwargs))

    def mod(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).mod(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def mode(self, dropna = True):
        return CallCol(lambda DF: self.__call__(DF).mode(dropna=dropna))

    def mul(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).mul(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def multiply(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).multiply(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def ne(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).ne(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def nlargest(self, n = 5, keep = 'first'):
        return CallCol(lambda DF: self.__call__(DF).nlargest(n=n, keep=keep))

    def notna(self):
        return CallCol(lambda DF: self.__call__(DF).notna())

    def notnull(self):
        return CallCol(lambda DF: self.__call__(DF).notnull())

    def nsmallest(self, n = 5, keep = 'first'):
        return CallCol(lambda DF: self.__call__(DF).nsmallest(n=n, keep=keep))

    def nunique(self, dropna = True):
        return CallCol(lambda DF: self.__call__(DF).nunique(dropna=dropna))

    def pad(self, axis = None, inplace = False, limit = None, downcast = None):
        return CallCol(lambda DF: self.__call__(DF).pad(axis=axis, inplace=inplace, limit=limit, downcast=downcast))

    def pct_change(self, periods = 1, fill_method = 'pad', limit = None, freq = None, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).pct_change(periods=periods, fill_method=fill_method, limit=limit, freq=freq, kwargs=kwargs))

    def pipe(self, func, *args, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).pipe(func=func, args=args, kwargs=kwargs))

    def pop(self, item):
        return CallCol(lambda DF: self.__call__(DF).pop(item=item))

    def pow(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).pow(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def prod(self, axis = None, skipna = True, numeric_only = False, min_count = 0, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).prod(axis=axis, skipna=skipna, numeric_only=numeric_only, min_count=min_count, kwargs=kwargs))

    def product(self, axis = None, skipna = True, numeric_only = False, min_count = 0, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).product(axis=axis, skipna=skipna, numeric_only=numeric_only, min_count=min_count, kwargs=kwargs))

    def quantile(self, q = 0.5, interpolation = 'linear'):
        return CallCol(lambda DF: self.__call__(DF).quantile(q=q, interpolation=interpolation))

    def radd(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).radd(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def rank(self, axis = 0, method = 'average', numeric_only = False, na_option = 'keep', ascending = True, pct = False):
        return CallCol(lambda DF: self.__call__(DF).rank(axis=axis, method=method, numeric_only=numeric_only, na_option=na_option, ascending=ascending, pct=pct))

    def ravel(self, order = 'C'):
        return CallCol(lambda DF: self.__call__(DF).ravel(order=order))

    def rdiv(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).rdiv(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def rdivmod(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).rdivmod(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def reindex(self, index = None, axis = None, method = None, copy = None, level = None, fill_value = None, limit = None, tolerance = None):
        return CallCol(lambda DF: self.__call__(DF).reindex(index=index, axis=axis, method=method, copy=copy, level=level, fill_value=fill_value, limit=limit, tolerance=tolerance))

    def reindex_like(self, other, method = None, copy = None, limit = None, tolerance = None):
        return CallCol(lambda DF: self.__call__(DF).reindex_like(other=_decide_if_call(other, DF), method=method, copy=copy, limit=limit, tolerance=tolerance))

    def rename(self, index = None, axis = None, copy = True, inplace = False, level = None, errors = 'ignore'):
        return CallCol(lambda DF: self.__call__(DF).rename(index=index, axis=axis, copy=copy, inplace=inplace, level=level, errors=errors))

    def rename_axis(self, mapper = lib.no_default, index = lib.no_default, axis = 0, copy = True, inplace = False):
        return CallCol(lambda DF: self.__call__(DF).rename_axis(mapper=mapper, index=index, axis=axis, copy=copy, inplace=inplace))

    def reorder_levels(self, order):
        return CallCol(lambda DF: self.__call__(DF).reorder_levels(order=order))

    def repeat(self, repeats, axis = None):
        return CallCol(lambda DF: self.__call__(DF).repeat(repeats=repeats, axis=axis))

    def replace(self, to_replace = None, value = lib.no_default, inplace = False, limit = None, regex = False, method = lib.no_default):
        return CallCol(lambda DF: self.__call__(DF).replace(to_replace=to_replace, value=value, inplace=inplace, limit=limit, regex=regex, method=method))

    def resample(self, rule, axis = 0, closed = None, label = None, convention = 'start', kind = None, on = None, level = None, origin = 'start_day', offset = None, group_keys = False):
        return CallCol(lambda DF: self.__call__(DF).resample(rule=rule, axis=axis, closed=closed, label=label, convention=convention, kind=kind, on=on, level=level, origin=origin, offset=offset, group_keys=group_keys))

    def reset_index(self, level = None, drop = False, name = lib.no_default, inplace = False, allow_duplicates = False):
        return CallCol(lambda DF: self.__call__(DF).reset_index(level=level, drop=drop, name=name, inplace=inplace, allow_duplicates=allow_duplicates))

    def rfloordiv(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).rfloordiv(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def rmod(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).rmod(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def rmul(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).rmul(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def rolling(self, window, min_periods = None, center = False, win_type = None, on = None, axis = 0, closed = None, step = None, method = 'single'):
        return CallCol(lambda DF: self.__call__(DF).rolling(window=window, min_periods=min_periods, center=center, win_type=win_type, on=on, axis=axis, closed=closed, step=step, method=method))

    def round(self, decimals = 0, *args, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).round(decimals=decimals, args=args, kwargs=kwargs))

    def rpow(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).rpow(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def rsub(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).rsub(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def rtruediv(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).rtruediv(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def sample(self, n = None, frac = None, replace = False, weights = None, random_state = None, axis = None, ignore_index = False):
        return CallCol(lambda DF: self.__call__(DF).sample(n=n, frac=frac, replace=replace, weights=weights, random_state=random_state, axis=axis, ignore_index=ignore_index))

    def searchsorted(self, value, side = 'left', sorter = None):
        return CallCol(lambda DF: self.__call__(DF).searchsorted(value=value, side=side, sorter=sorter))

    def sem(self, axis = None, skipna = True, ddof = 1, numeric_only = False, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).sem(axis=axis, skipna=skipna, ddof=ddof, numeric_only=numeric_only, kwargs=kwargs))

    def set_axis(self, labels, axis = 0, copy = None):
        return CallCol(lambda DF: self.__call__(DF).set_axis(labels=labels, axis=axis, copy=copy))

    def set_flags(self, copy = False, allows_duplicate_labels = None):
        return CallCol(lambda DF: self.__call__(DF).set_flags(copy=copy, allows_duplicate_labels=allows_duplicate_labels))

    def shift(self, periods = 1, freq = None, axis = 0, fill_value = None):
        return CallCol(lambda DF: self.__call__(DF).shift(periods=periods, freq=freq, axis=axis, fill_value=fill_value))

    def skew(self, axis = 0, skipna = True, numeric_only = False, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).skew(axis=axis, skipna=skipna, numeric_only=numeric_only, kwargs=kwargs))

    def sort_index(self, axis = 0, level = None, ascending = True, inplace = False, kind = 'quicksort', na_position = 'last', sort_remaining = True, ignore_index = False, key = None):
        return CallCol(lambda DF: self.__call__(DF).sort_index(axis=axis, level=level, ascending=ascending, inplace=inplace, kind=kind, na_position=na_position, sort_remaining=sort_remaining, ignore_index=ignore_index, key=key))

    def sort_values(self, axis = 0, ascending = True, inplace = False, kind = 'quicksort', na_position = 'last', ignore_index = False, key = None):
        return CallCol(lambda DF: self.__call__(DF).sort_values(axis=axis, ascending=ascending, inplace=inplace, kind=kind, na_position=na_position, ignore_index=ignore_index, key=key))

    def squeeze(self, axis = None):
        return CallCol(lambda DF: self.__call__(DF).squeeze(axis=axis))

    def std(self, axis = None, skipna = True, ddof = 1, numeric_only = False, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).std(axis=axis, skipna=skipna, ddof=ddof, numeric_only=numeric_only, kwargs=kwargs))

    def sub(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).sub(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def subtract(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).subtract(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def sum(self, axis = None, skipna = True, numeric_only = False, min_count = 0, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).sum(axis=axis, skipna=skipna, numeric_only=numeric_only, min_count=min_count, kwargs=kwargs))

    def swaplevel(self, i = -2, j = -1, copy = None):
        return CallCol(lambda DF: self.__call__(DF).swaplevel(i=i, j=j, copy=copy))

    def tail(self, n = 5):
        return CallCol(lambda DF: self.__call__(DF).tail(n=n))

    def take(self, indices, axis = 0, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).take(indices=indices, axis=axis, kwargs=kwargs))

    def to_clipboard(self, excel = True, sep = None, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).to_clipboard(excel=excel, sep=sep, kwargs=kwargs))

    def to_csv(self, path_or_buf = None, sep = ',', na_rep = '', float_format = None, columns = None, header = True, index = True, index_label = None, mode = 'w', encoding = None, compression = 'infer', quoting = None, quotechar = '"', lineterminator = None, chunksize = None, date_format = None, doublequote = True, escapechar = None, decimal = '.', errors = 'strict', storage_options = None):
        return CallCol(lambda DF: self.__call__(DF).to_csv(path_or_buf=path_or_buf, sep=sep, na_rep=na_rep, float_format=float_format, columns=columns, header=header, index=index, index_label=index_label, mode=mode, encoding=encoding, compression=compression, quoting=quoting, quotechar=quotechar, lineterminator=lineterminator, chunksize=chunksize, date_format=date_format, doublequote=doublequote, escapechar=escapechar, decimal=decimal, errors=errors, storage_options=storage_options))

    def to_dict(self, into = dict):
        return CallCol(lambda DF: self.__call__(DF).to_dict(into=into))

    def to_excel(self, excel_writer, sheet_name = 'Sheet1', na_rep = '', float_format = None, columns = None, header = True, index = True, index_label = None, startrow = 0, startcol = 0, engine = None, merge_cells = True, inf_rep = 'inf', freeze_panes = None, storage_options = None):
        return CallCol(lambda DF: self.__call__(DF).to_excel(excel_writer=excel_writer, sheet_name=sheet_name, na_rep=na_rep, float_format=float_format, columns=columns, header=header, index=index, index_label=index_label, startrow=startrow, startcol=startcol, engine=engine, merge_cells=merge_cells, inf_rep=inf_rep, freeze_panes=freeze_panes, storage_options=storage_options))

    def to_frame(self, name = lib.no_default):
        return CallCol(lambda DF: self.__call__(DF).to_frame(name=name))

    def to_hdf(self, path_or_buf, key, mode = 'a', complevel = None, complib = None, append = False, format = None, index = True, min_itemsize = None, nan_rep = None, dropna = None, data_columns = None, errors = 'strict', encoding = 'UTF-8'):
        return CallCol(lambda DF: self.__call__(DF).to_hdf(path_or_buf=path_or_buf, key=key, mode=mode, complevel=complevel, complib=complib, append=append, format=format, index=index, min_itemsize=min_itemsize, nan_rep=nan_rep, dropna=dropna, data_columns=data_columns, errors=errors, encoding=encoding))

    def to_json(self, path_or_buf = None, orient = None, date_format = None, double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None, lines = False, compression = 'infer', index = True, indent = None, storage_options = None, mode = 'w'):
        return CallCol(lambda DF: self.__call__(DF).to_json(path_or_buf=path_or_buf, orient=orient, date_format=date_format, double_precision=double_precision, force_ascii=force_ascii, date_unit=date_unit, default_handler=default_handler, lines=lines, compression=compression, index=index, indent=indent, storage_options=storage_options, mode=mode))

    def to_latex(self, buf = None, columns = None, header = True, index = True, na_rep = 'NaN', formatters = None, float_format = None, sparsify = None, index_names = True, bold_rows = False, column_format = None, longtable = None, escape = None, encoding = None, decimal = '.', multicolumn = None, multicolumn_format = None, multirow = None, caption = None, label = None, position = None):
        return CallCol(lambda DF: self.__call__(DF).to_latex(buf=buf, columns=columns, header=header, index=index, na_rep=na_rep, formatters=formatters, float_format=float_format, sparsify=sparsify, index_names=index_names, bold_rows=bold_rows, column_format=column_format, longtable=longtable, escape=escape, encoding=encoding, decimal=decimal, multicolumn=multicolumn, multicolumn_format=multicolumn_format, multirow=multirow, caption=caption, label=label, position=position))

    def to_list(self):
        return CallCol(lambda DF: self.__call__(DF).to_list())

    def to_markdown(self, buf = None, mode = 'wt', index = True, storage_options = None, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).to_markdown(buf=buf, mode=mode, index=index, storage_options=storage_options, kwargs=kwargs))

    def to_numpy(self, dtype = None, copy = False, na_value = lib.no_default, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).to_numpy(dtype=dtype, copy=copy, na_value=na_value, kwargs=kwargs))

    def to_period(self, freq = None, copy = None):
        return CallCol(lambda DF: self.__call__(DF).to_period(freq=freq, copy=copy))

    def to_pickle(self, path, compression = 'infer', protocol = 5, storage_options = None):
        return CallCol(lambda DF: self.__call__(DF).to_pickle(path=path, compression=compression, protocol=protocol, storage_options=storage_options))

    def to_sql(self, name, con, schema = None, if_exists = 'fail', index = True, index_label = None, chunksize = None, dtype = None, method = None):
        return CallCol(lambda DF: self.__call__(DF).to_sql(name=name, con=con, schema=schema, if_exists=if_exists, index=index, index_label=index_label, chunksize=chunksize, dtype=dtype, method=method))

    def to_string(self, buf = None, na_rep = 'NaN', float_format = None, header = True, index = True, length = False, dtype = False, name = False, max_rows = None, min_rows = None):
        return CallCol(lambda DF: self.__call__(DF).to_string(buf=buf, na_rep=na_rep, float_format=float_format, header=header, index=index, length=length, dtype=dtype, name=name, max_rows=max_rows, min_rows=min_rows))

    def to_timestamp(self, freq = None, how = 'start', copy = None):
        return CallCol(lambda DF: self.__call__(DF).to_timestamp(freq=freq, how=how, copy=copy))

    def to_xarray(self):
        return CallCol(lambda DF: self.__call__(DF).to_xarray())

    def transform(self, func, axis = 0, *args, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).transform(func=func, axis=axis, args=args, kwargs=kwargs))

    def transpose(self, *args, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).transpose(args=args, kwargs=kwargs))

    def truediv(self, other, level = None, fill_value = None, axis = 0):
        return CallCol(lambda DF: self.__call__(DF).truediv(other=_decide_if_call(other, DF), level=level, fill_value=fill_value, axis=axis))

    def truncate(self, before = None, after = None, axis = None, copy = None):
        return CallCol(lambda DF: self.__call__(DF).truncate(before=before, after=after, axis=axis, copy=copy))

    def tz_convert(self, tz, axis = 0, level = None, copy = None):
        return CallCol(lambda DF: self.__call__(DF).tz_convert(tz=tz, axis=axis, level=level, copy=copy))

    def tz_localize(self, tz, axis = 0, level = None, copy = None, ambiguous = 'raise', nonexistent = 'raise'):
        return CallCol(lambda DF: self.__call__(DF).tz_localize(tz=tz, axis=axis, level=level, copy=copy, ambiguous=ambiguous, nonexistent=nonexistent))

    def unique(self):
        return CallCol(lambda DF: self.__call__(DF).unique())

    def unstack(self, level = -1, fill_value = None):
        return CallCol(lambda DF: self.__call__(DF).unstack(level=level, fill_value=fill_value))

    def update(self, other):
        return CallCol(lambda DF: self.__call__(DF).update(other=_decide_if_call(other, DF)))

    def value_counts(self, normalize = False, sort = True, ascending = False, bins = None, dropna = True):
        return CallCol(lambda DF: self.__call__(DF).value_counts(normalize=normalize, sort=sort, ascending=ascending, bins=bins, dropna=dropna))

    def var(self, axis = None, skipna = True, ddof = 1, numeric_only = False, **kwargs):
        return CallCol(lambda DF: self.__call__(DF).var(axis=axis, skipna=skipna, ddof=ddof, numeric_only=numeric_only, kwargs=kwargs))

    def view(self, dtype = None):
        return CallCol(lambda DF: self.__call__(DF).view(dtype=dtype))

    def where(self, cond, other = lib.no_default, inplace = False, axis = None, level = None):
        return CallCol(lambda DF: self.__call__(DF).where(cond=_decide_if_call(cond, DF), other=_decide_if_call(other, DF), inplace=inplace, axis=axis, level=level))

    def xs(self, key, axis = 0, level = None, drop_level = True):
        return CallCol(lambda DF: self.__call__(DF).xs(key=key, axis=axis, level=level, drop_level=drop_level))

@dataclass
class Col(BaseCol):
    col_name: Any
    
    def __call__(self, DF):
        return DF[self.col_name]

@dataclass
class CallCol(BaseCol):
    fn: Callable
    
    def __call__(self, DF):
        return self.fn(DF)
