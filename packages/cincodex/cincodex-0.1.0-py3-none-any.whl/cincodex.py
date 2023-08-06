import hashlib
import importlib.util
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Generic, Iterator, Protocol, Sequence, TypeVar, cast

__version__ = '0.1.0'

logger = logging.getLogger(__name__)

T = TypeVar('T')
#: Plugin type variable
_PluginT = TypeVar('_PluginT')


class PluginMetadata:
    """
    Base class for plugin metadata.

    Applications should subclass this with additional metadata fields as necessary. At a minimum,
    the plugin metadata must have a unique ``id``.
    """

    def __init__(self, id: str):
        """
        :param id: unique plugin id.
        """
        self.id = id

    def __call__(self, plugin: _PluginT) -> _PluginT:
        """
        Bind the provided plugin to this metadata.

        This method is called when the plugin metadata is used as a decorator, such as:

        .. code-block:: python

            codex = create_codex(...)

            @codex.register
            @codex.metadata('my.plugin.id')
            class MyPlugin:
                ...

        This method must call :meth:`bind`.

        :param plugin: the plugin to bind this metadata to
        :returns: the plugin
        """
        return self.bind(plugin)

    def bind(self, plugin: _PluginT) -> _PluginT:
        """
        Bind the provided plugin to this metadata.

        This method should always set the ``plugin.__plugin_metadata__`` attribute to ``self``.

        :param plugin: the plugin to bind to this metadata to
        :returns: the plugin
        """
        cast(BoundPlugin, plugin).__plugin_metadata__ = self
        return plugin

    @classmethod
    def get(cls: type['_PluginMetadataT'], plugin: _PluginT) -> '_PluginMetadataT':
        """
        Get the metadata for a plugin.

        :param plugin: the plugin
        :returns: the metadata
        """
        return cast(BoundPlugin[_PluginMetadataT], plugin).__plugin_metadata__


#: Plugin metadata type variable, which must be a subclass of :class:`PluginMetadata`
_PluginMetadataT = TypeVar('_PluginMetadataT', bound=PluginMetadata)


class BoundPlugin(Protocol[_PluginMetadataT]):
    """
    A plugin that is bound to metadata.
    """

    #: The plugin metadata, set by the :meth:`PluginMetadata.bind` method
    __plugin_metadata__: _PluginMetadataT


@dataclass
class ModuleLocation:
    """
    A location of Python module on disk.
    """

    #: The root search directory where the module was discovered.
    root: Path
    #: The Python module filename, relative to ``root``
    filename: Path
    #: The Python module name (``__name__``)
    modname: str
    #: The Python module is a bundle
    is_bundle: bool = False


class PluginFinder:
    """
    Abstract base class for plugin finders.

    A plugin finder discovers Python modules that may contain potential plugins. The interface
    is similar to the Python import machinery :class:`~importlib.abc.Finder` interface with the
    exception that the ``PluginFinder`` accepts a *directory* to search for module source files
    rather than a single module name.
    """

    def discover(self, dirname: Path, modname: str | None = None) -> Iterator[ModuleLocation]:
        """
        Discover all Python modules within the root directory.

        This method may return a list or can be a generator that yields module locations. This
        method must produce module locations according to several rules:

        #. Within a single directory, all modules should be returned or yielded prior to recursing
           into any nested module or directory.
        #. The first module must be the ``__init__`` module, if it exists within the current
           directory being scanned.
        #. When a bundle module is discovered, no further scanning within that directory and all
           nested directories must stop. Bundle modules must not contain any nested modules.

        The directory must have a unique root module name that is part of each returned module
        location, this is either the ``modname`` argument or must be generated in a deterministic
        way if ``modname`` is empty.

        Plugins that are defined across multiple Python source files are bundle modules. Bundle
        modules have a special filename, which is ``__bundle__`` by default, and, when encountered,
        must stop all scanning in the current directory and nested directories. A bundle module may
        be similar to the following:

        .. code-block::

            # file: __bundle__.py
            from app import codex
            from .lib import do_stuff

            @codex.register
            @codex.metadata(id='my.plugin')
            def my_plugin():
                do_stuff()

        Subclasses must implement this method.

        :param dirname: root directory to scan for Python modules
        :returns: an iterator over discovered module locations
        """
        raise NotImplementedError()


