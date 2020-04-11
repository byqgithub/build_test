import re

http_raw = '''{"ResultCode":0,
"ResultMsg":"","
PeerNumbers":30,
"PeerResourceLis
t":[{"peerId":"0
f04afd7e6dd9e013
c41cc65539f8df67
5842658f018c5ddc
e2742f9f7b3dd16"
,"type":"skj","n
t":2,"hostname":
"OCPG121158610",
"cap":30,"monaAd
dr":"36.99.16.31
:1937","peerIp":
"49.87.171.123",
"tPort":59606,"i
p6":"","pt6":0,"
uPort":59608,"wP
ort":59843},{"pe
erId":"852c02ce7
064ed1e91aa29e7e
fe57a8e9630a4c3f
9c1404da5f126621
2329b08","type":
"skj","nt":2,"ho
stname":"OCPZ127
017197","cap":30
,"monaAddr":"36.
99.16.35:1942","
peerIp":"","tPor
t":0,"ip6":"","p
t6":0,"uPort":0,
"wPort":0},{"pee
rId":"6e92ebc883
52ebf6c0fef1f1c2
8a9f64708ed9bb15
284194d002c493af
f62d4b","type":"
skj","nt":2,"hos
tname":"OCPG1261
74130","cap":30,
"monaAddr":"222.
88.95.37:1942","
peerIp":"49.69.2
41.220","tPort":
59606,"ip6":"","
pt6":0,"uPort":0
,"wPort":59843},
{"peerId":"2168b
37c9a38d47fad2c3
bcbf06f33d3349d2
e779274761e10d35
bef9d9df48d","ty
pe":"skj","nt":4
,"hostname":"OCP
Z121292665","cap
":30,"monaAddr":
"61.155.182.195:
1942","peerIp":"
180.126.218.49",
"tPort":59606,"i
p6":"","pt6":0,"
uPort":59608,"wP
ort":59843},{"pe
erId":"cda9b11a4
888389d71e82d9c5
6c75c1ff09e2faa9
47de5495b45b03c2
fb74bbf","type":
"skj","nt":1,"ho
stname":"ikuai8-
adb32b8751fa4c3e
b790673c42d22ad4
","cap":0,"monaA
ddr":"123.160.28
.21:1938","peerI
p":"220.191.176.
158","tPort":596
00,"ip6":"","pt6
":0,"uPort":5970
0,"wPort":59800}
,{"peerId":"5cad
df4699336e1a6e9a
bb900559384f6a66
f7d070d957ab83ce
4aa19d18752c","t
ype":"skj","nt":
1,"hostname":"ik
uai8-eb425993679
d4123b76efe4b90b
7a565","cap":0,"
monaAddr":"123.1
60.28.21:1942","
peerIp":"125.109
.177.24","tPort"
:59600,"ip6":"",
"pt6":0,"uPort":
59700,"wPort":59
800},{"peerId":"
6e49468c1b503a01
b56a6ca74c67007d
e06481685557a4e3
dc202886f4b134fa
","type":"skj","
nt":1,"hostname"
:"ikuai8-fc4a7ea
46d814c299133e28
a7d9bc24f","cap"
:0,"monaAddr":"2
22.88.95.38:1940
","peerIp":"60.1
71.163.209","tPo
rt":59600,"ip6":
"","pt6":0,"uPor
t":59700,"wPort"
:59800},{"peerId
":"3fcb28d99bd29
dea51a6e71257300
63791749b467fde6
feec432e2562cc4b
3ca","type":"skj
","nt":4,"hostna
me":"OCPG11B1075
13","cap":30,"mo
naAddr":"222.88.
93.196:1941","pe
erIp":"106.118.2
15.74","tPort":5
9606,"ip6":"240e
:b2:6108:c190:22
2:6dff:fe4d:199e
","pt6":60606,"u
Port":59608,"wPo
rt":59843},{"pee
rId":"0ca77aed27
ea65d116eb871fda
1532c3a05094e401
0e3eb44913ce8a39
543619","type":"
skj","nt":2,"hos
tname":"OCPG1221
35314","cap":30,
"monaAddr":"222.
88.93.249:1942",
"peerIp":"","tPo
rt":0,"ip6":"","
pt6":0,"uPort":0
,"wPort":0},{"pe
erId":"63c6f058c
7438328552250897
a3d433b22e24665a
5d3240bfc760cac7
013294d","type":
"skj","nt":4,"ho
stname":"OCPG11C
204107","cap":0,
"monaAddr":"222.
88.95.35:1938","
peerIp":"","tPor
t":0,"ip6":"","p
t6":0,"uPort":0,
"wPort":0},{"pee
rId":"0b1f4e43b1
e96a767398ad1c77
e1af8b5b46cf6c73
8565a924c8a9f3cd
890cd7","type":"
skj","nt":4,"hos
tname":"OCPZ1213
50830","cap":0,"
monaAddr":"180.9
7.87.151:1939","
peerIp":"","tPor
t":0,"ip6":"","p
t6":0,"uPort":0,
"wPort":0},{"pee
rId":"87daaad642
48771968b8957c72
8c088c0dcff14444
9f3d57243c09a79f
d67ad4","type":"
skj","nt":2,"hos
tname":"OCPG11C0
86320","cap":0,"
monaAddr":"36.99
.16.34:1939","pe
erIp":"","tPort"
:0,"ip6":"","pt6
":0,"uPort":0,"w
Port":0},{"peerI
d":"68c8673eedd3
bf9ccdbff7d1c90e
a3dad7cbdfeb7c17
af4bd5678ff8f82c
176b","type":"sk
j","nt":2,"hostn
ame":"OCPG11B231
001","cap":30,"m
onaAddr":"222.88
.95.39:1942","pe
erIp":"","tPort"
:0,"ip6":"240e:3
45:1d30:f100:222
:6dff:fe4e:e523"
,"pt6":60606,"uP
ort":0,"wPort":0
},{"peerId":"866
c49d028354587962
3270af2126108d85
40b9693541c1f73e
b5003ca3710ce","
type":"skj","nt"
:4,"hostname":"O
CPZ11C089752","c
ap":0,"monaAddr"
:"61.158.133.181
:1937","peerIp":
"","tPort":0,"ip
6":"","pt6":0,"u
Port":0,"wPort":
0},{"peerId":"5a
9b346fceb551f98a
69aeac3108830217
0b887b726686d990
f64c122ad5dd13",
"type":"skj","nt
":4,"hostname":"
OCPG122174407","
cap":0,"monaAddr
":"103.45.76.195
:1938","peerIp":
"","tPort":0,"ip
6":"","pt6":0,"u
Port":0,"wPort":
0},{"peerId":"dc
b05caeb23e05e600
046eb28f4d70374a
ae5e9bb74f2cbe9f
f7974b26d52b83",
"type":"skj","nt
":2,"hostname":"
OCPG126131760","
cap":30,"monaAdd
r":"182.118.126.
162:1942","peerI
p":"124.91.92.16
3","tPort":59606
,"ip6":"","pt6":
0,"uPort":59608,
"wPort":59843},{
"peerId":"2fefc2
e590fa01ea2b99b8
ab5f07168ea920c4
c94cfd5c599ef83d
11eefbd1c9","typ
e":"skj","nt":4,
"hostname":"OCPG
126123745","cap"
:30,"monaAddr":"
61.158.160.101:1
940","peerIp":"1
23.156.133.104",
"tPort":59608,"i
p6":"2408:8340:7
620:c30:222:6dff
:fe63:4063","pt6
":60606,"uPort":
59610,"wPort":59
845},{"peerId":"
c0b5d77e7c14bcf5
94c462ba9e3b2371
dae5d2dd43e22df7
04a6a9c71cddb45c
","type":"skj","
nt":4,"hostname"
:"OCPG123115764"
,"cap":30,"monaA
ddr":"222.88.93.
249:1937","peerI
p":"","tPort":0,
"ip6":"240e:d2:3
e63:ae00:222:6df
f:fe61:eda2","pt
6":60606,"uPort"
:0,"wPort":0},{"
peerId":"293d40a
88c32d1595a2d7c7
4020d467d2e82874
d2d751f67a741eea
b793cdeb9","type
":"skj","nt":4,"
hostname":"OCPZ1
21370586","cap":
30,"monaAddr":"6
1.155.182.195:19
42","peerIp":"",
"tPort":0,"ip6":
"","pt6":0,"uPor
t":0,"wPort":0},
{"peerId":"649ea
9802eea66fd0795e
74f8ce50af59e903
4c423c382cd8819a
f87a3800b8c","ty
pe":"skj","nt":4
,"hostname":"OCP
Z121335667","cap
":30,"monaAddr":
"180.97.167.62:1
937","peerIp":""
,"tPort":0,"ip6"
:"","pt6":0,"uPo
rt":0,"wPort":0}
,{"peerId":"f30e
ca501b5c9ee44106
53e5837d9d9ed3d9
50c9c34d10508f61
aad9cb083d03","t
ype":"skj","nt":
4,"hostname":"OC
PZ121320571","ca
p":30,"monaAddr"
:"222.88.95.39:1
940","peerIp":""
,"tPort":0,"ip6"
:"240e:d2:3e69:3
900:b2d5:9dff:fe
e4:6771","pt6":6
0606,"uPort":0,"
wPort":0},{"peer
Id":"d203ac82aa5
bab8c483640af231
6728f1f997789492
00bb6e7bff68053b
9eda7","type":"s
kj","nt":4,"host
name":"OCPZ12137
0776","cap":30,"
monaAddr":"180.9
7.87.150:1937","
peerIp":"","tPor
t":0,"ip6":"240e
:d2:3e54:fb00:b2
d5:9dff:fee6:a7e
f","pt6":60610,"
uPort":0,"wPort"
:0},{"peerId":"e
be3c08b94e594364
d65ca6d9a4de8ce3
1452ddc8c92e4c48
2c3166c41b55e17"
,"type":"skj","n
t":4,"hostname":
"OCPG123118592",
"cap":30,"monaAd
dr":"222.88.95.3
6:1940","peerIp"
:"","tPort":0,"i
p6":"240e:d2:3e4
d:3f00:222:6dff:
fe61:e6a0","pt6"
:60606,"uPort":0
,"wPort":0},{"pe
erId":"064776655
c3bc3901c9911461
0276aecfdf12e1f9
355790ce6f87bca9
46e9f3a","type":
"skj","nt":4,"ho
stname":"OCPG122
184165","cap":30
,"monaAddr":"222
.88.93.248:1937"
,"peerIp":"","tP
ort":0,"ip6":"24
0e:d2:554f:8800:
222:6dff:fe5f:db
d","pt6":60606,"
uPort":0,"wPort"
:0},{"peerId":"a
47a944ee00d4811b
783aa336fc570b80
a4f7f0aed552a578
51d1eca00439ecd"
,"type":"skj","n
t":4,"hostname":
"OCPZ121366481",
"cap":30,"monaAd
dr":"123.160.28.
22:1938","peerIp
":"","tPort":0,"
ip6":"","pt6":0,
"uPort":0,"wPort
":0},{"peerId":"
3310a81e22d36347
fb48656eb89fed69
a1ce8a880260df33
8a04130ee1c90e34
","type":"skj","
nt":4,"hostname"
:"OCPZ121152441"
,"cap":30,"monaA
ddr":"61.155.182
.196:1943","peer
Ip":"","tPort":0
,"ip6":"240e:d2:
3e3d:d400:b2d5:9
dff:fee2:f63d","
pt6":60606,"uPor
t":0,"wPort":0},
{"peerId":"63ae7
bd6699cd5695aa3e
0ab2f286ad7d99ff
b3e8573147713041
ffaff5551f0","ty
pe":"skj","nt":4
,"hostname":"OCP
G123111667","cap
":30,"monaAddr":
"180.101.140.108
:1938","peerIp":
"","tPort":0,"ip
6":"240e:d2:3e02
:bd00:222:6dff:f
e61:f699","pt6":
60606,"uPort":0,
"wPort":0},{"pee
rId":"f505e49c4d
0b63098c5597b94c
2c33474bf6ed28ec
107cb8497235bdb1
6852a7","type":"
skj","nt":4,"hos
tname":"OCPG1213
64619","cap":30,
"monaAddr":"180.
101.140.116:1939
","peerIp":"","t
Port":0,"ip6":"2
40e:d2:5520:3200
:222:6dff:fe5c:f
64a","pt6":60606
,"uPort":0,"wPor
t":0},{"peerId":
"d560274dbc25b15
891d3f792937d698
4384746e603fe2e2
421510f5080355aa
1","type":"skj",
"nt":4,"hostname
":"OCPG121145779
","cap":30,"mona
Addr":"222.88.92
.198:1941","peer
Ip":"","tPort":0
,"ip6":"240e:d2:
5549:7f00:222:6d
ff:fe59:a7e3","p
t6":60606,"uPort
":0,"wPort":0},{
"peerId":"102c3c
60e6b792369b7693
37a5328728fa9f48
8fcae321cedab8cf
5c640d415f","typ
e":"skj","nt":4,
"hostname":"OCPZ
121367694","cap"
:30,"monaAddr":"
180.97.87.150:19
40","peerIp":"",
"tPort":0,"ip6":
"240e:d2:5516:8f
00:b2d5:9dff:fee
7:261","pt6":606
06,"uPort":0,"wP
ort":0}],"MUrl":
"v3-xg-p.ixigua.
com/video/tos/hx
sy/tos-hxsy-ve-2
6/0491e071b57d4b
47a94e51452644c7
e5?WUkeWEM/VlkYR
wc/WBMdCEAkXhkX"
}
'''
response_line = http_raw.splitlines()
http_content = ""
for i in response_line:
    http_content += i
