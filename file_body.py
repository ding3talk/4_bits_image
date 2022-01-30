from PIL import Image#引入图片处理库

def make_file_body(
	re_image_file, file_way, size=(1024, 1024), depth=32, cd='t', zip='n'):
	'''
	中间的参数与make_file_head的文件头参数相同；
	第一个参数为make_file_head生成的文件, 最后一个参数为转换之前的文件路径
	'''
	image_file = Image.open(file_way)#打开待转换的原文件

	if depth == 32:#确认色深是否为32位
		image_file.resize(size)#改变图片大小

		image_filelist = image_file.load()#读取文件信息

		if cd == 't':#判断是否为横向排列像素
			passed_r = None#设置红色的默认值

			for x in range(size[0]):
				for y in range(size[1]):
					r = image_filelist[x, y][0]

					if r == passed_r:
						rep_pixiv = []

					passed_r = r