#!/usr/bin/env python
# coding=utf-8
from __future__ import division
import word2vec, time, ConfigParser, os, codecs
from gensim.models import word2vec
from gensim.models.word2vec import Word2Vec
import numpy as np
import re

cfdic = 'config'
cf = ConfigParser.ConfigParser()
cf.read(cfdic)
home_path = cf.get('info', 'home_path')
englishweight = 2.0
englishvectorSize = 100
# model=Word2Vec.load(output+'/model')
model = None  # 这里先不使用wordvec的向量


def getwordvec(word):
    vec = []
    try:
        vec = (model[word])
    except BaseException:
        vec = np.random.random(englishvectorSize)
    return vec


def weight(clength, elength):
    '''根据设置的英文权重得到在之后需要归一化时的权重，
    当英文/中文长度为0时,直接返回
    '''
    if (clength == 0):
        return (0, 1)
    if (elength == 0):
        return (1, 0)
    alllength = clength + elength
    ew = elength / alllength
    cw = clength / alllength
    w2 = englishweight * ew
    w1 = 1 - w2
    return (w1, w2)


def getenglish(word):
    '''针对输入的字符串，抽取出英文，计算出向量，
    而后计算出剩余中文部分长度rlength.abs
    返回内容有英文向量，中文长度，英文单词个数中文字符串
    现返回内容有英文向量，中文权值，英文权值，中文字符串
    '''
    pat_1 = re.compile(ur'[\u4e00-\u9fa5]')
    res = filter(lambda x: x != '', pat_1.split(word))
    res = map(lambda x: x.strip('\n'), res)
    wordlength = 0
    elength = 0
    vector = np.zeros(englishvectorSize)
    for i in res:
        ii = filter(lambda x: x != '', i.split('-'))
        for iii in ii:
            wordlength = wordlength + 1
            elength += len(iii)
            vector += getwordvec(iii.lower()) * 1.0 / wordlength
        word.replace(i, '')
    if (wordlength == 0):
        return (vector, 1, 0, word)  # 如果其中不包含英文，直接返回
    rlength = len(word) - elength
    (w1, w2) = weight(rlength, wordlength)
    return (vector, w1, w2, word)


if __name__ == '__main__':
    print getwordvec('hello')
