# Author：zhaoyanqi
from db import modles
from lib import common
from tcpServer import user_data
import os
from conf import settings
from db import dbhandler
from interface import user_interface

def register(massage_json,conn):
    name = massage_json['name']
    user = modles.User.get_obj_by_name(name=name)
    if user:
        back_dic = {'flag': False, 'msg': '用户存在'}
        common.send_back(back_dic, conn)
    else:
        password = massage_json['password']
        user_type = massage_json['user_type']
        user = modles.User(name=name, password=password, user_type=user_type, is_vip=0, locked=0)
        back_dic = {'flag': True, 'msg': '注册成功'}
        common.send_back(back_dic, conn)

def login(massage_json,conn):
    user = modles.User.get_obj_by_name(name=massage_json['name'])
    if user:
        print('这是登陆的user_type', massage_json['user_type'])
        print('这是这个用户的user_type', user.user_type)
        if massage_json['user_type'] == user.user_type:

            if user.password == massage_json['password']:
                back_dic = {'flag': True, 'msg': '登陆成功'}
                session = common.get_uuid(massage_json['name'])
                back_dic['session'] = session
                #live_user = {addr:[session,user_id],addr:[session,user_id]}
                user_data.mutex.acquire()
                user_data.live_user[massage_json['addr']] = [session,user.name]
                user_data.mutex.release()
                if user.user_type == 'user':
                    back_dic['is_vip'] = user.is_vip
                    back_dic['last_notice'] = user_interface.check_notice_by_count(1)
                common.send_back(back_dic, conn)
            else:
                back_dic = {'flag': False, 'msg': '密码错误'}
                common.send_back(back_dic, conn)
        else:
            back_dic = {'flag': False, 'msg': '登录类型错误'}
            common.send_back(back_dic, conn)
    else:
        back_dic = {'flag': False, 'msg': '用户不存在'}
        common.send_back(back_dic, conn)


@common.login_auth
def check_movie_list(massage_json,conn):
    print('this is check movie')
    movie_list = get_all_movie()
    if movie_list:
        back_movie = []
        for movie in movie_list:
            if not movie.is_delete:
                if movie.is_free:
                    type = 'Free'
                else:
                    type = 'Not Free'
                if massage_json['movie_type'] =='all':
                    back_movie.append([movie.name,type])
                elif massage_json['movie_type'] == 'free':
                    if movie.is_free:
                        back_movie.append([movie.name, type])
                else:
                    if not movie.is_free:
                        back_movie.append([movie.name,type])

        if back_movie:
            back_dic = {'flag':True,'msg':'查询成功','back_movie_list':back_movie}
        else:
            back_dic = {'flag':False,'msg':'暂无电影'}
    else:
        back_dic = {'flag': False, 'msg': '暂无电影'}
    common.send_back(back_dic,conn)

def get_all_movie():
    movie_db_path = os.path.join(settings.DB_PATH,'movie')
    movie_file_list = common.get_all_file(movie_db_path)
    print(movie_file_list)
    movie_list = []
    # aa3 = dbhandler.select('aa3','movie')
    # print(aa3)
    for movie in movie_file_list:
        movie_list.append(dbhandler.select(movie,'movie'))
    return movie_list

# if __name__ == '__main__':
#     get_all_movie()