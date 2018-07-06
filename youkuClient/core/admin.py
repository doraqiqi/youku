# Author：zhaoyanqi
import socket,json
import struct
from lib import commcon
from tcpClient import tcpclient
import os
from conf import settings


user_data = {
    'session':None,
}

def admin_register(client):
    while True:
        name = input('请输入用户名：').strip()
        password = input('请输入密码:').strip()
        cof_password = input('请确认密码：').strip()
        if password == cof_password:
            user_dic = {'type':'register','name':name,'password':commcon.get_md5(password),'user_type':'admin'}
            back_dic = commcon.send_back(client,user_dic)
            if back_dic['flag']:
                # print(back_dic)
                # user_data['session'] = back_dic['session']
                print(back_dic['msg'])
                break
            else:
                print(back_dic['msg'])
        else:
            print('两次密码不一致')

def admin_login(client):
    while True:
        name = input('input user name:').strip()
        password = input('input password:').strip()
        send_dic = {'type':'login','name':name,'password':commcon.get_md5(password),'user_type':'admin'}
        back_dic = commcon.send_back(client,send_dic)
        if back_dic['flag']:
            user_data['session'] = back_dic['session']
            print(back_dic['msg'])
            break
        else:
            print(back_dic['msg'])

def release_notice(client):
    if not user_data['session']:
        print('请先登录')
        return
    while True:
        name = input('请输入公告标题：').strip()
        content = input('请输入公告内容').strip()
        send_dic = {'type':'release_notice','notice_name':name,'content':content,'session':user_data['session']}
        back_dic = commcon.send_back(client,send_dic)
        if back_dic['flag']:
            print(back_dic['msg'])
            break
        else:
            print(back_dic['msg'])

def delete_movie(client):
    if not user_data['session']:
        print('请先登录')
        return
    while True:
        send_dic = {'type':'check_movie_list','session':user_data['session'],'movie_type':'all'}
        back_dic = commcon.send_back(client,send_dic)
        print('删除电影',back_dic)
        if not back_dic['flag']:
            print(back_dic['msg'])
            break
        movie_list = back_dic['back_movie_list']
        if not movie_list:
            print('暂无影片')
            break
        for i,movie in enumerate(movie_list):
            print('%s : 电影名：%s 是否免费：%s'%(i,movie[0],movie[1]))
        choice = input('选择要删除的电影：').strip()
        if choice.isdigit():
            choice = int(choice)
            movie_name =movie_list[choice][0]
            send_dic = {'type':'delete_movie','session':user_data['session'],'movie_name':movie_name}
            back_dic = commcon.send_back(client,send_dic)
            if back_dic['flag']:
                print(back_dic['msg'])
                break
            else:
                print(back_dic['msg'])
        else:
            print('输入数字')

def upload_movie(client):
    if not user_data['session']:
        print('请先登录')
        return
    movie_list = commcon.get_upload_movie_list()
    if not movie_list:
        print('暂无可上传影片')
    for i,movie in enumerate(movie_list):
        print('%s: %s'%(i,movie))

    choice = input('输入要上传的影片序号：').strip()
    if choice.isdigit():
        choice = int(choice)
        #收费免费，文件大小，md5，文件名

        is_free = input('是否免费：（y/n）').strip()
        if is_free == 'y':
            movie_is_free = 1
        else:
            movie_is_free = 0

        file_path = os.path.join(settings.BASE_UPLOAD_MOVIE,movie_list[choice])
        filesize = os.path.getsize(file_path)

        send_dic = {'type':'upload_movie','session':user_data['session'],
                    'is_free':movie_is_free,
                    'file_md5':commcon.get_file_md5(file_path),
                    'file_name':movie_list[choice],
                    'filesize':filesize,
                    }
        back_dic = commcon.send_back(client,send_dic,file_path)
        if back_dic['flag']:
            print(back_dic['msg'])
        else:
            print(back_dic['msg'])


func_dic = {
    '1':admin_register,
    '2':admin_login,
    '3':upload_movie,
    '4':delete_movie,
    '5':release_notice
}

def admin_view():
    client = tcpclient.get_client()
    while True:
        print('''
        1 注册
        2 登录
        3 上传视频
        4 删除视频
        5 发布公告
        
        ''')

        choice = input('请选择功能：').strip()
        if choice == 'q':break
        if choice not  in func_dic:continue
        func_dic[choice](client)