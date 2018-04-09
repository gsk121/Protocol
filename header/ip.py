from struct import*


class IP:

  def __init__(self, raw=None):
    if raw != None:
      self._Ver_HeaderLen = raw[:1]
      self._Service = raw[1:2]
      self._TotalLen = raw[2:4]
      self._Id = raw[4:6]
      self._Flag_Offset= raw[6:8]
      self._ttl= raw[8:9]
      self._Protocol= raw[9:10]
      self._Checksum= raw[10:12]
      self._src = raw[12:16]
      self._dst = raw[16:20]

    else:
      self._Ver_HeaderLen = b'\x00'
      self._Service = b'\x00'
      self._TotalLen = b'\x00\x00'
      self._Id = b'\x00\x00'
      self._Flag_Offset = b'\x00\x00'
      self._ttl = b'\x00'
      self._Protocol = b'\x00'
      self._Checksum = b'\x00\x00'
      self._src = b'\x00\x00\x00\x00'
      self._dst = b'\x00\x00\x00\x00'

  @property
  def get_header(self):
    return self._Ver_HeaderLen + self._Service + self._TotalLen + self._Id + self._Flag_Offset + self._ttl + self._Protocol + self._Checksum + self._src + self._dst

  @property
  def Ver( self ):
    tmp = unpack('!B', self._Ver_HeaderLen)
    tmp = Ver_HeaderLen >> 4
    return tmp

  @Ver.setter
  def Ver( self, Ver ):
    (tmp,) = unpack('!B', self._Ver_HeaderLen)
    tmp = tmp & 0x0F
    Ver = Ver << 4
    tmpp = Ver + tmp
    self._Ver_HeaderLen = pack('!B', tmpp)

  @property
  def HeaderLen( self ):
    tmp = unpack('!B', self._Ver_HeaderLen)
    tmp = (tmp & 0x0F) << 2
    return tmp    

  @HeaderLen.setter
  def HeaderLen( self, Len ):
    (tmp,) = unpack('!B', self._Ver_HeaderLen)
    tmp = tmp & 0xF0
    Len = Len >>2
    tmpp = tmp + Len
    self._Ver_HeaderLen = pack('!B', tmpp)
  
  @property
  def Service( self ):
    tmp = unpack('!B', self._Service)
    return tmp
  
  @Service.setter
  def Service( self, service ):
    self._service = pack('!B', service)  

  @property
  def TotalLen( self ):
    (tmp,) = unpack('!H', self._TotalLen)
    return tmp
  
  @TotalLen.setter
  def TotalLen( self, total ):
    self._TotalLen = pack('!H', total)
  
  @property
  def Id( self ):
    (tmp,) = unpack('!H', self._Id)
    return tmp
  
  @Id.setter
  def Id( self, id ):
    self._Id = pack('!H', id)
  
  @property
  def Flag( self ):
    (tmp,) = unpack('!H', self._Flag_Offset)
    tmp = tmp >> 13
    return tmp
  
  @Flag.setter
  def Flag( self, flag ):
    (offset,) = unpack('!H', self._Flag_Offset)
    offset = offset & 0x1FFF
    flag = flag << 13
    tmp = flag + offset
    self._Flag_Offset = pack('!H', tmp)
  
  @property
  def Offset( self ):
    (tmp,) = unpack('!H', self._Flag_Offset)
    tmp = (tmp & 0x1FFF) << 2
    return tmp
  
  @Offset.setter
  def Offset( self, offset ):
    (flag,) = unpack('!H', self._Flag_Offset)
    flag = flag & 0xE000
    tmp = flag + offset
    self._Flag_Offset = pack('!H', tmp)
  
  @property
  def ttl( self ):
    tmp = unpack('!B', self._ttl)
    return tmp
  
  @ttl.setter
  def ttl( self, ttl ):
    self._ttl = pack('!B', ttl)
  
  @property
  def Protocol( self ):
    (tmp,) = unpack('!B', self._Protocol)
    return tmp  

  @Protocol.setter
  def Protocol( self, pro ):
    self._Protocol = pack('!B', pro)
  
  @property
  def Checksum( self ):
    (tmp,) = unpack('!H', self._Checksum)
    return tmp  

  @Checksum.setter
  def Checksum( self, sum ):
    self._Checksum = pack('!H', sum)
  
  @property
  def src( self ):
    tmp = unpack('!4B', self._src)
    tmp = '{:d}.{:d}.{:d}.{:d}'.format( *tmp)
    return tmp
  
  @src.setter
  def src( self, src ):
    src = src.split('.')
    src = [int(x) for x in src]
    self._src = pack('!4B', *src)
  
  @property
  def dst( self ):
    tmp = unpack('!4B', self._dst)
    tmp = '{:d}.{:d}.{:d}.{:d}'.format( *tmp)
    return tmp
  
  @dst.setter
  def dst( self, dst ):
    dst = dst.split('.')
    dst = [int(x) for x in dst]
    self._dst = pack('!4B', *dst)


