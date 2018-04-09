import socket
import struct
import sys

print(sys.argv)

sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
 
 text_input=input("input: ")
 sock.sendto(text_input.encode(),(sys.argv[1],int(sys.argv[2])))
 save_data=sock.recv(30000)
 print("echo: ",save_data.decode())


