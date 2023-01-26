import socket
import struct

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(('100.100.100.7',80))

request = "GET /index.html HTTP/1.1\r\n"
request += "HOST: 100.100.100.7\r\n"
request += "Cache-Control: nocache\r\n"
request += "\r\n"

response = ''

while True:
	sock.send(request.encode())



