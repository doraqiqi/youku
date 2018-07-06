# Author：zhaoyanqi

import os,sys

path=os.path.dirname(__file__)
sys.path.append(path)
from tcpServer import tcpserver

if __name__ == '__main__':
    tcpserver.run()