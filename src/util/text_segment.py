# coding=utf-8
# 这里做的工作有:合并字典，停止词，导入字典。
# 使用的时候对于路径有些要求，需要对应路径上有对应文件
import jieba, os, ConfigParser
import text
# 导入相关配置
cfdic = 'config'
cf = ConfigParser.ConfigParser()
cf.read(cfdic)
home_path = cf.get('info', 'home_path')
# home_path = '/home/lihang/disease_analysis/'
rawfile = home_path + 'data/segment_data/'
output = home_path + 'data_output/'


# 合并字典和停止词到一个文件(因为只能load一个用户字典)
def mergefile(filename, original):
    temp = open(filename, 'r')
    cont = temp.readlines()
    for i in cont:
        original.append(i)
    temp.close()


def treefile(treedir, filepath):
    f = open(filepath, 'a+')
    original = f.readlines()
    f.close()
    for root, dirs, files in os.walk(treedir):
        for file in files:
            filename = os.path.join(root, file)
            mergefile(filename, original)
    f = open(filepath, 'w')
    s = set(original)
    for i in s:
        f.write(i)
    f.close()


def merge():
    dictfile = rawfile + 'dict/'
    stopfile = rawfile + 'stop/'
    dict_now = rawfile + 'dict_now'
    stop_now = rawfile + 'stop_now'
    treefile(dictfile, dict_now)
    treefile(stopfile, stop_now)
    return dict_now, stop_now


def is_num(num):  # 判断分完词的词是否是纯数字，因为一个纯数字的话对应于tfidf和doc2vec似乎都是没有什么意义的
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_eng(eng):
    try:
        eng.decode('ascii')
        return True
    except UnicodeError:
        return False


dict_now, stop_now = merge()
jieba.load_userdict(dict_now)  # 这一步和下一步时间较久，故而全局只运行一次
stopwords = set(text.get_text_from_file(stop_now))


def get_dict_stop_path():
    return dict_now, stop_now


def segment(text):
    # text:文本串
    # 返回:分好词的文本串，以空格分割
    seg_list = jieba.cut(text)
    result = ''
    for i in seg_list:
        if (i not in stopwords and not is_num(i) and not is_eng(i)):
            result = result + ' ' + i
        result = result.strip()
    return result


print segment(u'hunt综合征')
