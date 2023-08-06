## 使用方式

#### 发布地址：

github地址  https://github.com/majormj/snemail

gitee 地址 https://gitee.com/manjim/snemail

#### 测试环境

目前测试支持的python版本3.6，和python 3.11
如果登录失败遇到错误 con 不存在，可尝试修改python版本的判断范围尝试（ssl的校验方式）

````python
def mail_login(self,user="",password=""):
    """登录邮箱"""

    self.emailCome = user       # 邮件的时间发送人（发邮件的时候调用）
    self.loginStatus = False    # 登录结果状态
    try:
        # 1、链接邮箱服务器(带 SSL 启用安全机制) # 端口号：465/25
        # 1.1 判断python版本
        vamax = sys.version_info.major   #  大版本号例如3.6.8  则表示3
        vsmin = sys.version_info.minor   #  小版本号例如3.6.8  则表示6

        if vamax == 3 and vsmin < 10:  #  python 版本号等于3，小版本号小于10

            self.con = smtplib.SMTP_SSL(self.server,self.port) 

        else:
            """ Python 3.10 及以上版本使用"""
            import ssl
            ctx = ssl.create_default_context()
            ctx.set_ciphers('DEFAULT')
            self.con = smtplib.SMTP_SSL(self.server,port=self.port, context = ctx)

        # 2、登录邮箱 # 链接对象.login(账号、密码)
        self.con.login(user,password) 
        self.loginStatus = True
        return '邮箱登录成功'
    except SMTPAuthenticationError as e:
        return '登录失败，请检查账户密码是否正确，或者尝试授权码登录%s'%repr(e)
    except Exception as error:
        return '邮箱登录遇到错误：%s'%repr(error)
````



#### 依赖说明

包依赖 smtplib 模块，和 email 模块，这两个库在python11中是标准库。如果在其他python中不存在折两个库
直接 pip install smtplib 可能安装失败，可以试下安装 PyEmail，但是这个没试过不确定能不能用

```shell
pip install  PyEmail
```

#### 安装包

```shell
# 安装库到最新版本
pip install --upgrade snemail
```

#### 使用方式

```python
# 引入包
from snemail import SnEmail

# 邮件服务器
server  = 'smtp.sina.net'

# 邮件端口
port    = 465

if __name__ == '__main__':
    # 初始化
    sn = SnEmail(server,port)

    # 设置邮件主题
    sn.mail_title(title="测试邮件")

    # 设置邮件正文内容，支持 文本 和thml格式 ，
    """
    添加邮件内容 参数说明
    content : 邮件内容
    ctype   : 邮件类型 plain 文本类型；html 为HTML类型；base64(二进制文件，也就是附件)
    encode  : 编码方式，默认 'utf-8'
    """
    sn.mail_content("文本内容1")
    sn.mail_content("文本内容2")


    # 将图片以内容形式添加到邮件正文，图片地址字符串类型
    sn.mail_image(image_path="图片地址1")
    sn.mail_image(image_path="图片地址2")

    # 添加邮件附件（中英文文件名都支持），传入参数 files 必须是列表
    sn.mail_file([r"C:\Users\manji\Downloads\全量商品列表.xlsx"])

    # 登录邮箱
    print(sn.login(user="",password=""))

    # 发送邮件，扩展参数可查看函数提示
    """
    发送邮件
    emailTo       收件人列表
    emailCC       抄送人列表
    emailNoSend   不发送的对象（会显示，实际不发送）
    emailComeShow 显示的发件人（和实际发件人可能不是同一个）
    """
    print(sn.mail_send(emailTo=['']))
```