class PluginPathFinder(PluginFinder):
    """
    Recursively scan directories for Python modules that may contain plugins.

    Bundle modules can have a configurable stem and extension. By default, with the stem name of
    ``__bundle__`` and allowed extensions of ``['.py']``, bundle modules must have the filename of
    ``__bundle__.py``.
    """

    def __init__(
        self,
        bundle_name: str = '__bundle__',
        extensions: list[str] = ['.py'],
        exclude: list[str] = ['__pycache__', '.git'],
        follow_symlinks: bool = False,
    ):
        """
        :param bundle_name: the stem portion of the filename for a bundle plugin
        :param extensions: list of filename extensions that may contain plugins
        :param exclude: file and directory names to exclude
        :param follow_symlinks: recurse into symlink directories and include symlink files
        """
        self.bundle_name = bundle_name
        self.extensions = list(extensions)
        self.exclude = list(exclude)
        self.follow_symlinks = follow_symlinks

    def discover(self, dirname: Path, modname: str | None = None) -> Iterator[ModuleLocation]:
        """
        Recursively discover all Python modules within the directory.

        :param dirname: directory to scan
        :returns: a generator that yields module locations
        """
        dirname = dirname.absolute()
        if not modname:
            hash = hashlib.sha1(str(dirname).encode(), usedforsecurity=False).hexdigest()
            modname = f'cincodex_plugins_{hash}'
        yield from self._discover(dirname, Path('.'), modname)

    def _check_special_file(self, root: Path, dirname: Path, stem: str) -> Path | None:
        """
        Check if the special file exists within the directory, honoring the configured
        ``extensions``.

        :param root: root scan directory
        :param dirname: directory to scan, relative to the root
        :param stem: the stem name (file basename without an extension)
        """
        basename = dirname / stem
        for ext in self.extensions:
            special = basename.with_suffix(ext)
            if (root / special).is_file():
                return special

        return None

    def _discover(self, root: Path, dirname: Path, root_modname: str) -> Iterator[ModuleLocation]:
        """
        Recursively discover all Python modules within the directory.

        :param dirname: directory to scan
        :returns: a generator that yields module locations
        """
        logger.debug('searching directory for modules: %s', dirname)
        directories: list[Path] = []
        base_modname = [root_modname] + list(dirname.parts)
        init = self._check_special_file(root, dirname, '__init__')
        bundle = self._check_special_file(root, dirname, self.bundle_name)
        if init:
            yield ModuleLocation(root, init, '.'.join(base_modname))

        if bundle:
            yield ModuleLocation(
                root, bundle, '.'.join(base_modname + [self.bundle_name]), is_bundle=True
            )
            return

        for item in (root / dirname).iterdir():
            if init and item.stem == '__init__':
                continue

            if self._exclude_path(item):
                continue

            if item.is_dir():
                directories.append(item)
            elif item.is_file() and item.suffix in self.extensions:
                filename = dirname / item.name
                name = filename.stem
                if '.' in name:
                    continue

                modname = '.'.join(base_modname + [name])
                logger.debug('found module: %s (%s)', filename, modname)
                yield ModuleLocation(root, filename, modname)

        for directory in directories:
            yield from self._discover(root, dirname / directory.name, root_modname)

    def _exclude_path(self, path: Path) -> bool:
        """
        Check if the given path should be excluded from the scan.

        :param path: absolute path to check
        :returns: the path should be excluded from the scan
        """
        return path.name in self.exclude or (path.is_symlink() and not self.follow_symlinks)


