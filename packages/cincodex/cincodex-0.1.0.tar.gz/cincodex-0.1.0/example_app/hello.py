from cincodex import Codex, PluginMetadata, register_codex


# First we create a custom plugin metadata class, inheriting from cincodex `PluginMetadata`
class HelloPluginMetadata(PluginMetadata):
    def __init__(self, id: str, *, lang: str):
        super().__init__(id)
        self.lang = lang


# Our plugin system will be class based. So, next we create a base class that all plugins must
# inherit from and implement the `say_hello` method.
class HelloPlugin:
    # __plugin_metadata__ is always set by cincodex with the call to `Codex.register`. We include
    # the field here so that the IDE / type checking knows that __plugin_metadata__ is a class
    # attribute.
    __plugin_metadata__: HelloPluginMetadata

    def say_hello(self) -> None:
        raise NotImplementedError()


# Create and register the codex
codex: Codex[type[HelloPlugin], HelloPluginMetadata] = Codex('hello', HelloPluginMetadata)
register_codex(codex)
