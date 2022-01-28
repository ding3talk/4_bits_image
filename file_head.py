import struct#引入字节处理库

def make_file_head(
        file_way, size=(1024, 1024), depth=32, cd='t', zip='n'):
    '''
    传入文件创建的路径、大小、色深、压缩时使用的方向与是否使用某种压缩（暂时不会开发）；
    depth目前只支持32位（透明）与24位（真彩）；
    cd有t、v两种状态，即压缩方向为横或竖；
    zip默认为n，即None；
    要提一下的是， 格式标识的长固定为6个字节，可以改变的只有2个（长宽）。
    '''

    image_file = open(file_way, mode='wb')#使用指定好的路径创建图片

    if not (size[0] or size[1]):#确认长宽不为0
        raise ValueError('长宽不能为0')

    if depth != 24 and depth != 32:#确认色深在支持范围内
        raise ValueError('使用了非支持的色深')

    if type(size[0]) != int or type(size[1]) != int or type(depth) != int:
        size = int(size[0]), int(size[1]), int(depth)
    #如数值不为整数，转为int

    else:
        size_format_str = b''#创建表示长宽格式的

        for i in size:
            if i >= 2 ** 64:
                raise ValueError('长宽大于了64位')
            elif 2 ** 32 <= i <= 2 ** 64:
                size_format_str = size_format_str + b'Q'
            elif 2 ** 16 <= i <= 2 ** 32:
                size_format_str = size_format_str + b'I'
            elif 2 ** 8 <= i <= 2 ** 16:
                size_format_str = size_format_str + b'H'
            elif  i <= 2 ** 8:
                size_format_str = size_format_str + b'B'
        #为格式串添加长宽的格式标识

        format_str = b'<' + size_format_str + b'Bss'#添加剩余三个标识的格式标识（较为固定）
        #创建表示文件头格式的字节字符串标识（struct）
        print(format_str)

        bytes_pack = struct.pack(
            format_str, size[0], size[1], depth, cd.encode('utf8'), zip.encode('utf8'))
        #使用生成好的格式标识打包文件头信息

        image_file.write(b'5B' + size_format_str)
        image_file.write(bytes_pack)#写入文件头

    return image_file#返回文件与格式标识

image_file = make_file_head('I:/python项目/5_bits_image/test_image/test_image.txt')
image_file.close()

def read_file_head(file_way):#刚才的逆函数
    image_file = open(file_way, mode='rb')

    if image_file.read(2) != b'5B':#判定是否为正确的文件
        raise TypeError('不是5_bits文件')

    format_str = b'<' + image_file.read(2) + b'Bss'#还原回原来的格式标识
    print(format_str)

    need_bytes = 0#设置需要读取的文件头字节的数量
    for i in format_str.decode('ascii'):
        if i == '<':
            pass
        if i == 'B' or i == 's':
            need_bytes += 1
        if i == 'H':
            need_bytes += 2
        if i == 'I':
            need_bytes += 4
        if i == 'Q':
            need_bytes += 8
    #根据格式标识计算需要读取的文件头字节的数量

    head_unpack = struct.unpack(format_str, image_file.read(need_bytes))#重新提取出文件头信息
    print(head_unpack)
    return image_file, head_unpack

read_file_head('I:/python项目/5_bits_image/test_image/test_image.txt')