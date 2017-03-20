#coding=utf-8
'''
本文件预先将先前订单数据里的当前诊断这一部分的向量求出并且存储到dict:{病单id，向量}
'''
from __future__ import division
import codecs,ConfigParser,csv
from numpy import linalg
import charvec
import numpy as np
cfdic = 'config'
cf = ConfigParser.ConfigParser()
cf.read(cfdic)
home_path = cf.get('info','home_path')
char = charvec.charvec()
dimension = 100


def get_text_from_file( filepath ):
    '''
    :param filepath:完整的文件路径
    :return:文件内容list，每行已经去除了换行'\n'
    '''
    file = codecs.open(filepath,'r','utf-8')
    filetext = file.readlines()
    file.close()
    filetext = map(lambda x: x.replace('\n',''),filetext)
    return filetext


def get_text_from_csvfile(filepath):
    '''
    :param filepath:完整的文件路径,文件为csv格式的
    :return: 文件内容list，每行已经去除了换行'\n'
    '''
    csv_reader = csv.reader(open(filepath))
    content_list = []
    for i in csv_reader:
        content_list.append(i)
    content_list = map(lambda x:map(lambda y:y.replace('\n',''),x),content_list)
    return content_list


def word_vec_dict():
    '''
    从原文件里获取出docid-当前诊断的list。
    :return:
    '''
    # detail_path = home_path+"data/expertword.txt"
    detail_path = home_path+"data/hhmdict_un"
    detail_list = get_text_from_file(detail_path)
    # 将每一个诊断都转换为vec。
    # 这里的vec类型为lnp.array比较好。
    detail_list = map(lambda x:[x,char.getwordchar(x)],detail_list)
    return detail_list


class VecSim(object):
    def __init__(self):
        self.detail_list = word_vec_dict()
        self.detail_list_dict = dict((x[0],x[1]) for x in self.detail_list)

    def calc_sim(self,text):
        '''
        针对输入的文本,首先将其转换为向量,而后求出其与前面所有订单的相似度值
        :param text:
        :return:返回{id:sim,id:sim}
        '''
        vec = char.getwordchar(text)
        sim_dict = {}
        for i in self.detail_list:
            sim = self.calc_sim_enc(vec,i[1])
            sim_dict[i[0]] = sim
        return sim_dict

    def calc_vec(self,text):
        '''
        给定词求出词向量
        :param text:
        :return:
        '''
        return char.getwordchar(text)

    def calc_vec_mean(self,textlist):
        '''
        给定一组词list，求出平均向量
        :param textlist:
        :return:
        '''
        res = np.zeros(dimension)
        if len(textlist) == 0:
            return res
        for i in textlist:
            res = self.calc_vec(i)/len(textlist)
        return res

    def calc_sim_by_vec(self,vec):
        '''
        通过向量值计算出相似dict
        :param vec:
        :return:
        '''
        sim_dict = {}
        for i in self.detail_list:
            sim = self.calc_sim_enc(vec,i[1])
            sim_dict[i[0]] = sim
        return sim_dict

    def calc_sim_topn_word_by_textlist(self,textlist,n):
        '''
        通过给定textlist和num，返回由这串textlist求出的相似词
        :param textlist:
        :param n:
        :return:
        '''
        sim_dict = self.calc_sim_by_vec(self.calc_vec_mean(textlist))
        sim_dict = sorted(sim_dict.iteritems(), key=lambda d:d[1], reverse = True)
        sim_dict = sim_dict[0:n]
        rl = map(lambda x:x[0],sim_dict)
        return rl

    def calc_sim_two(self,text1,text2):
        '''
        计算两个词之间的相似度
        :param text1:
        :param text2:
        :return:
        '''
        vec1 = char.getwordchar(text1)
        vec2 = char.getwordchar(text2)
        return self.calc_sim_enc(vec1,vec2)

    def calc_sim_cos(self,vec1,vec2):
        '''
        使用cos相似度计算向量间相似度
        :param vec1:
        :param vec2:
        :return:
        '''
        return np.dot(vec1, vec2) / ((np.dot(vec1, vec1) * np.dot(vec2, vec2)) ** 0.5)

    def calc_sim_enc(self,vec1,vec2):
        '''
        使用欧式距离来计算向量间相似度
        :param vec1:
        :param vec2:
        :return:
        '''
        return 1.0 /(1.0 + linalg.norm(vec2 - vec1))

    def calc_sim_topn(self, text, n):
        '''

        :param text:文本
        :param n:数目
        :return:[(id,sim),(id,sim)]
        '''
        sim_dict = self.calc_sim(text)
        sim_dict = sorted(sim_dict.iteritems(), key=lambda d:d[1], reverse = True)
        sim_dict = sim_dict[0:n]
        return sim_dict

    def text_topn(self,text,n):
        '''
        :param text:
        :param n:
        :return:
        '''
        res = self.calc_sim_topn(text, n)
        print '----'
        for i in res:
            print i[0]+' '+str(i[1])

    def calc_sim_topn_word(self,text,n):
        '''
        :param text:
        :param n:
        :return:
        '''
        res = self.calc_sim_topn(text,n)
        rl = map(lambda x:x[0],res)
        return rl
if __name__ == '__main__':
    text = u'尘肺 肺癌'
    vec = VecSim()
    vec.text_topn(text,10)
    print vec.calc_sim_topn_word(text, 10)
    print vec.calc_sim_two(u'脑梗', u'脑梗死')
    print vec.calc_sim_two(u'脑梗', u'脑干出血')
    res = vec.calc_sim_topn_word_by_textlist([u'尘肺', u'肺癌'],5)
    for i in res:
        print i
