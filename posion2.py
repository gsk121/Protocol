
from arp import*
from eth import*
from socket import*
from struct import*
from time import*

eth=Eth()
arp=Arp()

eth.dst='00:0C:29:D4:D3:B5'
eth.src='00:00:00:00:00:00'
eth.type=0x0806

arp.hw_type=1
arp.protocol_type= 0x0800
arp.hw_len=6
arp.protocol_len=4
arp.opcode=1
arp.sender_mac='00:50:56:32:C2:BF'
arp.sender_ip='192.168.1.8'
arp.target_mac='00:00:00:00:00:00'
arp.target_ip='192.168.1.23'


sock=socket(AF_PACKET, SOCK_RAW)
sock.bind(('eth0',SOCK_RAW))
print("set ok")

while True:
  sock.send(eth.get_header() + arp.get_header)
  sleep(1)
