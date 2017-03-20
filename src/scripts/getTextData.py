# coding=utf-8
import csv, codecs, ConfigParser
import sys

# 导入相关配置
cfdic = 'config'
cf = ConfigParser.ConfigParser()
cf.read(cfdic)
home_path = cf.get('info', 'home_path')
detail_path = home_path + 'data/by_o_order_detail.csv'
convert_path = home_path + 'data/by_order_detail_convert.csv'
write_path = home_path + 'data_output/disease_detail.txt'


def get_text_from_file(filepath):
    # filepath:完整的文件路径
    # 输出:文件内容list，每行已经去除了换行'\n'
    file = codecs.open(filepath, 'r', 'utf-8')
    filetext = file.readlines()
    file.close()
    filetext = map(lambda x: x.replace('\n', ''), filetext)
    return filetext


def get_text_from_csvfile(filepath):
    #    #filepath:完整的文件路径,文件为csv格式的
    # 输出:文件内容list，每行已经去除了换行'\n'
    csv_reader = csv.reader(open(filepath))
    content_list = []
    for i in csv_reader:
        content_list.append(i)
    content_list = map(lambda x: map(lambda y: y.replace('\n', ''), x), content_list)
    return content_list


detail_list = get_text_from_csvfile(detail_path)
convert_list = get_text_from_file(convert_path)
convert_list = map(lambda x: x.split("','"), convert_list)
print len(detail_list)
print len(convert_list)
detail_list = filter(lambda x: len(x) == 7, detail_list)  # 长度为说明有效字段
fail_list = filter(lambda x: len(x) != 4, convert_list)  # 查看是否有没有ocr数据的订单
for i in fail_list:
    print i
convert_list = filter(lambda x: len(x) == 4, convert_list)  # 同上
print len(detail_list)
print len(convert_list)
# print convert_list[0]
# convert_list = filter(lambda x:x[1]!='检查报告',convert_list)#考虑到检查报告的识别度不是很好，这里去掉测试一些效果如何
# 将病单里的文本都提取到一个句子中。并且以病单号为id建立dict
disease_analysis = {}


def id2id():
    idid = {}  # 病单id到接单医生id
    idid2 = {}  # 病单id到提单医生id
    for i in detail_list:
        idid[i[0]] = i[5]
        idid2[i[0]] = i[6]
    return (idid, idid2)


(idid, idid2) = id2id()
for i in detail_list:
    count = 0
    id = i[0]
    # test = i[3]+i[4]
    test = ''
    # 在ocr识别数据不好的情况下，如果不能很好的处理该数据，其实有的效果反而不如没有
    for j in convert_list:
        if (j[0] == id):
            count = count + 1
            test = test + j[3].encode('utf8')
    if (count == 0):
        print(id)
    test = test.replace('\n', '')
    test = test.replace('|#|', '')
    test = i[3] + '|#|' + i[4] + '|#|' + test
    disease_analysis[id] = test
write_file = codecs.open(write_path, 'w', 'utf-8')
for i in disease_analysis:
    write_file.write(i.decode('utf8'))
    write_file.write(u'|#|' + disease_analysis[i].decode('utf8') + u'|#|' + idid[i] + '|#|' + idid2[i] + '\n')
