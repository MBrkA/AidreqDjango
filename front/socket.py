import queue
import socket
import threading
import re


def get_input(client_socket,send_q):
    while True:
        if not send_q.empty():
            client_socket.sendall(send_q.get().encode())

def get_response(client_socket,recv_q, condition):
    while True:
        response = client_socket.recv(1024).decode()
        eof_check = True if response.find("##EOF##") != -1 else False
        if eof_check:
            response = response.replace("##EOF##", "")
        resp = re.search("##EOF##", response)
        if response:
            recv_q.put(response)
            #condition.notifyAll()
        if eof_check:
            break

class DjangoSocket:
    HOST = "127.0.0.1"
    PORT = 1423

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((DjangoSocket.HOST, DjangoSocket.PORT))
        self.send_q = queue.Queue()
        self.recv_q = queue.Queue()
        self.mutex = threading.Lock()
        self.cond = threading.Condition(self.mutex)
        
        self.in_thread = threading.Thread(target=get_input, args=(self.client_socket,self.send_q))
        self.out_thread = threading.Thread(target=get_response, args=(self.client_socket,self.recv_q,self.cond))

    def start(self):
        self.in_thread.start()
        self.out_thread.start()

    def stop(self):
        self.in_thread.join()
        self.out_thread.join()
        self.client_socket.close()
