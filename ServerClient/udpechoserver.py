import socket
import struct

port=35000

sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('192.168.1.9',port))

print("Cilent ip: {:s} | port: {:d}".format('192.168.1.9',port))

while True:
 
 data,data2= sock.recvfrom(30000)
 print("Client: {:s}/{:d}".format(data2[0],data2[1]))
 print("data: {:s}".format(data.decode()))

 sock.sendto(data,data2)

