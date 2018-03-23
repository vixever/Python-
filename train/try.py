# _*_coding:utf-8 _*_

import BaseHTTPServer
import sys, os
import subprocess


class base_case(object):
    # 条件处理基类

    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(full_path, msg)
            handler.handle_error(msg)

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')
    # 要求子类必须实现该接口

    def test(self, handler):
        assert False, 'Not implemented'

    def act(self, handler):
        assert False, 'Not implemented'


class case_no_file(object):
    # 该路径不存在

    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))


class case_existing_file(base_case):
    # 该路径是文件

    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self,handler):
        self.handle_file(handler, handler.full_path)


class case_always_fail(object):
    # 所有情况都不符合的默认处理类

    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))


class case_directory_index_file(base_case):

    # 判断目标路径是否是目录以及目录下是否有index.html
    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
                os.path.isfile(self.index_path(handler))

    # 响应index.html的内容
    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))


class case_cgi_file(base_case):
    # 脚本文件处理

    def test(self, handler):
        return os.path.isfile(handler.full_path) and \
                handler.full_path.endswith('.py')

    def act(self, handler):
        # 运行脚本文件
        self.run_cgi(handler)

    def run_cgi(self, handler):
        '''父进程等待子进程完成
        返回子进程向标准输出的输出结果
        检查退出信息，如果returncode不为0，则举出错误subprocess.CalledProcessError，
        该对象包含有returncode属性和output属性，output属性为标准输出的输出结果，
        可用try…except…来检查'''
        data = subprocess.check_output(['python', handler.full_path])
        handler.send_content(data)


class ServerException(Exception):
    # 服务器内部错误
    pass


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    # 处理请求并返回页面

   # 页面模板
    """Page = '''\
    <html>
    <body>
    <table>
    <tr>  <td>Header</td>        <td>Value</td>         </tr>
    <tr>  <td>Date and time</td> <td>{date_time}</td>   </tr>
    <tr>  <td>Client host</td>   <td>{client_host}</td> </tr>
    <tr>  <td>Client port</td>   <td>{client_port}</td> </tr>
    <tr>  <td>Command</td>       <td>{command}</td>     </tr>
    <tr>  <td>Path</td>          <td>{path}</td>        </tr>
    </table>
    </body>
    </html>
    '''
"""

    Cases = [case_no_file(),
             case_cgi_file(),
             case_directory_index_file(),
             case_existing_file(),
             case_always_fail()]

    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """

    # 处理一个GET请求
    def do_GET(self):
        try:

            # 得到完整的请求路径
            self.full_path = os.getcwd() + self.path

            # 遍历所有的情况并处理
            for case in self.Cases:
                if case.test(self):
                    case.act(self)
                    break

        # 处理异常
        except Exception as msg:
            self.handle_error(msg)


    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content, 404)

    """def create_page(self):
        values = {
            'date_time': self.date_time_string(),
            'client_host': self.client_address[0],
            'client_port': self.client_address[1],
            'command': self.command,
            'path': self.path
        }
        page = self.Page.format(**values)
        return page
"""
    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header('Content-type','text/html')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()

