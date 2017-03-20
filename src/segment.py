# coding=utf-8
from __future__ import division
import ConfigParser,codecs
from util import text,text_segment
from wordvec import wordvec,synonym
import multiprocessing
#导入配置信息
cfdic = 'config'
cf = ConfigParser.ConfigParser()
cf.read(cfdic)
home_path=cf.get('info','home_path')
dimension = 100
text_now = home_path+'data_output/disease_detail.txt'
outname = home_path+'data_output/disease_detail_segment.txt'
rawfile = home_path+'data/segment_data/'
dict_now,stop_now = text_segment.get_dict_stop_path()
word_vec_sim = wordvec.VecSim()
#all_word_path = home_path+"data/expertword.txt"
all_word_path = home_path+"data/hhmdict_un"
all_word = set(text.get_text_from_file(all_word_path))
def main():
    '''
    :parameter:
    :return: 多线程运行这个分词，查相似词，打印输出的过程
    '''
    pool = multiprocessing.Pool(processes=4)
    for i in range(4):
        pool.apply_async(segment, (text_now,outname,i))
    pool.close()
    pool.join()
def segment(text_now,outname,num):
    f = codecs.open(text_now,'r','utf-8')
    fout = codecs.open(outname,'a+','utf-8')
    fstrings = f.readlines()
    length = len(fstrings)
    start = int(length/4*num)
    end = int(length/4*num+length/4)
    fstrings = fstrings[start:end]
    f.close()
    flines = map(lambda x:x.split('|#|'),fstrings)
    print len(flines)
    for line in flines:
        id = line[0]
        d_text = line[1]
        writelist_d = text_segment.segment(d_text)
        d_text_sim_all = []
        d_text_list = writelist_d.split()
        for i in d_text_list:
            ilist = set()
            if u'症' in i:#这两句就是单独处理这两个字，，没想到更好的办法
                ilist.update(synonym.getsyn(i))
                ilist.update(synonym.getsyn(i.replace(u'症',u'征')))
            elif u'征' in i:
                ilist.update(synonym.getsyn(i))
                ilist.update(synonym.getsyn(i.replace(u'症',u'征')))
            ilist=list(ilist)
            if len(ilist)>1:#有同义词则肯定在疾病名称里面直接extend
                d_text_sim_all.extend(ilist)
            elif i in all_word:
                d_text_sim_all.append(i)           
        if writelist_d.replace(' ','')!='':
            d_text_sim_word = word_vec_sim.calc_sim_topn_word(writelist_d.replace(' ',''),5)
        #if d_text_list != []:
        #    d_text_sim_word = word_vec_sim.calc_sim_topn_word_by_textlist(d_text_list,5)
        else:
            d_text_sim_word = []
        for i in d_text_sim_word:
            if i in d_text_sim_all:
                d_text_sim_word.remove(i)
        d_text_sim_all.extend(d_text_sim_word[0:5-len(d_text_sim_all)])
        fout.write(id+'|#|'+writelist_d)
        fout.write('|#|'+' '.join(d_text_sim_all))
        fout.write('\n')           
def segment_t(text_now,outname):
    '''
    :param text_now:目前的需要分词的目录
    :param outname: 输出文件名称
    :return: None
    '''
    f = codecs.open(text_now,'r','utf-8')
    fout = codecs.open(outname,'w','utf-8')
    fstrings = f.readlines()
    length = len(fstrings)
    f.close()
    flines = map(lambda x:x.split('|#|'),fstrings)
    print len(flines)
    for line in flines:
        id = line[0]
        d_text = line[1]
        writelist_d = text_segment.segment(d_text)
        fout.write(id+'|#|'+writelist_d)
        fout.write('\n')           
if __name__=='__main__':
    main()
    #segment_t(text_now,outname)