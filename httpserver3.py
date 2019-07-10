# coding=utf-8

"""
name: minno
time: 2019/7/6
function: httpserver
"""
from socket import *
import sys
import re
from threading import Thread
from config import *


# 处理http请求类
class HTTPServer(object):

    def __init__(self, applet):
        """
        创建套接字
        """
        self.application = applet
        self.host, self.port = None, None
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def bind(self, host, port):
        """
        绑定地址
        :param host:
        :param port:
        :return:
        """
        self.port = port
        self.host = host
        self.sock.bind((self.host, self.port))

    def client_handler(self, conn):
        """
        接受浏览器请求
        :param conn:
        :return:
        """
        request = conn.recv(4096).decode()
        print(request)
        # 可以分析请求头和请求体
        request_lines = request.splitlines()
        # 获取请求头
        try:
            request_line = request_lines[0].split(' ')
            print(request_line)
            method = request_line[0]
            filename = request_line[1]
            # 将解析内容合成字典给web frame使用
            evn = {'METHOD': method, 'PATH_NAME': filename}
            print(evn)
        except:
            response_headers = 'HTTP/1.1 500 SERVER ERROR\r\n'
            response_headers += '\r\n'
            response_body = """
                            =======================
                            ERROR =================
                            =======================
            """
            conn.send((response_headers+response_body).encode())
        # 将env给Frame处理，得到返回内容
        response = self.application(evn)

        if response:
            conn.send(response.encode())
            conn.close()

    def server_forever(self):
        self.sock.listen(10)
        print("Listen the port {}".format(self.port))
        while True:
            conn, addr = self.sock.accept()
            print("Connect from {}".format(addr))
            handle_client = Thread(target=self.client_handler, args=(conn,))
            handle_client.start()


if __name__ == '__main__':
    # 将要导入的模块导入
    sys.path.insert(1, MODULE_PATH)
    m = __import__(MODULE)
    # getattr(obj,attr) 获取一个对象的属性 obj对象 attr属性 返回属性值
    application = getattr(m, APP)

    httpd = HTTPServer(application)
    httpd.bind(HOST, PORT)
    httpd.server_forever()