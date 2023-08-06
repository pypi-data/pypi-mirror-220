# -*- coding:utf-8 -*-
"""
@Time : 2023/3/29
@Author : skyoceanchen
@TEL: 18916403796
@File : str_operation.py 
@PRODUCT_NAME : PyCharm 
"""
from rest_framework.exceptions import ParseError
from PIL import Image, ImageDraw, ImageFont, ImageFilter
# 中文转英文
import pinyin.cedict
import datetime
import struct, binascii
import math, random
import string

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# <editor-fold desc="字符串类工具">
class StringOperation(object):
    _letter_cases = "abcdefhjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z ,g
    _upper_cases = _letter_cases.upper()  # 大写字母
    _numbers = ''.join(map(str, range(3, 10)))  # 数字
    init_chars = ''.join((_letter_cases, _upper_cases, _numbers))

    @staticmethod
    def random_psd(psd_length: int):
        """
            建议:psd_length 为 大于8的整数
        :param psd_length:
        :return:
        """
        if psd_length < 8:
            raise ParseError('密码不应小于8位')
        src_digits = string.digits  # string_数字
        src_uppercase = string.ascii_uppercase  # string_大写字母
        src_lowercase = string.ascii_lowercase  # string_小写字母
        # 随机生成数字、大写字母、小写字母的组成个数（可根据实际需要进行更改）
        digits_num = random.randint(1, 6)
        uppercase_num = random.randint(1, psd_length - digits_num - 1)
        lowercase_num = psd_length - (digits_num + uppercase_num)
        # 生成字符串
        password = random.sample(src_digits, digits_num) + random.sample(src_uppercase, uppercase_num) + random.sample(
            src_lowercase, lowercase_num)
        # 打乱字符串
        random.shuffle(password)
        # 列表转字符串
        new_password = ''.join(password)
        return new_password

    # <editor-fold desc="查看是否包含中文">
    @staticmethod
    def check_contain_zh_cn(file_name: str):
        """
            查看是否包含中文
        :param file_name:
        :return:
        """
        for ch in file_name:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        else:
            return False

    # </editor-fold>
    # <editor-fold desc="生成验证码">
    @staticmethod
    def create_validate_code(
            size=(120, 30),
            chars=init_chars,
            img_type="GIF",
            mode="RGB",
            bg_color=(255, 255, 255),
            fg_color=(0, 0, 255),
            font_size=18,
            font_type="media/ttf/MONACO.TTF",
            length=4,
            draw_lines=True,
            n_line=(1, 2),
            draw_points=True,
            point_chance=2):
        """
        @todo: 生成验证码图片
        @param size: 图片的大小，格式（宽，高），默认为(120, 30)
        @param chars: 允许的字符集合，格式字符串
        @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
        @param mode: 图片模式，默认为RGB
        @param bg_color: 背景颜色，默认为白色
        @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
        @param font_size: 验证码字体大小
        @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
        @param length: 验证码字符个数
        @param draw_lines: 是否划干扰线
        @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
        @param draw_points: 是否画干扰点
        @param point_chance: 干扰点出现的概率，大小范围[0, 100]
        @return: [0]: PIL Image实例
        @return: [1]: 验证码图片中的字符串
        """

        width, height = size  # 宽高
        # 创建图形
        img = Image.new(mode, size, bg_color)
        draw = ImageDraw.Draw(img)  # 创建画笔

        def get_chars():
            """生成给定长度的字符串，返回列表格式"""
            return random.sample(chars, length)

        def create_lines():
            """绘制干扰线"""
            line_num = random.randint(*n_line)  # 干扰线条数

            for i in range(line_num):
                # 起始点
                begin = (random.randint(0, size[0]), random.randint(0, size[1]))
                # 结束点
                end = (random.randint(0, size[0]), random.randint(0, size[1]))
                draw.line([begin, end], fill=(0, 0, 0))

        def create_points():
            """绘制干扰点"""
            chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

            for w in range(width):
                for h in range(height):
                    tmp = random.randint(0, 100)
                    if tmp > 100 - chance:
                        draw.point((w, h), fill=(0, 0, 0))

        def create_strs():
            """绘制验证码字符"""
            c_chars = get_chars()
            strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

            font = ImageFont.truetype(font_type, font_size)
            font_width, font_height = font.getsize(strs)

            draw.text(((width - font_width) / 3, (height - font_height) / 3),
                      strs, font=font, fill=fg_color)

            return ''.join(c_chars)

        if draw_lines:
            create_lines()
        if draw_points:
            create_points()
        strs = create_strs()

        # 图形扭曲参数
        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

        return img, strs

    # </editor-fold>
    # <editor-fold desc="需要补0的数字">
    @staticmethod
    def autoFill0(e, t):
        """

        :param e:  需要补0的数字
        :param t:  需要补充道多少位
        :return:
        """
        i = ""
        e_str = str(e)
        # t = t ||  2;
        for o in range(t - len(e_str)):
            if o < t:
                i += "0"
        return i + e_str if e < 10 ** (t - 1) else e_str

    # </editor-fold>
    @staticmethod
    def chinese_english(s):
        return pinyin.get(s, format="strip", delimiter="")

    # <editor-fold desc="字符串内拼接字符串">
    @staticmethod
    def str_concatenation(lis):
        """

        :param lis:
        :return: "'1','2','3'"
        """
        # lis = ['1', '2', '3', '4', '1', '2', '3', '4', '1', '2']
        lis1 = ",".join(["'%s'" for _ in range(len(lis))])
        str_ = f"""{lis1}""" % tuple(lis)
        return str_

    # </editor-fold>
    # <editor-fold desc="忽略顺序 非完全匹配 匹配俩个字符串的相似度">
    # 参考文档 ： https://mp.weixin.qq.com/s/hyJwYAHHHgfuk83DBls-3A
    @staticmethod
    def token_sort_ratio(str1, str2):
        """
        params: str1
        params: str1
        returns:int
        案例：
        fuzz.token_sort_ratio("西藏 自治区", "自治区 西藏")
        output：100
        """
        return fuzz.token_sort_ratio(str1, str2)

    # </editor-fold>
    # <editor-fold desc="在列表中找最佳匹配的多个字符串和相似度">
    @staticmethod
    def extract(lis, str, limit=1):
        """
      lis = ["河南省", "郑州市", "湖北省", "武汉市"]
      process.extract("郑州", lis, limit=2)
      output:[('郑州市', 90), ('河南省', 0)]
      """
        return process.extract(str, lis, limit=limit)

    # </editor-fold>

    # <editor-fold desc="在列表中找最佳匹配的字符串和相似度">
    @staticmethod
    def extractOne(lis, str):
        """
        lis = ["河南省", "郑州市", "湖北省", "武汉市"]
        process.extractOne("郑州", lis)
        output:('郑州市', 90)
        process.extractOne("北京", lis)
        output:('湖北省', 45)
        """
        return process.extractOne(str, lis)
    # </editor-fold>


