# Author：zhaoyanqi

from tcpClient import tcpclient
from lib import commcon
import time
import os
from conf import settings

user_data = {
    'session':None,
    'is_vip':None,
}
send_dic = {'type': None, 'user_type': 'user', 'session': None}

def user_register(client):
    while True:
        name = input('请输入用户名：').strip()
        password = input('请输入密码:').strip()
        cof_password = input('请确认密码：').strip()
        if password == cof_password:
            user_dic = {'type':'register','name':name,'password':commcon.get_md5(password),'user_type':'user'}
            back_dic = commcon.send_back(client,user_dic)
            if back_dic['flag']:
                print(back_dic['msg'])
                break
            else:
                print(back_dic['msg'])
        else:
            print('两次密码不一致')

def user_login(client):
    while True:
        name = input('input user name:').strip()
        password = input('input password:').strip()
        send_dic = {'type':'login','name':name,'password':commcon.get_md5(password),'user_type':'user'}
        back_dic = commcon.send_back(client,send_dic)
        if back_dic['flag']:
            user_data['session'] = back_dic['session']
            user_data['is_vip'] = back_dic['is_vip']
            print(back_dic['msg'])
            print(back_dic['last_notice'])
            break
        else:
            print(back_dic['msg'])
            break

def buy_member(client):
    print('购买会员')
    print('暂未完成')
    return
    # if not user_data['session']:
    #     print('请先登录')
    #     return
    # if user_data['is_vip']:
    #     print('您已经是会员了')
    #     return
    #
    # buy = input('sure to buy member(y/n): ').strip()
    # if buy == 'y':
    #     send_dic = {'type':'buy_member','session':user_data['session']}
    #     back_dic = commcon.send_back(client,send_dic)
    #     if back_dic['flag']:
    #         user_data['is_vip'] = 1
    #         print(back_dic['msg'])
    #     else:
    #         print(back_dic['msg'])
    # else:
    #     print('没有购买会员')


def download_free_movie(client):
    if not user_data['session']:
        print('请先登录')
        return
    while True:
        send_dic = {'type':'check_movie_list',
                    'session':user_data['session'],
                    'movie_type':'free'}
        back_dic = commcon.send_back(client,send_dic) #获得查的电影的列表
        if back_dic['flag']:
            back_movie_list = back_dic['back_movie_list']
            for i,movie in enumerate(back_movie_list):
                print('%s:电影名：%s'%(i,movie[0]))

            choice = input('请选择要下载的电影：').strip()
            if choice == 'q':break
            if choice.isdigit():
                choice = int(choice)
                if not choice >= len(back_movie_list):
                    send_dic = {'type':'download_movie',
                                'session':user_data['session'],
                                'movie_name':back_movie_list[choice][0],
                                # 'user_name':pass,
                                }
                    back_dic = commcon.send_back(client,send_dic)
                    if back_dic['flag']:
                        print('请等待:%s' % back_dic['wait_time'])
                        time.sleep(back_dic['wait_time'])
                        recv_size = 0
                        file_name = back_dic['movie_name']
                        file_path = os.path.join(settings.BASE_DOWNLOAD_MOVIE, file_name)
                        with open(file_path, 'wb') as f:
                            while recv_size < back_dic['movie_size']:
                                recv_data = client.recv(1024)
                                f.write(recv_data)
                                recv_size += len(recv_data)
                        print('下载成功！')
                        break
                    else:
                        print(back_dic['msg'])

            else:
                print('非数字')
        else:
            print(back_dic['msg'])

def check_download_record(client):

    send_dic = {'type':'check_download_record','session':user_data['session']}
    back_dic = commcon.send_back(client,send_dic)
    if back_dic['flag']:
        print(back_dic['movie_list'])

def check_movie(client):
    send_dic = {'type':'check_movie_list','session':user_data['session'],'movie_type':'all'}
    back_dic = commcon.send_back(client,send_dic)
    if back_dic['flag']:
        back_movie_list = back_dic['back_movie_list']
        for movie in back_movie_list:
            print('名字 ：%s ,是否免费：%s'%(movie[0],movie[1]))
    else:
        print(back_dic['msg'])

def download_charge_movie(client):
    if not user_data['session']:
        print('请先登录')
        return
    while True:
        send_dic = {'type':'check_movie_list',
                    'session':user_data['session'],
                    'movie_type':'charge'}
        back_dic = commcon.send_back(client,send_dic) #获得查的电影的列表
        if back_dic['flag']:
            back_movie_list = back_dic['back_movie_list']
            for i,movie in enumerate(back_movie_list):
                print('%s:电影名：%s'%(i,movie[0]))

            choice = input('请选择要下载的电影：').strip()
            if choice == 'q':break
            if choice.isdigit():
                choice = int(choice)
                if not choice >= len(back_movie_list):

                    if user_data['is_vip']:
                        charge = input('请缴费5元(y/n)').strip()
                    else:
                        charge = input('请缴费10元(y/n)').strip()
                    if not charge == 'y':
                        print('没交费')
                        break

                    send_dic = {'type':'download_movie',
                                'session':user_data['session'],
                                'movie_name':back_movie_list[choice][0],
                                'movie_type':'charge_movie'
                                # 'user_name':pass,
                                }
                    back_dic = commcon.send_back(client,send_dic)
                    if back_dic['flag']:

                        recv_size = 0
                        file_name = back_dic['movie_name']
                        file_path = os.path.join(settings.BASE_DOWNLOAD_MOVIE, file_name)
                        with open(file_path, 'wb') as f:
                            while recv_size < back_dic['movie_size']:
                                recv_data = client.recv(1024)
                                f.write(recv_data)
                                recv_size += len(recv_data)
                        print('下载成功！')
                        break
                    else:
                        print(back_dic['msg'])
            else:
                print('非数字')
        else:
            print(back_dic['msg'])

def check_notice(client):
    send_dic = {'type':'check_notice','session':user_data['session']}
    back_dic = commcon.send_back(client,send_dic)
    if back_dic['flag']:
        for notice in back_dic['back_notice_list']:
            print(notice)
    else:
        print(back_dic['msg'])


func_dic = {
    '1':user_register,
    '2':user_login,
    '3':buy_member,
    '4':check_movie,
    '5':download_free_movie,
    '6':download_charge_movie,
    '7':check_download_record,
    '8':check_notice,
}

def user_view():
    client = tcpclient.get_client()
    while True:
        print('''
        1 注册
        2 登录
        3 冲会员
        4 查看视频
        5 下载免费视频
        6 下载收费视频
        7 查看观影记录
        8 查看公告
        ''')
        choice = input('请选择功能：').strip()
        if choice == 'q': break
        if choice not in func_dic: continue
        func_dic[choice](client)

