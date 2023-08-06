# -*- coding:utf-8 -*-
"""
@Time : 2023/3/29
@Author : skyoceanchen
@TEL: 18916403796
@File : list_operation.py 
@PRODUCT_NAME : PyCharm 
"""

import itertools
import math, random
import numpy as np
from basic_type_operations.number_operation import NumberOperation


# <editor-fold desc="列表类工具">
class ListOperation(object):
    # <editor-fold desc="区间内随机生成一个一维列表">
    @staticmethod
    def random_list(start, stop, length, keep_decimal=2, integer=False):
        if length >= 0:
            length = int(length)
            start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
            random_list = []
            if keep_decimal:
                for i in range(length):
                    # 整数
                    # random_list.append(random.randint(start, stop))
                    # 小数
                    # random_list.append(random.uniform(start, stop))
                    # 保留n位置小数
                    random_list.append(round(random.uniform(start, stop), keep_decimal))
            else:
                for i in range(length):
                    # 整数
                    random_list.append(random.randint(start, stop))
                    # 小数
                    # random_list.append(random.uniform(start, stop))
                    # 保留n位置小数
                    # random_list.append(round(random.uniform(start, stop), keep_decimal))
            return random_list

    # </editor-fold>
    # <editor-fold desc="随机创建二维矩阵">
    @staticmethod
    def twomatrix(low, high, size_row, size_col, integer=False):
        """

        :param low:矩阵最小值
        :param high: 矩阵最大值，并都小于最大值
        :param size_row: 行
        :param size_col: 列
        :return:
        """
        # 不包含最大值
        # rand = np.random.randint(low=low, high=high, size=(size_row, size_col))
        # 包含最大值
        # rand = np.random.random_integers(low=low, high=high,  size=(size_row, size_col))
        # 随机小数
        if integer:
            rand = np.random.randint(low=low, high=high, size=(size_row, size_col))
        else:
            rand = np.random.uniform(low=low, high=high, size=(size_row, size_col))
        # print(rand)
        # print(rand.tolist())
        return rand.tolist()

    # print(twomatrix(0, 1, 100, 200, integer=True))

    # </editor-fold>
    # <editor-fold desc="随机创建三维矩阵">
    @staticmethod
    def threematrix(low, high, size_row, size_col, size_high, integer=False):
        """
        :param low:矩阵最小值
        :param high: 矩阵最大值，并都小于最大值
        :param size_row: 行
        :param size_col: 列
        :param size_high: 高
        :return:
        在size_row个二维  二维内又size_col个一维，一维数组内size_high个数据
        """
        # 不包含最大值
        # rand = np.random.randint(low=low, high=high, size=(size_row, size_col, size_high))
        # 包含最大值
        # rand = np.random.random_integers(low=low, high=high, size=(size_row, size_col, size_high))
        # 随机小数
        if integer:
            rand = np.random.randint(low=low, high=high, size=(size_row, size_col, size_high))
        else:
            rand = np.random.uniform(low=low, high=high, size=(size_row, size_col, size_high))
        # print(rand.tolist())
        return rand.tolist()

    # </editor-fold>
    # <editor-fold desc="不同长度的二维数组的转置">
    @staticmethod
    def dimensional_list_two(data_lis):
        try:
            max_len = max(len(i) for i in data_lis)
            b = [[] for _ in range(max_len)]  # 转置后列表
            if len(data_lis) > 0:
                for i in range(max_len):  # 行数
                    for ls in data_lis:
                        if i < ls.__len__():
                            b[i].append(ls[i])
                return b
            return None
        except:
            return None

    # </editor-fold>
    # <editor-fold desc="相同长度的二维数组的转置">
    @staticmethod
    def dimensional_list_two_same(data_lis):
        try:
            # max_len = len(data_lis[0])
            # b = [[] for _ in range(max_len)]  # 转置后列表
            # if len(data_lis) > 0:
            #     for i in range(max_len):  # 行数
            #         for ls in data_lis:
            #             b[i].append(ls[i])
            #     return b
            li = np.array(data_lis)
            li = li.T
            li = li.tolist()
            return li
            # return None
        except:
            return None

    # </editor-fold>
    # <editor-fold desc="取数组的中位数">
    @staticmethod
    def get_median(data):
        data.sort()
        half = len(data) // 2  # x//2  ==   int(x/2)
        return (data[half] + data[~half]) / 2  # x[-3]  ==  x[~2]

    # </editor-fold>
    # <editor-fold desc="列表的平均数">
    @staticmethod
    def avgList(lis, keep_decimal=2, integer=False):
        """uses floating-point division."""
        value = sum(lis) / len(lis)
        if integer:
            return round(value)
        if keep_decimal:
            return round(value, keep_decimal)
        return value
        # return round(sum(lis) / float(len(lis)), 2)

    # </editor-fold>
    # <editor-fold desc="列表最大值">
    @staticmethod
    def maxList(lis, keep_decimal=2, integer=False):
        value = max(lis)
        if integer:
            return math.ceil(value)  # 向上取整
        if keep_decimal:
            return round(value, keep_decimal)
        return value

    # </editor-fold>
    # <editor-fold desc="列表最小值">
    @staticmethod
    def minList(lis, keep_decimal=2, integer=False):
        value = min(lis)
        if integer:
            return math.floor(value)
        if keep_decimal:
            return round(value, keep_decimal)
        return value

    # </editor-fold>
    # <editor-fold desc="一维求百分比">
    # str(round(res.count(1) / len(res), 2) * 100) + '%'
    @staticmethod
    def one_dimensional_percent(lis):
        count = len(lis)
        dic = dict()
        for i in lis:
            if dic.get(i):
                dic[i] += 1
            else:
                dic[i] = 1
        lis = list(dic.keys())
        # lis = list(set(lis))
        lis.sort()
        for i in lis:
            # str(round(res.count(1) / len(res), 2) * 100) + '%'
            dic[i] = str(round(dic[i] / count, 2) * 100) + "%"
        return dic

    # </editor-fold>
    # <editor-fold desc="列表对应相除">
    @staticmethod
    def list_divide(lis1, lis2):
        num_len1 = len(lis1)
        num_len2 = len(lis2)
        num_len = num_len1
        if len(lis2) < num_len:
            num_len = num_len2
        lst3 = []
        for index in range(num_len):
            res = None
            if float(lis2[index]) == 0:
                res = 0
            else:
                res = round(float(lis1[index]) / float(lis2[index]), 2)
            lst3.append(res)
            # for i in lis2:
            #     if i == '0':
            #         rs = 0
            #     else:
            #         rs = round(float(item) / float(i), 2)
            #     lst3.append(rs)
        return lst3

    # </editor-fold>
    # <editor-fold desc="列表保留n位小数">
    @staticmethod
    def list_Keep_place(data, decimal=0):
        if decimal == 0:
            for i in range(len(data)):
                if isinstance(data[i], str):
                    continue
                else:
                    data[i] = NumberOperation.round_up(data[i])
        else:
            for i in range(len(data)):
                if isinstance(data[i], str):
                    continue
                else:
                    # data[i] = float('%.%f' % (data[i], decimal))
                    data[i] = NumberOperation.round_up(data[i], decimal)
                # print(data[i], type(data[i]))

        return data

    # </editor-fold>
    # <editor-fold desc="二维数组求平均值">
    @staticmethod
    def two_dimensional_avgList(lis, keep_decimal=2, integer=False):
        SumValue = sum([sum(row) for row in lis])
        numValue = len(lis[0]) * len(lis)
        if numValue != 0:
            value = SumValue / numValue
        else:
            value = SumValue
        if integer:
            return math.ceil(value)
        if keep_decimal:
            return round(value, keep_decimal)
        return value

    # </editor-fold>
    # <editor-fold desc="二维数组求最大值">
    @staticmethod
    def two_dimensional_maxList(lis, keep_decimal=2, integer=False):
        value = max(max(row) for row in lis)
        if integer:
            return math.ceil(value)
        if keep_decimal:
            return round(value, keep_decimal)
        return value

    # </editor-fold>
    # <editor-fold desc="二维数组求最小值">
    @staticmethod
    def two_dimensional_minList(lis, keep_decimal=2, integer=False):
        value = min([min(row) for row in lis])
        if integer:
            return math.floor(value)
        if keep_decimal:
            return round(value, keep_decimal)
        return value

    # </editor-fold>
    # <editor-fold desc="不同长度的二维数组合并一维数组">
    @staticmethod
    def dimensional_list_two_marge(two_list):
        # alist = [[3, 4, 5], [6, 7, 22], [35, 46, 78], [100]]
        # print(list(itertools.chain(alist[0], alist[1])))
        len_a = len(two_list)
        new_list = []
        for i in range(len_a):
            new_list = list(itertools.chain(new_list, two_list[i]))
        return new_list

    # </editor-fold>
    # <editor-fold desc="数组分成相同长度的二维数组">
    # def lst_trans0(test_list, n):
    #     """n: split list into `n` groups
    #     """
    #     len_list = len(test_list)
    #     m = math.ceil(len_list / float(n))
    #     alist = []
    #     group_m = -1
    #     for i in range(len_list):
    #         if i % m == 0:
    #             group_m += 1
    #             alist.append([test_list[i]])
    #         else:
    #             alist[group_m].append(test_list[i])
    #     return alist
    @staticmethod
    def lst_trans0(test_list, n):
        """n: 一组多少条数据
        """
        len_list = len(test_list)
        n = math.ceil(len_list / float(n))
        m = math.ceil(len_list / float(n))
        alist = []
        group_m = -1
        for i in range(len_list):
            if i % m == 0:
                group_m += 1
                alist.append([test_list[i]])
            else:
                alist[group_m].append(test_list[i])
        return alist

    @staticmethod
    def lst_trans1(lst, n):
        m = int(math.ceil(len(lst) / float(n)))
        sp_lst = []
        for i in range(n):
            sp_lst.append(lst[i * m:(i + 1) * m])
        return sp_lst

    # 可以不使用math模块
    @staticmethod
    def lst_trans2(lst, n):
        if len(lst) % n != 0:
            m = (len(lst) // n) + 1
        else:
            m = len(lst) // n
        sp_lst = []
        for i in range(n):
            sp_lst.append(lst[i * m:(i + 1) * m])
        return sp_lst

    @staticmethod
    def lst_trans3(lst, n):
        length = len(lst)
        sp_lst = []
        for i in range(n):
            sp_lst.append(
                lst[math.floor(i / n * length):math.floor((i + 1) / n * length)]
            )
        return sp_lst

    # </editor-fold>
    # <editor-fold desc="数组过长-取100个点">
    @staticmethod
    def array_too_long_take50points(data_lis, re_len=100):
        if len(data_lis) > re_len:
            yu_num = int(len(data_lis) / re_len)
            return [data_lis[i] for i in range(len(data_lis)) if i % yu_num == 0]

        else:
            return data_lis

    # </editor-fold>
    # <editor-fold desc="列表随机返回n个元素">
    @staticmethod
    def renyishuju(lis, n):
        # lis = [i * 10 for i in range(10)]
        return random.choices(lis, k=n)

    # </editor-fold>
    # <editor-fold desc="列表中大于一个数的个数">
    @staticmethod
    def greater_num_list(data: list, num):
        data = [i for i in data if i > num]
        return data, len(data)

    # </editor-fold>
    # <editor-fold desc="列表-列表字典排序">
    @staticmethod
    def list_order(data: list, fields=None):
        """
        :param data:
        :param value:list 传入 索引  字典传入keys
        :return: list
        """
        if fields:
            data: list = sorted(data, key=lambda k: k[fields])
        else:
            data.sort()
        return data

    # </editor-fold>
    # <editor-fold desc="取出两者之间的数据">
    @staticmethod
    def between(data, min_value=None, max_value=None):
        if max_value and min_value:
            l2 = [i for i in data if i >= min_value and i <= max_value]
        elif min_value:
            l2 = [i for i in data if i >= min_value]
        elif max_value:
            l2 = [i for i in data if i <= max_value]
        else:
            l2 = []
        return l2

    # </editor-fold>
    # <editor-fold desc="一维列表元素按指定个数分组">
    @staticmethod
    def list_group(lists, n):
        return [lists[i:i + n] for i in range(0, len(lists), n)]

    # </editor-fold>
    # <editor-fold desc="二维数据进行等比区间分组-固定组数-求个数">
    @staticmethod
    def no_grouping_equivalent_interval(lis, n):
        """
        data2, x = group_n(example_list, 10)
        :param a: lis
        :param n: 个数
        :return:
        """
        dimensional_lis = ListOperation.dimensional_list_two_same(lis)
        lis = dimensional_lis[0]
        lis1 = dimensional_lis[1]
        l = len(lis)
        interval = (max(lis) - min(lis)) / n  # 区间长度
        section = []  # 每个区间的范围
        # 横坐标
        x_section = []
        for i in range(n):
            section.append([min(lis) + i * interval, min(lis) + (i + 1) * interval])
            x_section.append(str(round(min(lis) + i * interval, 2)))
            # x_section.append(str(round(min(lis) + i * interval, 2)) + '~' + str(round(min(lis) + (i + 1) * interval, 2)))
        divided_list = [[] for i in range(n)]
        for i in range(l):
            for j in range(n):
                if section[j][0] <= lis[i] <= section[j][1]:
                    divided_list[j].append(lis1[i])
        y_section = []
        dic = {}
        for index, value in enumerate(divided_list):
            # y_section.append(value.__len__())
            # y_section.append(value)
            dic[x_section[index]] = round(len(value) / len(lis1), 2)
            # dic[x_section[index]] = value.__len__()
        # return y_section, x_section, dic
        return dic

    # </editor-fold>

    # <editor-fold desc="二维数据中，各个数据所占的百分比">
    @staticmethod
    def all_np_fen(arr_list):
        # 拼接数组函数
        List = list(itertools.chain.from_iterable(arr_list))
        arr = np.array(List)
        # print(arr.shape, type(arr.shape[0]))  # 二维元素的个数
        key = np.unique(arr)
        result = {}
        for k in key:
            mask = (arr == k)
            arr_new = arr[mask]
            v = arr_new.size
            result[k] = v
        key_list = list(result.keys())
        num_count = arr.shape[0]
        return_result = {}
        for keys in key_list:
            # print(result[keys] / num_count, type(result[keys] / num_count))
            dat = result[keys] / num_count
            return_result[str(keys)] = NumberOperation.decimalToPercentageFuncTwo(dat)

        # {1: 2, 2: 3, 3: 3, 4: 1, 5: 3}
        return return_result

    # def tuokonglv():
    #     dic = all_np_fen([[1, 1, 3, 2, 2, 2, 2, 2, 2, 2, 3], [3, 2, 1], [4, 5, 6]])
    #     print(dic)

    # tuokonglv()

    # </editor-fold>
# </editor-fold>
