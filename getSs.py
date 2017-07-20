#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auther: ni7eip

import requests, re, sys, os, signal, base64
from bs4 import BeautifulSoup

ssr_path = "/opt/shadowsocksr/shadowsocks/local.py"
S = {}

def CtrlCHandler(signum, frame):
    sys.exit("再见")
signal.signal(signal.SIGINT, CtrlCHandler)

def add_padding(data):
    return base64.b64decode(data + (data.__len__() % 4 + 1) * '=')

def parse_ss(ss):
    ss = add_padding(ss).split(':')
    if ss.__len__() == 3:
        return {'s':ss[1].split('@')[1],'p':ss[2],'O':'origin','m':ss[0],'o':'plain','k':ss[1].split('@')[0]}
    if ss.__len__() == 9:
        return {'s':':'.join([ss[1].split('@')[1], ss[2],  ss[3], ss[4], ss[5], ss[6], ss[7]]),'p':ss[8],'O':'origin','m':ss[0],'o':'plain','k':ss[1].split('@')[0]}
    if ss.__len__() == 11:
        password = add_padding(ss[10].split('/')[0])
        return {'s':':'.join([ss[0],ss[1],ss[2],ss[3],ss[4],ss[5]]),'p':ss[6],'O':ss[7],'m':ss[8],'o':ss[9],'k':password}
    password = add_padding(ss[5].split('/')[0])
    return {'s':ss[0],'p':ss[1],'O':ss[2],'m':ss[3],'o':ss[4],'k':password}

url = "https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
# comp_ogete_ss = re.compile("<p>服务器\d*(.*?)：([\w\.]+)\s*端口.*?(\d*)\s*密码.*?([\w\.-]*)\s*加密方式.*?([\w-]*)")
comp_ogete_ssr = re.compile("<p>服务器\d+.+?([\w\.]+)\s*端口.+?(\d*)\s*密码.+?([\w\.-]*)\s*加密方式.+?([\w\.-]*)\s*SSR协议.+?协议.+?([\w\.-]*)\s*混淆.+?([\w\.-]*)\s*\（自建\）.*")
try:
    print "正在获取 " + url
    res = requests.get(url).content
except:
    print "获取 " + url + " 失败"
html = re.findall("<p>服务器.*</p>", res)
for i in html:
    # res = re.match(comp_ogete_ss, i)
    # if res:
    #     S[S.__len__()] = {'s':res.group(1), 'i':res.group(2), 'p':res.group(3), 'k':res.group(4), 'm':res.group(5)}
    res = re.match(comp_ogete_ssr, i)
    if res:
        S[S.__len__()] = {'s':res.group(1),'p':res.group(2),'k':res.group(3),'m':res.group(4),'O':res.group(5),'o':res.group(6),'l':''}

url = "https://doub.bid/sszhfx"
try:
    print "正在获取 " + url
    session = requests.Session()
    session.get(url)
    session.post("https://doub.bid/wp-login.php?action=postpass", data={'post_password':'doub.io'})
    res = session.get(url).content
    soup = BeautifulSoup(res, 'lxml')
    for tr in soup.find_all('tr'):
        td = tr.find_all('td')
        if td.__len__() == 7:
            id = S.__len__()
            S[id] = parse_ss(td[6].find('a', "dl1")['href'].split('//')[2])
            S[id]['l'] = td[0].text
except:
    print "获取 " + url + " 失败"

if not S:
    sys.exit("列表为空")
for i, j in S.items():
    # print 'ID:%-3d地址:%-18s端口:%-6s密码:%-16s加密:%-s混淆:%-23s协议:%-23s' % (i, j['s'], j['p'], j['k'], j['m'], j['o'], j['O'])
    print 'ID:%-4d地址:%-25s位置:%s' % (i, j['s'], j['l'].encode('utf-8'))
id = raw_input("请输入id:")
while not id.isdigit() or int(id) not in S:
    id = raw_input("请输入正确的id:")
id = int(id)
c = ssr_path + " -s %s -p %s -k %s -m %s -o %s -O %s -d restart -q --pid-file /tmp/shadowsocksr.pid --log-file /tmp/shadowsocksr.log> /dev/null 2>&1" % (S[id]['s'],S[id]['p'],S[id]['k'],S[id]['m'],S[id]['o'],S[id]['O'])
if os.system(c) == 0:
    print "已开启服务: ID:%-4d地址:%-25s位置:%s" % (i, j['s'], j['l'].encode('utf-8'))
else:
    print "程序出错"