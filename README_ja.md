# txtra

txtra は、対象のドメインの名前解決で返される txt レコードを使用して、組織が使用しているクラウドサービスをプロファイリングするツールです。

# Installation

```bash
# Clone 
$ git clone https://github.com/wild0ni0n/txtra.git
$ cd txtra

# Install dependencies
$ pip3 install -r requirements.txt

# Install
$ python3 setup.py install --user
```
# Usage

オプション:
```bash
$ txtra -h
usage: txtra [-h] [-d DOMAIN] [-f FILE] [-s] [-c] [-j]

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Specify domain
  -f FILE, --file FILE  Specify domains file
  -s, --no-scan         No template scan is performed. Txtra returns only txt records
  -c, --csv             Output in CSV format. Cannot be used in conjunction with the --json option.
  -j, --json            Output in json format. Cannot be used in conjunction with the --csv option.
```

例:
```bash
$ txtra -d google.com   
[INF] Check 1 domains
[google.com] v=spf1 include:_spf.google.com ~all 
[google.com] [webex]  [token=479146de172eb01ddee38b1a455ab9e8bb51542ddd7f1fa298557dfa7b22d963] cisco-ci-domain-verification=479146de172eb01ddee38b1a455ab9e8bb51542ddd7f1fa298557dfa7b22d963
[google.com] globalsign-smime-dv=CDYX+XFHUw2wml6/Gb8+59BsH31KzUr6c1l2BPvqKX8= 
[google.com] [Facebook]  [token=22rm551cu4k0ab0bxsw536tlds4h95] facebook-domain-verification=22rm551cu4k0ab0bxsw536tlds4h95
[google.com] [GMail]  [token=wD8N7i1JTNTkezJ49swvWW48f8] google-site-verification=wD8N7i1JTNTkezJ49swvWW48f8_9xveREV4oB-0Hf5o
[google.com] [GMail]  [token=TV9] google-site-verification=TV9-DBe4R80X4v0M4U_bd_J9cpOJM0nikft0jAgjmsQ
[google.com] [docusign]  [token=05958488-4752-4ef2-95eb-aa7ba8a3bd0e] docusign=05958488-4752-4ef2-95eb-aa7ba8a3bd0e
[google.com] [docusign]  [token=1b0a6754-49b1-4db5-8540-d2c12664b289] docusign=1b0a6754-49b1-4db5-8540-d2c12664b289
[google.com] [Apple]  [token=30afIBcvSuDV2PLX] apple-domain-verification=30afIBcvSuDV2PLX
[google.com] MS=E4A68B9AB2BB9670BCE15412F62916164C0B20BB 
[google.com] onetrust-domain-verification=de01ed21f2fa4d8781cbc3ffb89cf4ef 
```