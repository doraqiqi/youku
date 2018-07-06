# Author：zhaoyanqi
import socket
import json
from  db import modles
from lib import common
from interface import common_interface,admin_interface,user_interface
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from tcpServer import user_data
import struct

conn_pool=ThreadPoolExecutor(5)
mutex=Lock()
user_data.mutex = mutex
func_dic = {
    'register':common_interface.register,
    'login':common_interface.login,
    'release_notice':admin_interface.release_notice,
    'upload_movie':admin_interface.upload_movie,
    'check_movie_list':common_interface.check_movie_list,
    'delete_movie':admin_interface.delete_movie,
    'buy_member':user_interface.buy_member,
    'download_movie':user_interface.download_move,
    'check_download_record':user_interface.check_download_record,
    'check_notice':user_interface.check_notice,


}

def get_server():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('127.0.0.1',8081))
    server.listen(5)
    while True:
        conn,addr = server.accept()
        conn_pool.submit(working,conn,addr)

def working(conn,addr):
    while True:
        try:
            head = conn.recv(4)
            if not head:break
            head_len = struct.unpack('i',head)[0]
            massage = conn.recv(head_len)
            massage_json = json.loads(massage.decode('utf-8'))
            print('接受内容',massage_json)
            massage_json['addr'] = str(addr)
            dispatch(massage_json,conn)
        except Exception as e:
            print(e)
            #当前正在与服务器通信的用户：
            #live_user = {addr:[session,user_id],addr:[session,user_id]}
            conn.close()
            user_data.mutex.acquire()
            if str(addr) in user_data.live_user:
                user_data.live_user.pop(str(addr))
            user_data.mutex.release()
            break

def dispatch(massage_json,conn):
    if massage_json['type'] in func_dic:
        print('发送来的type',massage_json['type'])
        func_dic[massage_json['type']](massage_json, conn)
    else:
        back_dic = {'flag': False, 'msg': '非合法请求！！'}
        common.send_back(back_dic, conn)

def run():
    get_server()
