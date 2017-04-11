# coding:utf-8
# /usr/bin/python
import smtplib
import string
import os,sys
from subprocess import Popen, PIPE
import time

Service_start_cmd = ("执行启动命令")

def Check_Port(port):
    cmd_output = Popen("lsof -i:{0}".format(port), shell=True, stdout=PIPE, stderr=PIPE).communicate()
    if  'LISTEN' not in str(cmd_output):
        data = '{0}端口没有启动'.format(port)
        Log_Write(data)
        os.system(Service_start_cmd)
    # Send_Email(data,data)

def Send_Email(SUBJECT,text):
    HOST = "smtp.qq.com"  # 定义smtp主机
    SUBJECT = SUBJECT # 定义邮件主题
    TO = "test@qq.com"  # 定义邮件收件人
    FROM = "mymail@gmail.com"  # 定义邮件发件人
    text = text # 邮件内容
    BODY = string.join((  # 组装sendmail方法的邮件主体内容，各段以"\r\n"进行分隔
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "", text
    ), "\r\n")
    try:
        server = smtplib.SMTP()  # 创建一个SMTP()对象
        server.connect(HOST, "25")  # 通过connect方法连接smtp主机server.starttls()    #启动安全传输模式
        server.login("mymail@gmail.com", "密码")  # 邮箱账号登录校验server.sendmail(FROM, [TO], BODY)    #邮件发送
        server.quit()  # 断开smtp连接
    except Exception, e:
        Log_Write("发送失败"+str(e))

def Log_Write(str):
    date_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    pwd = os.getcwd()
    with open(pwd+'/'+sys.argv[0]+'_log','a') as f:
        f.write(date_time+'       '+str+'\n')

if __name__ == '__main__':
    Check_Port(sys.argv[1])


