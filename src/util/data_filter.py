# coding=utf-8
import codecs, ConfigParser
import text

cfdic = 'config'
cf = ConfigParser.ConfigParser()
cf.read(cfdic)
home_path = cf.get('info', 'home_path')


def get_doctor_more(datalines):
    # 将接单树超过一次的医生的id放到set里返回
    doc_doctor = {}
    for i in datalines:
        doc_doctor[i[0]] = i[4]
    doctor_doc = {}  # {doctor-doclist}
    for i in doc_doctor:
        tmp = doctor_doc.get(doc_doctor[i], [])
        if tmp == []:
            doctor_doc[doc_doctor[i]] = [i]
        else:
            tmp.append(i)
            doctor_doc[doc_doctor[i]] = tmp
    # 将多余一个病单的医生的id存储到一个set里
    doctor = set()
    for i in doctor_doc:
        if (len(doctor_doc[i]) >= 2):
            doctor.add(i)
    return doctor


def remove_one_doctor(datalines):
    # datalines:已经进行了分割，每一行对应病单id，病单text，专家id
    # 从给定的所有数据里筛去对应医生只有一单的那些
    # 首先对应出病单到医生的dict，而后反过来医生到病单list的dict，而后医生到对应病单个数为1的dict，而后过滤
    doctor = get_doctor_more(datalines)
    # 过滤
    datafilter = filter(lambda x: x[4] in doctor, datalines)
    return datafilter


# 从给定的所有测试数据里筛去对应医生没有在训练数据里出现过的那些
def get_train_doctor():
    # 从过滤后的训练数据里获取医生id集合
    train_path = home_path + "data_output/disease_detail_segment.txt"
    saved_path = home_path + "data_output/model.bin"
    train_text = text.get_text_from_file(train_path)
    train_text = train_text[0:1500]  # 这里只选取前1500条作为训练
    train_text = map(lambda x: x.split('|#|'), train_text)
    train_text = filter(lambda x: len(x) == 6, train_text)
    doctor = get_doctor_more(train_text)
    return doctor


def remove_not_present(test_datalines):
    # 需要有一个训练数据里医生的set。
    doctor = get_train_doctor()
    test_datalines = filter(lambda x: x[4] in doctor, test_datalines)
    return test_datalines


if __name__ == '__main__':
    print(len(get_train_doctor()))
