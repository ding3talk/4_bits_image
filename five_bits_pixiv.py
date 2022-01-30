import struct#引入字节处理库
import bits_str#引入二进制串模块

class FiveBitsPixiv:
	def __init__(self, flag, color_ints):
		'''
		>>>FiveBitsPixiv(0, (25, 25, 25, 25))
		0000000001110010000100000
		'''
		self.flag = flag#压缩时使用的标志
		self.color_ints = color_ints#color_ints为需要写入的像素的元组
		self.bits_len = len(color_ints)#元组的长度
		self.is_byte = False

		self.bits_str = ''#设置需要输出的二进制串
		if self.flag == 0:#重复像素
			passed_p = None
			for p in color_ints:
				if passed_p != p and passed_p is not None:
					raise TypeError('flag为0但未传入相同像素')
				passed_p = p
			#如flag为0时判断是否有相同像素

			for i in range(0, 224, 32):
				if i <= p <= (i + 32):
					self.bits_str = '0000000001%s0000100000' % bin(p - i).lstrip('0b')
			#计算生成在有重复像素下的二进制串

		if self.bits_len % 8 == 0:
			self.is_byte = True#如果二进制串可被字节化时为Ture
			self._bytes = bits_str.encode(self.bits_str)
