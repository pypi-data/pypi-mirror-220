"""Automate the build of pandas_sans_lambdas.py"""

# %% Imports
import inspect
import operator
import re

import itertools

import pandas as pd

# %% Classes and functions
def flatten_comprehension(source_list, func):
    return list(itertools.chain.from_iterable(func(i) for i in source_list))

def flatten_tuple_comprehension(source_list, func):
    return list(itertools.chain.from_iterable(func(*i) for i in source_list))

def make_simple_property(property_name, fn="__call__", accessor = ""):
    accessor_text = f".{accessor}" if accessor else ""
    
    return [
        f"    @property",
        f"    def {property_name}(self, DF):",
        f"        return self.{fn}(DF){accessor_text}.{property_name}",
        "",
    ]

def write_property_code(properties, function_name="__call__", accessor=""):
    property_tuple = [(property_name, function_name, accessor) for property_name in properties]    
    return flatten_tuple_comprehension(property_tuple, make_simple_property)


def make_called_method(method, param_call_list, params_fn_def, params_positional_args, func="__call__", accessor=""):
    output = make_simple_method(method, params_fn_def, params_positional_args, func, accessor)

    for param in param_call_list:
        output[1] = re.sub(f"\\b={param}\\b", f"=_decide_if_call({param}, DF)", output[1])

    return output

def make_simple_method(method, params_fn_def, params_positional_args, func="__call__", accessor=""):
    accessor_text = f".{accessor}" if accessor else ""
    
    return [
        f"    def {method}({params_fn_def}):",
        f"        return CallCol(lambda DF: self.{func}(DF){accessor_text}.{method}({params_positional_args}))",
        f"",
    ]


def write_indexer_class(indexer_name):
    return [
        f"class _{indexer_name.capitalize()}Indexer:",
        f"    def __init__(self, func):",
        f"        self.func = func",

        f"    def __getitem__(self, *indexes):",
        f"        return CallCol(lambda DF: self.func(DF).{indexer_name}.__getitem__(*indexes))",
        f"",
    ]


def write_indexer(indexer_name):
    return [
        f"    @property",
        f"    def {indexer_name}(self):",
        f"        return _{indexer_name.capitalize()}Indexer(self.__call__)",
        f"",
    ]

def remove_types(txt):
    param = txt.split(':')[0].split("=")[0].strip()
    
    if ":" in txt:
        remainder = txt.split(":")[1]
    else:
        remainder = txt
    
    if "=" in txt:
        default_value = remainder.split("=")[1].strip()
        output = f"{param} = {default_value}"
    else:
        output = param
    
    return output

def make_code_helpers(series_object, method_name):
    params = inspect.signature(getattr(series_object, method_name)).parameters

    params_positional_args = ", ".join([f"{i}={i}" for i in params.keys()])

    param_values = [remove_types(str(value)) for value in params.values()]

    params_fn_def = (", ".join(["self", *param_values]))

    return params_fn_def, params_positional_args


def make_accessor_property_code(accessor):
    return [
        f"    @property",
        f"    def {accessor}(self):",
        f"        return _{accessor.capitalize()}Accessor(self.__call__)",
        f"",
    ]

# %%
def find_attrs(series_dict):
    most_attrs = []

    for _, series in series_dict.items():
        most_attrs = most_attrs + [i for i in dir(series) if not i.startswith("_")]

    return sorted(set(most_attrs))

def find_attr_groups(attr_list, series, accessors = ["cat", "dt", "str", "sparse", "plot"]):
    attr_groups = {
        "accessors": accessors,
        "indexers": [],
        "methods": [],
        "properties": [],
    }

    for attr_string in attr_list:
        if attr_string in attr_groups["accessors"]:
            continue
        
        attr = getattr(series, attr_string)
        type_string = str(type(attr)).lower()
        
        if "indexing" in type_string:
            attr_groups["indexers"].append(attr_string)
        elif "method" in type_string:
            if attr_string == "swapaxes":
                continue
            attr_groups["methods"].append(attr_string)
        elif callable(attr):
            raise Exception(f"The attr {attr_string} is not a method or an indexer")
        else:
            attr_groups["properties"].append(attr_string)
    return attr_groups

