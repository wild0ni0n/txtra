# txtra

txtra は、対象のドメインの名前解決で返される txt レコードを使用して、組織が使用しているクラウドサービスをプロファイリングするツールです。

# Installation

```bash
# Clone 
$ git clone https://github.com/wild0ni0n/txtra.git
$ cd txtra

# Install
$ pip3 install txtra
```

# Usage

オプション:
```bash
$ txtra -h
usage: txtra [-h] [-d DOMAIN] [-f FILE] [-s] [-c] [-j]

options:
  -h, --help           show this help message and exit
  -d, --domain DOMAIN  Specify domain
  -f, --file FILE      Specify domains file
  -s, --no-scan        No template scan is performed. Txtra returns only txt records
  -c, --csv            Output in CSV format. Cannot be used in conjunction with the --json option.
  -j, --json           Output in json format. Cannot be used in conjunction with the --csv option.
```

例:
```bash
$ txtra -d google.com   
[INF] Check 1 domains
[google.com] [GMail]  [token=wD8N7i1JTNTkezJ49swvWW48f8_9xveREV4oB-0Hf5o] google-site-verification=wD8N7i1JTNTkezJ49swvWW48f8_9xveREV4oB-0Hf5o
[google.com] [Apple]  [token=30afIBcvSuDV2PLX] apple-domain-verification=30afIBcvSuDV2PLX
[google.com] globalsign-smime-dv=CDYX+XFHUw2wml6/Gb8+59BsH31KzUr6c1l2BPvqKX8= 
[google.com] onetrust-domain-verification=de01ed21f2fa4d8781cbc3ffb89cf4ef 
[google.com] [Microsoft Office 365]  [token=E4A68B9AB2BB9670BCE15412F62916164C0B20BB] MS=E4A68B9AB2BB9670BCE15412F62916164C0B20BB
[google.com] [webex]  [token=479146de172eb01ddee38b1a455ab9e8bb51542ddd7f1fa298557dfa7b22d963] cisco-ci-domain-verification=479146de172eb01ddee38b1a455ab9e8bb51542ddd7f1fa298557dfa7b22d963
[google.com] [GMail]  [token=4ibFUgB-wXLQ_S7vsXVomSTVamuOXBiVAzpR5IZ87D0] google-site-verification=4ibFUgB-wXLQ_S7vsXVomSTVamuOXBiVAzpR5IZ87D0
[google.com] [Facebook]  [token=22rm551cu4k0ab0bxsw536tlds4h95] facebook-domain-verification=22rm551cu4k0ab0bxsw536tlds4h95
[google.com] [GMail]  [token=TV9-DBe4R80X4v0M4U_bd_J9cpOJM0nikft0jAgjmsQ] google-site-verification=TV9-DBe4R80X4v0M4U_bd_J9cpOJM0nikft0jAgjmsQ
[google.com] v=spf1 include:_spf.google.com ~all 
[google.com] [docusign]  [token=05958488-4752-4ef2-95eb-aa7ba8a3bd0e] docusign=05958488-4752-4ef2-95eb-aa7ba8a3bd0e
[google.com] [docusign]  [token=1b0a6754-49b1-4db5-8540-d2c12664b289] docusign=1b0a6754-49b1-4db5-8540-d2c12664b289
[_spf.google.com] v=spf1 include:_netblocks.google.com include:_netblocks2.google.com include:_netblocks3.google.com ~all 
[_netblocks.google.com] v=spf1 ip4:35.190.247.0/24 ip4:64.233.160.0/19 ip4:66.102.0.0/20 ip4:66.249.80.0/20 ip4:72.14.192.0/18 ip4:74.125.0.0/16 ip4:108.177.8.0/21 ip4:173.194.0.0/16 ip4:209.85.128.0/17 ip4:216.58.192.0/19 ip4:216.239.32.0/19 ~all 
[_netblocks2.google.com] v=spf1 ip6:2001:4860:4000::/36 ip6:2404:6800:4000::/36 ip6:2607:f8b0:4000::/36 ip6:2800:3f0:4000::/36 ip6:2a00:1450:4000::/36 ip6:2c0f:fb50:4000::/36 ~all 
[_netblocks3.google.com] v=spf1 ip4:172.217.0.0/19 ip4:172.217.32.0/20 ip4:172.217.128.0/19 ip4:172.217.160.0/20 ip4:172.217.192.0/19 ip4:172.253.56.0/21 ip4:172.253.112.0/20 ip4:108.177.96.0/19 ip4:35.191.0.0/16 ip4:130.211.0.0/22 ~all 
```