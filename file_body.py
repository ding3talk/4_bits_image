from PIL import Image#引入图片处理库
import numpy#引入numpy

from five_bits_pixiv import FiveBitsPixiv#引入5bits像素模块

def make_file_body(
        re_image_file, file_way: str, size=(1024, 1024), depth=32, cd='t', _zip='n'):
    '''
    后面的参数与make_file_head的文件头参数相同；
    第一个参数为make_file_head生成的文件, 下一个参数为转换之前的文件路径
    '''
    image_file = Image.open(file_way)#打开待转换的原文件

    if depth == 32:#确认色深是否为32位
        image_file.resize(size)#改变图片大小
        image_file_array = image_file.load()#读取文件信息
        print(image_file_array)
        if cd == 't':#判断是否为横向排列像素
            image_file_array.ravel()#以横向展平像素数组
        if cd == 'v':#竖向
            image_file_array.ravel(order='F')#以竖向展平像素数组
        print(image_file_array)
