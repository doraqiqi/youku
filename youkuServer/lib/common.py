# Author：zhaoyanqi
import json
import hashlib
import time
import os
from tcpServer import user_data
import struct


def login_auth(func):
    def wrapper(*args,**kwargs):
        for value in user_data.live_user.values():
            print(value)
            print(args[0])
            if value[0] == args[0]['session']:
                user_id = value[1]
                args[0]['user_id'] = user_id
                break
        user_id = args[0].get('user_id',None)
        if user_id:
            return func(*args,**kwargs)
        else:
            back_dic = {'flag':False,'msg':'你不是授权用户！'}
            send_back(back_dic,args[1])
    return wrapper


def send_back(back_dic,conn):
    back_byte = json.dumps(back_dic).encode('utf-8')
    conn.send(struct.pack('i',len(back_byte)))
    conn.send(back_byte)

def get_uuid(name):
    md = hashlib.md5()
    md.update(name.encode('utf-8'))
    md.update(str(time.clock()).encode('utf-8')) #获取CPU时间
    return md.hexdigest()

def get_nowtime():
    now_time = time.strftime('%Y:%m:%d %X')
    return now_time

def get_all_file(dir_path):
    return os.listdir(dir_path)







