# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
# pylint: disable=import-outside-toplevel




import datetime
from dataclasses import dataclass
import ast
from re import L
import re
from string import Template
from typing import Iterable, Union

import colemen_utils as c


# from silent.Import import ImportStatement as _imp
import silent.Import as _imp
# import silent.Module as _module


import silent.se_config as config
log = c.con.log


@dataclass
class EntityBase:

    main:config._main_type = None
    '''A reference to the project instance.'''

    package:config._package_type = None
    '''The package that this entity belongs to.'''

    module:config._py_module_type = None
    '''The module that this entity belongs to.'''

    pyclass:config._py_class_type = None
    '''The class that this entity belongs to.'''

    method:config._method_type = None
    '''The class that this entity belongs to.'''

    _name:c.string.Name = None
    '''The name of this entity'''

    description:str = None
    '''The documentation description of this entity.'''

    _file_name:str = None
    '''The name of the file this entity resides in.'''
    _file_path:str = None
    '''The path to where this entity is saved.'''

    _tags:Iterable[str] = None
    _data = None
    _auto_replace={}
    _body:str= None
    '''The user defined content to append to the entity's generated body'''

    overwrite:bool = True
    '''If True, this entity will overwrite an existing one when saved.'''


    def __init__(self,**kwargs):
        '''
            The base class used for all instances

            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-26-2022 08:35:16
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: Table
            * @xxx [12-26-2022 08:36:08]: documentation for Table
        '''

        self._tags = []
        self._data = {}
        '''A dictionary of user defined data to store in the entity.'''

        populate_from_dict(kwargs,self)
        if self.package is None and self.module is not None:
            self.package = self.module.package

        if self.main is not None:
            self.main.register(self)


        from silent.Method import Method
        if isinstance(self,Method.Method):
            if self.pyclass is not None:
                self.module = self.pyclass.module
            if self.module is not None:
                self.package = self.module.package

        from silent.Method.MethodArgument import MethodArgument
        if isinstance(self,MethodArgument):
            self.module = self.method.module
        #     if self.module is None and self.method is not None:
        #         self.module = self


    def set_key(self,key,value=None):
        '''
            Set a data key on this entity.

            ----------

            Arguments
            -------------------------
            `key` {str,dict}
                The key to set. If this is a dictionary all key/values will be added.

            [`value`=None] {any}
                The value to assign to the key.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-09-2023 09:13:42
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: set_key
            * @xxx [01-09-2023 09:15:02]: documentation for set_key
        '''
        if isinstance(key,(dict)):
            for k,v in key.items():
                self._data[k]=v
        if isinstance(key,(str)):
            self._data[key]=value

    def get_key(self,key,default=None):
        '''
            Retrieve a data key from this entity.

            ----------

            Arguments
            -------------------------
            `key` {str}
                The key to search for.
            [`default`=None] {any}
                The default value to return when the key is not found.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-09-2023 09:15:10
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: get_key
            * @xxx [01-09-2023 09:16:05]: documentation for get_key
        '''
        if key in self._data:
            return self._data[key]
        return default




    # @property
    # def summary(self):
    #     '''
    #         Get the summary property's value

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 12-06-2022 12:10:00
    #         `@memberOf`: __init__
    #         `@property`: summary
    #     '''
    #     value = {
    #         # "schema":self.table.database.database,
    #         # "name":self.name.name,
    #     }

    #     return value

    @property
    def name(self)->c.string.Name:
        '''
            Get the name value.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 14:04:26
            `@memberOf`: PostArg
            `@property`: name
        '''
        value = self._name
        return value

    @name.setter
    def name(self,value:str):
        '''
            Set the name value.

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 14:04:26
            `@memberOf`: PostArg
            `@property`: name
        '''
        if isinstance(value,(str)):
            self._name = c.string.Name(value)
        if isinstance(value,c.string.Name):
            self._name = value

    def has_tag(self,tag:Union[str,list],match_all=False):
        '''
            Check if this entity has matching tags.

            ----------

            Arguments
            -------------------------
            `tag` {str,list}
                A tag or list of tags to search for.

            [`match_all`=False] {bool}
                If True, all tags provided must be found.


            Return {bool}
            ----------------------
            True if the tag(s) are found.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-05-2023 09:29:33
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: has_tag
            * @xxx [01-05-2023 09:30:55]: documentation for has_tag
        '''
        tags = c.arr.force_list(tag)
        tags.sort()
        tags.sort(key=len, reverse=False)

        matched = []
        for tag in tags:
            if tag in self._tags:
                if match_all is False:
                    return True
                else:
                    matched.append(tag)
        diff = c.arr.find_list_diff(tags,matched)
        if len(diff) == 0:
            return True
        return False

    def add_tag(self,tag:Union[str,list],remove:Union[str,list]=None):
        '''
            Add a tag to this entity.
            ----------

            Arguments
            -------------------------
            `tag` {str,list}
                A tag or list of tags to add.
                This can also be a comma delimited string of tags

            `remove` {str,list}
                A tag or list of tags to remove.
                This can also be a comma delimited string of tags

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-05-2023 09:31:06
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_tag
            * @xxx [01-05-2023 09:31:39]: documentation for add_tag
        '''
        if isinstance(tag,(str)):
            tag = tag.split(",")

        tags = c.arr.force_list(tag)
        for tag in tags:
            if isinstance(tag,(str)) is False:
                raise Exception("Tags must be of type string.")
            self._tags.append(tag)
            self._tags = c.arr.remove_duplicates(self._tags)
            self._tags.sort()
            self._tags.sort(key=len, reverse=False)
        if remove is not None:
            self.delete_tag(remove)

    def delete_tag(self,tag:Union[str,list]):
        '''
            Delete a tag from this entity.
            ----------

            Arguments
            -------------------------
            `tag` {str,list}
                A tag or list of tags to delete.
                This can also be a comma delimited string of tags


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-05-2023 09:31:06
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: delete_tag
            * @xxx [01-05-2023 09:31:39]: documentation for delete_tag
        '''
        if isinstance(tag,(str)):
            tag = tag.split(",")

        rtags = c.arr.force_list(tag)
        output = []
        for tag in self._tags:
            if tag not in rtags:
                output.append(tag)
        # for tag in tags:
            # if tag not in self._tags:
                # output.append(tag)
        self._tags = output


    @property
    def file_name(self):
        '''
            Get the file_name property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 10:17:45
            `@memberOf`: __init__
            `@property`: file_name
        '''
        if self.name is not None:
            self._file_name = f"{self.name.name}.py"

        if self._file_name is not None:
            return self._file_name

        from silent.Method import Method
        if isinstance(self,Method.Method):
            return self.module.file_name

        from silent.Module import Module
        if isinstance(self,Module):
            if len(self.classes) > 0:
                value = f"{self.classes[0].name.name}.py"





        self._file_name = value
        return value


    @property
    def dir_path(self):
        '''
            Get the dir_path property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 10:20:19
            `@memberOf`: __init__
            `@property`: dir_path
        '''
        from silent.Package import Package
        if isinstance(self,Package):
            return self._file_path

        from silent.Module import Module
        if isinstance(self,Module):
            pkg = self.package
            return pkg.file_path

        from silent.Method import Method
        if isinstance(self,Method.Method):
            return self.module.file_path


    @property
    def file_path(self):
        '''
            Get the file_path property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 10:14:44
            `@memberOf`: __init__
            `@property`: file_path
        '''
        if self._file_path is not None:
            return self._file_path

        from silent.Package import Package
        if isinstance(self,Package):
            self._file_path = f"{self.dir_path}/__init__.py"

        from silent.Module import Module
        if isinstance(self,Module):
            self._file_path = f"{self.package.file_path}/{self.file_name}"

        from silent.Method import Method
        if isinstance(self,Method.Method):
            self.package = self.module.package
            self._file_path = f"{self.package.file_path}/{self.module.name.name}"

        from silent.Class import Class
        if isinstance(self,Class):
            self.package = self.module.package
            self._file_path = f"{self.package.file_path}/{self.module.name.name}"




        return self._file_path

    @file_path.setter
    def file_path(self,value):
        '''
            Set the file_path property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 09:57:27
            `@memberOf`: __init__
            `@property`: file_path
        '''
        self._file_path = value

    @property
    def relative_path(self):
        '''
            Get the relative_path property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 12:32:33
            `@memberOf`: __init__
            `@property`: relative_path
        '''

        value = self.file_path.replace(self.main.root_path,"")

        return value

    @property
    def import_path(self)->str:
        '''
            Get the import_path property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 12:44:16
            `@memberOf`: __init__
            `@property`: import_path
        '''
        value = None
        from silent.Module import Module
        if isinstance(self,Module):
            value = path_to_dot_path(self.relative_path)

        from silent.Class import Class
        if isinstance(self,Class):
            value = path_to_dot_path(self.relative_path)

        from silent.Package import Package
        if isinstance(self,Package):
            value = path_to_dot_path(self.relative_path)
        from silent.Method import Method
        if isinstance(self,Method.Method):
            value = path_to_dot_path(self.relative_path)
        return value

    @property
    def import_statement(self)->str:
        '''
            Get this entity's import statement as a string.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 13:22:04
            `@memberOf`: __init__
            `@property`: import_statement
        '''
        imp = _imp.ImportStatement()
        from silent.Package import Package
        if isinstance(self,Package):
            imp.add_subject(self.import_path)
            imp.alias = self.name.name
        else:
            imp.import_path=self.import_path
            imp.add_subject(self.name.name)
        value = imp.result
        return value



    def apply_auto_replaces(self,value):
        return c.string.dict_replace_string(value,self._auto_replace)

    def add_auto_replace(self,term,replace):
        self._auto_replace[term] = replace

    def get_auto_replace(self,term):
        if term in self._auto_replace:
            return self._auto_replace[term]



    @property
    def body(self):
        '''
            Get the body property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-14-2023 10:02:45
            `@memberOf`: __init__
            `@property`: body
        '''
        value = self._body
        if isinstance(value,(str)):
            value = self._format_single_line_comments(value)
        return value

    @body.setter
    def body(self,value):
        '''
            Set the body property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-14-2023 10:06:25
            `@memberOf`: __init__
            `@property`: body
        '''
        self._body = value

    def prepend_to_body(self,value,template_replace:dict=None):
        value = _body_pend_prep(self,value,template_replace)
        self.body = str(value) + self.body
        # self.body = self._format_single_line_comments(self.body)
        return self.body

    def append_to_body(self,value,template_replace:dict=None):
        '''
            Append content to the body.

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
        value = _body_pend_prep(self,value,template_replace)
        self.body = self.body + str(value)
        # self.body = self._format_single_line_comments(self.body)
        return self.body


    def _format_single_line_comments(self,value:str)->str:
        '''
            Finds all single line comments in the value provided and replaces them with a multi line version
            that is prefixed with "__SINGLE_LINE_COMMENT__"

            Due to the fact AST does not support single line comments, this provides a hacky workaround for
            keeping them.
            ----------

            Arguments
            -------------------------
            `value` {str}
                The value to format.

            Return {str}
            ----------------------
            The formatted value

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-14-2023 09:48:35
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: _format_single_line_comments
            # * @TODO []: documentation for _format_single_line_comments
        '''
        # print(f"value: {value}")
        # value = re.sub(r"^([^\r\n]*#[^\n]*)",r"'''__SINGLE_LINE_COMMENT__\1'''",value,0,re.MULTILINE)

        if isinstance(value,(str)):
            lines = value.split("\n")
            new_lines = []
            for line in lines:
                if "__SINGLE_LINE_COMMENT__" not in line and "#" in line:
                    line = re.sub(r"^([^\r\n]*)(#[^\n]*)",r"\1'''__SINGLE_LINE_COMMENT__\2__SINGLE_LINE_COMMENT__'''",line,0,re.MULTILINE)
                    # line = re.sub(r"^([^\r\n]*)(#[^\n]*)",r'\1"""__SINGLE_LINE_COMMENT__\2"""',line,0,re.MULTILINE)
                new_lines.append(line)
            value = '\n'.join(new_lines)
        return value

    def _reverse_format_single_line_comments(self,value:str)->str:
        value = re.sub(r"[^\s]{1,3}__SINGLE_LINE_COMMENT__([^\n]*)__SINGLE_LINE_COMMENT__[^\n]*",r"\1",value,0,re.MULTILINE)
        # if "__SINGLE_LINE_COMMENT__" in value:
            # value = re.sub(r"[^\s]{3}__SINGLE_LINE_COMMENT__([^\n]*)__SINGLE_LINE_COMMENT__[^\n]*",r"\1",value,0,re.MULTILINE)
            # value = re.sub
        # value = re.sub(r"['\"]{1,3}__SINGLE_LINE_COMMENT__([^\n]*)['\"]+",r"\1",value,0,re.MULTILINE)
        # value = re.sub(r"['\"]{1,3}__SINGLE_LINE_COMMENT__([^\n]*['\"]{,1})",r"\1",value,0,re.MULTILINE)
        return value


def _body_pend_prep(ent,value,template_replace:dict=None):
    if isinstance(value,(str)):
        if c.file.exists(value):
            value = c.file.readr(value)
    if isinstance(value,ast.AST):
        value = ast.unparse(value)
    if ent.body is None:
        ent.body = ""

    if isinstance(value,(str)):
        if isinstance(template_replace,(dict)):
            s = Template(value)
            s.substitute(**template_replace)
    return value

def populate_from_dict(data:dict,instance:EntityBase):
    for k,v in data.items():
        if hasattr(instance,k):
            if k == "name":
                if isinstance(v,(str)):
                    setattr(instance,'name',c.string.Name(v))
                if isinstance(v,c.string.Name):
                    setattr(instance,'name',v)
                continue
            setattr(instance,k,v)

def path_to_dot_path(relative_path:str):
    value = relative_path
    value = c.string.file_path(value,url=True)
    value = value.replace("/",".")
    value = c.string.strip(value,["."," "])
    value = c.string.strip(value,[".py"],"right")
    return value