class PluginLoader:
    """
    Abstract base class for plugin loaders.

    A plugin loader accepts a Python module location and loads it. Loading the module should honor
    the Python import machinery so that relative and absolute imports work as expected, as if the
    module were imported using the ``import`` statement.

    The default mechanism for loading a plugin is:

    1. Recursively scan a directory for Python modules (:class:`PluginPathFinder`)
    2. Load each module discovered (:class:`PluginPathLoader`)
    3. The loaded module calls :meth:`Codex.register` which registers the plugin
    """

    def load_module(self, codex: 'Codex', loc: ModuleLocation) -> ModuleType | None:
        """
        Load a module, honoring the Python import machinery, which includes:

        1. Import all missing parent modules.
        2. Registering the module in :data:`sys.modules`.

        For example, if the module ``plugins.foo.bar`` is being loaded, the modules ``plugins``
        and ``plugins.foo`` must first be loaded if they are not loaded already. This is to ensure
        that relative and absolute imports continue to work for plugin modules.

        Loaded modules must have their plugins registered with the provided ``codex``. This can be
        done automatically by plugins registering themselves on import or can be done manually
        within this plugin loader by calling :meth:`Codex.register`.

        :param loc: module location to import
        :returns: the imported module or ``None`` if the module could not be imported.
        """
        raise NotImplementedError()


class PluginPathLoader(PluginLoader):
    """
    Plugin loader implementation that mirrors the Python import machinery.
    """

    def load_module(self, codex: 'Codex', loc: ModuleLocation) -> ModuleType | None:
        """
        Load a module.

        :param loc: module location
        :returns: the imported module or ``None`` if the module could not be imported
        """
        parts = loc.modname.split('.')
        directory = loc.root
        modname = parts[0]

        if len(parts) > 1 and modname not in sys.modules:
            self._load_empty_module(directory, modname)

        for part in parts[1:-1]:
            modname += f'.{part}'
            directory = directory / part
            if modname not in sys.modules:
                self._load_empty_module(directory, modname)

        return self._load_module(loc)

    def _load_module(self, loc: ModuleLocation) -> ModuleType | None:
        """
        Load a module and update :data:`sys.modules`.

        :param loc: module location
        :returns: the imported module or ``None`` if the module could not be imported
        """
        existing = sys.modules.get(loc.modname)
        if existing:
            logger.debug('updating already imported module: %s (%s)', loc.filename, loc.modname)
            setattr(existing, '__cincodex_module__', loc)
            return existing

        logger.debug('loading module %s (%s)', loc.filename, loc.modname)
        spec = importlib.util.spec_from_file_location(loc.modname, str(loc.root / loc.filename))
        if not spec or not spec.loader:
            logger.error(
                'cannot load module %s (%s): no loader is available', loc.filename, loc.modname
            )
            return None

        module = importlib.util.module_from_spec(spec)
        setattr(module, '__cincodex_module__', loc)
        try:
            spec.loader.exec_module(module)
        except:  # noqa: E722
            logger.exception('failed to load module %s (%s)', loc.filename, loc.modname)
        else:
            sys.modules[loc.modname] = module

        return module

    def _load_empty_module(self, directory: Path, modname: str) -> ModuleType:
        """
        Create a module for the given module name and register it with :data:`sys.module`.

        This method is used when a parent module is missing, typically when a directory does not
        have a ``__init__`` file. This creates an empty module and "imports" it.

        :param directory: absolute path to the directory for the module being created
        :param modname: module name (``__name__``)
        :returns: the created module
        """
        init = directory / '__init__.py'
        logger.debug('loading empty module: %s (%s)', init, modname)
        if spec := importlib.util.spec_from_file_location(modname, str(init)):
            module = importlib.util.module_from_spec(spec)
        else:
            module = ModuleType(modname)

        setattr(module, '__cincodex_empty_module__', True)
        sys.modules[modname] = module
        return module


def _plugin_metadata_filter(attr: str, value: Any) -> Callable[[PluginMetadata], bool]:
    """
    Create a function that will filter plugin metadata based on an attribute's value.

    :param attr: attribute name
    :param value: attribute value
    :returns: a function that, when called with a plugin metadata object, returns ``True`` if the
        metadata matches the criteria and ``False`` otherwise
    """
    if isinstance(value, re.Pattern):

        def regex_filter_func(metadata: PluginMetadata) -> bool:
            return value.match(getattr(metadata, attr, '')) is not None

        return regex_filter_func

    def filter_func(metadata: PluginMetadata) -> bool:
        return getattr(metadata, attr, None) == value

    return filter_func


