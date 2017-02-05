# -*- coding: utf-8 -*-

import requests
import re
import json

url = "https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
comp = re.compile("<p>服务器\d*.*?([\w\.]+)\s*端口.*?(\d*)\s*密码.*?([\w\.-]*)\s*加密方式.*?([\w-]*)</p>")
filepath = "../../Program/shadowsocks/gui-config.json"

r = requests.get(url)
html = re.findall("<p>服务器.*</p>", r.content)

f = open(filepath, "r")
loadfile = json.loads(f.read())
for i in html:
    res = re.match(comp, i)
    loadfile["configs"].append({
        "remarks" : "",
        "id" : "EEF02D2205FE9963C1769F84CAA15607",
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
        "group" : "批量导入",
        "enable" : True,
        "udp_over_tcp" : False
    })

print "server count:" + str(html.__len__())
f = open(filepath, "w")
f.write(json.dumps(loadfile))