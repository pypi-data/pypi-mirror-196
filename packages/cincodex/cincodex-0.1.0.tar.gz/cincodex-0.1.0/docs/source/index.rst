Welcome to cincodex's documentation!
====================================


Cincodex is a simple, flexible, and unopinionated plugin system for Python projects. Cincodex is designed for both applications and libraries that wish to be extensible at runtime. Plugins can be any Python object including a class, a function, or an instance of an object. The following is a very basic example showing that the application creates a Codex, which is the plugin system, then discovers all available plugins within the ``./plugins`` directory, and the ``./plugins/foo/bar.py`` source file registers a function with the codex.

.. code-block:: python

   # app.py
   from cincodex import Codex, register_codex

   codex = Codex('my_app')
   register_codex(codex)

   codex.discover_plugins('./plugins')
   # after this, the `foo.bar` plugin is available and we can call it.
   codex.get('foo.bar')()
   # 'Hello world!'


   # ./plugins/foo/bar.py
   from app import codex

   @codex.register
   @codex.metadata(id='foo.bar')
   def foo_bar_plugin():
      print('Hello world!')


Cincodex has been tested on Linux and Windows systems but should support other operating systems as well. Cincodex supports Python 3.10 and newer.

Usage
-----

Plugin Types
^^^^^^^^^^^^

Its common that plugins must implement some uniform API by subclassing a base plugin class. Cincodex internally uses a type variable and doesn't care what the plugin type is. However, if you want to keep your type checking and IDE happy, you can specify a type hint when creating a codex:

.. code-block:: python

   # app.py
   from cincodex import Codex, register_codex, PluginMetadata

   class ApplicationPlugin:
      def run(self) -> None:
         raise NotImplementedError()


   codex: Codex[type[ApplicationPlugin], PluginMetadata] = Codex('my_app')
   register_codex(codex)

   # after discovering plugins, get one and run it:
   plugin_cls = codex.get('foo.bar')  # returns a `ApplicationPlugin` type.
   plugin = plugin_cls()  # instantiate the plugin
   plugin.run()  # run the plugin


The type hints is only meant to improve your experience and are not type checked at runtime. Additionally, a single codex can contain multiple types of plugins.

The type hint also works for functions and object instances, for example:

**Functions**

.. code-block:: python

   # app.py

   # plugins are functions that accept a string and return a number
   codex: Codex[Callable[[str], int], PluginMetadata] = Codex('my_app')
   func = codex.get('foo.bar')
   ans = func('hello world')
   print(ans)

   # plugins/foo/bar.py
   from app import codex

   @codex.register
   @codex.metadata(id='foo.bar')
   def foo_bar_plugin(message: str) -> int:
      return len(message)

**Objects**

.. code-block:: python

   # app.py

   # plugins are dictionaries
   codex: Codex[dict[str, Callable], PluginMetadata] = Codex('my_app')
   mapping = codex.get('foo.bar')
   ans = mapping['say_hello']()
   print(ans)

   # plugins/foo/bar.py
   from app import codex

   FOO_BAR_PLUGIN = {
      'say_hello': lambda: 'Hello world!'
   }

   # Because we can't use a decorator here, we call `PluginMetadata.bind`, which is what the
   # decorator does.
   codex.metadata(id='foo.bar').bind(FOO_BAR_PLUGIN)
   codex.register(FOO_BAR_PLUGIN)

Metadata
^^^^^^^^

Each plugin must have plugin metadata bound to it. The default :class:`~cincodex.PluginMetadata` class contains a single metadata attribute: a unique plugin ``id``. ``PluginMetadata`` can be subclassed to add additional application-specific metadata:

.. code-block:: python

   # app.py
   from cincodex import Codex, PluginMetadata, register_codex


   class AppPluginMetadata:
      def __init__(self, id: str, *, author: str, version: str):
         super().__init__(id)
         self.author = author
         self.version = version


   codex = Codex('my_app', AppPluginMetadata)
   register_codex(codex)

   codex.discover_plugins('./plugins')

   # get the `foo.bar` plugin and then get its metadata
   plugin = codex.get('foo.bar')
   metadata = AppPluginMetadata.get(plugin)
   # The metadata is also available in the `plugin.__plugin_metadata__` attribute.
   print('foo.bar plugin:')
   print(f'  author:  {metadata.author}')
   print(f'  version: {metadata.version}')


   # ./plugins/foo/bar.py
   from app import codex

   @codex.register
   @codex.metadata(
      'foo.bar',
      author='Acme, Inc.',
      version='1.0.0'
   )
   class FooBarPlugin:
      pass