print(http_content)
ip_list = re.findall("\d+\.\d+\.\d+\.\d+", http_content)
print("ip list: %s" % ip_list)

ip_string = ""
for i in ip_list:
    ip_string += i + ", "
print("ip string: %s" % ip_string)


object_raw = '''Member Key: seeds
            Array
                Object
                    Member Key: pid
                        String value: 000100018993490AA359FA4251EC6994
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 39.188.49.95
                        Key: pubIP
                    Member Key: pubport
                        Number value: 9362
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 000100013B6947269B550BEA922A4235
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 49.72.104.41
                        Key: pubIP
                    Member Key: pubport
                        Number value: 61032
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 00010001E5AA4BD298B3A736F134B168
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 42.49.49.152
                        Key: pubIP
                    Member Key: pubport
                        Number value: 20993
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 000100016E1247899F858CE3CB7C4ABF
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 27.186.231.1
                        Key: pubIP
                    Member Key: pubport
                        Number value: 6523
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 0001000105A6494AB049576271CDAFAB
                        Key: pid
                    Member Key: nat
                        Number value: 2
                        Key: nat
                    Member Key: pubIP
                        String value: 60.16.217.236
                        Key: pubIP
                    Member Key: pubport
                        Number value: 50649
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 00010001619D4D1D87CD9DBEAA666CD4
                        Key: pid
                    Member Key: nat
                        Number value: 2
                        Key: nat
                    Member Key: pubIP
                        String value: 139.214.103.20
                        Key: pubIP
                    Member Key: pubport
                        Number value: 5169
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 00010001A21B42B1897345A10E260B1C
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 222.214.113.79
                        Key: pubIP
                    Member Key: pubport
                        Number value: 21606
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 00010001B2D34A529D1060A6F6A67DE3
                        Key: pid
                    Member Key: nat
                        Number value: 2
                        Key: nat
                    Member Key: pubIP
                        String value: 112.13.60.192
                        Key: pubIP
                    Member Key: pubport
                        Number value: 34001
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 00010001D32041A4AC39EA2130F44BB8
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 117.34.143.249
                        Key: pubIP
                    Member Key: pubport
                        Number value: 23108
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 000100013B5047EEA238C3F131095123
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 121.33.172.90
                        Key: pubIP
                    Member Key: pubport
                        Number value: 53718
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 0001000134A3466EBD9BD2B931EFA19A
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 110.249.76.166
                        Key: pubIP
                    Member Key: pubport
                        Number value: 26381
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 0001000164114F949DDF75669B5FC59A
                        Key: pid
                    Member Key: nat
                        Number value: 2
                        Key: nat
                    Member Key: pubIP
                        String value: 223.96.131.96
                        Key: pubIP
                    Member Key: pubport
                        Number value: 2641
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 0001000157C44BA1BFCBF6CD1CD5A4AE
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 106.39.174.174
                        Key: pubIP
                    Member Key: pubport
                        Number value: 35237
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 000100013DAC44D3BD27949D335AA9E8
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 58.19.217.218
                        Key: pubIP
                    Member Key: pubport
                        Number value: 51686
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 00010001CD15457EABAD05DEB2C18917
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 1.196.159.160
                        Key: pubIP
                    Member Key: pubport
                        Number value: 6935
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 0001000155014E4F88CCE2605348223C
                        Key: pid
                    Member Key: nat
                        Number value: 2
                        Key: nat
                    Member Key: pubIP
                        String value: 119.115.92.165
                        Key: pubIP
                    Member Key: pubport
                        Number value: 36904
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 00010001CFBB49848B84973BFAF724A1
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 183.211.87.243
                        Key: pubIP
                    Member Key: pubport
                        Number value: 7169
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 0001000151AD4368A1D9436BE95786B0
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 220.161.47.111
                        Key: pubIP
                    Member Key: pubport
                        Number value: 5513
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 00010001E0C640F58A606E685D519326
                        Key: pid
                    Member Key: nat
                        Number value: 2
                        Key: nat
                    Member Key: pubIP
                        String value: 121.27.237.122
                        Key: pubIP
                    Member Key: pubport
                        Number value: 24159
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 00010001F8DC47BC9AB960AC16467BF4
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 101.30.29.9
                        Key: pubIP
                    Member Key: pubport
                        Number value: 25920
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 000100014E524C2A90B0BE1F85ACFDE4
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 120.200.188.38
                        Key: pubIP
                    Member Key: pubport
                        Number value: 3793
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 000100017B1342F8AE7577801028C583
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 110.82.117.155
                        Key: pubIP
                    Member Key: pubport
                        Number value: 35927
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 000100016FA247C7B9409811B45B509C
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 153.35.38.113
                        Key: pubIP
                    Member Key: pubport
                        Number value: 46833
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 000100017189474B9294E2CB09F71D7B
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 112.37.153.75
                        Key: pubIP
                    Member Key: pubport
                        Number value: 1353
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 000100017C7F49C5B323825358D4CED6
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 171.213.53.55
                        Key: pubIP
                    Member Key: pubport
                        Number value: 31875
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 000100018E544332BC44F44D41396F5E
                        Key: pid
                    Member Key: nat
                        Number value: 2
                        Key: nat
                    Member Key: pubIP
                        String value: 113.86.197.129
                        Key: pubIP
                    Member Key: pubport
                        Number value: 13426
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 000100017A7F4CC59EE993CFC2B2983D
                        Key: pid
                    Member Key: nat
                        Number value: 2
                        Key: nat
                    Member Key: pubIP
                        String value: 119.187.105.92
                        Key: pubIP
                    Member Key: pubport
                        Number value: 37668
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 00010001F8434767A62AEC0FF5295458
                        Key: pid
                    Member Key: nat
                        Number value: 2
                        Key: nat
                    Member Key: pubIP
                        String value: 117.170.14.92
                        Key: pubIP
                    Member Key: pubport
                        Number value: 15370
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 0001000196BB4239841181A1A145654F
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 112.38.106.201
                        Key: pubIP
                    Member Key: pubport
                        Number value: 10778
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 0001000188C145ADAA938AB55955AB30
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 60.23.97.31
                        Key: pubIP
                    Member Key: pubport
                        Number value: 26531
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 000100014E5B4A90A7B8C41C656530E2
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 111.122.11.36
                        Key: pubIP
                    Member Key: pubport
                        Number value: 13408
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 0001000107114F0AAC3A631D9D2FBF57
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 114.83.228.204
                        Key: pubIP
                    Member Key: pubport
                        Number value: 36482
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 00010001045340C8955B9D19EF7A5634
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 183.252.218.32
                        Key: pubIP
                    Member Key: pubport
                        Number value: 36931
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 000100015C0649009EF4D6C8BCED6570
                        Key: pid
                    Member Key: nat
                        Number value: 2
                        Key: nat
                    Member Key: pubIP
                        String value: 1.197.244.193
                        Key: pubIP
                    Member Key: pubport
                        Number value: 22387
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 0001000176774531B55C8D5B7052C0B1
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 1.197.132.1
                        Key: pubIP
                    Member Key: pubport
                        Number value: 1034
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 0001000150EF49E2928FFC8F71DB0BBA
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 221.196.85.15
                        Key: pubIP
                    Member Key: pubport
                        Number value: 47754
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 000100015A6A410A82662FDB48B228A8
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 120.15.172.169
                        Key: pubIP
                    Member Key: pubport
                        Number value: 46473
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 0001000145EE4E9C99F4F342D52CC409
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 111.19.106.98
                        Key: pubIP
                    Member Key: pubport
                        Number value: 33220
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 0001000160C04FE69742C4C071FDD17A
                        Key: pid
                    Member Key: nat
                        Number value: 2
                        Key: nat
                    Member Key: pubIP
                        String value: 27.221.140.70
                        Key: pubIP
                    Member Key: pubport
                        Number value: 48923
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 00010001F15B4082964F445614F58E28
                        Key: pid
                    Member Key: nat
                        Number value: 2
                        Key: nat
                    Member Key: pubIP
                        String value: 182.35.29.130
                        Key: pubIP
                    Member Key: pubport
                        Number value: 37091
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 00010001A8A143279B9DFA8847EC85C2
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 120.227.197.245
                        Key: pubIP
                    Member Key: pubport
                        Number value: 6345
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb
                Object
                    Member Key: pid
                        String value: 0001000147BF4E18BCB58F5F6FF07D30
                        Key: pid
                    Member Key: nat
                        Number value: 3
                        Key: nat
                    Member Key: pubIP
                        String value: 110.191.152.149
                        Key: pubIP
                    Member Key: pubport
                        Number value: 32306
                        Key: pubport
                    Member Key: stunIP
                        String value: 47.100.60.233
                        Key: stunIP
                    Member Key: cppb
                        Number value: 1
                        Key: cppb'''

# ip_string = ""
# object_string_list = object_raw.splitlines()
# for i, value in enumerate(object_string_list):
#     if "Member Key: pubIP" in value:
#         ip_string += object_string_list[i+1].rpartition(" ")[-1] + ":" + \
#                      object_string_list[i+4].rpartition(" ")[-1] + "，"
# print("ip and port: %s" % ip_string)
