from hello import HelloPlugin, codex


@codex.register
@codex.metadata('lang.english', lang='en-us')
class EnglishHello(HelloPlugin):
    def say_hello(self):
        name = input('What is your name? > ')
        print('Hello,', name)
