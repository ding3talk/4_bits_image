from PIL import Image#引入图片处理库
import numpy#引入numpy
import time#引入时间库

from four_bits_pixiv import FourBitsPixiv#引入4bits像素模块
import four_bits_write#引入二进制串写入模块
import bits_str#引入二进制串模块

def make_file_body(
        re_image_file, file_way: str, size=(1024, 1024), depth=32, cd='t', _zip='n'):
    '''
    后面的参数与make_file_head的文件头参数相同；
    第一个参数为make_file_head生成的文件, 第二个参数为转换之前的文件路径
    '''
    time_secs = time.perf_counter()#设置时间点

    image_file = Image.open(file_way)#打开待转换的原文件
    image_file = image_file.resize(size, Image.ANTIALIAS)#改变图片大小（高质量）

    if cd == 't':#判断是否为横向排列像素
        image_file_array = numpy.asarray(image_file)#以数组读取文件信息
    elif cd == 'v':#竖向
        image_file = image_file.rotate(90)#旋转
        image_file_array = numpy.asarray(image_file)#以数组读取文件信息

    else:
        raise ValueError('使用了未受支持的像素方向')

    if depth == 32:#确认色深是否为32位
        image_file_array = image_file_array.ravel(order='F')#展平像素数组
    elif depth == 24:#确认色深是否为24位
        image_file_array = numpy.delete(image_file_array, image_file_array[:, :, 3])#删除不透明度行（自动展平）

    else:
        raise ValueError('使用了未受支持的色深')

    passed_p = 128#设置上个像素的默认值(hack)
    rep_times = 0#设置重复次数的默认值
    fbps = FourBitsPixiv('?', [])#设置空二进制串
    near_list = []#设置相近像素列表
    for p in image_file_array:
        if passed_p == p:
            rep_times += 1
        else:
            if rep_times >= 1:
                fbps.append(FourBitsPixiv('!', [passed_p]))
                fbps = four_bits_write.bits_str_write(re_image_file, fbps)
                rep_times = 0
            elif (passed_p // 16) == (p // 16):
                if near_list:
                    near_list.append(passed_p)
                else:
                    near_list = [str(p // 16), p]
            else:
                if near_list:
                    fbps.append(FourBitsPixiv(near_list[0], near_list[1:]))
                    fbps = four_bits_write.bits_str_write(re_image_file, fbps)
                    near_list = []
                else:
                    fbps.append(FourBitsPixiv(str(p // 16), [p]))
                    fbps = four_bits_write.bits_str_write(re_image_file, fbps)

        passed_p = p
    #通过for循环读取其中信息并压缩写入

    if fbps:#如果还有存余像素
        fbps.zfill()#补0
        four_bits_write.bits_str_write(re_image_file, fbps)#写入
    print(time.perf_counter() - time_secs)#打印所用时间

import file_head
f = file_head.make_file_head('D:\\4_bits_image-main\\test\\test.4bi')
make_file_body(f, 'D:\\4_bits_image-main\\test\\3bd0338754784134aa48dda8128b223d.png')