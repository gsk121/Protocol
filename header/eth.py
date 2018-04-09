from struct import*

class Eth:

 def __init__( self, raw=None):

  if raw != None:
    self._dst= raw[:6]
    self._src = raw[6:12]
    self._type= raw[12:14]

  else:
    self._dst= b'\x00\x00\x00\x00\x00\x00'
    self._src= b'\x00\x00\x00\x00\x00\x00'
    self._type= b'\x00\x00'

 def get_header(self):
  return self._dst + self._src + self._type

 @property
 def dst( self ):
    tmp = unpack('!6B', self._dst)
    tmp = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format( *tmp )
    return tmp

 @dst.setter
 def dst( self, dst ):
  dst = dst.split(':')
  dst=[ int(x, 16) for x in dst ]
  self._dst = pack('!6B', *dst)


 @property
 def src( self ):
    tmp = unpack('!6B', self._src)
    tmp = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format( *tmp )
    return tmp

 @src.setter
 def src( self, src ):
  src = src.split(':')
  src=[ int(x, 16) for x in src ]
  self._src = pack('!6B', *src)


 @property
 def type( self ):
    (tmp, ) = unpack('!H', self._type)
    return tmp

 @type.setter
 def type(self, type):
  self._type = pack('!H', type)

