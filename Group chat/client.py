import socket
import sys
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (("127.0.0.1",3000))

server.connect(server_address)

data = server.recv(2048)
print data
userid = raw_input()
server.sendall(userid)
print server
while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print 'message from server:', message
        else:
            message = sys.stdin.readline()
            sendmsg = server.send(message)
            #print "send msg :",sendmsg
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()
server.close()
