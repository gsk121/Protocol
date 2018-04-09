from time import*
from socket import*
from struct import*
from udp import*
from ip import*
from eth import*
from chk import*

udp=Udp()

udp.src_port= 10000
udp.dst_port= 20000
udp.HeaderLen =0
udp.Checksum=0
udp.Data=b'hello'
udp.HeaderLen=len(udp.get_header)

ip=IP()
ip.Ver=4
ip.HeaderLen=20
ip.Service=0
ip.TotalLen= len(udp.get_header) + len(ip.get_header)
ip.Id=0
ip.Flag=0
ip.Offset=0
ip.ttl=64
ip.Protocol=17
ip.Checksum =0
ip.src='192.168.1.8'
ip.dst='192.168.1.2'
ip.Checksum = make_chksum(ip.get_header)

pseudo =ip._src + ip._dst + b'\x00'+ ip._Protocol + udp._HeaderLen + udp.get_header
udp.Checksum=make_chksum(pseudo)

eth=Eth()

eth.dst='f0:79:59:8d:be:fc'
eth.src='00:0c:29:cc:aa:71'
eth.type=0x0800

while True:
 sock = socket(AF_PACKET, SOCK_RAW)
 sock.bind(('eth0',SOCK_RAW))
 sock.send(eth.get_header() + ip.get_header + udp.get_header)
 sleep(1)

