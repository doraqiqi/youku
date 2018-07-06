# Author：zhaoyanqi
import json
import hashlib
import struct
import os
from conf import settings


def send_back(client,send_dic,file = None):

    print('发送内容',send_dic)
    send_json = json.dumps(send_dic)
    send_byte = send_json.encode('utf-8')
    client.send(struct.pack('i',len(send_byte)))
    client.send(send_byte)

    #如果传了文件路径就传文件
    if file:
        with open(file,'rb') as f:
            for line in f:
                client.send(line)


    head = client.recv(4)
    head_len = struct.unpack('i',head)[0]
    back_bytes = client.recv(head_len)
    back_dict=json.loads(back_bytes.decode('utf-8'))
    print('接受内容',back_dict)
    return back_dict

def get_md5(password):
    hd = hashlib.md5()
    hd.update(password.encode('utf-8'))
    return hd.hexdigest()

def get_upload_movie_list():
    movie_list = os.listdir(settings.BASE_UPLOAD_MOVIE)
    return movie_list

def get_file_md5(file_path):
    if os.path.exists(file_path):
        md = hashlib.md5()
        filesize = os.path.getsize(file_path)
        #把文件分成了四段：
        file_list = [0,filesize // 3,(filesize // 3)*2,filesize-10]
        with open(file_path,'rb') as f:
            for li in file_list:
                f.seek(li)
                md.update(f.read(10))
            return md.hexdigest()

