# Author：zhaoyanqi

from db import dbhandler
from db import modles
import uuid

class BasicClass:

    @classmethod
    def get_obj_by_name(cls, name):
        return dbhandler.select(name, cls.__name__.lower())

    def save(self):
        dbhandler.save(self)

class User(BasicClass):
    def __init__(self,name,password,user_type,is_vip,locked):
        self.name = name
        self.password = password
        self.user_type = user_type
        self.is_vip = is_vip
        self.locked = locked
        self.save()

class Notice(BasicClass):
    def __init__(self,name,content,create_time,user_id):
        self.name = name
        self.content = content
        self.create_time = create_time
        self.user_id = user_id
        self.save()

class Movie(BasicClass):
    def __init__(self,name,path,is_free,is_delete,create_time,user_id,file_md5):
        self.name = name
        self.path = path
        self.is_free = is_free
        self.is_delete = is_delete
        self.create_time = create_time
        self.user_id = user_id
        self.file_md5 = file_md5
        self.save()

class Download_record(BasicClass):
    def __init__(self,name,user_name,movie_name):
        self.name = name
        self.user_name = user_name
        self.movie_name = movie_name
        self.save()

if __name__ == '__main__':
    movie = modles.Movie(name='aa2',path='11',is_free=0,is_delete=0,create_time='2018-5-5',user_id=1,file_md5='aaa')
    print(movie.name)

    aa3 = dbhandler.select('aa3','movie')
    print(aa3)

