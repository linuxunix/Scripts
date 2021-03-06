#-*- coding: utf-8 -*-
#!/usr/bin/python
import paramiko
import threading
def IP_list(ip_list):
    with open(ip_list, 'r') as f:
        ip_list = f.readlines()
        for ip in ip_list:
            cmd="echo '{0}' | passwd --stdin {1}".format(ip.strip('\n').split(' ')[3],ip.strip('\n').split(' ')[1])
            a = threading.Thread(target=ssh2, args=(ip.strip('\n').split(' ')[0], ip.strip('\n').split(' ')[1], ip.strip('\n').split(' ')[2], cmd))
            a.start()

def ssh2(ip,username,passwd,cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, passwd, timeout=15)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdin.write("Y")
        out = stderr.readlines()
        if out:
            print '========' + ip + "==================>ERROR"
            for o in out:
                print o[:-1]
        else:
            out = stdout.readlines()
            print '========' + ip + "==================>OK"
            for o in out:
                print o[:-1]
    except Exception, e:
        print '%s\tError\n' % (e)

if __name__=='__main__':
    IP_list('ip.list')
    threads = [2]



===================================================
ip_list格式
ip username 更改前密码 更改后密码

===================================================
新增日志版本

#-*- coding: utf-8 -*-
#!/usr/bin/python
import os,sys
import paramiko
import threading
def IP_list(ip_list):
    with open(ip_list, 'r') as f:
        ip_list = f.readlines()
        for ip in ip_list:
            cmd="echo '{0}' | passwd --stdin {1}".format(ip.strip('\n').split(' ')[3],ip.strip('\n').split(' ')[1])
            a = threading.Thread(target=ssh2, args=(ip.strip('\n').split(' ')[0], ip.strip('\n').split(' ')[1], ip.strip('\n').split(' ')[2], cmd))
            a.start()

def Write_log(log):
    pwd = os.getcwd()
    with open(pwd+'/'+sys.argv[0] + '_log','a') as f_log:
        f_log.write(log)

def ssh2(ip,username,passwd,cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, passwd, timeout=15)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdin.write("Y")
        out = stderr.readlines()
        if out:
            print '========' + ip + "==================>ERROR"
            Write_log( '========' + ip + "==================>ERROR\n")
            for o in out:
                print o[:-1]
                Write_log(o[:-1]+'\n')
        else:
            out = stdout.readlines()
            print '========' + ip + "==================>OK"
            Write_log('========' + ip + "==================>OK\n")
            for o in out:
                print o[:-1]
                Write_log(o[:-1]+'\n')
    except Exception, e:
        print '%s\tError\n' % (e)
        Write_log('%s\tError\n' % (e))
if __name__=='__main__':
    IP_list('ip.list')
    threads = [2]

