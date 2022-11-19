import ssl
import sys
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer


# 单线程HTTPS Server
class HTTPSServer(HTTPServer):
    def __init__(self, server_address: tuple[str, int], request_handler_class,
                 cert_file: str, key_file: str, password: str, **kwargs):
        """
        用于创建单线程HTTPS服务器
        :param server_address: tuple[str, int]，ip和端口
        :param request_handler_class: 继承自BaseHTTPRequestHandler的类，并非实例
        :param cert_file: 证书路径
        :param key_file: 私钥路径
        :param password: 证书密码，没有密码设置空字符串
        :param kwargs: 其他参数，会直接传递给父类(HTTPServer)
        """
        # 继承HTTPServer
        super().__init__(server_address, request_handler_class, **kwargs)

        # 创建ssl上下文，装饰socket为ssl_socket，并替换原来的socket
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file, password)
        ssl_socket = context.wrap_socket(self.socket, server_side=True)
        self.socket = ssl_socket

    # 重载exit上下文管理接口
    def __exit__(self, *args):
        super().__exit__(*args)
        self.socket.close()


# 支持多线程HTTPS服务器类
class ThreadingHTTPSServer(ThreadingMixIn, HTTPSServer):
    # 设置为守护线程，主线程结束子线程也会结束
    daemon_threads = True


if __name__ == '__main__':
    port = 8000
    # 创建支持多线程的https服务器，使用SimpleHTTPSRequestHandler作为请求处理类
    # SimpleHTTPSRequestHandler特点：入口文件为工作目录的index.html，缺少入口文件则表现为文件浏览器
    ssl_cert_config = ('ssl/server.crt', 'ssl/server.key', '')
    with ThreadingHTTPSServer(('0.0.0.0', port), SimpleHTTPRequestHandler, *ssl_cert_config) as httpd:
        print(f'Serving HTTPS on 0.0.0.0 port {port}')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('Keyboard interrupt received, exiting.')
            sys.exit(0)
