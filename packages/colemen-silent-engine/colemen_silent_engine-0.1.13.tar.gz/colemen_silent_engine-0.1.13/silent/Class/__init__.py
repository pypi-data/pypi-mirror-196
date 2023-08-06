# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import




import datetime
import ast
from dataclasses import dataclass
from string import Template
from typing import Iterable, Union

import colemen_utils as c
import silent.EntityBase as _eb


import silent.Class.Property as _prop
import silent.Method.Method as _method

import silent.se_config as config
import silent.settings.types as _types
import silent.Decorator.Decorator as _dec
log = c.con.log


@dataclass
class Class(_eb.EntityBase):

    # module:config._py_module_type = None
    # '''The module that this class belongs to'''

    _properties:Iterable[config._py_property_type] = None
    '''A dictionary of property instances associated to this class.'''


    _methods:Iterable[config._method_type] = None
    '''A dictionary of methods that belong to this class.'''

    _bases:Iterable[str] = None
    '''A list of classes that this class bases'''
    _classes:Iterable[_types._py_class_type] = None

    is_dataclass:bool = False
    '''True if this class is a dataclass'''

    # description:str = None
    # '''The description for this class's docblock'''

    _gen_init:bool = True
    '''If True, the init method is generated automatically.'''

    init_body:str = None
    '''The body to apply to the init method.'''

    gen_getter_setters:str = None
    '''If False, getters and setters will not be generated'''

    _type_name:str = None
    '''The type name of this class.'''

    _decorators:Iterable[_types._decorator_type] = None
    '''A list of decorator instances for this class.'''
    _parent_class:Iterable[_types._py_class_type] = None

    # _args = None
    # _kwargs = None

    def __init__(self,main:config._main_type,module:config._py_module_type,name:str=None,
                description:str=None,bases:Union[str,list]=None,init_body:str=None,
                is_dataclass:bool=False,tags:Union[str,list]=None,gen_init:bool=True,
                body:str=None,gen_getter_setters:bool=True,_p:_types._py_class_type=None
            ):
        '''
            Represents a python class

            Arguments
            ------------------
            `main` {Main}
                The project that this class belongs to.

            `module` {Module}
                The module instance that this class belongs to.

            [`name`=None] {str}
                The name of this class

            [`description`=None] {str}
                The docblock description of this class

            [`bases`=None] {str,list}
                The class or list of classes that this class will extend

            [`init_body`=None] {str}
                The body of the __init__ method.

            [`is_dataclass`=False] {bool}
                True if this class is a dataclass

            [`tags`=None] {list,str}
                A tag or list of tags to add after it is instantiated.

            [`gen_init`=True] {bool}
                if False, the class will not include an init method

            [`body`=None] {str}
                The content to apply to the body of the class.

                The value can be a literal string of content or a file path to the content


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-26-2022 08:35:16
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: Table
            * @xxx [12-26-2022 08:36:08]: documentation for Table
        '''
        kwargs= {}
        kwargs['main'] = main
        kwargs['module'] = module
        kwargs['name'] = name
        kwargs['description'] = description
        kwargs['init_body'] = init_body
        kwargs['is_dataclass'] = is_dataclass
        kwargs['gen_getter_setters'] = gen_getter_setters
        kwargs['_gen_init'] = gen_init
        kwargs['_parent_class'] = _p
        super().__init__(**kwargs)

        if isinstance(tags,(list,str)):
            self.add_tag(tags)
        # self.main:config._main_type = main

        self.bases = []
        self._properties = {}
        self._methods = {}
        self._decorators = []
        self._classes = {}

        if body is not None:
            self.append_to_body(body)

        if isinstance(bases,(list,str)):
            self.add_base(bases)

        if self.is_dataclass is True:
            self.module.add_import("dataclasses","dataclass",is_standard_library=True)


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
            "is_dataclass":self.is_dataclass,
            "properties":[],
            "methods":[],
            "tags":self._tags,
        }

        for prop in self.properties:
            value['properties'].append(prop.summary)
        for method in self.methods:
            value['methods'].append(method.summary)


        return value

    def add_base(self,class_name:str):
        '''
            Add a base class that this class will extend.

            ----------

            Arguments
            -------------------------
            `class_name` {str,list}
                The class or list of classes that this class will extend


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-09-2023 10:48:25
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_base
            * @xxx [01-09-2023 10:49:08]: documentation for add_base
        '''

        if isinstance(class_name,(str)):
            class_name = class_name.split(",")
        for base in class_name:
            self.bases.append(base)
        # self.bases.append(class_name)





    @property
    def type_name(self)->str:
        '''
            Get the type_name for this class.

            This is used for type hinting, it is just the classname with "_type" suffixed.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 16:09:19
            `@memberOf`: __init__
            `@property`: type_name
        '''
        if self._type_name is not None:
            return self._type_name
        # print(f"self.package.name.name: {self.package.name.name}")
        # print(f"self.name.name:{self.name.name}")
        value = f"_{self.package.name.name}_{self.name.name}_type"
        return value

    @type_name.setter
    def type_name(self,value):
        '''
            Set the type_name property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 16:25:50
            `@memberOf`: __init__
            `@property`: type_name
        '''
        self._type_name = value

    @property
    def private_type_name(self):
        '''
            Get the private_type_name property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-13-2023 15:02:55
            `@memberOf`: __init__
            `@property`: private_type_name
        '''
        value = f"_{self.type_name}"
        return value

    @property
    def type_declaration(self)->str:
        '''
            The typevar declaration for this class

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 16:06:58
            `@memberOf`: __init__
            `@property`: type_declaration
        '''
        rand = f"_{c.rand.rand(6,digits=False)}"
        value = f'''    import {self.import_path} as {rand}
    {self.type_name} = _TypeVar('{self.type_name}', bound={rand}.{self.name.name})'''
        return value





    # ---------------------------------------------------------------------------- #
    #                                    CLASSES                                   #
    # ---------------------------------------------------------------------------- #


    def add_class(self,name:str,description:str=None,init_body:str=None,is_dataclass:bool=False,
                bases:Union[str,list]=None,tags:Union[str,list]=None,gen_init:bool=True,body:str=None,
                gen_getter_setters:bool=True
                )->config._py_class_type:
        '''
            Create a class instance and associate it to this module.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the class

            `description` {str}
                The documentation description of the class

            [`init_body`=None] {str}
                The body of the __init__ method.

            [`is_dataclass`=False] {bool}
                True if the class should be a dataclass.

            [`bases`=None] {str,list}
                The class or list of classes that this class will extend

            [`tags`=None] {list,str}
                A tag or list of tags to add after it is instantiated.

            [`gen_init`=True] {bool}
                if False, the class will not include an init method

            [`body`=None] {str}
                The content to apply to the body of the class.

                The value can be a literal string of content or a file path to the content

            Return {Class}
            ----------------------
            The class instance

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-05-2023 11:30:17
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_class
            * @xxx [01-05-2023 11:36:41]: documentation for add_class
        '''
        nclass = Class(
            self.main,
            module=self.module,
            _p=self,
            name=name,
            description=description,
            init_body=init_body,
            is_dataclass=is_dataclass,
            tags=tags,
            bases=bases,
            gen_init=gen_init,
            body=body,
            gen_getter_setters=gen_getter_setters,
        )

        # if bases is not None:
        #     if isinstance(bases,(str)):
        #         bases = bases.split(",")
        #     for base in bases:
        #         nclass.add_base(base)
        self._classes[name] = nclass
        return nclass

    @property
    def classes(self)->Iterable[config._py_class_type]:
        '''
            Get a list of class instances associated to this module

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 10:49:39
            `@memberOf`: __init__
            `@property`: classes
        '''
        value:Iterable[config._py_class_type] = list(self._classes.values())
        return value

    def get_class(self,name:str=None,tags:Union[str,list]=None)->config._method_argument_type:
        '''
            Get an class from this module with a matching name or tags
            ----------

            Arguments
            -------------------------
            [`name`=None] {str}
                The name to search for.

            [`tags`=None] {str,list}
                A tag or list of tags to search for.
                This is only used if a name match is not found or name is not provided.

                The class must have all tags in order to match.

            Return {None,Class}
            ----------------------
            The class instance if it exists, None otherwise.

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
            for arg in self.classes:
                if arg.name.name == name:
                    return arg
        if tags is not None:
            tags = c.arr.force_list(tags,allow_nulls=False)
            if len(tags) > 0:
                for arg in self.classes:
                    if arg.has_tag(tags):
                        return arg
        return None



    # ---------------------------------------------------------------------------- #
    #                                  PROPERTIES                                  #
    # ---------------------------------------------------------------------------- #

    def add_property(self,name:str,description:str=None,data_type:str=None,default=None,
                    private:bool=False,tags:Union[str,list]=None,prop:config._py_property_type=True,
                    gen_getter:bool=True,gen_setter:bool=True,getter_body:str=None,setter_body:str=None
                    )->config._py_property_type:
        '''
            Add a property to this class
            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the property to add.

            `tags` {str,list}
                A list or string of tags to add the the property
                This can be a comma delimited list.

            [`data_type`=None] {str}
                The python data type stored in this property

            [`default`=None] {any}
                The default value to assign to this property

            [`description`=None] {str}
                The Docblock description for this property

            [`private`=False] {bool}
                True if this property is private to its class.

            [`gen_getter`=True] {bool}
                If False, this will NOT automatically generate the getter method for this property
                This overrides the gen_getter_setters option provided to the class

            [`gen_setter`=True] {bool}
                If False, this will automatically generate the setter method for this property
                This overrides the gen_getter_setters option provided to the class

            [`getter_body`=None] {str}
                The body of the getter method, the default will return the property.

            [`setter_body`=None] {str}
                The body of the setter method, the default will set the property.

            Return {Property}
            ----------------------
            The newly instantiated property.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 09:23:52
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_property
            * @xxx [01-04-2023 09:26:32]: documentation for add_property
        '''
        prop = _prop.Property(
            self.main,
            self,
            name = name,
            data_type = data_type,
            default = default,
            description = description,
            private = private,
            tags = tags,
        )

        o_gen = self.gen_getter_setters
        if gen_getter is True or gen_setter is True:
            # @Mstep [] temporarily override the gen_getters_setters property
            self.gen_getter_setters = True

        if private is True or self.is_dataclass is False and self.gen_getter_setters is True:
            if gen_getter:
                g = self.add_getter(name=prop.name.name,prop=prop)
                if getter_body is not None:
                    g.body = getter_body
            if gen_setter:
                s = self.add_setter(name=prop.name.name,prop=prop)
                if setter_body is not None:
                    s.body = setter_body
        self.gen_getter_setters = o_gen


        typetype = config.contains_typing_type(data_type)
        if typetype is not False:
            self.module.add_import(import_path="typing",subjects=typetype)

        self._properties[name] = prop

        return prop

    @property
    def properties(self)->Iterable[config._py_property_type]:
        '''
            Get a list of properties for this class.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 09:30:42
            `@memberOf`: __init__
            `@property`: properties
        '''
        value = list(self._properties.values())
        return value

    @property
    def property_names(self)->Iterable[str]:
        '''
            Get the property_names property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 07:37:35
            `@memberOf`: __init__
            `@property`: property_names
        '''
        value = [x.name.name for x in self.properties]
        return value

    @property
    def private_props(self)->Iterable[config._py_property_type]:
        '''
            Get the private properties for this class

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 09:28:10
            `@memberOf`: __init__
            `@property`: private_props
        '''
        value = []
        for prop in self.properties:
            if prop.is_private:
                value.append(prop)
        return value

    @property
    def _dataclass_properties(self)->Iterable[config._py_property_type]:
        '''
            Get a list of properties that are handled by the dataclass.

            These properties are assigned prior to the init method so that the dataclass will automatically handle
            the getters and setters.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 11:04:35
            `@memberOf`: __init__
            `@property`: _dataclass_properties
        '''
        if self.is_dataclass is False:
            return None
        value = []
        for prop in self.properties:
            value.append(prop)
        return value

    def get_property(self,name:str=None,tags:Union[str,list]=None)->_types._py_property_type:
        '''
            Get a property from this method with a matching name or tag
            ----------

            Arguments
            -------------------------
            [`name`=None] {str}
                The name to search for.

            [`tags`=None] {str,list}
                A tag or list of tags to search for.
                This is only used if a name match is not found or name is not provided.

                The property must have all tags in order to match.

            Return {MethodDecorator}
            ----------------------
            The method property if it exists, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-10-2023 08:18:26
            `memberOf`: Method
            `version`: 1.0
            `method_name`: get_arg
            * @xxx [03-10-2023 08:19:36]: documentation for get_property
        '''
        if name is not None:
            if name in self._properties:
                return self._properties[name]
            if f"_{name}" in self._properties:
                return self._properties[f"_{name}"]

            # for arg in self._decorators:
            #     if arg.name.name == name:
            #         return arg
        if tags is not None:
            tags = c.arr.force_list(tags,allow_nulls=False)
            if len(tags) > 0:
                prop:_types._py_property_type
                for _,prop in self._properties.items():
                    if prop.has_tag(tags):
                        return prop
        return None

    def get_properties_by_tag(self,tag,match_all=False):
        '''
            Get the get_properties_by_tag property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 17:04:31
            `@memberOf`: __init__
            `@property`: get_properties_by_tag
        '''
        if isinstance(tag,(str)):
            tag = tag.split(",")

        value = []
        tags = c.arr.force_list(tag)
        for prop in self.properties:
            if prop.has_tag(tags,match_all):
                value.append(prop)
        return value


    # ---------------------------------------------------------------------------- #
    #                                    METHODS                                   #
    # ---------------------------------------------------------------------------- #

    def add_method(self,name:str,description:str=None,body:str=None,return_type:str=None,return_description:str=None,
                tags:Union[list,str]=None,replacements:dict=None
            )->config._method_type:
        '''
            Add a method to this class.
            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the method.

            [`description`=None] {str}
                The docblock description for this method.

            [`body`="pass"] {str}
                The body of the method.

            [`return_type`=None] {str}
                The type returned by this method

            [`return_description`=None] {str}
                A description of the return value

            [`tags`=None] {list,str}
                A tag or list of tags to add after it is instantiated.

            [`replacements`=None] {dict}
                A dictionary of replacements to apply to the body template.


            Return {Method}
            ----------------------
            The new method instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 13:28:59
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_method
            * @xxx [01-09-2023 10:15:24]: documentation for add_method
        '''

        if body is not None and replacements is not None:
            if isinstance(body,Template) is False:
                if c.file.exists(body):
                    body = c.file.readr(body)
                if isinstance(body,(str)):
                    body = Template(body)

            body = body.substitute(**replacements)
        method = _method.Method(
            self.main,
            pyclass=self,
            package=self.package,
            name=name,
            description=description,
            body=body,
            return_type=return_type,
            return_description=return_description,
            is_class_method=True,
        )
        if isinstance(tags,(list,str)):
            method.add_tag(tags)

        self._methods[method.local_name] = method
        return method

    def add_getter(self,name:str,description:str=None,body:str=None,
                return_type:str=None,return_description:str=None,
                tags:Union[list,str]=None,prop:config._py_property_type=None
            )->config._method_type:
        '''
            Add a getter method to this class.
            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the method.

            [`description`=None] {str}
                The docblock description for this method.

            [`body`=None] {str}
                The body of the method.

            [`return_type`=None] {str}
                The type returned by this method

            [`return_description`=None] {str}
                A description of the return value

            [`tags`=None] {list,str}
                A tag or list of tags to add after it is instantiated.

            [`prop`=None] {Property}
                A reference to the property that is being retrieved.

            Return {Method}
            ----------------------
            The new method instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 13:28:59
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_method
            * @TODO []: documentation for add_method
        '''
        # @Mstep [IF] if the prop was not provided
        if prop is None:
            # @Mstep [] attempt to retrieve the property by name.
            prop = self.get_property(name)

        # @Mstep [IF] if a property was provided or exists on this class already.
        if prop is not None:
            # @Mstep [] override the other settings with the property settings.
            name = prop.name.name
            if description is None:
                description = f"Retrieve this {self.name.name}'s {prop.name.name} property value"
            description = f"{description}\n    {prop.description}"
            if return_type is None:
                return_type=prop.data_type
            if return_description is None:
                return_description=f"This {self.name.name}'s {name} property value."
            add_tags=["getter","method",self.module.name.name]
            if tags is None:
                tags = add_tags
            else:
                tags = tags + add_tags





        if body is None:
            body = f"return self.{name}"
            if prop.is_private:
                body = f"return self._{name}"

        # @Mstep [] instantiate the method.
        method = _method.Method(
            self.main,
            pyclass=self,
            package=self.package,
            name=name,
            description=description,
            body=body,
            return_type=return_type,
            return_description=return_description,
            tags=tags,
            prop=prop,
            is_getter=True,
            is_setter=False,
            is_class_method=True,
        )

        if prop is not None:
            prop.getter_method = method
            method.prop = prop


        # self.get_property(prop.name.name)
        self._methods[method.local_name] = method
        return method

    def add_setter(self,name:str,description:str=None,body:str=None,
                return_type:str=None,return_description:str=None,
                tags:Union[list,str]=None,prop:config._py_property_type=None
            )->config._method_type:
        '''
            Add a setter method to this class.
            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the method.

            [`description`=None] {str}
                The docblock description for this method.

            [`body`="pass"] {str}
                The body of the method.

            [`return_type`=None] {str}
                The type returned by this method

            [`return_description`=None] {str}
                A description of the return value

            [`tags`=None] {list,str}
                A tag or list of tags to add after it is instantiated.

            [`prop`=None] {Property}
                A reference to the property that is being retrieved.

            Return {Method}
            ----------------------
            The new method instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 13:28:59
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_method
            * @TODO []: documentation for add_method
        '''
        # @Mstep [IF] if the prop was not provided
        if prop is None:
            # @Mstep [] attempt to retrieve the property by name.
            prop = self.get_property(name)

        
        # @Mstep [IF] if a property was provided.
        if prop is not None:
            # @Mstep [] override the other settings with the property settings.
            name = prop.name.name
            description = f"Retrieve this {self.name.name}'s {prop.name.name} property value\n    {prop.description}"
            return_type=prop.data_type
            return_description=f"This {self.name.name}'s {name} property value."
            tags=["setter","method",self.module.name.name]

        if body is None:
            tmp_name = name
            if prop.is_private:
                tmp_name = f"_{name}"
            body = f"self.{tmp_name} = value\nreturn self.{tmp_name}"

        # @Mstep [] instantiate the method.
        method = _method.Method(
            self.main,
            pyclass=self,
            package=self.package,
            name=name,
            description=description,
            body=body,
            return_type=return_type,
            return_description=return_description,
            tags=tags,
            prop=prop,
            is_getter=False,
            is_setter=True,
            is_class_method=True,
        )
        if prop is not None:
            prop.setter_method = method
            method.prop = prop
            
        method.add_arg("value",description=f"The new {method.name.name} value",tags="arg,setter,method_argument")

        # self.get_property(prop.name.name)
        self._methods[method.local_name] = method
        return method

    def get_method(self,name:str,partial_match=False,is_getter:bool=False,is_setter:bool=False)->config._method_type:
        '''
            retrieve a method by its name

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the method to search for.

            [`partial_match`=True] {bool}
                If True, the method name must contain the searched name

            [`is_getter`=False] {bool}
                If True, this will only search for getter methods
                
            [`is_setter`=False] {bool}
                If True, this will only search for setter methods

            Return {Method}
            ----------------------
            The method instance, None if it is not found.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-06-2023 08:55:24
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: get_method
            * @xxx [01-06-2023 08:56:24]: documentation for get_method
        '''
        result = []
        
        if is_getter:
            get_loc_name = f"{name}____get"
            if get_loc_name in self._methods:
                return self._methods[get_loc_name]

        if is_setter:
            set_loc_name = f"{name}____set"
            if set_loc_name in self._methods:
                return self._methods[set_loc_name]
        
        
        if partial_match is False:
            if name in self._methods:
                return self._methods[name]

            get_loc_name = f"{name}____get"
            if get_loc_name in self._methods:
                return self._methods[get_loc_name]

            set_loc_name = f"{name}____set"
            if set_loc_name in self._methods:
                return self._methods[set_loc_name]
        else:
            for k,v in self._methods.items():
                if name in k:
                    return v

    def get_methods_by_tag(self,tag:Union[str,list],match_all:bool=False)->Iterable[config._method_type]:
        '''
            Retrieve all methods with matching tags
            ----------

            Arguments
            -------------------------
            `tag` {str,list}
                The tag or list of tags to search for.

            [`match_all`=False] {bool}
                If True, all tags provided must be found.

            Return {list}
            ----------------------
            A list of methods that contain the matching tags, an empty list if None are found.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-06-2023 10:02:34
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: get_methods_by_tag
            * @xxx [01-06-2023 10:04:42]: documentation for get_methods_by_tag
        '''
        value = []
        for mod in self.methods:
            if mod.has_tag(tag,match_all):
                value.append(mod)
        return value

    def get_getter_setter_by_prop(self,prop_name:str)->Iterable[config._method_type]:
        prop = self.get_property(prop_name)
        if prop is not None:
            return [prop.getter_method,prop.setter_method]
        else:
            c.con.log(f"Failed to locate property {prop_name} on class {self.name.name}","warning")

    @property
    def method_names(self)->Iterable[str]:
        '''
            Get a list of method names associated to this class.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 07:38:46
            `@memberOf`: __init__
            `@property`: method_names
        '''

        value = [x.name for x in self.methods]
        return value

    @property
    def methods(self)->Iterable[config._method_type]:
        '''
            Get a list of method instances associated to this class.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 13:37:45
            `@memberOf`: __init__
            `@property`: methods
        '''
        value = list(self._methods.values())
        return value


    @property
    def _gen_getter_setter_methods(self):
        value = []

        for prop in self.properties:
            res = self.get_getter_setter_by_prop(prop.name.name)
            
            if res[0] is not None:
                value.append(ast.unparse(res[0].declaration_ast))
            if res[1] is not None:
                value.append(ast.unparse(res[1].declaration_ast))
        return '\n'.join(value)

    @property
    def _gen_getter_methods(self):
        '''
            Get the _gen_getter_methods property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 13:33:41
            `@memberOf`: __init__
            `@property`: _gen_getter_methods
        '''
        value = []
        for method in self.methods:
            if method.is_getter:
                value.append(ast.unparse(method.declaration_ast))
        return '\n'.join(value)

    @property
    def _gen_setter_methods(self):
        '''
            Get the _gen_setter_methods property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 13:33:41
            `@memberOf`: __init__
            `@property`: _gen_setter_methods
        '''
        value = []
        for method in self.methods:
            if method.is_setter:
                value.append(ast.unparse(method.declaration_ast))
        return '\n'.join(value)

    @property
    def _gen_misc_methods(self):
        '''
            Get the _gen_setter_methods property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 13:33:41
            `@memberOf`: __init__
            `@property`: _gen_setter_methods
        '''
        value = []
        for method in self.methods:
            if method.name.name == "__init__":
                continue
            if method.is_setter is False and method.is_getter is False:
                func_def =method.declaration_ast
                if isinstance(func_def,(str)):
                    value.append(func_def)
                    continue
                # print(ast.dump(method.declaration_ast,indent=4))
                value.append(ast.unparse(method.declaration_ast))
        return '\n'.join(value)




    @property
    def gen_init(self)->config._method_type:
        '''
            Get the __init__ method for this class or create it.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 14:29:44
            `@memberOf`: __init__
            `@property`: gen_init
        '''

        value = self.get_method("__init__")
        if value is None:
            initsuper = "super().__init__()" if len(self.bases) else ""

            ib = self.init_body
            if ib is None:
                ib = "pass"
            if len(initsuper) > 0:
                if "super().__init__" not in ib:
                    ib = f"{initsuper}\n{ib}"
                    # @Mstep [IF] if the last line of the body is "pass"
                    if ib.split("\n")[-1] == "pass":
                        # @Mstep [] remove the last line from the body.
                        ib = '\n'.join(ib.split("\n")[:-1])

            value = self.add_method(
                "__init__",
                description=self.description,
                body=ib
            )
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
            for arg in self.decorators:
                if arg.name.name == name:
                    return arg
        if tags is not None:
            tags = c.arr.force_list(tags,allow_nulls=False)
            if len(tags) > 0:
                for arg in self.decorators:
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
        return value




    # @property
    # def _gen_bases(self):
    #     '''
    #         Generate a comma delimited list of classes that are extended by this class.

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 01-04-2023 09:37:05
    #         `@memberOf`: __init__
    #         `@property`: _gen_bases
    #     '''
    #     value = ""
    #     if len(self.bases) > 0:
    #         el = ','.join(self.bases)
    #         value = f"({el})"
    #     return value

    # ---------------------------------------------------------------------------- #
    #                                   __INIT__                                   #
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
        ):
        '''
            Add an argument to this class's init method.

            If the name matches a property it will be automatically assigned in the __init__ method.

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
            `created`: 01-04-2023 14:46:25
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_arg
            * @xxx [01-05-2023 07:47:58]: documentation for add_arg
        '''
        if self._gen_init is False:
            c.con.log(f"Adding an argument to the {self.name.name} class while _gen_init is False","warning")
            c.con.log("This will force the init method to be generated.","warning")
            self._gen_init = True

        value = self.gen_init
        return value.add_arg(name,data_type,default,description,arg,tags,prop)

    @property
    def arguments(self)->Iterable[config._method_argument_type]:
        '''
            Get the arguments property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 11:31:10
            `@memberOf`: __init__
            `@property`: arguments
        '''
        value = self.gen_init.arg_list
        return value

    def add_kwarg(self,name,**kwargs):
        '''
            Add a keyword argument to this class's init method.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the argument.


            Keyword Arguments
            -------------------------
            [`data_type`=None] {str}
                The expected type of the argument

            [`default_value`=None] {any}
                The default value to use if no value is provided.

            [`description`=None] {any}
                The documentation description


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 14:45:43
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_kwarg
            * @TODO []: documentation for add_kwarg
        '''
        value = self.gen_init
        value.add_kwarg(name,**kwargs)

    def _apply_init_arg_assignments(self):
        '''
            Add property assignments when the init method has an argument with name matching a class property.

            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-05-2023 07:46:39
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: _apply_init_arg_assignments
            * @xxx [01-05-2023 07:47:43]: documentation for _apply_init_arg_assignments
        '''
        init = self.gen_init
        for arg in init.arg_list:
            for prop in self.properties:
                if arg.name.name == prop.name.name:
                    arg = init.get_arg(prop.name.name)
                    if arg is None:
                        continue
                    arg.data_type = prop.data_type
                    arg.description = prop.description
                    arg.default = prop.default
                    # print(f"init.body:{init.body}")
                    assign = prop.assign_result(arg.name.name,True)
                    # assign = f"self.{prop.attribute_name}{prop.attribute_type} = {arg.name.name}"
                    if assign not in init.body:
                        # @Mstep [IF] if the last line of the body is "pass"
                        if init.body.split("\n")[-1] == "pass":
                            # @Mstep [] remove the last line from the body.
                            init.body = '\n'.join(init.body.split("\n")[:-1])
                        # @Mstep [] concatenate the property assignment with the init body.
                        init.body=f"{init.body}\n{assign}"


    def get_arg(self,name:str=None,tags:Union[str,list]=None)->config._method_argument_type:
        '''
            Get an init argument from this class with a matching name or tags
            ----------

            Arguments
            -------------------------
            [`name`=None] {str}
                The name to search for.

            [`tags`=None] {str,list}
                A tag or list of tags to search for.
                This is only used if a name match is not found or name is not provided.

                The argument must have all tags in order to match.

            Return {None,Argument}
            ----------------------
            The argument instance if it exists, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-10-2023 08:18:26
            `memberOf`: Method
            `version`: 1.0
            `method_name`: get_arg
            * @xxx [03-10-2023 08:19:36]: documentation for get_arg
        '''
        init = self.gen_init
        return init.get_arg(name,tags)



    @property
    def _gen_ast_bases(self):
        '''
            Get the _gen_ast_bases property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 11:57:15
            `@memberOf`: __init__
            `@property`: _gen_ast_bases
        '''
        bases = []
        for base in self.bases:
            bases.append(ast.Name(id=base,ctx=ast.Load()))
        return bases









    @property
    def ast(self):
        '''
            Get this class's ast object.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 11:40:02
            `@memberOf`: __init__
            `@property`: ast
        '''
        value = ast.ClassDef(
            name=self.name.name,
            bases=self._gen_ast_bases,
            keywords=[],
            body=[],
            decorator_list=[],
        )

        if self.body is not None:
            value.body.append(ast.parse(self.body))
        
        for cc in self.classes:
            value.body.append(cc.ast)

        for d in self.decorators:
            value.decorator_list.append(d.declaration_ast)

        if self.is_dataclass is True:
            # value.decorator_list.append(ast.Name(id='dataclass',ctx=ast.Load()))
            self.add_decorator("dataclass")

        # xxx [01-05-2023 15:06:43]: apply properties to body
        if self.is_dataclass:
            for prop in self.properties:
                past = prop.declaration_ast
                if isinstance(past,(list)):
                    value.body = value.body + past
                else:
                    value.body.append(past)
        elif self._gen_init is True:
            init = self.gen_init
            for prop in self.properties:
                if init.get_arg(prop.name.name) is not None:
                    continue

                assign = prop.assign_result(prop.default,True)
                if assign not in init.body:
                    # @Mstep [IF] if the last line of the body is "pass"
                    if init.body.split("\n")[-1] == "pass":
                        # @Mstep [] remove the last line from the body.
                        init.body = '\n'.join(init.body.split("\n")[:-1])
                    # @Mstep [] concatenate the property assignment with the init body.
                    init.body = f"{init.body}\n{assign}"

        if self._gen_init is True:
            self._apply_init_arg_assignments()
            # self.gen_init.Doc.description = self.description
            # self.gen_init.Doc.subject_name = self.name.name
            # xxx [01-05-2023 15:06:38]: apply init to body.
            value.body.append(self.gen_init.declaration_ast)

        # TODO []: apply methods to body
        # @Mstep [] add the custom getter methods
        if len(self._gen_getter_setter_methods) > 0:
            value.body.append(ast.parse(self._gen_getter_setter_methods))
        # value.body.append(ast.parse(self._gen_getter_methods))

        # @Mstep [] add the custom setter methods
        # value.body.append(ast.parse(self._gen_setter_methods))

        # @Mstep [] add additional methods to the body
        if len(self._gen_misc_methods) > 0:
            value.body.append(ast.parse(self._gen_misc_methods))



        if len(value.body) == 0:
            c.con.log(f"Creating a class {self.name.name} with no content, this will cause errors","warning")
            value.body.append(ast.Pass())


        value = ast.fix_missing_locations(value)
        return value


    @property
    def result(self)->str:
        '''
            Get this class's source code.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 11:42:40
            `@memberOf`: __init__
            `@property`: result
        '''
        # value = self.result
        value = ast.unparse(self.ast)
        value = self.apply_auto_replaces(value)
        return value


    @property
    def instantiate_call(self):
        '''
            Get the statement used to instantiate this class.


            ClassName(some,args)

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 12:04:15
            `@memberOf`: __init__
            `@property`: instantiate_call
        '''
        return ast.unparse(self.instantiate_call_ast)

    # def instantiate_call(self,args:str=None):
    #     value = f"{self.name.name}({args})"
    #     value = ast.parse(value)
    #     return value

    @property
    def instantiate_call_ast(self):
        '''
            Get the instantiate_call_ast property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 12:04:15
            `@memberOf`: __init__
            `@property`: instantiate_call_ast
        '''

        args = ','.join([x.name.name for x in self.arguments])

        value = f"{self.name.name}({args})"
        value = ast.parse(value)
        return value
