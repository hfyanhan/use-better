import os
import requests
import screct
import json
import re
import zipfile 
import sqlite3

def scan_music(path):
    music_list=[]
    mp3=re.compile("^.+\.mp3$")
    zip_cp=re.compile("^.+\.zip$")
    flac=re.compile("^.+\.flac$")
    past_path=os.getcwd()
    try:
        os.chdir(path)
    except Exception:
        return []
    #TODO:扫描文件夹下的音乐文件,包含压缩包中的
    file_list=os.scandir(path)
    for file_own in file_list:
        if file_own.is_file():
            if re.match(mp3,file_own.name) or re.match(flac,file_own.name):
                item={'name':file_own.name,'path':file_own.path}
                music_list.append(item)
            if re.match(zip_cp,file_own.name):
                try:
                    zip_fl=zipfile.ZipFile(file_own.path)
                except Exception:
                    print(file_own.name+"is a damaged zip file")
                for name in zip_fl.namelist():
                    if re.match(mp3,name) or re.match(flac,name):
                        path=file_own.path+"\\"+name
                        path=path.replace("/","\\")
                        name=path[path.rfind('\\')+1:len(path)]
                        item={'name':name,'path':path}
                        music_list.append(item)
        if file_own.is_dir():
            a=scan_music(file_own.path)
            for item in a:
                music_list.append(item)
        
    os.chdir(past_path)
    return music_list
        
    
def push_database(item,dbfile,table="main"):
    a=1
    #TODO:将音乐文件提交至数据库管理
    #item 字典
    cre=sqlite3.connect(dbfile)
    q=cre.cursor()
    cstr="insert into "+table+"("
    num=0
    values=[]
    for key in item.keys():
        num=num+1   
        cstr=cstr+key+","
        values.append(item[key])
    cstr=cstr[0:-1]+") Values("
    for i in range(1,num+1):
        cstr=cstr+"?,"
    cstr=cstr[0:-1]+");"
    q.execute(cstr,values)
    cre.commit()

def hifini_sign_auto():
    cookies=screct.hifini_cookies
    url = 'https://www.hifini.com/sg_sign.htm'
    r = requests.post(url, cookies=cookies, headers={"Content-type": "text/html; charset=utf-8","User-Agent":'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'})
    if "成功" in r.text:
        print("Hifini成功签到")
        return 
    if "已经签过" in  r.text:
        print("Hifini已经签到")
    else:
        print("Hifini签到失败")


#hifini_sign_auto()

#push_database(item,"1.db")

