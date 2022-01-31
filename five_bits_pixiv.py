import struct#引入字节处理库
import doctest#引入文档测试库

import bits_str#引入二进制串模块

class FiveBitsPixiv:
    def __init__(self, flag: str, pixiv_ints: list):
        '''
        >>> FiveBitsPixiv('!', [25, 25, 25, 25]).bits_str
        '1111100000110010000011111'
        >>> fbp = FiveBitsPixiv('0', [28, 25, 30, 15])
        >>> fbp_1 = FiveBitsPixiv('0', [6, 5, 13, 15])
        >>> fbp.bits_str
        '000001110011001111100111100000'
        >>> fbp.append(fbp_1)
        '000001110011001111100111100000000000011000101011010111100000'
        '''
        self.flag = flag#压缩时使用的标志
        self.pixiv_ints = pixiv_ints#pixiv_ints为需要写入的像素的元组
        self.bits_len = len(pixiv_ints)#元组的长度
        self.is_byte = False#可被字节化？

        if self.flag in (str(i) for i in range(0, 8)):
            self.bits_flag = bin(int(flag)).lstrip('0b').zfill(5)
        elif self.flag == '!':
            self.bits_flag = '11111'
        else:
            raise ValueError('不合法的标志')

        self.bits_str = ''#设置需要输出的二进制串
        if self.flag == '!':#重复像素
            passed_p = None
            for p in self.pixiv_ints:
                if passed_p != p and passed_p is not None:
                    raise TypeError('flag为0但未传入相同像素')
                passed_p = p
            #如flag为!时判断是否有相同像素

            self.p_flag = p // 32#重复像素的flag
            self.rep_bits_flag = bin((p // 32)).lstrip('0b').zfill(5)#生成重复像素的bits_flag（并补0）

            if self.p_flag * 32 <= p < (self.p_flag * 32 + 32):
                self.bits_str = '%s%s%s%s%s' % (
                    self.bits_flag, self.rep_bits_flag,
                    bin(p - self.p_flag * 32).lstrip('0b').zfill(5), self.rep_bits_flag, self.bits_flag)
            #计算生成在有重复像素下的二进制串

        else:
            self.bits_str = self.bits_flag#设置需要输出的二进制串
            for pixiv in self.pixiv_ints:
                self.bits_str = self.bits_str + bin(
                    pixiv - (int(flag) * 32)).lstrip('0b').zfill(5)#将5_bits化的像素注入二进制串
            self.bits_str = self.bits_str + self.bits_flag#结尾

        if self.bits_len % 8 == 0:
            self.is_byte = True#如果二进制串可被字节化时为Ture
            self._bytes = bits_str.encode(self.bits_str)#编码为字节

    def append(self, *fbp):
        if type(fbp) == FiveBitsPixiv:#判断是否传入多个对象
            self.bits_str = self.bits_str + fbp.bits_str
        elif type(fbp) == tuple:
            for fbp_obj in fbp:
                self.bits_str = self.bits_str + fbp_obj.bits_str
        #将她们的二进制串连在一起

        else:
            raise TypeError('不是合法的FiveBitsPixiv对象')

        return self.bits_str

if __name__ == '__main__':
    doctest.testmod()#测试