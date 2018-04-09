from struct import*
from socket import*
from eth import*
from ip import*
from tcp import*
from chk import*
from time import*

client_seq=1
server_seq=0

client_port =int(input('클라이언트 포트를 입력하세요:'))
server_port = 12000


# syn
tcp=Tcp()
tcp.src_port= client_port
tcp.dst_port= server_port
tcp.Seq_Num= client_seq
tcp.Ack_Num= server_seq
tcp.Offset=0
tcp.Flag= 0b_0000_0010
tcp.Window_Size= 65535
tcp.Checksum=0
tcp.Urgent_Pointer=0
tcp.Offset=len(tcp.get_header)


ip=IP()
ip.Ver=4
ip.HeaderLen=20
ip.Service=0
ip.TotalLen= len(ip.get_header) + len(tcp.get_header)
ip.Id=0
ip.Flag=0
ip.Offset=0
ip.ttl=64
ip.Protocol=6
ip.Checksum =0
ip.src='192.168.1.9'
ip.dst='192.168.1.8'
ip.Checksum = make_chksum(ip.get_header)


tcpLen=pack('!H',tcp.Offset)
pseudo =ip._src + ip._dst + b'\x00'+ ip._Protocol + tcpLen + tcp.get_header
tcp.Checksum = make_chksum(pseudo)

eth=Eth()

eth.dst='00:0C:29:CC:AA:71'
eth.src='00:50:56:32:C2:BF'
eth.type=0x0800

sock=socket(AF_PACKET, SOCK_RAW)
sock.bind(('eth0', SOCK_RAW))
sock.send(eth.get_header() + ip.get_header + tcp.get_header)


#recv SYN_ACK

#while True:

raw = sock.recv(65535)
eth = Eth(raw[:14])
if eth.type == 0x0800:
  ip=IP(raw[14:34])
  if ip.Protocol ==6:
    tcp=Tcp(raw[34:])
    client_seq+=1
    server_seq = tcp.Seq_Num




server_seq+=1
print('client_seq: {:08x} | server_seq: {:08x}'.format(client_seq, server_seq))


# send ACK

tcp=Tcp()
tcp.src_port= client_port
tcp.dst_port= server_port
tcp.Seq_Num= client_seq
tcp.Ack_Num= server_seq
tcp.Offset=0
tcp.Flag= 0b_0001_0000
tcp.Window_Size= 65535
tcp.Checksum=0
tcp.Urgent_Pointer=0
tcp.Offset=len(tcp.get_header)


ip=IP()
ip.Ver=4
ip.HeaderLen=20
ip.Service=0
ip.TotalLen= len(ip.get_header) + len(tcp.get_header)
ip.Id=0
ip.Flag=0
ip.Offset=0
ip.ttl=64
ip.Protocol=6
ip.Checksum =0
ip.src='192.168.1.9'
ip.dst='192.168.1.8'
ip.Checksum = make_chksum(ip.get_header)

tcpLen=pack('!H',tcp.Offset)
pseudo =ip._src + ip._dst + b'\x00'+ ip._Protocol + tcpLen + tcp.get_header
tcp.Checksum = make_chksum(pseudo)

eth=Eth()

eth.dst='00:0C:29:CC:AA:71'
eth.src='00:50:56:32:C2:BF'
eth.type=0x0800

sock=socket(AF_PACKET, SOCK_RAW)
sock.bind(('eth0', SOCK_RAW))

sock.send(eth.get_header() + ip.get_header + tcp.get_header)

#send DATA
