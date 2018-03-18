# _*_ coding:utf-8 _*_

ip = '0.0.0.0'

port = '21'

# 上传速度300kb/s
max_upload = 300*1024

# 下载速度300kb/s
max_download = 300*1024

# 最大链接数
max_cons = 150

# 最多ip数
max_per_ip = 10

# 被动端口范围，被动端口数量要比最大ip数多
passive_ports = (2000, 2200)

# 是否开启匿名访问 on|off
enable_anonymous = 'off'

# 匿名用户登录
anonymous_path = 'E:/python/Pycharm/train1'

# 是否开启日志 on|off
enable_logging = 'off'

# 日志文件
loging_name = 'pyftp.log'

# 欢迎信息
welcome_msg = 'Welcome to my ftp'
