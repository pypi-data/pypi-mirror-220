#!/usr/bin/python3
#Copyright by Chen Chuan (kcchen@139.com)

import os,random,datetime,math,sys,shutil,hashlib

def filemd5(filename):#获取文件的md5值
    if not os.path.isfile(filename):return ""
    m = hashlib.md5()
    with open(filename,'rb') as f:
        m.update(f.read())
    return m.hexdigest()

def filetime(filename): #获取文件的修改时间
    if not os.path.exists(filename):
        return 0
    return os.stat(filename).st_mtime

def 同步文件(文件1,文件2):
    修改时间1=filetime(文件1)
    修改时间2=filetime(文件2)
    if 修改时间1>修改时间2:
        print("%s  ==>  %s" %(文件1,文件2))
        shutil.copy2(文件1,文件2)
    if 修改时间1<修改时间2:
        print("%s  ==>  %s" %(文件2,文件1))
        shutil.copy2(文件2,文件1)
    if 修改时间1==修改时间2:
        print("%s & %s has same change time!" %(文件1,文件2))

def 检查文件(文件1,文件2):
    if os.path.exists(文件1) and not os.path.isfile(文件1):
        return False
    if os.path.exists(文件2) and not os.path.isfile(文件2):
        return False
    if not os.path.isfile(文件1) and not os.path.isfile(文件2):
        print("%s & %s not exists!" %(文件1,文件2))
        return False
    if not os.path.isfile(文件1) or not os.path.isfile(文件2):
        return True
    if filemd5(文件1)!=filemd5(文件2):
        return True

def dsync():    #双向同步
    目录1=""
    目录2=""
    if len(sys.argv)>1:
        配置文件=sys.argv[1]
    else:
        配置文件="dsync.conf"
    if not os.path.isfile(配置文件):
        print("Can't find " + 配置文件)
    f=open(配置文件)
    配置内容=f.readlines()
    f.close()
    for conf in 配置内容:
        conf=conf.strip().split("=")
        if len(conf)!=2:continue
        i,v=conf
        if i.lower()=="d1":目录1=v
        if i.lower()=="d2":目录2=v
        if i.lower()=="f":
            文件1=os.path.join(目录1,v)
            文件2=os.path.join(目录2,v)
            if 检查文件(文件1,文件2):
                同步文件(文件1,文件2)

if __name__ == "__main__":
    dsync()
