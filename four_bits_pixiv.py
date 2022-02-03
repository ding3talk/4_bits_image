import struct#引入字节处理库
import doctest#引入文档测试库
import bits_str#引入二进制串模块

class FourBitsPixiv:
    def __init__(self, flag: str, pixiv_ints: list):
        self.flag = flag#压缩时使用的标志
        self.pixiv_ints = pixiv_ints#pixiv_ints为需要写入的像素的列表

        if self.flag in (str(i) for i in range(0, 16)):
            self.bits_flag = bin(int(flag)).lstrip('0b').zfill(4)
        elif self.flag == '!':
            self.bits_flag = '1111'
        elif self.flag == '?':
            pass
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

            self.p_flag = p // 16#重复像素的flag
            self.rep_bits_flag = bin(self.p_flag).lstrip('0b').zfill(4)#生成重复像素的bits_flag（并补0）

            if self.p_flag * 16 <= p < (self.p_flag * 16 + 16):
                self.bits_str = '%s%s%s%s%s' % (
                    self.bits_flag, self.rep_bits_flag,
                    bin(p - self.p_flag * 16).lstrip('0b').zfill(4), self.rep_bits_flag, self.bits_flag)
            #计算生成在有重复像素下的二进制串

        elif self.flag == '?':  # 如果flag为'?'，代表空二进制串
            bits_str = ''

        else:
            self.bits_str = self.bits_flag#设置需要输出的二进制串
            for pixiv in self.pixiv_ints:
                self.bits_str = self.bits_str + bin(
                    pixiv // 16).lstrip('0b').zfill(4)#将4_bits化的像素注入二进制串
            self.bits_str = self.bits_str + self.bits_flag#结尾

    def is_byte(self):#可被字节化？
        self.bits_len = len(self.bits_str)#列表的长度

        if (self.bits_len % 8) == 0 and (self.bits_len != 0):
            self._bytes = bits_str.encode(self.bits_str)#如果可以，编码为字节
            return True
        else:
            return False

    def zfill(self):
        self.bits_str = self.bits_str + (8 - (self.bits_len % 8)) * '0'
        self._bytes = bits_str.encode(self.bits_str)#如果可以，编码为字节

    def append(self, fbp):
        self.bits_str = self.bits_str + fbp.bits_str#将她们的二进制串连在一起
        return self.bits_str

    def __bool__(self):
        return bool(self.bits_str)#返回二进制串的布尔值

'''if __name__ == '__main__':
    doctest.testmod()#测试'''