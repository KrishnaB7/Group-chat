import socket
import sys
from thread import *

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = "127.0.0.1"
port = 3000
sock.bind((host,port))
sock.listen(5)

def clientthread(conn, addr):
    userid = conn.recv(2048)
    dic[userid] = conn
    conn.send("Welcome to this chatroom!")
    while True:
        try:
            message = conn.recv(2048)
            #print 'recv:', message
            if message:
                if message[0] == '/':
                    receiver = message.strip("/").split(" ")[0]
                    #print 'found:', a
                    client_conn = dic[receiver]
                    #print 'found:', client_conn
                    message_to_send = message.split(" ",1)[1]
                    message_to_send = "<" + userid + ">" + message_to_send
                    sendmsg = client_conn.send(message_to_send)
                    #print "send msg: ",sendmsg
                else:
                    message_to_send = "<" + "Broadcast from " + userid + "> " + message
                    broadcast(message_to_send, conn)
            else:
                print 'removing: ', conn
                remove(conn)
        except Exception as e:
            print("type error: " + str(e))
            print 'Got exception: '
            continue


def broadcast(message, connection):
    for clients in dic.values():
        if clients != connection:
            try:
                sendmsg = clients.send(message)
                #print "send msg : ",sendmsg
            except:
                clients.close()
                remove(clients)

dic = {}
print "waiting for connection"
while True:
    conn, addr = sock.accept()
    message = "what do u want your user ID to be?"
    conn.sendall(message)
    print "conn is: ",conn
    start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()
