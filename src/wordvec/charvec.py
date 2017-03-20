# coding=utf-8
from __future__ import division
import codecs, string, ConfigParser, re
import numpy as np
import num2str
import changeweight
import english

# 本文件是字向量求相似度的应用，目前是打算应用在当前诊断这个字段上
# 因为这个字段里面大都是比较规范的疾病名称，但又不是严格的，恰好可以使用之前的字向量模型方法
cfdic = 'config'
cf = ConfigParser.ConfigParser()
cf.read(cfdic)
home_path = cf.get('info', 'home_path')
charpath = home_path + 'data/char.txt'
dimension = 100


def makestr2num(strlist):
    """将str list的str转为float
    """
    tem = []
    tem.append(strlist[0])
    tem.append(strlist[1])
    for i in range(2, len(strlist)):
        tem.append(string.atof(strlist[i]))
    return tem


def readchar():
    """从char里读取出所有的(k,v)值存入dict里
    k=tuple(word,index),v=list[float]
    """
    fchar = codecs.open(charpath, 'r', 'utf-8')
    flines = fchar.readlines()
    fchar.close()
    flineslist = map(lambda x: x.split("\t"), flines)
    """读取char文件后每行长度和内容"
    从上面输出可以看到从char读取的每行103个，最后有一位\n符号。
    这里通过filter去除开始的几行，通过map去除了每行最后的\n
    """
    ftemp1 = filter(lambda x: len(x) == (dimension + 3), flineslist)
    ftemp2 = map(lambda x: x[0:-1], ftemp1)
    ftemp3 = map(makestr2num, ftemp2)
    ftemp = map(lambda x: ((x[0], x[1]), x[2:]), ftemp3)
    fmap = dict((k, v) for k, v in ftemp)
    return fmap


class charvec(object):
    def __init__(self):
        # 初始化的时候导入相关的文件放到内存里
        self.fmap = readchar()

    def getchar(self, c):
        """从c为依据获取char里这个字符的对应向量
        """
        defaultlist = []
        reslist = self.fmap.get(c, [])
        if (isinstance(reslist, list)):
            return reslist
        return []

    def FullToHalf(self, s):
        n = []
        for char in s:
            num = ord(char)
            if num == 0x3000:
                num = 32
            elif 0xFF01 <= num <= 0xFF5E:
                num -= 0xfee0
            num = unichr(num)
            n.append(num)
        return ''.join(n)

    def getwordchar(self, word):
        """对word里每一个汉字都依次读取出向量并归一化加和
        其中需要根据字符在word的位置来分case取，返回np.ndarray向量转为list
        之后还需要根据设定好的权重来进行归一化
        !还没处理空串！
        """
        word = word.replace(' ', '')
        word = self.FullToHalf(word)  # 将word里全角符号转换为半角符号
        word = num2str.makeNumtoStr(word)  # 这里的word已经将阿拉伯数字转换
        word = num2str.temproman(word)  # 这里的word已经将罗马数字转换
        word = re.sub("[)＋－：\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）【】]+".decode("utf8"), "".decode("utf8"), word)
        (englishvec, cw, ew, word) = english.getenglish(word)  # 这里的word已经截出了英文内容
        weight = changeweight.getwm(word, 1.5, 0.5)
        length = len(word)
        c = ("word", "index")
        reslist = np.zeros(dimension)
        if (length == 0):
            return reslist
        count = 0  # 应该和length一样后续简化去除掉
        rl = []
        for i in range(length):
            if (length == 1):
                c = (word[i], 's')  # 单独
            elif (i == 0):
                c = (word[i], 'b')  # 开始
            elif (i == length - 1):
                c = (word[i], 'e')  # 结束
            else:
                c = (word[i], 'm')  # 中间
            clist = np.array(self.getchar(c))
            if (clist.shape == (dimension,)):
                count = count + 1
                rl.append(clist * weight[i])
        for i in rl:
            reslist += i / count
        # res=np.ndarray.tolist(reslist)
        reslist = reslist * cw + englishvec * ew  # 对于英文处理的权重分配
        res = reslist
        return res


"""下面是测试部分
"""


def test():
    dui = charvec()
    word = u"失眠"
    res = dui.getwordchar(word)
    print(res)
    word = u'无语'
    res = dui.getwordchar(word)
    print(res)


def main():
    test()


if __name__ == '__main__':
    main()
