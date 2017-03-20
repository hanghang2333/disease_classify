# coding=utf-8
from __future__ import division
import os, codecs, ConfigParser
import numpy as np

cfdic = 'config'
cf = ConfigParser.ConfigParser()
cf.read(cfdic)
home_path = cf.get('info', 'home_path')
wfilepath = home_path + 'data/body.txt'
mfilepath = home_path + 'data/common.txt'


def calculate(all, w, m, wr, mr):
    '''根据加重权计算减轻权
    按照相应想要降低和增加权重，重新安排权重，所以设置时应该wr>1,mr<1.
    '''
    tempall = all - w - m + w * wr + m * mr
    if (tempall == 0):
        return (1, 1, 1)
    wrr = wr * all / tempall
    mrr = mr * all / tempall
    nrr = 1 * all / tempall
    return (wrr, mrr, nrr)


def getwm(wordlist, wr, mr):
    '''给定需要加重和减轻以及总数，和加重比例，输出
    权重list。
    '''
    wfile = codecs.open(wfilepath, "r", "utf-8")
    importword = wfile.readlines()
    importword = map(lambda x: x[0:-1], importword)
    wfile.close()
    mfile = codecs.open(mfilepath, "r", "utf-8")
    commonword = mfile.readlines()
    commonword = map(lambda x: x[0:-1], commonword)
    mfile.close()

    all = len(wordlist)
    w = 0
    m = 0
    for i in wordlist:
        if (i in importword):
            w = w + 1
        elif (i in commonword):
            m = m + 1
    (wrr, mrr, nrr) = calculate(all, w, m, wr, mr)
    weightlist = []
    for i in wordlist:
        if (i in importword):
            weightlist.append(wrr)
            # weightlist.append(1)
        elif (i in commonword):
            weightlist.append(mrr)
            # weightlist.append(1)
        else:
            weightlist.append(nrr)
            # weightlist.append(1)
    return weightlist


def test(word, wr, mr):
    res = getwm(word, wr, mr)
    print res


def main():
    word = u"病症"
    wr = 1.3
    mr = 0.7
    test(word, wr, mr)


if __name__ == '__main__':
    main()
