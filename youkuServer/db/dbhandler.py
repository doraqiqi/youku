# Author：zhaoyanqi

import pickle
import os
from conf import settings

def save(obj):
    path_obj = os.path.join(settings.DB_PATH,obj.__class__.__name__.lower())
    if not os.path.isdir(path_obj):
        os.mkdir(path_obj)
    db_file = os.path.join(path_obj,obj.name)
    with open(db_file,'wb') as f:
        pickle.dump(obj,f)
        f.flush()


def select(name, type):
    '''
    查询方法，传入name和type(admin,course,school,teacher,student)
    :param name:
    :param type:
    :return:
    '''
    path_obj=os.path.join(settings.DB_PATH, type)

    if not os.path.isdir(path_obj):
        os.mkdir(path_obj)
    path_file = os.path.join(path_obj, name)
    if  os.path.exists(path_file):
        with open(path_file, 'rb') as f:
            return pickle.load(f)
    else:
        return False