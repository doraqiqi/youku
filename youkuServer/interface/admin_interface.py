# Author：zhaoyanqi

from db import modles
from lib import common
from db import dbhandler
import time
from conf import settings
import os



@common.login_auth
def release_notice(user_dic,conn):
    notice = modles.Notice(name=user_dic['notice_name'],
                           content = user_dic['content'],
                           user_id=user_dic['user_id'],
                           create_time=common.get_nowtime())
    back_dic = {'flag':True,'msg':'发布工作成功！'}
    common.send_back(back_dic,conn)


@common.login_auth
def delete_movie(user_dic,conn):
    movie = dbhandler.select(name=user_dic['movie_name'],type='movie')
    movie.is_delete = 1
    movie.save()
    back_dic = {'flag': True, 'msg': '删除成功！'}
    common.send_back(back_dic, conn)

@common.login_auth
def upload_movie(user_dic,conn):
    print('user_dic',user_dic)
    recv_size = 0
    file_name = common.get_uuid(user_dic['file_name'])+user_dic['file_name']
    file_path = os.path.join(settings.BASE_MOVIE_DIR,file_name)
    with open(file_path, 'wb') as f:
        while recv_size < user_dic['filesize']:
            recv_data = conn.recv(1024)
            f.write(recv_data)
            recv_size+=len(recv_data)
            print(recv_size)

    movie = modles.Movie(name=file_name,
                         path=file_path,
                         is_free=user_dic['is_free'],
                         is_delete=0,
                         create_time=common.get_nowtime(),
                         user_id=user_dic['user_id'],
                         file_md5=user_dic['file_md5'],
                         )
    back_dic = {'flag':True,'msg':'上传成功'}
    common.send_back(back_dic,conn)
