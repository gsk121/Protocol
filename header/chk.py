from struct import*

def make_chksum( header ):
  size =len(header)
  if(size % 2) != 0:
    header = header + b'\x00'
    size = len(header)

  header = unpack('!' + str(size//2)+'H', header)  
  chksum = sum(header)

  carry = chksum & 0b_1111_1111_0000_0000_0000_0000   #and 0xFF0000
  carry >>= 16
  while carry != 0:
    chksum = chksum & 0b_0000_0000_1111_1111_1111_1111
    chksum = chksum + carry
    carry = chksum & 0b_1111_1111_0000_0000_0000_0000
    carry >>= 16

  chksum = chksum ^ 0b_1111_1111_1111_1111
  return chksum
