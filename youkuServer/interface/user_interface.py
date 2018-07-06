# Author：zhaoyanqi

from lib import common
from db import modles
import os
from conf import settings
from db import dbhandler
import uuid

@common.login_auth
def buy_member(user_dic,conn):
    user = modles.User.get_obj_by_name(user_dic['name'])
    user.is_vip = 1
    user.save()

    back_dic = {'flag':True,'msg':'购买会员成功'}
    common.send_back(back_dic,conn)


@common.login_auth
def download_move(user_dic,conn):
    print('download_movie的user_dic',user_dic)
    movie = modles.Movie.get_obj_by_name(user_dic['movie_name'])
    user = modles.User.get_obj_by_name(user_dic['user_id'])
    # if not user_dic['movie_type'] == 'charge_movie':
    if user.is_vip:
        wait_time = 0
    else:
        wait_time = 5
    # else:
    #     wait_time = 0
    #1 电影名 2 电影大小 3 md5值
    movie_name = movie.name
    movie_path = movie.path
    movie_size = os.path.getsize(movie_path)
    send_dic = {'flag':True,
                'movie_name':movie_name,
                'movie_size':movie_size,
                'file_md5':movie.file_md5,
                'wait_time':wait_time,
                }
    common.send_back(send_dic,conn)
    print(user_dic['user_id'],user_dic['movie_name'])
    download_record = modles.Download_record(name=str(uuid.uuid1()),user_name=user_dic['user_id'],movie_name=user_dic['movie_name'])
    download_record.save()

    with open(movie_path,'rb') as f:
        for line in f:
            conn.send(line)

@common.login_auth
def check_download_record(user_dic,conn):
    print(user_dic)
    all_record_list = get_all_download_record()#获取所有下载记录
    record_list = []#获取该用户的记录对象
    for obj in all_record_list:
        if obj.user_name == user_dic['user_id']:
            record_list.append(obj)
    movie_list = []#获取对象的电影名称
    for record in record_list:
        movie_list.append(record.movie_name)
    back_dic = {'flag':True,'msg':'查看成功','movie_list':movie_list}
    common.send_back(back_dic,conn)


def get_all_download_record():
    download_record_db_path = os.path.join(settings.DB_PATH,'download_record')
    download_record_file_list = common.get_all_file(download_record_db_path)
    print(download_record_file_list)
    record_list = []
    for download_record in download_record_file_list:
        record_list.append(dbhandler.select(download_record ,'download_record'))
    return record_list

@common.login_auth
def check_notice(user_dic,conn):
    back_notice_list = check_notice_by_count()
    back_dic = {'flag':True,'back_notice_list':back_notice_list}
    common.send_back(back_dic,conn)

def check_notice_by_count(count = None):#none是1就是查询1条，就查所有的
    notice_list = get_all_notice()
    back_notice_list = []
    if not count:
        #什么都没传，就是True，就是查所有
        for notice in notice_list:
            back_notice_list.append({notice.name: notice.content})
        return back_notice_list
    elif count == 1:
        notice_list = sorted(notice_list,key=lambda notice:notice.create_time)
        notice = notice_list[-1]
        return {notice.name:notice.content}



def get_all_notice():
    notice_db_path = os.path.join(settings.DB_PATH,'notice')
    notice_file_list = common.get_all_file(notice_db_path)
    print(notice_file_list)
    notice_list = []
    for notice in notice_file_list:
        notice_list.append(dbhandler.select(notice ,'notice'))
    return notice_list