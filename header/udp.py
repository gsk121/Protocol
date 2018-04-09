from struct import*

class Udp:

  def __init__(self, raw=None):
    if raw != None:
      self._src_port = raw[:2]
      self._dst_port = raw[2:4]
      self._HeaderLen = raw[4:6]
      self._Checksum = raw[6:8]
      self._Data = raw[8:]

    else:
      self._src_port = b'\x00\x00'
      self._dst_port = b'\x00\x00'
      self._HeaderLen = b'\x00\x00'
      self._Checksum = b'\x00\x00'
      self._Data = b''

  @property
  def get_header(self):
    return self._src_port + self._dst_port + self._HeaderLen + self._Checksum + self._Data

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
  def HeaderLen(self):
    (tmp,)= unpack('!H', self._HeaderLen)
    return tmp

  @HeaderLen.setter
  def HeaderLen(self, Len):
    self._HeaderLen = pack('!H', Len)

  @property
  def Checksum(self):
    (tmp,) = unpack('!H', self._Checksum)
    return tmp

  @Checksum.setter
  def Checksum(self, chk):
    self._Checksum = pack('!H', chk)

  @property
  def Data(self):
    tmp = self._Data
    return tmp

  @Data.setter
  def Data(self, data):
    self._Data = data

