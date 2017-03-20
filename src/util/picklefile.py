# coding=utf-8
# 文件主要包含给定文件名称和对象进行序列化的步骤和从文件中恢复
import pickle


def pickleit(filepath, file):
    fileout = open(filepath, 'wb')
    pickle.dump(file, fileout, -1)
    fileout.close()


def unpickleit(filepath):
    filein = open(filepath, 'rb')
    file = pickle.load(filein)
    filein.close()
    return file
