import queue
import socket
import threading
import re

stop_thread = False
watches = []

def get_input(client_socket,send_q):
    global stop_thread
    while True:
        if stop_thread:
            print("SENDER: stopping thread")
            break
        if not send_q.empty():
            print("SENDER: sending request")
            client_socket.sendall(send_q.get().encode())

def get_response(client_socket,recv_q, condition):
    while True:
        response = client_socket.recv(1024).decode()
        eof_check = True if response.find("##EOF##") != -1 else False
        watch_check = True if response.find("WATCH MATCHED") != -1 else False
        if eof_check:
            response = response.replace("##EOF##", "")
        resp = re.search("##EOF##", response)
        if watch_check:
            global watches
            watches.append({'token': response.split()[-1], 'response': response})
            continue
        if response:
            print("THREAD: response received")
            recv_q.put(response)
        if eof_check:
            continue


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
        global stop_thread
        stop_thread = True
        self.in_thread.join()
        self.out_thread.join()
        self.client_socket.close()
        stop_thread = False


def socket_service(msg, socket):
    print("socket_service")
    received = ""
    with socket.cond:
        socket.send_q.put(msg)
        received = socket.recv_q.get()
    return received

def get_watches(token):
    global watches
    result = []
    for watch in watches:
        if watch['token'] == token:
            result.append(watch['response'])
    return result