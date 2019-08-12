#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 14:37:57 2017

@author: Yaozhong Xu
"""

import urllib.request as urllib2
import urllib
import re
from bs4 import BeautifulSoup

USER = input("Singername starts with 1, User name starts with 2, space accpted with Singer:")
longlist={}
if USER[0]=='2':
    tld = 'http://www.xiami.com'
    url = tld + "/user/search?spm=a1z1s.3061781.226669510.17.XMMUcG&key=" + USER[1:]  
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8')
    respone = urllib2.urlopen(req)
    mainpage = str(respone.read().decode('utf8',errors='replace')) #decoding Chinese
    soup = BeautifulSoup(mainpage,"lxml")
    m=soup.prettify()
    re.sub(r'<br[ ]?/?>', '\n', m)
    
    with open(USER + '.csv', 'w') as fp:
        for i in soup.find_all('ul'):
            #print(i)
            j = i.attrs
            if 'class' in j:                                        # find 'ul' with class attribute
                (clearfix, user_list) = j['class']                      
                if user_list == 'user_list':
                    for x in i.find_all('div'):
                        y = x.attrs
                        if 'class' in y and y['class'] == ['user_info']:    #find user info under div of 'ul'
                            for m in x.find_all('a'):
                                print('User', m.text, '...', end=' ')
                                songs = []                                  #build an empty song list for the user
                                n = m.attrs
                                longlist[m.text]=[]
                                url2=tld + n['href']                        #get the main page of the user
                                req2 = urllib2.Request(url2)
                                req2.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8')
                                respone2=urllib2.urlopen(req2)
                                mainpage2=str(respone2.read().decode('utf8',errors='replace'))
                                soup2=BeautifulSoup(mainpage2,"lxml")
                                for i2 in soup2.find_all('li'):
                                    j2=i2.attrs
                                    if 'class' in j2 and ['showmore'] == j2['class']: #find 'li' with class "showmore"
                                        for xx in i2.find_all('a'):
                                            nn=xx.attrs
                                            if 'recent' in nn['href']:
                                                
                                                url3=tld+nn['href']
                                                req3=urllib2.Request(url3)          #locate the page of the user's recent songs
                                                req3.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8')
                                                respone3=urllib2.urlopen(req3)
                                                mainpage3=str(respone3.read().decode('utf8',errors='replace'))
                                                soup3=BeautifulSoup(mainpage3,"lxml")
                                                for i3 in soup3.find_all('td'):
                                                    j3=i3.attrs
                                                    if 'class' in j3 and ['song_name']==j3['class']:    #find song names from the table
                                                        for xxx in i3.find_all('a'):
                                                            nnn=xxx.attrs
                                                            if 'song' in nnn['href']:
                                                                songs.append(nnn['title'])
                                
                                print(m.text, ':'.join(songs), sep=',', file=fp, flush=True)
                                print('finished')
    songs=[]                            
    print('DONE')
elif USER[0]=='1':
    data = urllib.parse.urlencode({'key': USER[1:]})
    data = data.encode('ascii')
    req = urllib2.Request("http://www.xiami.com/search", data) #find singer main page
    req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8')
    respone = urllib2.urlopen(req)
    mainpage = str(respone.read().decode('utf8',errors='replace'))
    soup = BeautifulSoup(mainpage,"lxml")
    m=soup.prettify()
    re.sub(r'<br[ ]?/?>', '\n', m)
    songs=[]
    with open(USER[1:] + '.csv', 'w') as fp:
        for i3 in soup.find_all('td'):
            j3=i3.attrs
            if 'class' in j3 and ['song_name']==j3['class']: #find singer's songs from the table
                for xxx in i3.find_all('a'):
                    nnn=xxx.attrs
                    if 'song' in nnn['href']:
                        songs.append(nnn['title'])
                        print(':'.join(songs), sep=',', file=fp, flush=True)
                        print('finished')
                        songs=[]                            
        print('DONE')
               
                    