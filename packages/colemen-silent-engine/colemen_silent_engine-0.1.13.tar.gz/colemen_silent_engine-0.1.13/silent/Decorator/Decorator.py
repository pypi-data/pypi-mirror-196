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
import silent.Decorator.DecoratorArgument as _da
# from config import column_type,_relationship_type,endpointdoc_type,route_type,root_directory,susurrus_type
import silent.settings.types as _types
import silent.se_config as config
log = c.con.log


@dataclass
class Decorator(_eb.EntityBase):
    method:config._method_type = None
    _args:Iterable[_types._decorator_argument_type] = None
    _kwargs:Iterable[_types._decorator_argument_type] = None


    def __init__(
        self,
        main:_types._main_type,
        name:str,
        method:_types._method_type=None,
        pyclass:_types._py_class_type=None,
        tags:Union[str,list]=None
        ):
        '''
            Class used to generate a python decorator.
            ----------

            Arguments
            -------------------------
            `main` {_main_type}
                A reference to the master

            [`method`=None] {_method_type}
                A reference to the method that this decorator applies to.

            [`pyclass`=None] {_method_type}
                A reference to the class that this decorator applies to.

            `name` {str}
                The name of this method.


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
        kwargs['pyclass'] = pyclass
        kwargs['method'] = method
        kwargs['name'] = name
        kwargs['tags'] = tags


        super().__init__(**kwargs)
        # _=self.declaration_ast


        if isinstance(tags,(list,str)):
            self.add_tag(tags)
        # self.main:config._main_type = main
        # self.pyclass:config._py_class_type = pyclass
        self.Doc = None
        self._args = []
        self._kwargs = []
        # self.Doc = _docblock.ClassMethodDocBlock(self)


        # self.body = self._format_single_line_comments(self.body)

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
            # "is_class_method":self.is_class_method,
            # "return_description":self.return_description,
            # "return_type":self.return_type,
            # "is_getter":self.is_getter,
            # "is_setter":self.is_setter,
            "arguments":[],
            "keyword_arguments":[],
            "import_statement":self.import_statement,
        }
        # for arg in self.arg_list:
        #     value['arguments'].append(arg.summary)


        return value

    # ---------------------------------------------------------------------------- #
    #                                   ARGUMENTS                                  #
    # ---------------------------------------------------------------------------- #



    def add_arg(self,name:str=None,value="__NO_VALUE_PROVIDED__",tags:Union[str,list]=None)->_types._decorator_argument_type:
        '''
            Add an argument to this decorator.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the argument.

            [`value`=__NO_VALUE_PROVIDED__] {any}
                The value to assign to this argument.

            [`tags`=None] {list,str}
                The tags to apply to this decorator argument

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
            c.con.log(f"Duplicate Argument provided for decorator {self.name.name} : {name}","warning")
            return False


        ma = _da.DecoratorArgument(
            main=self.main,
            decorator=self,
            name=name,
            value = value,
            tags = tags,
        )
        self._args.append(ma)

        return ma


    def get_arg(self,name:str=None,tags:Union[str,list]=None)->_types._decorator_argument_type:
        '''
            Get an argument from this decorator with a matching name
            ----------

            Arguments
            -------------------------
            [`name`=None] {str}
                The name to search for.
            [`tags`=None] {str,list}
                A tag or list of tags to search for.
                This is only used if a name match is not found or name is not provided.

                The argument must have all tags in order to match.

            Return {decoratorArgument}
            ----------------------
            The decorator argument if it exists, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-10-2023 08:18:26
            `memberOf`: Decorator
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
    def arg_list(self)->Iterable[_types._decorator_argument_type]:
        '''
            Get a list of decorator argument instances

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





    # ---------------------------------------------------------------------------- #
    #                                CODE GENERATION                               #
    # ---------------------------------------------------------------------------- #

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
        # value = ast.Call()
        value = _parse_dec_name_ast(self.name.name,self.arg_list)
        dic_val = value.__dict__
        print(f"dic_val:{dic_val}")


        value = ast.fix_missing_locations(value)
        # value = self._reverse_format_single_line_comments(value)
        return value


def _parse_dec_name_ast(name,args:Iterable[_types._decorator_argument_type]):
    '''
        This is hacky as shit but it works consistently.
        string => ast
        
        Essentially we take the name, concatenate it to a dummy function
        then use ast to parse the entire thing, and return the decorator.
        
        This simplifies a lot of potentially weird scenarios.
        ----------

        Return {type}
        ----------------------
        returns the ast of the decorator.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-10-2023 09:43:34
        `memberOf`: Decorator
        `version`: 1.0
        `method_name`: _parse_dec_name_ast
        * @xxx [03-10-2023 09:45:31]: documentation for _parse_dec_name_ast
    '''
    ar = []
    if len(args) > 0:
        ar = [x.string_value for x in args]

    print(f"ar:{ar}")
    argstring = ','.join(ar)
    
    name = c.string.strip(name,"@")
    if len(ar) == 0:
        name = f"@{name}\ndef hey():\n    pass"
    else:
        name = f"@{name}({argstring})\ndef hey():\n    pass"

    tree = ast.parse(name,'<string>','exec')
    for e in tree.body:
        a = e.__dict__
        # print(f"a: {a}")
        dl = a['decorator_list']
        # print(dl)
        return dl[0]


