cincodex api
------------

Codex
^^^^^

.. autoclass:: cincodex.Codex
    :members:

.. autofunction:: cincodex.register_codex

.. autofunction:: cincodex.get_codex


Plugin Finders and Loaders
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: cincodex.PluginPathFinder
    :members:

.. autoclass:: cincodex.PluginPathLoader
    :members:


Plugin Metadata
^^^^^^^^^^^^^^^

.. autoclass:: cincodex.PluginMetadata
    :members:


Base Classes
^^^^^^^^^^^^

These base classes can be subclassed and customized for applications that need to change some of
the default behavior of cincodex and, specifically, the :class:`~cincodex.Codex`.

.. autoclass:: cincodex.PluginFinder
    :members:

.. autoclass:: cincodex.PluginLoader
    :members:

.. autoclass:: cincodex.ModuleLocation
    :members:
