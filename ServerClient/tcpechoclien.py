import socket
import struct
import sys

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect( (sys.argv[1], int(sys.argv[2])) )

while 1:
 text_input = input("input: ")
 sock.send(text_input.encode())
 data= sock.recv(30000)
 print("echo: ", data.decode())
