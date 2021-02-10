import os
import requests
import screct
import json
import re

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
        if file_own.is_dir():
            a=scan_music(file_own.path)
            for item in a:
                music_list.append(item)

    os.chdir(past_path)
    return music_list
        
    
def push_database(item):
    a=1
    #TODO:将音乐文件提交至数据库管理



def hifini_sign_auto():
    cookies=screct.hifini_cookies
    url = 'https://www.hifini.com/sg_sign.htm'
    r = requests.post(url, cookies=cookies, headers={"Content-type": "text/html; charset=utf-8"})
    if "成功" in r.text:
        print("Hifini成功签到")
        return 
    if "已经签过" in  r.text:
        print("Hifini已经签到")
    else:
        print("Hifini签到失败")

for item in scan_music("C:\YH"):
    print(item["path"])


