
from struct import*

class Tcp:

  def __init__(self, raw=None):
    if raw != None:
      self._src_port = raw[:2]
      self._dst_port = raw[2:4]
      self._Seq_Num = raw[4:8]
      self._Ack_Num = raw[8:12]
      self._Offset_Reserved = raw[12:13]
      self._Flag = raw[13:14]
      self._Window = raw[14:16]
      self._Checksum = raw[16:18]
      self._Urgent_Pointer = raw[18:20]

    else:
      self._src_port = b'\x00\x00'
      self._dst_port = b'\x00\x00'
      self._Seq_Num = b'\x00\x00\x00\x00'
      self._Ack_Num = b'\x00\x00\x00\x00'
      self._Offset_Reserved = b'\x00'
      self._Flag = b'\x00'
      self._Window = b'\x00\x00'
      self._Checksum = b'\x00\x00'
      self._Urgent_Pointer = b'\x00\x00'


  @property
  def get_header(self):
    return self._src_port + self._dst_port + self._Seq_Num + self._Ack_Num + self._Offset_Reserved + \
           self._Flag + self._Window + self._Checksum + self._Urgent_Pointer


  @property
  def src_port(self):
    (tmp,) = unpack('!H', self._src_port)
    return tmp

  @src_port.setter
  def src_port(self, src_port):
    self._src_port = pack('!H', src_port)

  @property
  def dst_port(self):
    (tmp,) = unpack('!H', self._dst_port)
    return tmp

  @dst_port.setter
  def dst_port(self, dst_port):
    self._dst_port = pack('!H', dst_port)

  @property
  def Seq_Num(self):
    (tmp,) = unpack('!L', self._Seq_Num)
    return tmp

  @Seq_Num.setter
  def Seq_Num(self,Seq_Num):
    self._Seq_Num = pack('!L', Seq_Num)

  @property
  def Ack_Num(self):
    (tmp,) = unpack('!L', self._Ack_Num)
    return tmp

  @Ack_Num.setter
  def Ack_Num(self, Ack_Num):
    self._Ack_Num = pack('!L', Ack_Num)

  @property
  def Offset(self):
    (tmp,) = unpack('!B', self._Offset_Reserved)
    tmp = tmp >> 2
    return tmp

  @Offset.setter
  def Offset(self, Offset):
    (Re,)= unpack('!B', self._Offset_Reserved)
    Re = Re & 0b_0000_1111_1111_1111
    Offset = Offset << 2
    tmp = Offset + Re
    self._Offset_Reserved = pack('!B', tmp)

  @property
  def Flag(self):
    (tmp,) = unpack('!B', self._Flag)
    return tmp

  @Flag.setter
  def Flag(self, Flag):
    self._Flag = pack('!B', Flag)

  @property
  def Window_Size(self):
    (tmp,) = unpack('!H', self._Window)
    return tmp

  @Window_Size.setter
  def Window_Size(self, Win):
    self._Window = pack('!H', Win)

  @property
  def Checksum(self):
    (tmp,) = unpack('!H', self._Checksum)
    return tmp

  @Checksum.setter
  def Checksum(self, chk):
    self._Checksum = pack('!H', chk)

  @property
  def Urgent_Pointer(self):
    (tmp,) = unpack('!H', self._Urgent_Pointer)
    return tmp

  @Urgent_Pointer.setter
  def Urgent_Pointer(self, Urg):
    self._Urgent_Pointer = pack('!H', Urg)
