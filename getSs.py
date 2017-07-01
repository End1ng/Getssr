# -*- coding: utf-8 -*-
# auther: end1ng

import requests, re, sys, os, signal

url = "https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
comp = re.compile("<p>服务器\d*(.*?)：([\w\.]+)\s*端口.*?(\d*)\s*密码.*?([\w\.-]*)\s*加密方式：([\w-]*)")

if os.geteuid() != 0:
    sys.exit("需要root权限： sudo python getss.py")

def CtrlCHandler(signum, frame):
    sys.exit("再见")
signal.signal(signal.SIGINT, CtrlCHandler)

try:
    print "获取中..."
    r = requests.get(url)
except:
    sys.exit("网络错误")

server_list = {}
count = 1
html = re.findall("<p>服务器.*</p>", r.content)
for i in html:
    res = re.match(comp, i)
    if res:
        server_list[count] = {'s':res.group(1), 'i':res.group(2), 'p':res.group(3), 'k':res.group(4), 'm':res.group(5)}
        count = count + 1
for i, j in server_list.items():
    print 'ID:%-3dIP:%-18sPORT:%-6sPASS:%-16sMETHOD:%-sLOCATION:%-23s' % (i, j['i'], j['p'], j['k'], j['m'], j['s'])
id = raw_input("请输入id:")
while not id.isdigit() or int(id) not in server_list:
    id = raw_input("请输入正确的id:")
id = int(id)
c = "sslocal -s %s -p %s -k %s -m %s -d restart -q > /dev/null 2>&1" % (server_list[id]['i'], server_list[id]['p'], server_list[id]['k'], server_list[id]['m'])
if os.system(c) == 0:
    print "已开启服务:%s:%s在%s" % (server_list[id]['i'], server_list[id]['p'], server_list[id]['s'])
else:
    print "程序出错"