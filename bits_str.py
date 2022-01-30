import struct#引入字节处理库

def encode(bits_str):#将二进制串转换为字节
    bits_len = len(bits_str)#计算二进制串的长度

    _bytes = b''#设置输出的字节
    if bits_len % 8 != 0:
        bits_str = bits_str + '0' * (8 - bits_len % 8)
        print('警告，未使用可字节化的二进制串')
    #如果不能字节化则补0
    for i in range(8, bits_len + 1, 8):
        eight_bit_str = bits_str[i - 8:i]#截取8个bit为字节
        _bytes = _bytes + struct.pack(b'B', int(eight_bit_str, 2))#字节化

    return _bytes

def decode(_bytes):#将字节转换为二进制串
    return ''.join([bin(i).lstrip('0b') for i in _bytes])#计算转换后的二进制串