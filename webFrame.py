# coding=utf-8
from view import *

# 设置静态文件夹路径

STATIC_DIR = "./static"


# 应用
class Application(object):

    def __init__(self, urls):
        self.urls = urls

    def __call__(self, env):
        method = env.get("METHOD", "GET")
        path = env.get("PATH_NAME", "/")
        if method == 'GET':
            if path == '/' or path[-5:] == '.html':
                response = self.get_htmnl(path)

            else:
                response = self.get_data(path)
            return response
        elif method == 'POST':
            pass

    def get_htmnl(self, path):
        if path == '/':
            page = STATIC_DIR + '/index.html'
        else:
            page = STATIC_DIR + path
        try:
            f = open(page, 'rb')
        except IOError:
            # 没有找到网页
            response_headers = "HTTP/1.1 400 not found\r\n"
            response_headers += "\r\n"
            response_body = """
                            =============================
                            Sorry the page not found=====
                            =============================
            """
        else:
            response_body = f.read().decode()
            response_headers = "HTTP/1.1 200 OK\r\n"
            response_headers += "Content - Type: text/html\r\n"
            response_headers += '\r\n'
            f.close()
        finally:
            response_text = response_headers + response_body
            return response_text

    def get_data(self, path):
        for url, handler in self.urls:
            if path == url:
                rh = "HTTP/1.1 200 OK\r\n"
                rh += "\r\n"
                rb = handler()
                return rh + rb
        rh = "HTTP/1.1 400 not found\r\n"
        rh += "\r\n"
        rb = "Sorry not found"
        return rh + rb


urls = [
    ('/time', show_time),
    ('/hello', say_hello),
    ('/bye', say_bye)
]
app = Application(urls)