# 字符串判断
class StringJudge(object):
    # <editor-fold desc="所有字符都是数字或者字母">
    @staticmethod
    def isalnum(str):
        """
        :param str: 字符串
        :return:True
        """
        return str.isalnum()

    # </editor-fold>
    # <editor-fold desc="所有字符都是字母">
    @staticmethod
    def isalpha(str):
        """
        :param str: 字符串
        :return:True
        """
        return str.isalpha()

    # </editor-fold>
    # <editor-fold desc="所有字符都是数字">
    @staticmethod
    def isdigit(str):
        """
        :param str: 字符串
        :return:True
        """
        return str.isdigit()

    # </editor-fold>
    # <editor-fold desc="所有字符都是小写">
    @staticmethod
    def islower(str):
        """
        :param str: 字符串
        :return:True
        """
        return str.islower()

    # </editor-fold>
    # <editor-fold desc="所有字符都是大写">
    @staticmethod
    def isupper(str):
        """
        :param str: 字符串
        :return:True
        """
        return str.isupper()

    # </editor-fold>
    # <editor-fold desc="所有单词都是首字母大写，像标题">
    @staticmethod
    def istitle(str):
        """
        :param str: 字符串
        :return:True
        """
        return str.istitle()

    # </editor-fold>
    # <editor-fold desc="所有字符都是空白字符、\t、\n、\r">
    @staticmethod
    def isspace(str):
        """
        :param str: 字符串
        :return:True
        """
        return str.isspace()
    # </editor-fold>


