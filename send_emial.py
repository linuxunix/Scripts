# coding: utf-8
import smtplib
from email.mime.multipart import MIMEMultipart  # 导入MIMEMultipart类
from email.mime.text import MIMEText  # 导入MIMEText类
from email.mime.image import MIMEImage  # 导入MIMEImage类

HOST = "smtp.139.com"  # 定义smtp主机
SUBJECT = u"网站日报"  # 定义邮件主题
TO = "xx@qq.com"  # 定义邮件接收人
FROM = "xx@139.com"  # 定义邮件发件人


msg = MIMEMultipart('related')  # 创建MIMEMultipart对象，采用related定义内嵌资源

# 创建一个MIMEText对象，附加文档,win下需要添加r
attach = MIMEText(open(r"路径路径", "r").read(), "base64", "utf-8")
attach["Content-Type"] = "application/octet-stream"  # 指定文件格式类型
msgtext = MIMEText("""   正文内容
""", "html", "utf-8")

msg.attach(msgtext)  # MIMEMultipart对象附加MIMEText的内容

# 指定Content-Disposition值为attachment则出现下载保存对话框，保存的默认文件名使用
attach["Content-Disposition"] = "attachment; filename=\"发送文件名\"".decode("utf-8").encode("gb18030")
msg.attach(attach)  # MIMEMultipart对象附加MIMEText附件内容
msg['Subject'] = SUBJECT  # 邮件主题
msg['From'] = FROM  # 邮件发件人,邮件头部可见
msg['To'] = TO  # 邮件收件人,邮件头部可见

try:
    server = smtplib.SMTP()  # 创建一个SMTP()对象
    server.connect(HOST, "25")  # 通过connect方法连接smtp主机
    server.starttls()  # 启动安全传输模式
    server.login("xx@139.com", "密码")  # 邮箱账号登录校验
    server.sendmail(FROM, TO, msg.as_string())  # 邮件发送
    server.quit()  # 断开smtp连接
    print "邮件发送成功！"
except Exception, e:
    print "失败：" + str(e)