def write_regular_methods_code(obj, methods):
    output_code = []

    for method in methods:
        code_helpers = make_code_helpers(obj, method)
        if method == "ewm":
            code = make_called_method(method, ["times"], *code_helpers)
        elif method == "map":
            code = make_called_method(method, ["arg"], *code_helpers)
        elif method == "fillna":
            code = make_called_method(method, ["value"], *code_helpers)
        elif method in ["where", "mask"]:
            code = make_called_method(method, ["cond", "other"], *code_helpers)
        elif "other" in code_helpers[1]:
            code = make_called_method(method, ["other"], *code_helpers)
        else:
            code = make_simple_method(method, *code_helpers)
        output_code += code

    return output_code

def write_indexer_class_code(indexer_list):
    return flatten_comprehension(indexer_list, write_indexer_class)

def write_indexer_code(indexer_list):
    return flatten_comprehension(indexer_list, write_indexer)

def write_accessor_code(accessor_list):
    return flatten_comprehension(accessor_list, make_accessor_property_code)

def get_methods_and_properties(obj, extra_attrs = []):
    attrs = [i for i in dir(obj) if not i.startswith("_")]
    attrs += extra_attrs

    methods = []
    properties = []

    for attr in attrs:
        if callable(getattr(obj, attr)):
            methods.append(attr)
        else:
            properties.append(attr)
    
    return methods, properties

def write_accessor_class_code(series_dict, accessor_name, extra_attrs = []):
    obj = getattr(series_dict[accessor_name], accessor_name)
    methods, properties = get_methods_and_properties(obj, extra_attrs)

    output_code = [
        f"@dataclass",
        f"class _{accessor_name.capitalize()}Accessor(object):",
        f"    _fn: Callable",
        f"",
    ]

    output_code += write_property_code(properties, "_fn", accessor_name)
    
    for method in methods:
        code_helpers = make_code_helpers(obj, method)        
        if accessor_name == "plot" and method in ("hexbin", "scatter"):
            continue
        if accessor_name == "sparse" and method == "from_coo":
            continue
        if accessor_name == "str" and method == "cat":
            output_code += make_called_method(method, ["others"], *code_helpers, func="_fn", accessor=accessor_name)
        else:
            output_code += make_simple_method(method, *code_helpers, func="_fn", accessor=accessor_name)
    return output_code

def check_series_dunder_attrs(operator_dunder_attrs, series):
    exclusion_list = [
        "__concat__",
        "__iconcat__",
        "__ilshift__",
        "__imatmul__",
        "__index__",
        "__inv__",
        "__irshift__",
        "__lshift__",
        "__not__",
        "__rshift__",
    ]

    for attr in operator_dunder_attrs:
        if attr in exclusion_list:
            continue

        attr_type = type(getattr(operator, attr))

        if "builtin_function_or_method" not in str(attr_type):
            continue
        try:
            type(getattr(series, attr))
        except AttributeError:
            raise AttributeError(f"{attr} | {attr_type}")

def find_dunder_attr_groups(attrs, series):
    attr_groups = {
        "builtins": [],
        "methods": [],
        "properties": [],
    }    
    
    for attr in attrs:
        if attr == "__weakref__":
            continue

        attr_obj = getattr(series, attr)
        type_string = str(type(attr_obj))

        if "builtin" in type_string:
            attr_groups["builtins"].append(attr)
        elif attr == "__class__":
            attr_groups["methods"].append(attr)
        elif "method" in type_string:
            attr_groups["methods"].append(attr)
        elif callable(attr_obj):
            raise Exception(f"The callable attr {attr} is not a builtin or method")
        else:
            attr_groups["properties"].append(attr)
    
    return attr_groups

def write_dunder_methods_code(series, methods):
    methods_to_exclude = [
        "__array_ufunc__",
        "__copy__",
        "__deepcopy__",
        "__delattr__",
        "__delitem__",
        "__dir__",
        "__finalize__",
        "__getattr__",
        "__getattribute__",
        "__getitem__",
        "__getstate__",
        "__init__",
        "__iter__",
        "__new__",
        "__repr__",
        "__setattr__",
        "__setitem__",
        "__setstate__",
        "__sizeof__",
        "__str__",
        "__weakref__",
    ]
    
    output_code = []
    
    for method in methods:
        if method in methods_to_exclude:
            continue

        code_helpers = make_code_helpers(series, method)

        if method == "__class__":
            code = make_called_method(method, ["data"], *code_helpers)
        elif "other" in code_helpers[1]:
            code = make_called_method(method, ["other"], *code_helpers)
        else:
            code = make_simple_method(method, *code_helpers)

        output_code += code
    
    return output_code

