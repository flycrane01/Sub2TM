#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import os

def downloader(link):
    """
    创建以该字幕命名的文件夹，将元信息存储到meta-info.txt中，并将字幕文件保存至该文件夹中
    """
    page = BeautifulSoup(urllib.request.urlopen(link),'html5lib')
    if page.title.text == '字幕发布详情说明页':                                     #确定该页面是字幕页面
        title = page.find(name='h2',attrs={'class':'subtitle-tit'}).string        #获取本字幕标题
        info = page.find(name='ul',attrs={'class':'subtitle-info'})               #获取本字幕元信息
        items = [i for i in info.children]
        os.mkdir(title)                                                           #以字幕名为名创建新文件夹
        os.chdir(title)                                                           #定位到此目录
        metainfo = open('meta-info.txt','a+',encoding='utf-8')                    #创建meta-info.txt存储元信息
        for i in range(1,15,2):
            metainfo.write(items[i].text + '\n')                                  #写入元信息
        metainfo.close()
        reallink = page.find(name='a',attrs={'class':'f3'})['href']               #定位下载页面
        dlpage = BeautifulSoup(urllib.request.urlopen(reallink),'html5lib')       #打开下载页面
        dllink = dlpage.find(name='a',attrs={'class':'btn-click'})['href']        #定位下载地址
        filetitle = dlpage.find(name='a',attrs={'class':'btn-click'}).text        #获取本字幕文件的名称
        urllib.request.urlretrieve(dllink,filetitle)                              #保存本字幕文件至本地
        os.chdir('..')                                                            #回到上一级目录


link = 'http://www.zimuzu.tv/subtitle/56106'
downloader(link)