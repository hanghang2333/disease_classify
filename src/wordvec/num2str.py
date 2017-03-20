#coding=utf-8
from __future__ import division
import re
ChineseNum = [u"零", u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九"]
num = ["0","1","2","3","4","5","6","7","8","9"]
numset=set(num)
RomanChineseNum = [u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九",u"十"]
RomanNum = [u"Ⅰ", u"Ⅱ", u"Ⅲ", u"Ⅳ", u"Ⅴ", u"Ⅵ", u"Ⅶ", u"Ⅷ", u"Ⅸ", u"Ⅹ"]
RomanNumset=set(RomanNum)
replace_dict = dict(zip(RomanNum, RomanChineseNum))
replace_num=dict(zip(num,ChineseNum))


def makeNumtoStr(word):
    '''将字符串里的数字替换为汉字
    '''
    for i in word:
        if(i in numset):
            word = word.replace(i,replace_num[i])
        if(i ==u'〇' or i==u'○'):#这个东西,,,,目前就这样处理吧
            word = word.replace(i,u'零')
    return word


def temproman(word):
    '''将字符串里的罗马数字替换为汉字
    目前没有写出更加通用的办法，只能处理罗马一到十数组的替换,
    不过数据里其实也只有一到十的罗马数字
    '''
    for i in word:
        if(i in RomanNumset):
            word = word.replace(i,replace_dict[i])
    return word


def roman(match):
    # 目前没有使用这个函数
    return replace_dict[str(match.group(0)).encode('utf-8')]   


def makeRomantoStr(word):
    # 目前没有使用这个函数
    print "here"
    pattern = re.compile(r'Ⅳ')
    match = pattern.match(word)
    if match:
        print "match"
        word = pattern.sub(roman, word)
    return word
'''下面是测试部分
'''
def test():
    teststr=u"ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ"
    res=makeNumtoStr(teststr)
    res=temproman(res)
    print res
    return res
def main():
    test()
if __name__=='__main__':
    main()