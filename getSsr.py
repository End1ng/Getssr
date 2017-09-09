#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auther: ni7eipr

import requests, re, sys, os, signal, base64, json, time
from bs4 import BeautifulSoup

ssr_path = "/opt/shadowsocksr/shadowsocks/local.py"
S = {}

if not os.path.exists(ssr_path):
    sys.exit("未找到shadowsocksr 请安装:\n  sudo git clone https://github.com/Ni7eipr/shadowsocksr.git /opt/shadowsocksr\n或更改配置:\n  8 ssr_path = \"path\"")
def CtrlCHandler(signum, frame):
    sys.exit("\n再见!")
signal.signal(signal.SIGINT, CtrlCHandler)

def add_padding(data):
    return base64.b64decode(data + (data.__len__() % 4 + 1) * '=')

def parse_ss(ss):
    ss = add_padding(ss).split(':')
    # ipv4 ssr链接
    if ss.__len__() == 6:
        return {'s':ss[0],'p':ss[1],'O':ss[2],'m':ss[3],'o':ss[4],'k':add_padding(ss[5].split('/')[0])}
    # ipv4 ss链接
    if ss.__len__() == 3:
        return {'s':ss[1].split('@')[1],'p':ss[2],'O':'origin','m':ss[0],'o':'plain','k':ss[1].split('@')[0]}
    # ipv6 链接
    return {'s':':'.join(ss[:-5]),'p':ss[-5],'O':ss[-4],'m':ss[-3],'o':ss[-2],'k':add_padding(ss[-1].split('/')[0])}

def Alvin9999():
    url = "https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
    # comp_ogete_ss = re.compile("<p>服务器\d*(.*?)：([\w\.]+)\s*端口.*?(\d*)\s*密码.*?([\w\.-]*)\s*加密方式.*?([\w-]*)")
    comp_ogete_ssr = re.compile("<p>服务器\d+.+?([\w\.]+)\s*端口.+?(\d*)\s*密码.+?([\w\.-]*)\s*加密方式.+?([\w\.-]*)\s*SSR协议.+?协议.+?([\w\.-]*)\s*混淆.+?([\w\.-]*)\s*\（自建\）.*")
    try:
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

def doub():
    url = "https://doub.bid/sszhfx"
    try:
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'
        }
        res = session.get(url, headers=headers)
        print re.search('<p id="problem">(.*)</p>', res.text).group(1)
        input_text = raw_input("请输入答案:")
        session.post(re.search('<form action="(.*)" method="post">', res.text).group(1), data={'post_password':input_text}, headers=headers)
        res = session.get(url,  headers=headers).content
        soup = BeautifulSoup(res, 'lxml')
        for tr in soup.find_all('tr'):
            td = tr.find_all('td')
            if td.__len__() == 7:
                id = S.__len__()
                S[id] = parse_ss(td[6].find('a', "dl1")['href'].split('//')[2])
                S[id]['l'] = td[0].text
    except:
        print "获取 " + url + " 失败"

# 检查缓存文件如果在1小时之内就加载缓存
temp_file = '~/.getSsr/ss_temp.json'
if not os.path.exists(temp_file) or time.time() - os.path.getmtime(temp_file) > 3600 * 12:
    print "获取中......"
    doub()
    # Alvin9999()
    f = open(temp_file, 'w').write(json.dumps(S)) if S else True
else:
    print "获取缓存数据 创建于%d分钟之前" % ((time.time() - os.path.getmtime(temp_file)) / 60)
    S = {int(i): j for i, j in json.loads(open(temp_file, 'r').read()).items()}
True if S else sys.exit("未获取到数据")

for i, j in S.items():
    print 'ID:' + str(i).ljust(4) + u'地址:' + j['s'].ljust(35) + u'位置:' + j['l']
id = -1
while id not in S:
    id = int(raw_input("请输入正确的id:"))
c = ssr_path + " -s %s -p %s -k %s -m %s -o %s -O %s -d restart -q --pid-file /tmp/shadowsocksr.pid --log-file /tmp/shadowsocksr.log> /dev/null 2>&1" % (S[id]['s'],S[id]['p'],S[id]['k'],S[id]['m'],S[id]['o'],S[id]['O'])
print u'已开启服务:ID:' + str(i).ljust(4) + u'地址:' + j['s'].ljust(35) + u'位置:' + j['l'] if os.system(c) == 0 else "程序出错"