#!/usr/bin/env python
# -*- coding: utf-8 -*-

# auther: ni7eipr

"""
-h 获取帮助
-c 使用缓存列表
-f 强制刷新
-t 停止已开启服务
-s ssr://*** 直接使用当前地址
"""

import requests, re, sys, os, signal, base64, json, time
from bs4 import BeautifulSoup

# 声明变量
ssr_path = "/opt/shadowsocksr/shadowsocks/local.py"
temp_path = os.path.expanduser('~') + "/.getSsr"
True if os.path.exists(temp_path) else os.makedirs(temp_path)
temp_file = temp_path + '/temp_config.json'
stop_file = temp_path + '/stop.sh'
True if os.path.exists(stop_file) else open(stop_file, 'w')
S = {}
requests.packages.urllib3.disable_warnings()
cid = -1

# 获取参数
sys.exit(__doc__) if '-h' in sys.argv else False
use_old_data = True if '-c' in sys.argv else False
use_new_data = True if '-f' in sys.argv else False
use_stop = True if '-t' in sys.argv else False
drect = True if '-s' in sys.argv else False

#定义函数
def CtrlCHandler(signum, frame):
    sys.exit("\n再见!")
signal.signal(signal.SIGINT, CtrlCHandler)

def parse_base64(data):
    return base64.b64decode(data + (data.__len__() % 4 + 1) * '=')

def parse_ss(ss):
    ss = parse_base64(ss.split('//')[-1]).split(':')
    # ipv4 ssr链接
    if ss.__len__() == 6:
        return {'s':ss[0],'p':ss[1],'O':ss[2],'m':ss[3],'o':ss[4],'k':parse_base64(ss[5].split('/')[0])}
    # ipv4 ss链接
    if ss.__len__() == 3:
        return {'s':ss[1].split('@')[1],'p':ss[2],'O':'origin','m':ss[0],'o':'plain','k':ss[1].split('@')[0]}
    # ipv6 链接
    return {'s':':'.join(ss[:-5]),'p':ss[-5],'O':ss[-4],'m':ss[-3],'o':ss[-2],'k':parse_base64(ss[-1].split('/')[0])}

def default():
    with open('data.txt') as f:
        for i in f:
            sid = S.__len__()
            S[sid] = parse_ss(i.strip())
            S[sid]['l'] = "self"

True if os.path.exists(ssr_path) else sys.exit("未找到shadowsocksr 请安装:\n  sudo git clone https://github.com/Ni7eipr/shadowsocksr.git /opt/shadowsocksr\n或更改配置:\n  8 ssr_path = \"path\"")

f_c = open(stop_file, 'r')
os.system(f_c.read()) or sys.exit('停止成功') if use_stop else False

# 检查缓存文件
if not use_new_data and os.path.exists(temp_file) and time.time() - os.path.getmtime(temp_file) < 3600 * 12 or use_old_data:
    print "获取缓存数据 创建于%d分钟之前" % ((time.time() - os.path.getmtime(temp_file)) / 60)
    S = {int(i): j for i, j in json.loads(open(temp_file, 'r').read()).items()}
else:
    print "获取中......"

    doub()
    # Alvin9999()
    default()

f = open(temp_file, 'w').write(json.dumps(S)) if S else sys.exit("未获取到数据")

if drect:
    sid = S.__len__()
    S[sid] = parse_ss(sys.argv[2])
    S[sid]['l'] = "drect"
    cid = sid

for i, j in S.items():
    print 'ID:' + str(i).ljust(4) + u'地址:' + j['s'].ljust(35) + u'位置:' + j['l']

while cid not in S:
    cid = raw_input("请输入id:")
    cid = int(cid) if cid.isdigit() else -1

c = ssr_path + " -s %s -p %s -k %s -m %s -o %s -O %s -d %s -q --pid-file %s/shadowsocksr.pid --log-file %s/shadowsocksr.log > /dev/null 2>&1" % (S[cid]['s'],S[cid]['p'],S[cid]['k'],S[cid]['m'],S[cid]['o'],S[cid]['O'],'%s',temp_path,temp_path)
c_start = c % 'restart'
c_stop = c % 'stop'
f_c = open(stop_file, 'w')
f_c.write(c_stop)
print u'已开启服务:ID:' + str(cid).ljust(4) + u'地址:' + S[cid]['s'].ljust(35) + u'位置:' + S[cid]['l'] if os.system(c_start) == 0 else "程序出错"
