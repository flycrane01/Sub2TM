#!/usr/bin/env python

import glob
import os
import re
import pysubs2
import shutil

"""
将字幕文件中的有用信息用“/////”分隔保存到results.txt中（原因：直接向db文件中写入速度非常慢，
不知道是何原因）
"""

def filter(path, keyword):
    '''
    遍历path及子目录，寻找所有文件名（及后缀名）中包含keyword的文件，返回其相对路径列表
    '''
    tmp = dict()
    files = glob.glob(path+'\**',recursive=True)
    for file in files:
        if keyword in file:
            tmp[os.path.splitext(file)[0]] = os.path.splitext(file)[1]  #利用字典的键唯一性确保同名文件不会被重复读取
    desired = [i+tmp[i] for i in tmp]
    return desired

def has_chinese(string):
    '''
    判断字符串中含不含中文字符
    '''
    for char in string:
        if '\u4e00' <= char <='\u9fff':
            return True

def retrive_info(folder,tagPattern=re.compile('【(.*?)】')):
    '''
    从folder目录中获取字幕文件信息
    '''
    print(folder)
    tag = tagPattern.search(folder).group(1)
    metainfo = open(folder+'\meta-info.txt',encoding='utf-8').read().split('\n')
    ch_title=metainfo[0].replace('【中文】','')         #获取影片中文标题
    en_title=metainfo[1].replace('【英名】','')         #获取影片英文标题
    assets = filter(folder,'简体&英文')                 #获取文件名中含“简体&英文”的文件
    for i in assets:
        try:
            subfile = pysubs2.load(i)
        except:
            try:
                subfile = pysubs2.load(i,encoding='gbk')
            except:
                continue
        for lines in subfile:
            try:
                upperline, lowerline = lines.text.split('\n')         #利用\n分隔双语字幕，若无法分隔说明是单语，直接跳过
            except ValueError:
                try:
                    upperline, lowerline = lines.text.split(r'\N')
                except:
                    continue
            if has_chinese(lowerline):                    #双语字幕中，一般英文字幕在下方。若下方字幕中含有中文字符，说明本行字幕有问题，直接跳过
                continue
            upperline = re.sub('{.*?}','',upperline)      #将字幕中“{}”之间的样式信息删除
            lowerline = re.sub('{.*?}','',lowerline)
            start = pysubs2.time.ms_to_str(lines.start)   #获取字幕开始时间
            print(lowerline,upperline,en_title,ch_title,start,tag,sep='/////',file=result)
    if assets != []:            #本文件夹若有可用文件，处理完毕后直接删除，便于后期处理不规则命名文件
        shutil.rmtree(folder)


if __name__ == '__main__':
    result = open('result_5.txt','a+',encoding='utf-8')
    os.chdir('../5')
    folders = glob.glob('*')
    for folder in folders:
        try:
            retrive_info(folder)
        except:
            print('Failed!')    
    result.close