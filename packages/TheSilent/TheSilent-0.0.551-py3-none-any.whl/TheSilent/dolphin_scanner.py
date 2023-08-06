import random
import socket
import time
import threading
from TheSilent.clear import clear

port_list = []
CYAN = "\033[1;36m"

def connect_scan(host,port):
    global port_list
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.settimeout(15)
    try:
        my_socket.connect((host,port))
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port_list.append(port)

    except:
        pass

def dolphin_scanner(host):
    global port_list
    clear()
    host = host.replace("https://", "")
    host = host.replace("http://", "")

    init_port_list = []
    for ports in range(1,65536):
        init_port_list.append(ports)

    init_port_list = random.sample(init_port_list[:], len(init_port_list[:]))

    print(CYAN + "dolphin is scanning")
    thread_list = []
    for port in init_port_list:
        my_thread = threading.Thread(target=connect_scan, args=[host,port])
        thread_list.append(my_thread)

    for thread in range(0,65535):
        thread_list[thread].start()
        if thread % 8 == 0:
            thread_list[thread].join()
            print(CYAN + "*", end="")

    port_list.sort()

    return port_list
