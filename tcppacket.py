from struct import*
from socket import*
from eth import*
from ip import*
from tcp import*
from chk import*

# TCP 패킷 전송

client_seq=int(input('클라이언트 스퀀스를 입력하세요: '))
server_seq=int(input('서버의 시퀀스를 입력하세요: '))

client_port =int(input('클라이언트 포트를 입력하세요: '))
server_port = int(input('서버 포트를 입력하세요: '))

print()
print('========================상태 정보====================')
print('==== FIN: 1, SYN: 2 , ACK: 16, SYNACK: 18, ACKFIN:17, ACKPSH: 24 ===')
print('===================================================')
Flags=int(input('TCP상태를 설정하세요: '))


tcp1=Tcp()
tcp1.src_port=client_port
tcp1.dst_port=server_port
tcp1.Seq_Num= client_seq
tcp1.Ack_Num= server_seq
tcp1.Offset=0
tcp1.Flag= Flags
tcp1.Window_Size=65535
tcp1.Checksum=0
tcp1.Urgent_Pointer=0
tcp1.Offset=len(tcp1.get_header)

ip=IP()
ip.Ver=4
ip.HeaderLen=20
ip.Service=0
ip.TotalLen= len(ip.get_header) + len(tcp1.get_header)
ip.Id=0
ip.Flag=0
ip.Offset=0
ip.ttl=64
ip.Protocol=6
ip.Checksum =0
ip.src='192.168.1.9' 
ip.dst='192.168.1.8'
ip.Checksum = make_chksum(ip.get_header)

tcpLen=pack('!H',tcp1.Offset)
pseudo =ip._src + ip._dst + b'\x00'+ ip._Protocol + tcpLen + tcp1.get_header
tcp1.Checksum = make_chksum(pseudo)

eth=Eth()

eth.dst='00:0C:29:CC:AA:71'
eth.src='00:50:56:32:C2:BF'
eth.type=0x0800


sock=socket(AF_PACKET, SOCK_RAW)
sock.bind(('eth0', SOCK_RAW))
sock.send(eth.get_header() + ip.get_header + tcp1.get_header)

