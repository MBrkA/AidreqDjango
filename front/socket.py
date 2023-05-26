import queue
import socket
import threading
import re

stop_thread = False

def socket_service(msg):
    received = ""
    socket = DjangoSocket()
    socket.start()
    with socket.cond:
        socket.send_q.put(msg)
        received = socket.recv_q.get()
    socket.stop()
    return received

def get_input(client_socket,send_q):
    global stop_thread
    while True:
        if stop_thread:
            break
        if not send_q.empty():
            client_socket.sendall(send_q.get().encode())

def get_response(client_socket,recv_q, condition):
    while True:
        #client_socket.settimeout(100)
        response = client_socket.recv(1024).decode()
        #client_socket.settimeout(None)
        eof_check = True if response.find("##EOF##") != -1 else False
        if eof_check:
            response = response.replace("##EOF##", "")
        resp = re.search("##EOF##", response)
        if response:
            print("THREAD: response received")
            recv_q.put(response)
            #condition.notifyAll()
        if eof_check:
            #break
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
        print("THREAD: stopping threads")
        self.in_thread.join()
        print("THREAD: in_thread joined")
        #self.out_thread.join()
        print("THREAD: out_thread joined")
        self.client_socket.close()
        print("THREAD: socket closed")
        stop_thread = False


        ## TODO
        ## STOP_THREAD HERKESİ ÖLDÜREBİLİR