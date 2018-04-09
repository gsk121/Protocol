import socket
import struct
import threading

port=35000

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.1.9',port))
sock.listen(0)

def gsk():

	client_sock,info =sock.accept()
	th=threading.Thread(target=gsk)
	th.start()

	while 1:
		data= client_sock.recv(30000)
		client_sock.send(data)
		print("echo: ",data.decode())
		print("client: ", info[0], info[1])
gsk()

sock.close()

