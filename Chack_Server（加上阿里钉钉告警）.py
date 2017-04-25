# coding:utf-8
# /usr/bin/python
import requests
import json
import string
import os,sys
from subprocess import Popen, PIPE
import time

Service_start_cmd ="cmd启动命令"

def Check_Port(port):
    cmd_output = Popen("lsof -i:{0}".format(port), shell=True, stdout=PIPE, stderr=PIPE).communicate()
    if  'LISTEN' not in str(cmd_output):
        data = '{0}端口没有启动'.format(port)
        Log_Write(data)
        send_data= {
            "msgtype": "text",
            "at": {
                "atMobiles": [
                    "135xxx219",
                ],
                "isAtAll": 'false',
            },
            "text": {
                "content": "ELK节点中的{0},端口没有启动，正在执行启动。".format(port)
            },
        }
        Dingding_Send(send_data)
        os.system(Service_start_cmd)

def Check_Service(service):
    cmd_output=Popen("ps -ef |grep {0}|grep -v grep".format(service), shell=True, stdout=PIPE, stderr=PIPE).communicate()
    if service  not in str(cmd_output):
        data = '{0}服务没有启动'.format(service)
        Log_Write(data)
        send_data = {
            "msgtype": "text",
            "at": {
                "atMobiles": [
                    "135xxx219",
                ],
                "isAtAll": 'false',
            },
            "text": {
                "content": "ELK节点中的{0}服务没有启动，正在执行启动。".format(service)
            },
        }
        os.system(Service_start_cmd)
        Dingding_Send(send_data)


def Dingding_Send(data):
    headers = {'Content-Type': 'application/json'}
    Api_Url = 'https://oapi.dingtalk.com/robot/send?access_token=xxx'
    print requests.post(url=Api_Url, headers=headers, data=json.dumps(data)).text

def Log_Write(str):
    date_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    pwd = os.getcwd()
    with open(pwd+'/'+sys.argv[0]+'_log','a') as f:
        f.write(date_time+'       '+str+'\n')

if __name__ == '__main__':
    Check_Port(9200)
    Check_Service('elasticsearch')
