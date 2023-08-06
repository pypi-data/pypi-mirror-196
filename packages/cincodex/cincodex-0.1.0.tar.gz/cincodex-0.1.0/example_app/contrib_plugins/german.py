from hello import HelloPlugin

from cincodex import get_codex

# We registered the codex so we don't technically need to import it
codex = get_codex('hello')


@codex.register
@codex.metadata('lang.german', lang='de')
class GermanLang(HelloPlugin):
    def say_hello(self):
        name = input('Wie heissen sie? > ')
        print('Guten tag,', name)


# cspell:ignore heissen Guten
