# coding=utf-8
# 从sql文件里导出来相应的csv表格，最后的csv以逗号进行分割
# 但是这里的sql文件是已经去除了头部相关说明的sql文件，也就是需要自己再处理一下
# 写这个的原因是有个sql导入到sql wordbench里从而生成csv表出现错误，未知原因
import codecs, ConfigParser

# 导入相关配置
cfdic = 'config'
cf = ConfigParser.ConfigParser()
cf.read(cfdic)
home_path = cf.get('info', 'home_path')
input_path = home_path + 'data/hhm_data_170227/hhm_data_170227/by_order_detail_convert.sql'
output_path = home_path + 'data/by_order_detail_convert.csv'
inputfile = codecs.open(input_path, 'r', 'utf-8')
inputfile = inputfile.readlines()
output_file = codecs.open(output_path, 'w', 'utf-8')
inputfile = map(lambda x: x.replace('\n', ' '), inputfile)
result = []
for i in inputfile:
    i = i.replace("INSERT INTO `by_order_detail_convert` VALUES", '')
    listi = i.split(" ('O201")
    listi = filter(lambda x: len(x) != 0, listi)
    listi = map(lambda x: "'O201" + x, listi)  # 恢复id号
    listi = map(lambda x: x[0:-2], listi)  # 去除末尾括号和逗点
    listi = map(lambda x: x.replace("", ''), listi)
    listi = map(lambda x: x.replace(" ", ''), listi)
    listi = map(lambda x: x[1:-1], listi)
    listi = map(lambda x: x.replace('null', "''"), listi)
    for j in listi:
        result.append(j)
for i in result:
    output_file.write(i + '\n')
