# _*_ coding:utf-8 _*_

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
import setting
import logging


def get_user(userfile):
    # 定义一个用户列表
    user_list = []
    # 使用with后不管with中的代码出现什么错误，都会进行对当前对象进行清理工作。
    with open(userfile) as f:
        for line in f:
            # split()通过指定分隔符对字符串进行切片，如果参数num 有指定值，则仅分隔 num 个子字符串
            print(len(line.split()))
            # 字符串开头为#且不为空
            if line:
                if len(line.split()) == 4:
                    user_list.append(line.split())
                else:
                    print('user.conf配置错误')
    return user_list


def ftp_server():
    # 实例化虚拟用户
    authorizer = DummyAuthorizer()

    # 添加用户权限和路径，括号内参数是（用户名，密码，用户目录，权限）
    # authorizer.add_user('user', '12345', 'E:\\', perm='elradfmw')
    user_list = get_user('user.txt')
    print(user_list)
    for user in user_list:
        name, passwd, permit, homedir = user
        try:
            authorizer.add_user(name, passwd, homedir, perm=permit)
        except Exception as e:
            print(e)

    # 添加匿名用户 只需要路径
    if setting.enable_anonymous == 'on':
        authorizer.add_anonymous('E:/python/Pycharm/train1')

    # 下载上传速度设置
    dtp_handler = ThrottledDTPHandler
    dtp_handler.read_limit = setting.max_download
    dtp_handler.write_limit = setting.max_upload

    # 初始化ftp句柄
    handler = FTPHandler
    handler.authorizer = authorizer

    # 日志记录
    if setting.enable_logging == 'on':
        logging.basicConfig(filename=setting.loging_name, level=logging.INFO)

    # 欢迎信息
    handler.banner = setting.welcome_msg

    # 添加被动端口范围
    handler.passive_ports = range(setting.passive_ports[0], setting.passive_ports[1])

    # 监听ip和端口
    server = FTPServer((setting.ip, setting.port), handler)

    # 最大链接数
    server.max_cons = setting.max_cons
    server.max_cons_per_ip = setting.max_per_ip

    # 开始服务
    print('开始服务')
    server.serve_forever()


if __name__ == "__main__":
    ftp_server()