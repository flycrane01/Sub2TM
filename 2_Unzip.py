#!/usr/bin/python
#coding=utf-8

"""
解压各个目录下的文件
"""

import zipfile
import os
import codecs
import glob
from pathlib import Path


def dirlist(path, keyword):
    '''
    遍历path及子目录，寻找所有文件名（及后缀名）中包含keyword的文件，返回其相对路径列表
    '''
    tmp = dict()
    files = glob.glob(path+'\**',recursive=True)
    for file in files:
        if keyword in file:
            tmp[os.path.splitext(file)[0]] = os.path.splitext(file)[1]
    desired = [i+tmp[i] for i in tmp]
    return desired


def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    for names in zip_file.namelist():
        p = Path(zip_file.extract(names,file_name + "_files/"))
        try:
            #使用cp437对文件名进行解码还原
            names = names.encode('cp437')
            #win下一般使用的是gbk编码
            names = names.decode("gbk")
            p.rename(file_name + "_files/" + names)
        except:
            #如果已被正确识别为utf8编码时则不需再编码
            pass
    zip_file.close()


if __name__ == '__main__':
    path = r'../1'
    dirs = dirlist(path,".zip")
    for m in dirs:
        try:
            print(m)
            un_zip(m) #解压zip文件
        except:
            print('Failed!')
            pass