# Author：zhaoyanqi
import socket
def get_client():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(('127.0.0.1',8081))
    return client