# 进制 互转 binary 二进制
class BaseConversion(object):
    """
    # chr(i)函数返回 Unicode 码位为整数 i 的字符的字符串格式。例如，chr(97) 返回字符串 ‘a’，chr(8364) 返回字符串 ‘€’
    # ord函数对表示单个 Unicode 字符的字符串，返回代表它 Unicode 码点的整数。例如 ord(‘a’) 返回整数 97， ord(‘€’) （欧元符号）返回 8364

    """

    # <editor-fold desc="二进制转换">
    # 二进制转字符串
    def bin_to_chr(self, msg):
        x = '0b100111000000000'
        return chr(int(msg, 2))

    # </editor-fold>
    # <editor-fold desc="八进制转换">
    # 八进制转字符串
    def oct_to_chr(self, msg):
        return chr(int(msg, 8))

    # </editor-fold>
    # <editor-fold desc="十进制转换">
    # 十进制转换字符串
    def int_to_chr(self, msg):
        return chr(msg)

    # 十进制转16进制
    def int_to_hex(self, msg):
        return hex(msg)

    # </editor-fold>
    # <editor-fold desc="十六进制转换">
    # 十六进制转换bytes
    def hex_to_bytes(self, msg):
        data = binascii.a2b_hex(msg)
        # print(binascii.a2b_hex(msg).decode())
        # x = '0x4e00'
        # print(chr(int(x, 16)))
        # x = r'\u4E00'
        # print(eval("u'" + x + "'"))
        return data

    # 十六进制转换字符串
    def hex_to_chr(self, msg):
        data = binascii.unhexlify(msg)
        return data.decode('utf-8')

    # 16--int
    def hex_to_int(self, msg):
        # print(msg)
        # print(eval(msg),type(eval(msg)))
        # print(hex(eval(msg)).upper())
        # print(hex(eval(msg)).upper(), 16)
        data = int(msg, 16)
        return data

    # 16进制转float
    def hex_to_float(self, msg, round_number=2):
        i = int(msg, 16)
        return round(struct.unpack('<f', struct.pack('<I', i))[0], round_number)

    # 16进制转 双进度 float
    def hex_to_double(self, msg):
        i = int(msg, 16)
        return struct.unpack('<d', struct.pack('<Q', i))[0]

    # 16-二进制
    def hex_to_bin(self, msg):
        data = ''
        for i in range(int(len(msg) / 2)):
            c = int(msg[i * 2:(i + 1) * 2], 16)
            state_2 = '{:08b}'.format(c)
            data += state_2
        return data

    # 16进制转中文
    def hex_to_chinese(self, data):
        return bytes.fromhex(data).decode('gbk')

    # </editor-fold>
    # <editor-fold desc="字符串转换">
    # 字符串转二进制
    def chr_to_bin(self, msg):
        return bin(ord(msg))

    # 字符串转八进制
    def chr_to_oct(self, msg):
        return oct(ord(msg))

    # 字符串转十进制 /Unicode编码方法
    def chr_to_ord(self, msg):
        return ord(msg)

    #  # 字符串转十六进制
    def chr_to_hex(self, msg):
        return msg.encode().hex()

    # </editor-fold>
    # <editor-fold desc="Unicode编码">
    # Unicode编码转化为字符方法
    def ord_to_chr(self, msg):
        return chr(msg)

    # </editor-fold>
    # <editor-fold desc="时间转换成16进制">
    def datetime_to_chr16(self, date=None):
        if not date:
            date = datetime.datetime.now()
        year = date.year - 2000
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute
        second = date.second
        bit = ''.join([self.int_to_hex(i) for i in [year, month, day, hour, minute, second]])
        return bit

    # </editor-fold>
    # <editor-fold desc="float 转16进制">
    # float 转16进制
    def float_to_hex(self, msg):
        return hex(struct.unpack('<I', struct.pack('<f', msg))[0])

    # 双浮点型转16进制
    def double_to_hex(self, msg):
        return hex(struct.unpack('<Q', struct.pack('<d', msg))[0])

    # </editor-fold>
    # <editor-fold desc="中文">
    # 中文转16进制
    def chinese_to_chr16(self, data):
        return_dat = ''
        for c in data:
            if not ('\u4e00' <= c <= '\u9fa5'):
                st = c.encode().hex()
                return_dat += '00' + st
                # return False
            else:
                st = c.encode('raw_unicode_escape')
                st = st.decode("utf-8")
                st = st.replace("\\u", "")
                return_dat += st

        # return True
        return return_dat

    # </editor-fold>

# </editor-fold>