def check_builtins(builtins):
    known_builtins = [
        '__format__',
        '__init_subclass__',
        '__new__',
        '__reduce__',
        '__reduce_ex__',
        '__subclasshook__',
    ]

    for builtin_name in builtins:
        if builtin_name not in known_builtins:
            raise Exception(f"The builtin {builtin_name} is not accounted for.")

# %% Write non-dunder methods, properties and classes
series_dict = {
    "plot": pd.Series([1, 2, 3], name="beep"),
    "cat": pd.Series(pd.Categorical(['c', 'b', 'c'])),
    "dt": pd.Series(pd.date_range("2000-01-01", periods=3, freq="ns")),
    "str": pd.Series(list("abc"), dtype="string"),
    "sparse": pd.Series(pd.arrays.SparseArray([0, 0, 1, 1, 1], fill_value=0)),
}

attr_groups = find_attr_groups(find_attrs(series_dict), series_dict["plot"])

# %% Dunders
integer_series = series_dict["plot"]

operator_dunder_attrs = sorted([i for i in dir(operator) if i.startswith("__")])
series_dunder_attrs = sorted([i for i in dir(integer_series) if i.startswith("__")])

# %% Check that all operator dunders are series dunders, except the exclusion list
check_series_dunder_attrs(operator_dunder_attrs, integer_series)

# %% Find dunder attr groups
dunder_attr_groups = find_dunder_attr_groups(series_dunder_attrs, integer_series)
check_builtins(dunder_attr_groups["builtins"])


# %% Write the output as a list
output = [
    "\"\"\"Auto-generated dunder method col implementation\"\"\"",
    "",
    "# %% Imports",
    "from abc import abstractmethod",
    "from dataclasses import dataclass",
    "from typing import Any, Callable",
    "",
    "import pandas as pd",
    "from pandas._libs import lib",
    "",
    "# %% Classes and functions",
    "def _is_col_test(obj):",
    "    return hasattr(obj, \"_is_col\")",
    "",
    "def _decide_if_call(obj, DF):",
    "    return obj(DF) if _is_col_test(obj) else obj",
    "",
    *write_indexer_class_code(attr_groups["indexers"]),
    *write_accessor_class_code(series_dict, "str"),
    *write_accessor_class_code(series_dict, "cat"),
    *write_accessor_class_code(series_dict, "dt"),
    *write_accessor_class_code(series_dict, "sparse"),
    *write_accessor_class_code(series_dict, "plot", extra_attrs = ["__call__"]),
    "class BaseCol(object):",
    "    _is_col = True",
    "",
    "    @abstractmethod",
    "    def __call__(self, df):",
    "        pass",
    "",
    "    def __getitem__(self, *indexes):",
    "        return CallCol(lambda DF: self.__call__(DF).at.__getitem__(*indexes))",
    "",
    *write_property_code(dunder_attr_groups["properties"]),
    *write_accessor_code(attr_groups["accessors"]),
    *write_property_code(attr_groups["properties"]),
    *write_indexer_code(attr_groups["indexers"]),
    *write_dunder_methods_code(integer_series, dunder_attr_groups["methods"]),
    *write_regular_methods_code(integer_series, attr_groups["methods"]),
    "@dataclass",
    "class Col(BaseCol):",
    "    col_name: Any",
    "    ",
    "    def __call__(self, DF):",
    "        return DF[self.col_name]",
    "",
    "@dataclass",
    "class CallCol(BaseCol):",
    "    fn: Callable",
    "    ",
    "    def __call__(self, DF):",
    "        return self.fn(DF)",
    "",
]

# %% Apply final patches to the output
output = [i.replace("<no_default>", "lib.no_default") for i in output]
output = [i.replace("<class 'dict'>", "dict") for i in output]

# %% Write the output as a file
with open("./src/pandas_sans_lambdas/helpers.py", "w") as f:
    f.write("\n".join(output))
