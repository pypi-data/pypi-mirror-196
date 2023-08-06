# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import




from dataclasses import dataclass
from string import Template
from typing import Iterable, Union
import datetime
import ast

import colemen_utils as c
import silent.EntityBase as _eb

# import agod.TypeDeclaration as _type_dec
# from config import column_type,_relationship_type,endpointdoc_type,route_type,root_directory,susurrus_type
import silent.se_config as config
import silent.settings.types as _types
log = c.con.log


@dataclass
class DecoratorArgument(_eb.EntityBase):



    decorator:_types._decorator_type = None
    '''A reference to the decorator that this argument belongs to.'''

    value = "__NO_VALUE_PROVIDED__"
    '''The value to assign to this decorator argument'''

    def __init__(self,main:_types._main_type,decorator:_types._decorator_type,name:str,
                value="__NO_VALUE_PROVIDED__",tags:Union[str,list]=None):
        '''
            A class used to represent an argument passed to a decorator.

            ----------


            Arguments
            -------------------------
            `main` {_main_type}
                A reference to the master

            `decorator` {Decorator}
                A reference to the Decorator this argument belongs to.

            `name` {str}
                The name of the argument.

            [`value`=None] {any}
                The value to assign to this argument.

            [`tags`=None] {list,str}
                The tags to apply to this decorator argument

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
        kwargs['decorator'] = decorator
        kwargs['name'] = name
        kwargs['value'] = value


        super().__init__(**kwargs)

        if isinstance(tags,(str,list)):
            self.add_tag(tags)

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
            "value":self.value
        }
        return value

    @property
    def is_keyword(self)->bool:
        '''
            Get this DecoratorArgument's is_keyword

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-10-2023 10:05:48
            `@memberOf`: DecoratorArgument
            `@property`: is_keyword
        '''
        
        if self.value is not "__NO_VALUE_PROVIDED__":
            return True
        return False

    @property
    def string_value(self):
        '''
            Get this DecoratorArgument's string_value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-10-2023 10:28:13
            `@memberOf`: DecoratorArgument
            `@property`: string_value
        '''
        return ast.unparse(self.ast)

    @property
    def ast(self)->ast.arg:
        '''
            Get this DecoratorArgument's ast

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 12:46:57
            `@memberOf`: DecoratorArgument
            `@property`: ast
        '''
        
        return _parse_arg(self.name.name,self.value)




def _parse_arg(key,value):

    if value == "__NO_VALUE_PROVIDED__":
        # print(f"_parse_arg_parse_arg_parse_arg_parse_arg_parse_arg_parse_arg")
        at = f"@a({key})\ndef hey():\n    pass"
        tree = ast.parse(at,'<string>','exec')
        for e in tree.body:
            a = e.__dict__
            dl = a['decorator_list'][0]
            args = dl.__dict__['args']
            return args[0]
    else:
        at = f"@a({key}={value})\ndef hey():\n    pass"
        tree = ast.parse(at,'<string>','exec')
        for e in tree.body:
            a = e.__dict__
            dl = a['decorator_list'][0]
            keywords = dl.__dict__['keywords']
            # keywords = dl.__dict__['keywords']
            # print(f"dl['keywords']:{dl}")
            # keywords = dl['keywords']
            return keywords[0]

    
    





