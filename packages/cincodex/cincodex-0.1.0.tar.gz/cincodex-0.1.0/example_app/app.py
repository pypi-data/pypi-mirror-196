if __name__ == '__main__':
    try:
        import cincodex  # noqa: F401
    except ImportError:
        import sys
        from pathlib import Path

        sys.path.append(str(Path(__file__).parents[1]))

    from hello import HelloPluginMetadata, codex

    # Discover builtin and contributed plugins
    codex.discover_plugins('./builtin_plugins')
    codex.discover_plugins('./contrib_plugins')

    # iterate over all available plugins
    for plugin_cls in codex:
        # `plugin_cls` is a type[HelloPlugin]
        # get the plugin metadata
        metadata = HelloPluginMetadata.get(plugin_cls)
        # our codex registers plugin *classes*, so we need to first instantiate an instance of this
        # plugin
        plugin = plugin_cls()
        print(f'Running plugin: {metadata.id} (lang: {metadata.lang})')
        plugin.say_hello()
        print()
