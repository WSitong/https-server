# https-server
a simple python https server

## 模块说明
class HTTPSServer(http.server.HTTPServer) 单线程HTTPS服务器 <br>
class ThreadingHTTPSServer(socketserver.ThreadingMixIn, HTTPSServer) 多线程HTTPS服务器
<br>
## 用法
```python
import sys
from https_server import ThreadingHTTPSServer
from http.server import SimpleHTTPRequestHandler

port = 8000
ssl_cert_config = ('ssl/server.crt', 'ssl/server.key', '')
with ThreadingHTTPSServer(('0.0.0.0', port), SimpleHTTPRequestHandler, *ssl_cert_config) as httpd:
    print(f'Serving HTTPS on 0.0.0.0 port {port}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Keyboard interrupt received, exiting.')
        sys.exit(0)
```

## OpenSSL生成自签名证书
### 安装OpenSSL
官网安装OpenSSL：
<br>
https://www.openssl.org/
<br>
Windows便携版安装OpenSSL：
<br>
http://slproweb.com/products/Win32OpenSSL.html
<br>
### 生成证书
首先使用openssl执行如下命令生成一个key
```commandline
openssl genrsa -des3 -out server.key 1024
```

建议去除key文件密码，因为每次reload nginx配置时候都要你验证这个PAM密码
```commandline
openssl rsa -in server.key -out server.key
```

根据这个key文件生成证书请求文件nginx.csr
```commandline
openssl req -new -key nginx.key -out nginx.csr
```

最后根据这2个文件生成10年crt证书文件
```commandline
openssl x509 -req -days 3650 -in nginx.csr -signkey nginx.key -out nginx.crt
```

如果需要用pfx 可以用以下命令生成
```commandline
openssl pkcs12 -export -inkey nginx.key -in nginx.crt -out nginx.pfx
```