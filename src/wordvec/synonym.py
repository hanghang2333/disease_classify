#coding=utf-8
from __future__ import division
from __future__ import unicode_literals
import codecs , ConfigParser , redis
cfdic = 'config'
cf = ConfigParser.ConfigParser()
cf.read(cfdic)
home_path = cf.get('info','home_path')
filepath = home_path+'data/synonym'
'''读取同义词文件,并建立dict,是后续相近词查找的一个基础'''


def makedict():
    '''
    初步读取同义词文件得到初步dict
    :return:
    '''
    syndict = {}
    file = codecs.open(filepath, 'r', 'utf-8')
    filetext = file.readlines()
    file.close()
    filetext = map(lambda x:x.strip("\n"),filetext)
    filetext = map(lambda x:x.split(','), filetext)
    for line in filetext:
        for word in line:
            try:
                res = syndict[word].split()
                res.extend(line)
                syndict[word]=' '.join(list(set(res)))
            except Exception as e:
                syndict[word]=' '.join(line)
    return syndict


def getsyn(word):
    '''
    针对一个词，输出其所有同义词包括自己
    :param word:
    :return:
    '''
    syms = []
    try:
        syms=syndictb[word.lower()].split()
    except Exception as e:
        syms=[word]
    return syms
# 建立词典
syndict=makedict()
# 对词典处理，使得其真正能够对每一个词都输出所有同义词，即处理相互调用这种情况
for keyword in syndict:
    res=syndict[keyword].split()
    restmp=list(res)
    for valueword in restmp:
        try:
            dd=syndict[valueword].split()
            res.extend(dd)
        except Exception:
            pass
    syndict[keyword]=' '.join(list(set(res)))
# 对词典处理，即将键值都换为小写
syndictb = {}
for i in syndict:
    syndictb[i.lower()]=syndict[i]
def main():
    res=getsyn('hunt综合征')
    #print res
    for i in res:
        print i
if __name__ == '__main__':
    main()
