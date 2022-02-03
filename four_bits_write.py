from four_bits_pixiv import FourBitsPixiv#引入4bits像素模块

def bits_str_write(file, fbp):
    if fbp.is_byte():
        file.write(fbp._bytes)#如果可写入则写入
        return FourBitsPixiv('?', [])#清空
    else:
        return fbp#反之返回原样