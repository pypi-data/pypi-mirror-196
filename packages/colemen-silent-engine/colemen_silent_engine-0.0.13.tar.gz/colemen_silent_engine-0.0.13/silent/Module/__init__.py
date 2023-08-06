# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

'''
    A module containing the Module class declaration

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 01-06-2023 11:03:46
    `memberOf`: __init__
    `version`: 1.0
    `method_name`: Module
    * @TODO []: documentation for Module
'''


import datetime
from dataclasses import dataclass
import ast
import re
from string import Template
import traceback
from typing import Iterable, Union

import colemen_utils as c

import silent.EntityBase as _eb

# import silent.Import.ImportStatement as _imp
from silent.Import import ImportStatement as _imp
from silent.DocBlock import ModuleDocBlock as _doc

import silent.Class as _class


import silent.se_config as config
import silent.settings.types as _types
log = c.con.log
import silent.Method.Method as _method


@dataclass
class Module(_eb.EntityBase):


    _methods:Iterable[config._method_type] = None
    '''A list of methods contained in the module'''

    _classes:Iterable[config._py_class_type] = None
    '''A dictionary of classes contained in this module'''

    _imports:Iterable[config._py_import_type] = None
    '''A list of import statement instances.'''

    # body:str= None
    # '''The user defined content to append to the body of the module'''

    methods:Iterable[config._method_type] = None

    _document_prepends:str = None
    '''The content to prepend before the module docblock'''

    def __init__(self,main:config._main_type,package:config._package_type,name:str,description:str,
                overwrite:bool=True,tags:Union[str,list]=None
        ):
        '''
            Represents a python module.

            ----------

            Arguments
            -------------------------

            `main` {Main}
                A reference to the project instance.

            `package` {Package}
                A reference to the package this module belongs to.

            `name` {str}
                The name of this module.

            `description` {str}
                The documentation description of this module

            [`overwrite`=True] {bool}
                If False, this file will not save over an already existing version.

            [`tags`=None] {list,str}
                A tag or list of tags to add after it is instantiated.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-26-2022 08:35:16
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: Table
            * @xxx [12-26-2022 08:36:08]: documentation for Table
        '''
        kwargs={}
        kwargs['main'] = main
        kwargs['package'] = package
        kwargs['name'] = name
        kwargs['description'] = description
        kwargs['overwrite'] = overwrite
        super().__init__(**kwargs)
        

        if isinstance(tags,(str,list)):
            self.add_tag(tags)

        self._classes = {}
        self._methods = []
        self._properties = {}
        self._imports = []
        self.Doc = _doc.ModuleDocBlock(self.main,self)




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
            "imports":[],
            "classes":[],
            "methods":[],
            # "schema":self.table.database.database,
        }
        # value['imports'] = []
        for imp in self._imports:
            value['imports'].append(imp.summary)
        for cl in self.classes:
            value['classes'].append(cl.summary)
        for method in self.methods:
            value['methods'].append(method.summary)
        return value

    def save(self):
        path = self.file_path
        if c.file.exists(path):
            if self.overwrite is True:
                c.file.write(path,self.result)
        else:
            c.file.write(path,self.result)
        # c.file.write(self.file_path,self.result)


    # ---------------------------------------------------------------------------- #
    #                                    IMPORTS                                   #
    # ---------------------------------------------------------------------------- #


    def add_import(self,import_path:str=None,subjects:Union[list,str]=None,alias:str=None,is_standard_library:bool=False,is_third_party:bool=False)->config._py_import_type:
        '''
            Add an import statement to this module.

            ----------

            Arguments
            -------------------------

            [`import_path`=None] {str}
                The import path where the imported value is located.

            [`subjects`=None] {list,str}
                The subject or list of subjects to import

            [`alias`=None] {str}
                The alias to use for this import

            [`is_standard_library`=False] {bool}
                True if this import is from the python standard library.

            [`is_third_party`=False] {bool}
                True if this is importing from a third party library.



            Return {Import}
            ----------------------
            The new import statement instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 10:19:47
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_import
            * @TODO []: documentation for add_import
        '''
        # imp = None
        if import_path is not None:
            imp = self.get_import(import_path=import_path)
            if imp is not None:
                imp.add_subject(subjects)
                return imp
        # print(f"add import: {subjects}")
        i = _imp(
            main=self.main,
            package=self.package,
            module=self,
            import_path=import_path,
            alias=alias,
            is_standard_library=is_standard_library,
            is_third_party=is_third_party,
        )
        i.add_subject(subjects)
        self._imports.append(i)
        return i

    @property
    def standard_library_imports(self)->Iterable[config._py_import_type]:
        '''
            Get the standard_library_imports property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 10:26:05
            `@memberOf`: __init__
            `@property`: standard_library_imports
        '''
        std_imports = []
        for imp in self._imports:
            # print(f"import:{imp.subjects}")
            if imp.is_standard_library:
                std_imports.append(imp)
        return std_imports

    @property
    def third_party_imports(self)->Iterable[config._py_import_type]:
        '''
            Get a list of third party import statement instances associated to this module.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 10:26:05
            `@memberOf`: __init__
            `@property`: thrd_party_imports
        '''
        std_imports = []
        for imp in self._imports:
            if imp.is_third_party:
                std_imports.append(imp)
        return std_imports

    @property
    def local_imports(self)->Iterable[config._py_import_type]:
        '''
            Get the local_imports property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 10:26:05
            `@memberOf`: __init__
            `@property`: local_imports
        '''
        std_imports = []
        for imp in self._imports:
            if imp.is_standard_library is False and imp.is_third_party is False:
                std_imports.append(imp)
        return std_imports

    @property
    def _import_statements(self):
        '''
            Get the _import_statements property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 10:21:03
            `@memberOf`: __init__
            `@property`: _import_statements
        '''
        std_imports = '\n'.join(list([x.result for x in self.standard_library_imports]))
        thrd_imports = '\n'.join(list([x.result for x in self.third_party_imports]))
        local_imports = '\n'.join(list([x.result for x in self.local_imports]))

        value = f"{std_imports}\n{thrd_imports}\n{local_imports}"
        return value

    def get_import(self,subject_name:str=None,import_path:str=None):
        # imports = []
        for im in self._imports:
            if subject_name is not None:
                if subject_name in c.arr.force_list(im.subjects):
                    return im
            if import_path in c.arr.force_list(im.import_path):
                return im



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
        nclass = _class.Class(
            self.main,
            module=self,
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
    #                                    METHODS                                   #
    # ---------------------------------------------------------------------------- #


    def add_method(self,name:str,description:str=None,body:str=None,return_type:str=None,return_description:str=None,
                tags:Union[list,str]=None)->config._method_type:
        '''
            Add a method to this module.

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

            Return {Method}
            ----------------------
            The new method instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 13:28:59
            `memberOf`: Module
            `version`: 1.0
            `method_name`: add_method
            * @xxx [01-06-2023 10:33:45]: documentation for add_method
        '''
        # kwargs['name'] = name
        method = _method.Method(
            self.main,
            module=self,
            package=self.package,
            name=name,
            description=description,
            body=body,
            return_type=return_type,
            return_description=return_description,
            tags=tags,
            is_getter=False,
            is_setter=False,
            is_class_method=False,
        )

        self._methods.append(method)
        return method


    @property
    def methods(self)->Iterable[config._method_type]:
        '''
            Get a list of methods that belong to this module.

            This does NOT include class methods only globally available methods.

            `default`:[]


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 11:24:35
            `@memberOf`: __init__
            `@property`: methods
        '''
        return self._methods

    def get_method(
        self,
        name:Union[str,list]=None,
        tags:Union[str,list]=None,
        )->_types._method_type:
        '''
            Retrieve a method from this module.
            ----------

            Arguments
            -------------------------
            [`name`=None] {str,list}
                The name or list of names to search for.

            [`tags`=None] {str,list}
                The tag or list of tags to search for.


            Return {None,method}
            ----------------------
            The first method with a matching name or tag.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-10-2023 08:41:16
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: get_method
            * @xxx [03-10-2023 08:45:35]: documentation for get_method
        '''

        if name is not None:
            names = c.arr.force_list(name,allow_nulls=False)
            for mthd in self._methods:
                if mthd.name.name in names:
                    return mthd

        if tags is not None:
            tags = c.arr.force_list(tags,allow_nulls=False)
            for mthd in self._methods:
                if mthd.has_tag(tags):
                    return mthd
        return None

    def get_methods(
        self,
        name:Union[str,list]=None,
        tags:Union[str,list]=None,
        )->Iterable[_types._method_type]:
        '''
            Retrieve a list of methods from this module.
            ----------

            Arguments
            -------------------------
            [`name`=None] {str,list}
                The name or list of names to search for.

            [`tags`=None] {str,list}
                The tag or list of tags to search for.


            Return {None,list}
            ----------------------
            A list of methods with a matching name or tag.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-10-2023 08:41:16
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: get_methods
            * @xxx [03-10-2023 08:45:35]: documentation for get_methods
        '''
        value = []
        if name is not None:
            names = c.arr.force_list(name,allow_nulls=False)
            for mthd in self._methods:
                if mthd.name.name in names:
                    value.append(mthd)

        if tags is not None:
            tags = c.arr.force_list(tags,allow_nulls=False)
            for mthd in self._methods:
                if mthd.has_tag(tags):
                    value.append(mthd)
                    
        if len(value) == 0:
            value = None
        return value







    def prepend_to_document(self,value,template_replace:dict=None):
        '''
            Prepend content to the module document.
            
            This is where you can add linter ignore comments
            
            ----------

            Arguments
            -------------------------
            `value` {str}
                The value can be a literal string of content or a file path to the content
            [`template_replace`=None] {dict}
                A dictionary, any string matching a key in this dicionary is replaced with the value.
                The string.Template engine is used for this templating.

            Return {str}
            ----------------------
            The new body value.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-13-2023 12:29:30
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: append_to_body
            * @TODO []: documentation for append_to_body
        '''
        value = _doc_pend_prep(self,value,template_replace)
        # value = self._format_single_line_comments(value)
        # if value.startswith("#"):
            # value = f"'''__SINGLE_LINE_COMMENT__{value}'''"
        self._document_prepends = self._document_prepends + value

    @property
    def document_prepends(self):
        '''
            Get the document_prepends property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-14-2023 09:24:52
            `@memberOf`: __init__
            `@property`: document_prepends
        '''
        value = self._document_prepends
        if value is None:
            value = ""
        else:
            value = value + "\n"
        return value




    # ---------------------------------------------------------------------------- #
    #                                  GENERATION                                  #
    # ---------------------------------------------------------------------------- #

    @property
    def ast(self)->ast.Module:
        '''
            Get this modules ast object.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 11:03:02
            `@memberOf`: __init__
            `@property`: ast
        '''
        value = ast.Module(body=[],type_ignores=[])

        # value.body.append(ast.parse(self.document_prepends))
        value.body.append(ast.parse(self._import_statements))
        # for imp in self._imports:
            # print(f"imp.result:{imp.result}")
            # value.body.append(ast.parse(self._import_statements))
            # value.body.append(imp.ast)

        # if self._body is not None:
        #     value.body.append(ast.parse())

        # TODO []: apply global variables to body
        # xxx [01-06-2023 11:29:06]: apply classes to body
        for cl in self.classes:
            value.body.append(cl.ast)

        # xxx [01-06-2023 11:29:03]: apply functions to body
        for method in self.methods:
            value.body.append(method.declaration_ast)


        # @Mstep [] apply the module docblock to the body.
        value.body.insert(0,ast.Expr(value=ast.Constant(value=self.Doc.result)))
        # value.body.insert(1,ast.parse(self.document_prepends))
        value = ast.fix_missing_locations(value)
        return value

    @property
    def result(self):
        '''
            Get the result property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 11:49:00
            `@memberOf`: __init__
            `@property`: result
        '''
        try:
            value = ast.unparse(self.ast)
        except TypeError as e:
            # print(ast.dump(self.ast,indent=4))
            # traceback.print_stack()
            c.con.log(ast.dump(self.ast,indent=4),"error")
            c.con.log(e,"error")

        if self.body is not None:
            value = f"{value}\n{self.body}"
        if isinstance(self.document_prepends,(str)):
            value = f"{self.document_prepends}\n{value}"
        value = self.apply_auto_replaces(value)
        value = self._reverse_format_single_line_comments(value)
        return value





def _doc_pend_prep(ent,value,template_replace:dict=None):
    if isinstance(value,(str)):
        if c.file.exists(value):
            value = c.file.readr(value)
    if isinstance(value,ast.AST):
        value = ast.unparse(value)
    if ent._document_prepends is None:
        ent._document_prepends = ""
        
        
    if isinstance(value,(str)):
        if isinstance(template_replace,(dict)):
            s = Template(value)
            s.substitute(**template_replace)
    return value
