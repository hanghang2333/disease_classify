# coding=utf-8
import codecs, csv


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
