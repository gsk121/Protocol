from struct import*

class Arp:



 def __init__(self, raw=None):
  if raw != None:
   self._hw_type = raw[:2]
   self._protocol_type = raw[2:4]
   self._hw_len = raw[4:5]
   self._protocol_len = raw[5:6]
   self._opcode = raw[6:8]
   self._sender_mac= raw[8:14]
   self._sender_ip = raw[14:18]
   self._target_mac = raw[18:24]
   self._target_ip = raw[24:28]

  else:
   self._hw_type = b'\x00\x00'
   self._protocol_type = b'\x00\x00'
   self._hw_len = b'\x00'
   self._protocol_len = b'\x00'
   self._opcode = b'\x00\x00'
   self._sender_mac = b'\x00\x00\x00\x00\x00\x00'
   self._sender_ip = b'\x00\x00\x00\x00'
   self._target_mac = b'\x00\x00\x00\x00\x00\x00'
   self._target_ip = b'\x00\x00\x00\x00'



 @property
 def get_header(self):
  return self._hw_type + self._protocol_type + self._hw_len + self._protocol_len + self._opcode + self._sender_mac + self._sender_ip + self._target_mac + self._target_ip

 @property
 def hw_type(self):
  tmp= unpack('!H', self._hw_type)
  return tmp

 @hw_type.setter
 def hw_type(self, type):
  self._hw_type = pack('!H', type)

 @property
 def protocol_type(self):
  tmp = unpack('!H', self._protocol_type)
  return tmp

 @protocol_type.setter
 def protocol_type(self, type):
  self._protocol_type = pack('!H', type)

 @property
 def hw_len(self):
  tmp = unpack('!B', self._hw_len)
  return tmp

 @hw_len.setter
 def hw_len(self, len):
  self._hw_len = pack('!B', len)

 @property
 def protocol_len(self):
  tmp = unpack('!B', self._protocol_len)
  return tmp

 @protocol_len.setter
 def protocol_len(self, len):
  self._protocol_len = pack('!B', len)

 @property
 def opcode(self):
  tmp = unpack('!H', self._opcode)
  return tmp

 @opcode.setter
 def opcode(self, opcode):
  self._opcode=pack('!H', opcode)

 @property
 def sender_mac(self):
  tmp = unpack('!6B', self._sender_mac)
  tmp = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(*tmp)
  return tmp

 @sender_mac.setter
 def sender_mac(self, sender_mac):
  sender_mac = sender_mac.split(':')
  sender_mac = [ int(x, 16) for x in sender_mac ]
  self._sender_mac = pack('!6B', *sender_mac)

 @property
 def sender_ip(self):
  tmp = unpack('!4B', self._sender_ip)
  tmp = '{:d}.{:d}.{:d}.{:d}'.format(*tmp)
  return tmp

 @sender_ip.setter
 def sender_ip(self, sender_ip):
  sender_ip = sender_ip.split('.')
  sender_ip = [ int(x) for x in sender_ip ]
  self._sender_ip = pack('!4B', *sender_ip)

 @property
 def target_mac(self):
  tmp = unpack('!6B', self._target_mac)
  tmp = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(*tmp)
  return tmp

 @target_mac.setter
 def target_mac(self, target_mac):
  target_mac = target_mac.split(':')
  target_mac = [ int(x, 16) for x in target_mac ]
  self._target_mac = pack('!6B', *target_mac)

 @property
 def target_ip(self):
  tmp = unpack('!4B', self._target_ip)
  tmp = '{:d}.{:d}.{:d}.{:d}'.format(*tmp)
  return tmp

 @target_ip.setter
 def target_ip(self, target_ip):
  target_ip = target_ip.split('.')
  target_ip = [ int(x) for x in target_ip ]
  self._target_ip = pack('!4B', *target_ip)

