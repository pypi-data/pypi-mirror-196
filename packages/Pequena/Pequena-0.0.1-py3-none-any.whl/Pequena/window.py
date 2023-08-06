import webview


def say_hello():
    print('World')


def create_window(_path, _win_name="Hello World!"):
    webview.create_window(_win_name, _path)
    webview.start()
