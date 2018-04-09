
from socket import*
from struct import*
from eth import*
from arp import*
from ip import*
from udp import*
from tcp import*

sock=socket(AF_PACKET, SOCK_RAW)
sock.bind(('eth0',SOCK_RAW))

while True:
 rawData = sock.recv(65535)
 eth= Eth(rawData[:14])

 if eth.type ==0x0800:
  ip=IP(rawData[14:])
  if ip.Protocol == 1: #and (ip.src == '192.168.1.8' or ip.dst=='192.168.1.8'):
    (type,) = unpack('!B', rawData[34:35])
    print('{:s} -> {:s} type: {:d}'.format(ip.src, ip.dst, type))

  elif ip.Protocol == 6 and (ip.src == '192.168.1.8' or ip.dst =='192.168.1.8'):
    tcp = Tcp(rawData[34:])
    print('{:d} -> {:d} Seq:{:d}, Ack:{:d} Flag: {:08b}'.format(tcp.src_port, tcp.dst_port, tcp.Seq_Num, tcp.Ack_Num, tcp.Flag))
