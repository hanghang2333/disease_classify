# coding=utf-8
# 将字符串里的英文转换为中文，无法处理希腊字母，这里将希腊字母简单转化为a，b
import re, codecs, ConfigParser
from translate import Translator

translator = Translator(to_lang="zh")
cfdic = 'config'
cf = ConfigParser.ConfigParser()
cf.read(cfdic)
home_path = cf.get('info', 'home_path')
flog = codecs.open(home_path + 'data/englishtochinese1.txt', 'r', 'utf-8')
enchlog = flog.readlines()
flog.close()
flog = codecs.open(home_path + 'englishtochinese1.txt', 'a', 'utf-8')
enchlog = map(lambda x: x.replace('\n', ''), enchlog)
enchlog = map(lambda x: x.split(), enchlog)
enchlog = filter(lambda x: len(x) == 2, enchlog)
enlog = map(lambda x: x[0], enchlog)
enlog = map(lambda x: x.lower(), enlog)  # 将键值都设置为小写
chlog = map(lambda x: x[1], enchlog)
enchzip = zip(enlog, chlog)
enchdict = dict((name, value) for name, value in enchzip)


def hasenglish(word):
    '''存在英文返回True，不存在返回flase
    '''
    for c in word:
        if (c >= u'\u0041' and c <= u'\u005a') or (c >= u'\u0061' and c <= u'\u007a'):
            return True
    return False


def FullToHalf(s):
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


def en2ch(word):  # 直接整个翻译,目前使用的是这种方式
    translation = ''
    word = word.strip('\n')
    word = word.strip().lower()  # 去除开头结尾的空格
    word = word.replace(' ', '-')  # 将词之间的空格转换为-
    if (hasenglish(word) == True):
        try:
            translation = enchdict[word]
        except BaseException as e:
            print 'need search'
            print word
            return word
            # 下面是联网翻译，这一步需要加一个exceprion
            # 不过速度非常慢，是否有必要非翻译不可呢
            '''
            try:
                translation = translator.translate(word.encode('utf8'))
                flog.write(word+' '+translation.replace(' ','')+'\n')
                enchdict[word]=translation.replace(' ','')
            except BaseException as e:
                print 'can not translate'
            '''
        return translation
    else:
        return word


def test():
    file = codecs.open('/home/lihang/wordembed/data/english.txt', 'r', 'utf-8')
    filetext = file.readlines()
    file.close()
    fwrite = codecs.open('/home/lihang/wordembed/output/englishtochinese.txt', 'w', 'utf-8')
    for i in filetext:
        print 'h'
        fwrite.write(i.strip('\n') + ' ' + en2ch(i) + '\n')
    fwrite.close()


def main():
    print en2ch(u'AD')


if __name__ == '__main__':
    main()