class Codex(Generic[_PluginT, _PluginMetadataT]):
    """
    A plugin system that maintains the list of available plugins.

    A codex is the primarily interface for both registering plugins and retrieving available
    plugins. Typically the application will create a codex that an extension will import and then
    register the plugin with, similar to the following:

    .. code-block:: python

        # app.py
        from cincodex import Codex, register_codex

        codex = Codex('app')
        register_codex(codex)

        codex.discover_plugins('./plugins')


        # plugins/foo/bar.py
        from app import codex

        @codex.register  # register the plugin and metadata
        @codex.metadata(id='foo.bar')  # plugin metadata
        def foo_bar_plugin():
            print('hello world!')

    The codex can also be retrieve with the :func:`get_codex` function:

    .. code-block:: python

        # plugins/foo/bar.py
        from cincodex import get_codex

        codex = get_codex('app')

        @codex.register
        @codex.metadata(id='foo.bar')
        def foo_bar_plugin():
            print('hello world!')

    Plugins can be any Python object: a function, a class, or an object instance. Each plugin must
    have metadata that describe it, which includes at the very least a unique ``id``. Plugin
    metadata can be retrieved using the :meth:`PluginMetadata.get` method:

    .. code-block:: python

        plugin = codex.get('foo.bar')
        # plugin is the `foo_bar_plugin` function
        metadata = PluginMetadata.get(plugin)
        # metadata is the metadata created within the `codex.metadata` decorator
        # or, optionally, the metadata is stored in the plugin's __plugin_metadata__ attribute
        metadata = plugin.__plugin_metadata__
    """

    def __init__(
        self,
        namespace: str,
        metadata: type[_PluginMetadataT] | None = None,
        finder: PluginFinder | None = None,
        loader: PluginLoader | None = None,
    ):
        """
        :param namespace: codex namespace
        :param metadata: plugin metadata class or :class:`PluginMetadata` if not specified
        :param finder: the plugin finder or the default :class:`PluginPathFinder` if not specified
        :param loader: the plugin loader or the default :class:`PluginPathLoader` if not specified
        """
        self.namespace = namespace
        self.metadata = metadata or PluginMetadata
        self.finder = finder or PluginPathFinder()
        self.loader = loader or PluginPathLoader()
        self._plugins: dict[str, _PluginT] = {}

    def register(self, plugin: T) -> T:
        """
        Register a plugin.

        This is typically used as a decorator for function and class plugins but can be called
        directly with the plugin to register for object instance plugins. For example:

        .. code-block:: python

            codex = Codex('app')

            # Class plugin
            @codex.register
            @codex.metadata(id='class_plugin')
            class Plugin:
                pass

            # Function plugin
            @codex.register
            @codex.metadata(id='func_plugin')
            def func_plugin():
                pass

            # Object instance plugin
            class MyPlugin:
                pass

            obj_plugin = MyPlugin()
            codex.register(codex.metadata(id='object_plugin').bind(obj_plugin))

        The plugin being registered must have metadata bound to it via
        :meth:`PluginMetadata.bind` or using the ``codex.metadata`` as a decorator.

        :param plugin: plugin to register
        """
        id = cast(BoundPlugin[_PluginMetadataT], plugin).__plugin_metadata__.id
        self._plugins[id] = cast(_PluginT, plugin)
        logger.debug('registered new plugin: %s (%s)', id, plugin)
        return plugin

    def get(self, id: str) -> _PluginT | None:
        """
        Get a plugin by its unique id.

        :param id: plugin metadata id
        :returns: the registered plugin or ``None`` if the plugin does not exist
        """
        return self._plugins.get(id)

    def find(
        self, *plugin_filters: Callable[[_PluginT], bool], **metadata_criteria
    ) -> list[_PluginT]:
        """
        Find plugins that match the given criteria.

        Two types of criteria can be supplied to this function:

        1. ``plugin_filters`` - callables that accept a plugin and return ``True`` if the plugin
           if the plugin matches the criteria.
        2. ``metadata_criteria`` - key/value pairs that must all match the plugin metadata.

        For example, the following block finds plugins that are subclasses of ``AppPlugin`` and
        are authored by ``Acme, Inc.``:

        .. code-block:: python

            class AppPlugin:
                pass

            class AppPluginMetadata(PluginMetadata):
                def __init__(self, id: str, author: str, version: str):
                    super().__init__(id)
                    self.author = author
                    self.version = version

            codex = Codex('app', AppPluginMetadata)

            # ... after registering plugins ...

            codex.find(lambda plugin: issubclass(plugin, AppPlugin), author='Acme, Inc.')

        The ``metadata_criteria`` also handled regular expressions. If the value is a
        :class:`re.Pattern` instance, :meth:`re.Pattern.match` is called to check if the attribute
        matches.

        :param plugin_filter: list of callables that filter based on plugins
        :param metadata_criteria: dictionary of key/value pairs that the plugin metadata must have
        :returns: the list of plugins that match all filters
        """
        return list(self._filter(plugin_filters, metadata_criteria))

    def find_one(
        self, *plugin_filters: Callable[[_PluginT], bool], **metadata_criteria
    ) -> _PluginT | None:
        """
        Find the first plugin that matches all criteria.

        This method accepts the same arguments with the same semantics as :meth:`find`. The
        difference is that ``find_one`` returns the first plugin that matches all the criteria
        rather than returning all plugins that match the criteria. This method is useful when
        finding a plugin based on some unique combination of criteria other than the plugin
        metadata ``id``.

        :param plugin_filter: list of callables that filter based on plugins
        :param metadata_criteria: dictionary of key/value pairs that the plugin metadata must have
        :returns: the list of plugins that match all filters
        """
        return next(self._filter(plugin_filters, metadata_criteria))

    def _filter(
        self, plugin_filters: Sequence[Callable[[_PluginT], bool]], metadata_criteria: dict
    ) -> Iterator[_PluginT]:
        """
        Filter plugins based on the provided criteria.

        The return value is a generator that yield plugins that match the criteria. This method
        accepts the same arguments with the same semantics as :meth:`find`.

        :param plugin_criteria: list of callables that filter based on plugins
        :param metadata_criteria: dictionary of key/value pairs that the plugin metadata must have
        :returns: the list of plugins that match all filters
        """
        metadata_filters: list[Callable[[PluginMetadata], bool]] = []
        for attr, value in metadata_criteria.items():
            metadata_filters.append(_plugin_metadata_filter(attr, value))

        for plugin in self._plugins.values():
            metadata = self.metadata.get(plugin)
            if all(func(plugin) for func in plugin_filters) and all(
                func(metadata) for func in metadata_filters
            ):
                yield plugin

    def discover_plugins(self, dirname: str | Path, modname: str | None = None) -> None:
        """
        Discover and register all plugins.

        This method uses the plugin finder and loader to find all plugins within a directory and
        then registers them with the codex.

        :param dirname: root directory to scan for plugins
        """
        for loc in self.finder.discover(Path(dirname), modname):
            self.loader.load_module(self, loc)

    def __iter__(self) -> Iterator[_PluginT]:
        """
        Iterate over all plugins.
        """
        return iter(self._plugins.values())


class _Cincodex:
    """
    Internal singleton class that registers available codexes.
    """

    def __init__(self) -> None:
        self._namespaces: dict[str, Codex] = {}

    def register_codex(self, codex: Codex) -> None:
        """
        Register a new codex. A codex is registered by its ``namespace``, which must be
        unique. Registered codexes can be retrieved using the :func:`get_codex` method.

        :param codex: the codex to register
        """
        self._namespaces[codex.namespace] = codex

    def get_codex(self, namespace: str) -> Codex | None:
        """
        Get a registered codex by its ``namespace``.

        :param namespace: codex namespace
        :returns: the registered codex if it exists or ``None`` if it doesn't
        """
        return self._namespaces.get(namespace)


_cincodex = _Cincodex()

get_codex = _cincodex.get_codex
register_codex = _cincodex.register_codex
