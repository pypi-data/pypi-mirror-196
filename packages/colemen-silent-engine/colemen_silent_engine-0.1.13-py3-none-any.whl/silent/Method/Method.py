# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import




from dataclasses import dataclass
import re
from string import Template
from typing import Iterable, Union
import datetime
import ast

import colemen_utils as c
import silent.EntityBase as _eb

import silent.DocBlock.ClassMethodDocBlock as _docblock
import silent.Method.MethodArgument as _ma
import silent.Decorator.Decorator as _dec
# from config import column_type,_relationship_type,endpointdoc_type,route_type,root_directory,susurrus_type
import silent.se_config as config
import silent.settings.types as _types
log = c.con.log


@dataclass
class Method(_eb.EntityBase):


    body:str = None
    '''The method's body'''

    return_description:str = None
    '''A description of the return value'''

    return_type:str = None
    '''The type returned by this method'''

    _is_getter:bool = False
    '''If True the property decorator is added to the method'''

    _is_setter:bool = False
    '''If True the property setter decorator is added to the method'''

    indent:int = 0

    is_class_method:bool = False
    
    _decorators:Iterable[_types._decorator_type] = None
    '''A list of decorator instances for this method.'''

    _args:Iterable[config._method_argument_type] = None
    _kwargs:Iterable[config._method_argument_type] = None

    prop:config._py_property_type=None
    '''The property instance that this method modifies. (if this is a getter or setter.)'''


    def __init__(self,main:config._main_type,package:config._package_type,name:str,
                pyclass:config._py_class_type=None,module:config._py_module_type=None,description:str=None,
                body:str="pass",return_type:str=None,return_description:str=None,is_getter:bool=False,
                is_setter:bool=False,is_class_method:bool=False,tags:Union[str,list]=None,
                prop:config._py_property_type=None,decorators:Union[str,list]=None):
        '''
            Class used to generate a python class method.
            ----------

            Arguments
            -------------------------
            `main` {_main_type}
                A reference to the master

            `name` {str}
                The name of this method.

            [`pyclass`=None] {Class}
                A reference to the class that this method belongs to.

            [`module`=None] {Module}
                A reference to the module that this method belongs to.

            [`description`=None] {str}
                The docblock description for this method.

            [`body`="pass"] {str}
                The body of the method.

            [`return_type`=None] {str}
                The type returned by this method

            [`return_description`=None] {str}
                A description of the return value

            [`is_getter`=False] {bool}
                If True the property decorator is added to the method

            [`is_setter`=False] {bool}
                If True the property setter decorator is added to the method

            [`is_class_method`=False] {bool}
                True if this method belongs to a class.

            [`tags`=None] {list,str}
                A tag or list of tags to add after it is instantiated.

            [`prop`=None] {Property}
                A reference to the property that is being retrieved.
                Only applies if this a class attribute getter or setter.

            [`decorators`=None] {list,str}
                A decorator or list of decorators to add to this method.



            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-26-2022 08:35:16
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: Table
            * @xxx [12-26-2022 08:36:08]: documentation for Table
        '''
        kwargs = {}
        kwargs['main'] = main
        kwargs['package'] = package
        kwargs['name'] = name
        kwargs['pyclass'] = pyclass
        kwargs['module'] = module
        kwargs['description'] = description
        kwargs['body'] = body
        kwargs['return_type'] = return_type
        kwargs['return_description'] = return_description
        kwargs['is_getter'] = is_getter
        kwargs['is_setter'] = is_setter
        kwargs['is_class_method'] = is_class_method
        kwargs['prop'] = prop
        # kwargs['_decorators'] = []

        super().__init__(**kwargs)
        # _=self.declaration_ast


        if isinstance(tags,(list,str)):
            self.add_tag(tags)
        # self.main:config._main_type = main
        # self.pyclass:config._py_class_type = pyclass
        self.Doc = None
        self._args = []
        self._kwargs = []
        self._decorators = []

        decs = c.arr.force_list(decorators,allow_nulls=False)
        if len(decs) > 0:
            for d in decs:
                self.add_decorator(d)
        # self._decorators = []
        # self.Doc = _docblock.ClassMethodDocBlock(self)


        # populate_from_dict(kwargs,self)

        if self.is_class_method is True:
            self.indent = 4
            self.add_tag(self.pyclass.name.name)

        # self.Doc.indent = self.indent + 4
        self.regen_imports()
        self.body = self._format_single_line_comments(self.body)

    @property
    def summary(self):
        '''
            Get the summary property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-06-2022 12:10:00
            `@memberOf`: __init__
            `@property`: summary
        '''
        value = {
            "name":self.name.name,
            "description":self.description,
            "is_class_method":self.is_class_method,
            "return_description":self.return_description,
            "return_type":self.return_type,
            "is_getter":self.is_getter,
            "is_setter":self.is_setter,
            "arguments":[],
            "keyword_arguments":[],
            "import_statement":self.import_statement,
        }
        for arg in self.arg_list:
            value['arguments'].append(arg.summary)


        return value


    @property
    def local_name(self)->str:
        '''
            Get this Method's local_name

            The local name is used by the class for distinguishing methods with the same name.
            Specifically, this solves the name collisions caused by getters and setters having the same
            name. It does this by applying a suffix:

            propname____get
            propname____set

            If this method is not a getter or setter, its normal name is returned.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 09:00:57
            `@memberOf`: Method
            `@property`: get_local_name
        '''
        if self.is_getter:
            return f"{self.name.name}____get"
        if self.is_setter:
            return f"{self.name.name}____set"
        return self.name.name


    @property
    def is_getter(self)->bool:
        '''
            Get the is_getter value.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 10:09:11
            `@memberOf`: PostArg
            `@property`: is_getter
        '''
        value = self._is_getter
        return value

    @is_getter.setter
    def is_getter(self,value:bool):
        '''
            Set the is_getter value.

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 10:09:11
            `@memberOf`: PostArg
            `@property`: is_getter
        '''
        if value is True:
            self.add_tag("getter","setter")
        else:
            self.delete_tag("getter")
        self._is_getter = value

    @property
    def is_setter(self)->bool:
        '''
            Get the is_setter value.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 10:16:05
            `@memberOf`: PostArg
            `@property`: is_setter
        '''
        value = self._is_setter
        return value

    @is_setter.setter
    def is_setter(self,value:bool):
        '''
            Set the is_setter value.

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 10:16:05
            `@memberOf`: PostArg
            `@property`: is_setter
        '''
        if value is True:
            self.add_tag("setter","getter")
        else:
            self.delete_tag("setter")
        self._is_setter = value



    # ---------------------------------------------------------------------------- #
    #                                   ARGUMENTS                                  #
    # ---------------------------------------------------------------------------- #



    def add_arg(
        self,
        name:str=None,
        data_type:str=None,
        default="__NO_DEFAULT_PROVIDED__",
        description:str="",
        arg:config._method_argument_type=None,
        tags:Union[str,list]=None,
        prop:config._py_property_type=None
        )->_types._method_argument_type:
        '''
            Add an argument to this method.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the argument.

            [`data_type`=None] {str}
                The expected type of the argument

            [`default`="__NO_DEFAULT_PROVIDED__"] {any}
                The default value to use if no value is provided.

            [`description`=""] {any}
                The documentation description

            [`tags`=None] {list,str}
                A tag or list of tags to add to this argument after it is instantiated.

            [`arg`=None] {Method_Argument}
                A method argument instance to copy.
                This is useful when you want to add the same argument to another method.

            [`prop`=None] {Property}
                A property instance to use as an argument.


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-03-2023 15:41:59
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_arg
            * @xxx [01-03-2023 15:43:13]: documentation for add_arg
        '''
        if self.get_arg(name) is not None:
            return False

        if name is None and arg is None and prop is None:
            raise TypeError("You must provide a name, argument or property")


        ma = _ma.MethodArgument(
            main=self.main,
            method=self,
            name=name,
            arg = arg,
            prop = prop,
            data_type = data_type,
            default = default,
            description = description,
            tags = tags,
        )

        if ma.has_default:
            self._args.append(ma)
        else:
            self._args.insert(0,ma)
        # self._args.append(ma)
        return ma


    def add_kwarg(self,name,**kwargs):
        '''
            Add a keyword argument to this method.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the argument.

            Keyword Arguments
            -------------------------
            [`data_type`=None] {str}
                The expected type of the argument
            [`default`=None] {any}
                The default value to use if no value is provided.
            [`description`=None] {any}
                The documentation description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-03-2023 15:41:59
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_arg
            * @xxx [01-03-2023 15:43:13]: documentation for add_arg
        '''


        # ma = _ma.MethodArgument(self.main,self)
        ma = _ma.MethodArgument(
            self.main,
            self,
            name=name,
            data_type = c.obj.get_kwarg(['data_type','type'],None,(str),**kwargs),
            default = c.obj.get_kwarg(['default_value','default'],"__NO_DEFAULT_PROVIDED__",None,**kwargs),
            description = c.obj.get_kwarg(['description'],"",None,**kwargs),
        )

        # data_type = c.obj.get_kwarg(['py_type','type'],None,(str),**kwargs)
        # default_value = c.obj.get_kwarg(['default_value','default'],"__NO_DEFAULT_VALUE_SET__",None,**kwargs)
        # description = c.obj.get_kwarg(['description'],"",None,**kwargs)
        # ma.name = name
        # ma.py_type = data_type
        # ma.default_value = default_value
        # ma.description = description

        if ma.has_default:
            self._kwargs.append(ma)
        else:
            self._kwargs.insert(0,ma)
        # self._args.append(ma)

    def get_arg(self,name:str=None,tags:Union[str,list]=None)->config._method_argument_type:
        '''
            Get an argument from this method with a matching name
            ----------

            Arguments
            -------------------------
            [`name`=None] {str}
                The name to search for.
            [`tags`=None] {str,list}
                A tag or list of tags to search for.
                This is only used if a name match is not found or name is not provided.

                The argument must have all tags in order to match.

            Return {MethodArgument}
            ----------------------
            The method argument if it exists, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-10-2023 08:18:26
            `memberOf`: Method
            `version`: 1.0
            `method_name`: get_arg
            * @xxx [03-10-2023 08:19:36]: documentation for get_arg
        '''
        if name is not None:
            for arg in self.arg_list:
                if arg.name.name == name:
                    return arg
        if tags is not None:
            tags = c.arr.force_list(tags,allow_nulls=False)
            if len(tags) > 0:
                for arg in self.arg_list:
                    if arg.has_tag(tags):
                        return arg
        return None

    @property
    def arg_list(self)->Iterable[config._method_argument_type]:
        '''
            Get a list of method argument instances

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-03-2023 16:00:40
            `@memberOf`: __init__
            `@property`: arg_list
        '''
        value = self._args
        if value is None:
            value = []
        return value

    @property
    def kwarg_list(self)->Iterable[config._method_argument_type]:
        '''
            Get the kwarg_list property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-03-2023 16:23:06
            `@memberOf`: __init__
            `@property`: kwarg_list
        '''
        value = self._kwargs
        if value is None:
            value = []
        return value



    # ---------------------------------------------------------------------------- #
    #                                  DECORATORS                                  #
    # ---------------------------------------------------------------------------- #

    def add_decorator(self,
        name:str,
        tags:Union[str,list]=None
        )->_types._decorator_type:
        if self.get_decorator(name) is not None:
            c.con.log(f"Duplicate Decorator provided for method {self.name.name}: {name}","warning")
            return False



        d = _dec.Decorator(self.main,name=name,method=self,tags=tags)
        self._decorators.append(d)

        return d

    def get_decorator(self,name:str=None,tags:Union[str,list]=None)->_types._decorator_type:
        '''
            Get a decorator from this method with a matching name or tag
            ----------

            Arguments
            -------------------------
            [`name`=None] {str}
                The name to search for.

            [`tags`=None] {str,list}
                A tag or list of tags to search for.
                This is only used if a name match is not found or name is not provided.

                The decorator must have all tags in order to match.

            Return {MethodDecorator}
            ----------------------
            The method decorator if it exists, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-10-2023 08:18:26
            `memberOf`: Method
            `version`: 1.0
            `method_name`: get_arg
            * @xxx [03-10-2023 08:19:36]: documentation for get_arg
        '''
        if name is not None:
            for arg in self._decorators:
                if arg.name.name == name:
                    return arg
        if tags is not None:
            tags = c.arr.force_list(tags,allow_nulls=False)
            if len(tags) > 0:
                for arg in self._decorators:
                    if arg.has_tag(tags):
                        return arg
        return None

    def has_decorator(self,name:str)->bool:
        '''
            Check if this method has a decorator with a matching name.
            ----------

            Arguments
            -------------------------
            `name` {str}
                The name to search for.

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-10-2023 10:47:53
            `memberOf`: Method
            `version`: 1.0
            `method_name`: has_decorator
            * @TODO []: documentation for has_decorator
        '''
        for d in self._decorators:
            if d.name.name == name:
                return True
        return False

    @property
    def decorators(self)->Iterable[_types._decorator_type]:
        '''
            Get the decorator property's value

            returns an empty list if the method has no decorators.

            `default`:[]


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-03-2023 12:05:57
            `@memberOf`: __init__
            `@property`: decorator
        '''
        value = self._decorators
        if self.is_getter is True and self.has_decorator("property") is False:
            self.add_decorator("property")
            # value.append("@property")
        if self.is_setter is True and self.has_decorator(f"{self.name.name}.setter") is False:
            self.add_decorator(f"{self.name.name}.setter")
            # value.append(f"@{self.name}.setter")


        return value





    @property
    def _body(self):
        '''
            Get this Method's _body

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 14:14:46
            `@memberOf`: Method
            `@property`: _body
        '''
        value = self.body
        if value is None:
            return "pass"
        return value

        return value

    def regen_imports(self):
        _=self._gen_return_type

    @property
    def _gen_return_type(self):
        '''
            Parse this methods return type to check if it uses any of the python typing classes.

            If it does, it will add the import to the module this method belongs to.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 15:54:20
            `@memberOf`: Method
            `@property`: _gen_return_type
        '''
        if self.return_type is None:
            return ast.Constant(value=None)

        value = ast.parse(self.return_type)
        # print(f"_gen_return_type:")
        # print(ast.dump(value,indent=4))
        value = value.body[0].value
        # if "[" not in self.return_type:
            # return value
        # print(f"\n\n_gen_return_type:")
        # print(ast.dump(value,indent=4))
        # print(f"========================================================================")

        typetype = config.contains_typing_type(value)
        if typetype is not False:
            # print(f"add typing import: {typetype} => {self.return_type}")
            self.module.add_import(import_path="typing",subjects=typetype,is_standard_library=True)
        return value

    @property
    def declaration_ast(self):
        '''
            Get this Method's ast

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 12:34:44
            `@memberOf`: Method
            `@property`: ast
        '''
        self.body = self._format_single_line_comments(self.body)
        # return_type = ast.parse(self.return_type) if self.return_type is not None else ast.Constant(value=None)
        value = ast.FunctionDef(
            name=self.name.name,
            args=ast.arguments(
                posonlyargs=[],
                args=[],
                kwonlyargs=[],
                kw_defaults=[],
                # TODO []: add **kwargs to method.
                kwarg=[],
                defaults=[]),
            body=[],
            decorator_list=[],
            returns=self._gen_return_type
        )
        # if self.return_type is not None:
        #     print(f"return_type: {self.return_type}")
        #     value.returns = ast.parse(self.return_type)
            # print(ast.dump(returns))

        if self.is_class_method:
            # @Mstep [] add the "self" argument to the method.
            value.args.args.insert(0,ast.arg(arg='self'))
            # @Mstep [] add the getter/setter decorators.
            # # TODO []: determine what to do with this now that there is a decorator class.
            # if self.is_getter:
            #     value.decorator_list.append(ast.Name(
            #         id='property',
            #         ctx=ast.Load()
            #         )
            #     )
            # if self.is_setter:
            #     attr = ast.Attribute(
            #                 value=ast.Name(
            #                     id=self.name.name,
            #                     ctx=ast.Load()
            #                 ),
            #                 attr='setter',
            #                 ctx=ast.Load()
            #             )
            #     value.decorator_list.append(attr)

        for d in self.decorators:
            value.decorator_list.append(d.declaration_ast)
        # _ = [value.decorator_list.append(x) for x in self.decorators]

        # print(f"self.arg_list: {len(self.arg_list)}")
        for arg in self.arg_list:
            value.args.args.append(arg.ast)
            if arg.default != "__NO_DEFAULT_VALUE_SET__":
                value.args.defaults.append(ast.Constant(value=arg.default))

        # @Mstep [IF] if there are keyword arguments
        if len(self.kwarg_list) > 0:
            # @Mstep [] add the keyword argument variable to the method.
            value.args.kwarg = ast.arg(arg='kwargs')

        # @Mstep [] apply the body.
        value.body.append(ast.parse(self._body))

        # @Mstep [] prepend the docblock to the method body.
        # self.Doc.subject_name = self.name.name
        # self.Doc.description = self.description
        self.Doc = _docblock.ClassMethodDocBlock(self)
        self.Doc.indent = self.indent + 4
        value.body.insert(0,ast.Expr(value=ast.Constant(value=self.Doc.result)))



        value = ast.fix_missing_locations(value)
        # value = self._reverse_format_single_line_comments(value)
        return value


# def populate_from_dict(data:dict,instance:Method):
#     for k,v in data.items():
#         if hasattr(instance,k):
#             setattr(instance,k,v)


