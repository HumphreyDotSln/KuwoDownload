# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import html5lib
from urllib import parse
import ssl
import re
import os.path
import msvcrt
import os
import threading
import time
import requests
import sys
global song_name
global album_name
global singer_name
global song_link
def get_song_list(soup):
    song_name = []
    album_name = []
    singer_name = []
    song_link = []
    nametag_song = soup.find_all("a",attrs={"target":"_blank","href":re.compile("http://www.kuwo.cn/yinyue/+")})
    print('歌曲名称获取成功…')
    nametag_album = soup.find_all("a",attrs={"target":"_blank","href":re.compile("http://www.kuwo.cn/album/+")})
    print('专辑信息获取成功…')
    nametag_singer = soup.find_all("a",attrs={"target":"_blank","href":re.compile("http://www.kuwo.cn/mingxing/+")})
    print('歌手信息获取成功…')
    for item in nametag_song:
        song_name.append(item.get('title'))
        song_link.append(re.findall('[0-9]{,9}',item.get('href'))[26])
    print('歌曲名称解析成功…')
    print('歌曲链接解析成功…')
    for item in nametag_album:
        album_name.append(item.get('title'))
    print('专辑信息解析成功…')
    for item in nametag_singer:
        singer_name.append(item.get('title'))
    print('歌手信息解析成功…')
    information = [song_name,song_link,album_name,singer_name]
    return information
def print_songs(soup,current_page):
    information = get_song_list(soup)
    print('第%s页'%current_page)
    for i in range(0,len(information[1])):
        try:
            print(str(i + 1) + ' ' + information[0][i] + '  -  ' + information[3][i] + '  -  ' + information[2][i])
        except:
            print(str(i + 1) + ' ' + information[0][i] + '  -  ' + information[3][i])
    return information
def HTML_parse(name,curreng_page):
    html = urllib.request.urlopen('http://sou.kuwo.cn/ws/NSearch?key=%s&type=music&pn=%s'%(name,str(current_page)))
    print('网页抓取成功…')
    soup = BeautifulSoup(html,'html5lib')
    print('HTML解析成功…')
    return soup
def download(target_number,information):
    request_link = 'http://antiserver.kuwo.cn/anti.s?format=aac|mp3&rid=MUSIC_%s&type=convert_url&response=res'%information[1][target_number]
    request_headers = {
        'Accept':'audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection':'keep-alive',
        'Host':'antiserver.kuwo.cn',
        'Range':'bytes=0-',
        'Referer':'http://www.kuwo.cn/',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
        }

    request_session = requests.session()
    request_r = request_session.get(request_link,headers = request_headers,allow_redirects=False)
    down_link = str(request_r.headers['Location'])
    down_host = re.findall(r'((\w+\.)+cn)',down_link)[0][0]
	#当正则没有分组是返回的就是正则的匹配
	#有一个分组返回的是分组的匹配而不是整个正则的匹配
	#因此假如我们需要拿到整个正则和每个分组的匹配，使用findall我们需要将整个正则作为一个分组
    down_headers = {
        'Accept':'audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection':'keep-alive',
        'Host':down_host,
        'Range':'bytes=0-',
        'Referer':'http://www.kuwo.cn/',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Pragma':'no-cache',
        'Cache-Control':'no-cache'
        }
    down_session = requests.session()
    down_r = down_session.get(down_link,headers = down_headers)
    with open(str(information[0][target_number])+'.aac','wb') as fd:
        fd.write(down_r.content)
    print('下载成功…')
    return

name = parse.quote_plus(input('输入歌曲名称…\n'))
ssl._create_default_https_context = ssl._create_unverified_context
current_page = 1
soup = HTML_parse(name,current_page)
page = soup.find_all(href = re.compile("/ws/NSearch\?key=%s&type=music&pn=+"%name))[2].get_text()
print('搜索页数获取成功…')
information = print_songs(soup,current_page)
while True:
    print('J/K翻页 D下载 Q退出…')
    key = ord(msvcrt.getch())
    if key == 107 and current_page < int(page):
        current_page += 1
        soup = HTML_parse(name,current_page)
        os.system('cls')#清屏
        information = print_songs(soup,current_page)
    elif key == 106 and current_page > 1:
        current_page -= 1
        soup = HTML_parse(name,current_page)
        os.system('cls')#清屏
        information = print_songs(soup,current_page)
    elif key == 113:
        sys.exit()
    elif key == 100:
        try:
            target_number = int(input('输入序号…\n')) - 1
            download_thread = threading.Thread(target = download(target_number,information),args=('one',))
            download_thread.start()
            download_thread.join()
        except:
            print(Exception.args)
    else:
        print('输入不符规范…')

