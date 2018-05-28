#!/usr/bin/python

import sqlite3

"""
向“subtitles.db”中写入数据
"""

if __name__ == '__main__':
    db = sqlite3.connect('subtitles.db')
    con = db.cursor()
    result = open('result_5.txt',encoding='utf-8').readlines()
    commands = list()
    for line in result:
        a,b,c,d,e,f = line.split('/////')
        f = f.replace('\n','')      #去除每行最后的换行符
        commands.append((a,b,c,d,e,f))
    con.executemany('''INSERT INTO subs VALUES (?,?,?,?,?,?)''', commands)
    db.commit()
    db.close