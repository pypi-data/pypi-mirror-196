# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
# pylint: disable=import-outside-toplevel

from dataclasses import dataclass
from typing import Iterable, Union
import colemen_utils as c
import silent.se_config as config
import silent.settings.types as _types
import silent.Package as _package


@dataclass
class Main:
    project_name:str = None
    root_path:str = None

    def __init__(self):
        self._entities = {
            "packages":[],
            "modules":{},
            "imports":[],
            "classes":[],
            "methods":[],
            "properties":[],
            "decorators":[],
        }
        # self._packages = []
        self.data = {}


    def master(self):
        print("master")

    @property
    def summary(self):
        '''
            Get this main's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 09:39:11
            `@memberOf`: main
            `@property`: summary
        '''
        value = {
            "packages":{}
        }

        for pkg in self.packages:
            value['packages'][pkg.name.name] = pkg.summary
        c.file.writer.to_json("tmp.json",value)
        return value

    def save(self):
        imports = []
        # print(f"{len(self.packages)}")
        for pkg in self.packages:
            # self.save_nested_packages(pkg)
            pkg.save()
            # @Mstep [] only include direct child packages as imports.
            if len(pkg.import_path.split(".")) <= 2:
                imports.append(pkg.import_statement)

        imports = '\n'.join(imports)
        c.file.write(f"{self.root_path}/{self.project_name}/__init__.py",imports)

    def get_classes_by(
        self,
        props:Union[str,list]=None,
        methods:Union[str,list]=None,
        tags:Union[str,list]=None,
        decorators:Union[str,list]=None,
        args:Union[str,list]=None,
        names:Union[str,list]=None,
        )->Iterable[_types._py_class_type]:
        '''
            Retrieve a list of classes that match the data provided.
            ----------

            Arguments
            -------------------------
            [`props`=None] {str,list}
                The prop name or list of props to search for.

            [`methods`=None] {str,list}
                The method name or list of methods to search for.

            [`tags`=None] {str,list}
                The tag name or list of tags to search for.

            [`decorators`=None] {str,list}
                The decorator name or list of decorators to search for.

            [`args`=None] {str,list}
                The argument name or list of names to search for.

            [`names`=None] {str,list}
                The name or list of names to search for.




            Return {list}
            ----------------------
            A list of functions that match any of the values provided.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-10-2023 14:47:43
            `memberOf`: silent_engine
            `version`: 1.0
            `method_name`: get_classes_by
            * @xxx [03-10-2023 14:58:22]: documentation for get_classes_by
        '''
        results = []

        names = c.arr.force_list(names,allow_nulls=False)
        if len(names) > 0:
            names.sort()
            names.sort(key=len, reverse=False)

        decorators = c.arr.force_list(decorators,allow_nulls=False)
        if len(decorators) > 0:
            decorators.sort()
            decorators.sort(key=len, reverse=False)

        props = c.arr.force_list(props,allow_nulls=False)
        if len(props) > 0:
            props.sort()
            props.sort(key=len, reverse=False)

        args = c.arr.force_list(args,allow_nulls=False)
        if len(args) > 0:
            args.sort()
            args.sort(key=len, reverse=False)

        methods = c.arr.force_list(methods,allow_nulls=False)
        if len(methods) > 0:
            methods.sort()
            methods.sort(key=len, reverse=False)

        tags = c.arr.force_list(tags,allow_nulls=False)
        if len(tags) > 0:
            tags.sort()
            tags.sort(key=len, reverse=False)

        for cc in self.classes:
            if len(decorators) > 0:
                for dec in decorators:
                    if cc.get_decorator(dec):
                        results.append(cc)

            if len(props) > 0:
                for prop in props:
                    if cc.get_property(prop):
                        results.append(cc)

            if len(methods) > 0:
                for method in methods:
                    if cc.get_method(method):
                        results.append(cc)

            if len(tags) > 0:
                if cc.has_tag(tags):
                    results.append(cc)

            if len(args) > 0:
                for prop in args:
                    if cc.get_arg(prop):
                        results.append(cc)

            if len(names) > 0:
                if cc.name.name in names:
                    results.append(cc)

        return results

    def get_funcs_by(
        self,
        args:Union[str,list]=None,
        names:Union[str,list]=None,
        tags:Union[str,list]=None,
        decorators:Union[str,list]=None,
        include_class_methods:bool=True,
        )->Iterable[_types._method_type]:
        '''
            Retrieve a list of functions that match the data provided.
            ----------

            Arguments
            -------------------------
            [`args`=None] {str,list}
                The argument name or list of names to search for.

            [`tags`=None] {str,list}
                The tag name or list of tags to search for.

            [`names`=None] {str,list}
                The name or list of names to search for.

            [`decorators`=None] {str,list}
                The decorator name or list of decorators to search for.

            [`include_class_methods`=True] {bool}
                If False, class methods are excluded.

            Return {list}
            ----------------------
            A list of functions that match any of the values provided.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-10-2023 14:47:43
            `memberOf`: silent_engine
            `version`: 1.0
            `method_name`: get_funcs_by
            * @xxx [03-10-2023 14:58:12]: documentation for get_funcs_by
        '''
        results = []
        # entity_type = c.string.to_snake_case(entity_type)

        decorators = c.arr.force_list(decorators,allow_nulls=False)
        if len(decorators) > 0:
            decorators.sort()
            decorators.sort(key=len, reverse=False)

        args = c.arr.force_list(args,allow_nulls=False)
        if len(args) > 0:
            args.sort()
            args.sort(key=len, reverse=False)

        names = c.arr.force_list(names,allow_nulls=False)
        if len(names) > 0:
            names.sort()
            names.sort(key=len, reverse=False)

        tags = c.arr.force_list(tags,allow_nulls=False)
        if len(tags) > 0:
            tags.sort()
            tags.sort(key=len, reverse=False)

        for cc in self.methods:
            if include_class_methods is False and cc.is_class_method is True:
                continue
            if len(decorators) > 0:
                for dec in decorators:
                    if cc.get_decorator(dec):
                        results.append(cc)

            if len(args) > 0:
                for prop in args:
                    if cc.get_arg(prop):
                        results.append(cc)

            if len(names) > 0:
                if cc.name.name in names:
                    results.append(cc)

            if len(tags) > 0:
                if cc.has_tag(tags):
                    results.append(cc)

        return results

    def get_by_tag(self,tag,entity_type:str=None):
        results = []
        entity_type = c.string.to_snake_case(entity_type)
        tags = c.arr.force_list(tag)
        tags.sort()
        tags.sort(key=len, reverse=False)


        if entity_type not in self._entities:
            print(f"{entity_type} is not a recognized entity type.")
            return False


        for pkg in self.packages:
            if pkg.has_tag(tags):
                results.append(pkg)

        for mod in self.modules:
            if mod.has_tag(tags):
                results.append(mod)

        for mod in self.classes:
            if mod.has_tag(tags):
                results.append(mod)

        for mod in self.methods:
            if mod.has_tag(tags):
                results.append(mod)

        return results


    # ---------------------------------------------------------------------------- #
    #                                   PACKAGES                                   #
    # ---------------------------------------------------------------------------- #

    def add_package(self,name:str,description:str=None,overwrite:bool=True,
                    tags:Union[str,list]=None,append_imports:bool=False,init_file_name:str=None)->config._package_type:
        '''
            add a new package to this project.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the package

            [`description`=None] {str}
                The documentation description for the package.

            [`overwrite`=True] {bool}
                If False, this file will not save over an already existing version.

            [`tags`=None] {list,str}
                A tag or list of tags to add after it is instantiated.

            [`append_imports`=False] {bool}
                If True, the existing __init__ file will have the imports appended instead of overwriting.

            [`init_file_name`=None] {str}
                If provided, this package's __init__ file will use this name instead.

                This is useful for creating an init file that the generator can update while leaving the actual __init__
                intact. All you need to do is add the import statement to the __init__.py file.




            Return {Package}
            ----------------------
            The new package instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-05-2023 09:09:47
            `memberOf`: main
            `version`: 1.0
            `method_name`: add_package
            * @xxx [01-05-2023 09:11:21]: documentation for add_package
        '''
        pkg = self.get_package(name)
        if pkg is not None:
            return pkg

        file_path = f"{self.root_path}/{self.project_name}/{name}"
        pkg = _package.Package(
            self,
            name=name,
            description=description,
            file_path=file_path,
            overwrite=overwrite,
            append_imports=append_imports,
            init_file_name=init_file_name,
            tags=tags,
        )
        return pkg

    def get_package(self,name:Union[str,list]=None,tags:Union[str,list]=None,default=None)->Iterable[config._package_type]:
        '''
            Retrieve a package by its name or import path.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name to search for.

            Return {Package}
            ----------------------
            The package instance upon success, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-06-2023 15:11:08
            `memberOf`: silent_engine
            `version`: 1.0
            `method_name`: get_package
            * @xxx [01-06-2023 15:11:54]: documentation for get_package
        '''
        tags = c.arr.force_list(tags,allow_nulls=False)
        name = c.arr.force_list(name,allow_nulls=False)
        result = []
        for pkg in self.packages:
            # print(f"pkg.import_path:{pkg.import_path}")
            if len(name) > 0:
                if pkg.name.name in name:
                    result.append(pkg)
                if pkg.import_path in name:
                    result.append(pkg)
            if len(tags) > 0:
                if pkg.has_tag(tags):
                    result.append(pkg)


        if len(result) == 0:
            return default
        return result

    @property
    def packages(self)->Iterable[config._package_type]:
        '''
            Get a list of this project's packages

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 09:48:14
            `@memberOf`: main
            `@property`: packages
        '''
        # value = self._entities['packages']
        value = self._entities['packages']
        return value



    # ---------------------------------------------------------------------------- #
    #                                    MODULES                                   #
    # ---------------------------------------------------------------------------- #


    def get_modules_by_tag(self,tag:str)->Iterable[config._py_module_type]:
        '''
            Get this main's get_modules_by_tag

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 09:59:00
            `@memberOf`: main
            `@property`: get_modules_by_tag
        '''
        value = []
        for mod in self.modules:
            if mod.has_tag(tag):
                value.append(mod)
        return value

    def get_modules(
        self,
        name:Union[str,list]=None,
        tags:Union[str,list]=None,
        default=None
        )->Iterable[_types._py_module_type]:
        '''
            Retrieve a list of modules by searching for name, import path or tags..

            ----------

            Arguments
            -------------------------
            `name` {list,str}
                The name or list of names to search for.
                This can also be an import path.

            `tags` {list,str}
                The tag or list of tags to search for.

            Return {Package}
            ----------------------
            The package instance upon success, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-06-2023 15:11:08
            `memberOf`: silent_engine
            `version`: 1.0
            `method_name`: get_package
            * @xxx [01-06-2023 15:11:54]: documentation for get_package
        '''
        tags = c.arr.force_list(tags,allow_nulls=False)
        name = c.arr.force_list(name,allow_nulls=False)
        result = []
        for mdl in self.modules:
            if len(name) > 0:
                if mdl.name.name in name:
                    result.append(mdl)
                if mdl.import_path in name:
                    result.append(mdl)
            if len(tags) > 0:
                if mdl.has_tag(tags):
                    result.append(mdl)


        if len(result) == 0:
            return default
        return result

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
            if mod.has_tag(tag):
                value.append(mod,match_all)
        return value



    @property
    def modules(self)->Iterable[config._py_module_type]:
        '''
            Get a list of this project's modules

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 09:48:14
            `@memberOf`: main
            `@property`: modules
        '''
        value = list(self._entities['modules'].values())
        return value

    @property
    def classes(self)->Iterable[config._py_class_type]:
        '''
            Get a list of this project's classes

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 09:48:14
            `@memberOf`: main
            `@property`: classes
        '''
        value = self._entities['classes']
        return value

    @property
    def methods(self)->Iterable[config._method_type]:
        '''
            Get a list of this project's methods

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 09:48:14
            `@memberOf`: main
            `@property`: classes
        '''
        value = self._entities['methods']
        return value

    @property
    def decorators(self)->Iterable[_types._decorator_type]:
        '''
            Get a list of this project's decorators

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 09:48:14
            `@memberOf`: main
            `@property`: decorators
        '''
        value = self._entities['decorators']
        return value






















    def register(self,instance):
        from silent.Package import Package
        if isinstance(instance,Package):
            # print(f"Register new package: {instance.name.name}")
            self._entities['packages'].append(instance)

        from silent.Module import Module
        if isinstance(instance,Module):
            self._entities['modules'][instance.name.name] = instance

        from silent.Import import ImportStatement
        if isinstance(instance,ImportStatement):
            self._entities['imports'].append(instance)

        from silent.Class import Class
        if isinstance(instance,Class):
            self._entities['classes'].append(instance)

        # from silent.Method.Method import Method
        from silent.Method import Method
        if isinstance(instance,Method.Method):
            self._entities['methods'].append(instance)

        from silent.Class.Property import Property
        if isinstance(instance,Property):
            self._entities['properties'].append(instance)

        from silent.Decorator import Decorator
        if isinstance(instance,Decorator.Decorator):
            self._entities['decorators'].append(instance)


def new(project_name:str,root_path:str,**kwargs):
    m = Main()
    m.project_name = project_name
    m.root_path = root_path
    # m.use_random_type_names = c.obj.get_kwarg(['use_random_type_names'],True,(bool),**kwargs)
    return m



# if __name__ == '__main__':
#     m = Main()
#     m.master()

