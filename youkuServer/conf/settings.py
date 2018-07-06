# Author：zhaoyanqi

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_MOVIE_DIR = os.path.join(BASE_DIR,'movie_dir')
DB_PATH = os.path.join(BASE_DIR,'db')


if __name__ == '__main__':
    print(BASE_MOVIE_DIR)