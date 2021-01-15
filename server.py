import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server = ''
port = 4200

server_ip = socket.gethostbyname(server)
print(server_ip)
try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(4)
print("Waiting for a connection")

sockets = []
food = ''
currentId = 0


def threaded_client(sock, player):
    global sockets, food
    sock.send(str.encode(str(player)))
    if player == 0:
        food = sock.recv(2048)
    else:
        sock.sendall(food)
    reply = ''
    while True:
        try:
            data = sock.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                sock.send(str.encode("Goodbye"))
                break
            else:
                print("Received: " + reply)
                for s in sockets:
                    if s != sock:
                        s.sendall(data)
        except:
            break

    print("Connection Closed")
    sock.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    sockets.append(conn)

    start_new_thread(threaded_client, (conn, currentId))
    currentId = currentId + 1
