# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

import ast
from inspect import getmembers
import inspect
import os
from typing import TypeVar as _TypeVar
from typing import Union as _Union
from typing import Iterable as _Iterable
from typing import TYPE_CHECKING
import colemen_utils as _c



# ---------------------------------------------------------------------------- #
#                               TYPE DECLARATIONS                              #
# ---------------------------------------------------------------------------- #

_main_type = None
_package_type = None
_py_class_type = None
_py_property_type = None
_py_module_type = None
_py_import_type = None
_method_type = None
_method_argument_type = None
_decorator_type = None
_decorator_argument_type = None



# ControlPanel = _control_panel.ControlPanel()

if TYPE_CHECKING:

    import silent_engine as _m
    _main_type = _TypeVar('_main_type', bound=_m.Main)

    import silent.Package as _p
    _package_type = _TypeVar('_package_type', bound=_p.Package)

    import silent.Class as _class
    _py_class_type = _TypeVar('_py_class_type', bound=_class.Class)

    import silent.Class.Property as _prop
    _py_property_type = _TypeVar('_py_property_type', bound=_prop.Property)

    import silent.Module as _mod
    _py_module_type = _TypeVar('_py_module_type', bound=_mod.Module)

    import silent.Import.ImportStatement as _imps
    _py_import_type = _TypeVar('_py_import_type', bound=_imps.ImportStatement)


    import silent.Method.Method as _classM
    _method_type = _TypeVar('_method_type', bound=_classM.Method)

    import silent.Method.MethodArgument as _methArg
    _method_argument_type = _TypeVar('_method_argument_type', bound=_methArg.MethodArgument)

    from silent.Decorator.Decorator import Decorator as _rF4Z
    _decorator_type = _TypeVar('_decorator_type', bound=_rF4Z)

    from silent.Decorator.DecoratorArgument import DecoratorArgument as _chRf
    _decorator_argument_type = _TypeVar('_decorator_argument_type', bound=_chRf)
