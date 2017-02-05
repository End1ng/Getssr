# -*- coding: utf-8 -*-

import requests
import re
import json
import sys
import time

filepath = "../../Program/shadowsocks/gui-config.json"

url = "https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
comp = re.compile("<p>服务器\d*.*?([\w\.]+)\s*端口.*?(\d*)\s*密码.*?([\w\.-]*)\s*加密方式.*?([\w-]*)</p>")
old_num = 0
configs = []
configs_old = []

try:
    r = requests.get(url)
except:
    sys.exit(u"网络错误")

html = re.findall("<p>服务器.*</p>", r.content)
for i in html:
    res = re.match(comp, i)
    configs.append({
        "remarks" : "",
        "id" : "",
        "server" : res.group(1),
        "server_port" : res.group(2),
        "server_udp_port" : 0,
        "password" : res.group(3),
        "method" : res.group(4),
        "protocol" : "origin",
        "protocolparam" : "",
        "obfs" : "plain",
        "obfsparam" : "",
        "remarks_base64" : "",
        "group" : "import-" + time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()),
        "enable" : True,
        "udp_over_tcp" : False
    })
print u"获取服务器数量:" + str(html.__len__())

f = open(filepath, "r")
loadfile = json.loads(f.read())
configs_old = loadfile["configs"]

print u"原服务器数量:" + str(configs_old.__len__())
for i in configs_old:
    if not i["group"].startswith("import-"):
        configs.append(i)
        old_num += 1
print u"删除 %d 服务器,保留 %d 服务器" % (configs_old.__len__() - old_num, old_num)

loadfile["configs"] = configs
f = open(filepath, "w")
f.write(json.dumps(loadfile))
print u"完成，请重启shadowsocks"