Bundle Plugins
^^^^^^^^^^^^^^

Cincodex is designed for plugins to be defined and contained within a single Python source file. Larger and more complex plugins can be defined across multiple source files by making the plugin module a bundle. Bundle modules are named ``__bundle__`` and have special treatment within cincodex: hen a directory has a ``__bundle__`` module, no further scanning of the directory or any nested directory is performed. Essentially a bundle plugin is an entire directory tree and cannot contain more than a single plugin.

For example, the following is a simple bundle plugin that imports a several relative modules that actually perform the work:

.. code-block:: python

   # ./plugins/foo/__bundle__.py
   from app import codex

   # import modules needed by the plugin
   from .lib import do_stuff
   from .deps.third_party import six


   @codex.register
   @codex.metadata(id='foo')
   def foo_plugin():
      print('hello from foo plugin!')
      do_stuff()
      print('goodbye from foo plugin!')


   # ./plugins/foo/lib.py
   def do_stuff():
      print('doing stuff now')


The default bundle name of ``__bundle__`` can be changed by creating a :class:`~cincodex.PluginPathFinder` and passing it to the codex. For example, to load bundle plugins from the ``package`` module instead:

.. code-block:: python

   from cincodex import Codex, PluginPathFinder, register_codex

   codex = Codex('my_app', finder=PluginPathFinder(bundle_name='package'))
   register_codex(codex)


Registering a Codex
^^^^^^^^^^^^^^^^^^^

The previous examples all call :func:`~cincodex.register_codex` after creating a codex. This is so that the codex is available to all plugins without having to import it:

.. code-block:: python

   # app.py
   from cincodex import Codex, register_codex

   codex = Codex('my_app')
   register_codex(codex)


   # ./plugins/foo/bar.py
   from cincodex import get_codex

   codex = get_codex('my_app')

   @codex.register
   @codex.metadata(id='foo.bar')
   def foo_bar_plugin():
      # just like the other examples
      pass


Without the call to ``register_codex()``, plugins will have to import the codex directly and will not be able to get it via :func:`~cincodex.get_codex`. Registering the codex is optional if you want to make the codex private.

Listing and Retrieving Plugins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once registered, there are several methods of listing and getting specific plugins from the codex.

**Listing**

The codex implements ``__iter__`` which returns an iterator to all discovered plugins:

.. code-block:: python

   for plugin in codex:
      metadata = PluginMetadata.get(plugin)
      print('plugin:', {plugin})
      print('  id:', metadata.id)
      print()

**Get by id**

Each plugin must have a unique id which is specified in the call to the plugin metadata. To retrieve a plugin by its unique id, use the :meth:`codex.get <cincodex.Codex.get>` method.

.. code-block:: python

   plugin = codex.get('foo.bar')
   metadata = PluginMetadata.get(plugin)
   print('plugin:', {plugin})
   print('  id:', metadata.id)
   print()

**Find by criteria**

Find a list of plugins that match a set of criteria by calling the :meth:`codex.find <cincodex.Codex.find>` method. The method accepts two types of criteria:

- ``*plugin_filters`` - a list of functions or lambdas that accept the plugin and return ``True`` if the plugin matches the criteria.
- ``**metadata_criteria`` - a dictionary where the key is the attribute name being filtered and the value being the attribute value that the plugin metadata must have.

For example, to find all plugins that are a subclass of ``AppPlugin`` and have an author of ``Acme, Inc``:

.. code-block:: python

   for plugin in codex.find(lambda plugin: issubclass(plugin, AppPlugin), author='Acme, Inc'):
      metadata = PluginMetadata.get(plugin)
      print('plugin:', {plugin})
      print('  id:', metadata.id)
      print()

``codex.find()`` returns a list of plugins that match all the provided criteria. Use the :meth:`codex.find_one <cincodex.Codex.find_one>`` method to find the first plugin that matches all of the search criteria.

.. code-block:: python

   plugin = codex.find_one(lambda plugin: issubclass(plugin, AppPlugin), author='Acme, Inc')
   metadata = PluginMetadata.get(plugin)
   print('plugin:', {plugin})
   print('  id:', metadata.id)
   print()

Use ``codex.find_one()`` when searching based on a unique set of criteria.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
