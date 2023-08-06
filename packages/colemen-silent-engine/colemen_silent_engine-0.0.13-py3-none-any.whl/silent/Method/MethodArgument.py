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
log = c.con.log


@dataclass
class MethodArgument(_eb.EntityBase):


    arg:config._method_argument_type = None
    '''A reference to another method argument to copy data from.'''
    prop:config._py_property_type = None
    '''A reference to a property to copy data from.'''
    
    data_type:str = None
    '''The expected python type for this argument'''

    default = "__NO_DEFAULT_VALUE_SET__"
    '''The default value to assign if the argument is not provided.'''




    def __init__(self,main:config._main_type,method:config._method_type,name:str,data_type:str=None,
                default="__NO_DEFAULT_PROVIDED__",description:str="",arg:config._method_argument_type=None,
                pyclass:config._py_class_type=None,tags:Union[str,list]=None,prop:config._py_property_type=None
        ):
        '''
            A class used to represent an argument passed to a Method.

            ----------


            Arguments
            -------------------------
            `main` {_main_type}
                A reference to the master

            `method` {Method}
                A reference to the Method this argument belongs to.


            `name` {str}
                The name of this method.

            [`data_type`=None] {str}
                The expected type of the argument

            [`description`=None] {str}
                The docblock description for this method.

            [`default`=None] {str}
                The default value for this argument

            [`arg`=None] {Method_Argument}
                A method argument instance to copy.
                This is useful when you want to add the same argument to another method.

            [`pyclass`=None] {Class}
                A reference to the class that this method belongs to.

            [`prop`=None] {Property}
                A property instance to use as an argument.

            [`tags`=None] {list,str}
                A tag or list of tags to apply to this method argument

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
        kwargs['method'] = method
        kwargs['name'] = name
        kwargs['data_type'] = data_type
        kwargs['default'] = default
        kwargs['description'] = description
        kwargs['arg'] = arg
        kwargs['prop'] = prop
        kwargs['pyclass'] = pyclass

        if default in ["__NO_DEFAULT_PROVIDED__","__NO_DEFAULT_VALUE_SET__"]:
            del kwargs['default']

        super().__init__(**kwargs)

        if arg is not None:
            self.name = arg.name.name
            self.data_type = arg.data_type
            self.default = arg.default
            self.description = arg.description


        tags = c.arr.force_list(tags,allow_nulls=False)
        if isinstance(tags,(str,list)):
            self.add_tag(tags)
        # self.main:config._main_type = main
        
        # if self.prop is not None:
        #     prop = self.prop
        #     self.name = prop.name.name
        #     self.description = prop.description
        #     self.data_type = prop.data_type
        #     self.default = prop.default

        # self.class_method:config._method_type = class_method

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
            "default":self.default,
        }
        return value

    @property
    def has_default(self):
        '''
            Get this MethodArgument's has_default

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-03-2023 12:22:13
            `@memberOf`: MethodArgument
            `@property`: has_default
        '''
        value = False
        if self.default not in ["__NO_DEFAULT_VALUE_SET__","__NO_DEFAULT_PROVIDED__"]:
            value = True
        return value

    # @property
    # def _data_type(self):
    #     '''
    #         Get this MethodArgument's _data_type

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 01-03-2023 12:09:51
    #         `@memberOf`: MethodArgument
    #         `@property`: _data_type
    #     '''
    #     value =""
    #     if self.data_type is not None:
    #         value = f":{self.data_type}"
    #     return value

    # @property
    # def _default_value(self):
    #     '''
    #         Get this MethodArgument's _default_value

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 01-03-2023 12:11:30
    #         `@memberOf`: MethodArgument
    #         `@property`: _default_value
    #     '''
    #     value = ""
    #     if self.default != "__NO_DEFAULT_VALUE_SET__":
    #         value = f"={self.default}"
    #     return value

    @property
    def name_type(self):
        '''
            Get this MethodArgument's name and type as a string
            
            arg:str

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 12:09:57
            `@memberOf`: MethodArgument
            `@property`: name_type
        '''
        value = f"{self.name.name}"
        if self.data_type is not None:
            value = f"{value}:{self.data_type}"
        if self.default not in ["__NO_DEFAULT_PROVIDED__","__NO_DEFAULT_VALUE_SET__"]:
            value = f"{value}={self.default}"
        return value

    @property
    def _gen_data_type(self):
        '''
            Parse this arguments data type to check if it uses any of the python typing classes.

            If it does, it will add the import to the module this method belongs to.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 15:54:20
            `@memberOf`: Method
            `@property`: _gen_data_type
        '''
        if self.data_type is None:
            return ast.Constant(value=None)

        value = ast.parse(self.data_type)
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
            self.module.add_import(import_path="typing",subjects=typetype,is_standard_library=True)
        return value



    @property
    def ast(self)->ast.arg:
        '''
            Get this MethodArgument's ast

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 12:46:57
            `@memberOf`: MethodArgument
            `@property`: ast
        '''
        if self.prop is not None:
            prop = self.prop
            self.name = prop.name.name
            self.description = prop.description
            self.data_type = prop.data_type
            
            self.default = prop.default
    
        if self.arg is not None:
            # import silent.Method.MethodArgument as _ma
            if isinstance(self.arg,MethodArgument):
                arg = self.arg
                self.name = arg.name.name
                self.description = arg.description
                self.data_type = arg.data_type
        
        value = ast.arg(
            arg=self.name.name,
        )
        value.annotation = self._gen_data_type


        # if self.default != "__NO_DEFAULT_VALUE_SET__":
        #     value.defaults = [
        #         ast.Constant(value=self.default)
        #     ]
        # if self.data_type is not None:
        #     types = self.data_type.split(".")
        #     if len(types) == 1:
        #         value.annotation = ast.Name(id=types[0], ctx=ast.Load())

        #     if len(types) == 2:
        #         value.annotation=ast.Attribute(
        #             value=ast.Name(id=types[0], ctx=ast.Load()),
        #             attr=types[1],
        #             ctx=ast.Load()
        #         )
        #     if len(types) > 2:
        #         ann = ast.Attribute(
        #             value=ast.Name(id=types[0], ctx=ast.Load()),
        #             attr=types[1],
        #             ctx=ast.Load()
        #         )
        #         # @Mstep [] remove the first and second element.
        #         types = types[2:]
        #         # @Mstep [] reverse the list.
        #         # types.reverse()

        #         # if isinstance(types,(list)):
        #         # atypes = []
        #         for typ in types:
        #             ann=ast.Attribute(
        #                 value=ann,
        #                 attr=typ,
        #                 ctx=ast.Load()
        #             )

        #         value.annotation = ann

        return value

    # @property
    # def result(self):
    #     '''
    #         Get the result property's value

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 12-28-2022 16:49:44
    #         `@memberOf`: __init__
    #         `@property`: result
    #     '''
    #     return f"{self.name}{self._data_type}{self._default_value}"

