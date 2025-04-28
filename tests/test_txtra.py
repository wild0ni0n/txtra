from txtra.__main__ import (
    Domain,
    Txtra,
    TxtRecord,
    TxtRecords,
    get_etldp1
)

import unittest
from unittest.mock import MagicMock, patch

txtra = Txtra()

class TestDomain(unittest.TestCase):
    def test_get_etldp1(self):
        # Basic domain
        self.assertEqual(get_etldp1("example.com"), "example.com")
        # Subdomain
        self.assertEqual(get_etldp1("sub.example.com"), "example.com")
        # Multiple subdomains
        self.assertEqual(get_etldp1("a.b.example.com"), "example.com")
        # Public suffix
        self.assertEqual(get_etldp1("example.co.uk"), "example.co.uk")
        # Subdomain of public suffix
        self.assertEqual(get_etldp1("sub.example.co.uk"), "example.co.uk")

class TestApp(unittest.TestCase):
    def mock_resolve(self, test_domain, test_txt_value) -> TxtRecords:
        domain = Domain(test_domain)
        r = TxtRecords(domain=domain)

        return_value = [TxtRecord(value=test_txt_value)]
        r.resolve = MagicMock(return_value=return_value)  # type: ignore
        r.resolve()
        r.records = return_value
        return r

    def test_resolve(self):
        domain = Domain("example.com")
        records = TxtRecords(domain=domain)

        records.resolve = MagicMock(return_value=[TxtRecord(value="test")])
        r = records.resolve()

        self.assertEqual(r[0].value, TxtRecord(value="test").value)

    def test_spf_recursive_scan(self):
        domain = Domain("example.com")
        records = TxtRecords(domain=domain)

        # メインドメインのSPFレコードをモック
        records.resolve = MagicMock(return_value=[
            TxtRecord(value="v=spf1 include:_spf.example.com include:thirdparty.com ~all")
        ])
        records.records = records.resolve()

        # インクルードされたドメインのSPFレコードをモック
        included_records = TxtRecords(Domain("_spf.example.com"))
        included_records.resolve = MagicMock(return_value=[
            TxtRecord(value="v=spf1 ip4:192.0.2.1 ~all", source_domain="_spf.example.com")
        ])
        included_records.records = included_records.resolve()  # モックの戻り値をrecordsに設定


        # TxtRecordsの作成をパッチ
        with patch('txtra.__main__.TxtRecords') as mock_txtrecords:
            mock_txtrecords.side_effect = lambda domain: included_records if domain.name == "_spf.example.com" else records

            # スキャンを実行
            records.scan(templates=txtra.templates)

            # 全てのレコードが存在することを確認
            all_records = [r.value for r in records.records]
            self.assertEqual(len(all_records), 2)
            self.assertIn("v=spf1 include:_spf.example.com include:thirdparty.com ~all", all_records)
            self.assertIn("v=spf1 ip4:192.0.2.1 ~all", all_records)

            # 再帰的にスキャンされたドメインが正しいことを確認
            scanned_domains = [r.source_domain for r in records.records if r.source_domain]
            self.assertIn("_spf.example.com", scanned_domains)

    def test_activegate_ss(self):
        records = self.mock_resolve("example.com", "v=spf include:_spf.ecample.com include:_spf.activegate-ss.jp ~all")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Active! gate SS")
                self.assertEqual(record.token, "")

    def test_adobe_sign(self):
        records = self.mock_resolve("example.com", "adobe-sign-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Adobe Acrobat Sign")
                self.assertEqual(record.token, "test")

    def test_adobe(self):
        records = self.mock_resolve("example.com", "adobe-idp-site-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Adobe")
                self.assertEqual(record.token, "test")

    def test_akamai_cloudpiercer(self):
        records = self.mock_resolve("example.com", "cloudpiercer-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Akamai Cloudpiercer")
                self.assertEqual(record.token, "test")

    def test_alibaba_cloud(self):
        records = self.mock_resolve("example.com", "aliyun-site-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Alibaba Cloud")
                self.assertEqual(record.token, "test")

    def test_android_mdm1(self):
        records = self.mock_resolve("example.com", "android-enroll=http://example.com")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "android mobile mdm")
                self.assertEqual(record.token, "http://example.com")

    def test_android_mdm2(self):
        records = self.mock_resolve("example.com", "android-mdm-enroll=http://example.com")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "android mobile mdm")
                self.assertEqual(record.token, "http://example.com")

    def test_anodot(self):
        records = self.mock_resolve("example.com", "anodot-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "anodot")
                self.assertEqual(record.token, "test")

    def test_apple(self):
        records = self.mock_resolve("example.com", "apple-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Apple")
                self.assertEqual(record.token, "test")

    def test_atlassian(self):
        records = self.mock_resolve("example.com", "atlassian-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Atlassian")
                self.assertEqual(record.token, "test")

    def test_aws_ses(self):
        records = self.mock_resolve("example.com", "amazonses:test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Amazon Simple Email")
                self.assertEqual(record.token, "test")

    def test_azure(self):
        records = self.mock_resolve("example.com", "test.azurewebsites.net")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Azure")
                self.assertEqual(record.token, "test")

    def test_barracuda_bvm(self):
        records = self.mock_resolve("example.com", "bvm-site-verification=test1234")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Barracuda Vulnerability Manager")
                self.assertEqual(record.token, "test1234")

    def test_blitz(self):
        records = self.mock_resolve("example.com", "blitz=test-1234")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Feedblitz")
                self.assertEqual(record.token, "test-1234")

    def test_botify(self):
        records = self.mock_resolve("example.com", "botify-site-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Botify")
                self.assertEqual(record.token, "test")

    def test_brave(self):
        records = self.mock_resolve("example.com", "brave-ledger-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Brave")
                self.assertEqual(record.token, "test")

    def test_bugcrowd(self):
        records = self.mock_resolve("example.com", "bugcrowd-verification=abcdef0123456789")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "bugcrowd")
                self.assertEqual(record.token, "abcdef0123456789")

    def test_citrix1(self):
        records = self.mock_resolve("example.com", "citrix-verification-code=test-1234")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Citrix")
                self.assertEqual(record.token, "test-1234")

    def test_citrix2(self):
        records = self.mock_resolve("example.com", "citrix.mobile.ads.otp=test-1234")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Citrix")
                self.assertEqual(record.token, "test-1234")

    def test_cloudcontrol1(self):
        records = self.mock_resolve("example.com", "cloudcontrol-verification:abcdef1234")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "cloudControl")
                self.assertEqual(record.token, "abcdef1234")

    def test_cloudcontrol2(self):
        records = self.mock_resolve("example.com", "cloudcontrol-verification: abcdef1234")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "cloudControl")
                self.assertEqual(record.token, "abcdef1234")

    def test_cloudcontrol3(self):
        records = self.mock_resolve("example.com", "cloudControl-verification:abcdef1234")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "cloudControl")
                self.assertEqual(record.token, "abcdef1234")

    def test_cloudcontrol4(self):
        records = self.mock_resolve("example.com", "cloudControl-verification: abcdef1234")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "cloudControl")
                self.assertEqual(record.token, "abcdef1234")

    def test_dailymotion(self):
        records = self.mock_resolve("example.com", "dailymotion-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "dailymotion")
                self.assertEqual(record.token, "test")

    def test_detectify(self):
        records = self.mock_resolve("example.com", "detectify-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "detectify")
                self.assertEqual(record.token, "test")

    def test_docusign(self):
        records = self.mock_resolve("example.com", "docusign=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "docusign")
                self.assertEqual(record.token, "test")

    def test_dropbox(self):
        records = self.mock_resolve("example.com", "dropbox-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Dropbox")
                self.assertEqual(record.token, "test")

    def test_dynatrace(self):
        records = self.mock_resolve("example.com", "Dynatrace-site-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Dynatrace")
                self.assertEqual(record.token, "test")
    
    def test_dynatrace2(self):
        records = self.mock_resolve("example.com", "dynatrace-site-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Dynatrace")
                self.assertEqual(record.token, "test")

    def test_facebook(self):
        records = self.mock_resolve("example.com", "facebook-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Facebook")
                self.assertEqual(record.token, "test")

    def test_firebase(self):
        records = self.mock_resolve("example.com", "firebase=test-test-123")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Firebase")
                self.assertEqual(record.token, "test-test-123")

    def test_globalsign1(self):
        records = self.mock_resolve(
            "example.com", "_globalsign-domain-verification=test"
        )
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Global Sign")
                self.assertEqual(record.token, "test")

    def test_globalsign2(self):
        records = self.mock_resolve(
            "example.com", "globalsign-domain-verification=test"
        )
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Global Sign")
                self.assertEqual(record.token, "test")

    def test_gmail(self):
        records = self.mock_resolve("example.com", "google-site-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "GMail")
                self.assertEqual(record.token, "test")

    def test_godaddy1(self):
        records = self.mock_resolve("example.com", "DZC: test-test.com")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "GoDaddy Web Services")
                self.assertEqual(record.token, "test-test.com")

    def test_godaddy2(self):
        records = self.mock_resolve("example.com", "godaddyverification=/Hoge==")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "GoDaddy Web Services")
                self.assertEqual(record.token, "/Hoge==")

    def test_haveibeenpwned(self):
        records = self.mock_resolve("example.com", "have-i-been-pwned-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Have I been pwned")
                self.assertEqual(record.token, "test")

    def test_heroku(self):
        records = self.mock_resolve("example.com", "heroku-site-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "heroku")
                self.assertEqual(record.token, "test")

    def test_knowbe4(self):
        records = self.mock_resolve("example.com", "knowbe4-site-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "knowbe4")
                self.assertEqual(record.token, "test")
          
    def test_letsencript(self):
        records = self.mock_resolve("example.com", "_acme-challenge=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Let's Encrypt")
                self.assertEqual(record.token, "test")      
             

    def test_line_works1(self):
        records = self.mock_resolve("example.com", "worksmobile-certification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "LINE WORKS")
                self.assertEqual(record.token, "test")
          
    def test_line_works2(self):
        records = self.mock_resolve("example.com", "worksmobile.certification.test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "LINE WORKS")
                self.assertEqual(record.token, "test")      
             
    def test_loaderio(self):
        records = self.mock_resolve("example.com", "loaderio=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "loaderio")
                self.assertEqual(record.token, "test") 
             
    def test_logmein(self):
        records = self.mock_resolve("example.com", "logmein-verification-code=668e156b-f5d3-430e-9944-f1d4385d043e")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "logmein")
                self.assertEqual(record.token, "668e156b-f5d3-430e-9944-f1d4385d043e") 

    def test_mailigen(self):
        records = self.mock_resolve("example.com", "mailigen-site-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "mailigen")
                self.assertEqual(record.token, "test")

    def test_mailjet(self):
        records = self.mock_resolve("example.com", "mailjet-domain-validation=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Mailjet")
                self.assertEqual(record.token, "test")

    def test_mailru(self):
        records = self.mock_resolve("example.com", "mailru-verification:test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Mail.Ru")
                self.assertEqual(record.token, "test")

        records = self.mock_resolve("example.com", "mailru-verification: test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Mail.Ru")
                self.assertEqual(record.token, "test")    
                              
    def test_o3651(self):
        records = self.mock_resolve("example.com", "ms=12345")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Microsoft Office 365")
                self.assertEqual(record.token, "123456")
                              
    def test_o3652(self):
        records = self.mock_resolve("example.com", "mscid=test123==")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Microsoft Office 365")
                self.assertEqual(record.token, "test123==")  
                            
    def test_o3653(self):
        records = self.mock_resolve("example.com", "MS=ABCDEF0123456789")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Microsoft Office 365")
                self.assertEqual(record.token, "ABCDEF0123456789")   
    def test_pardot(self):
        records = self.mock_resolve("example.com", "pardot_foo.bar=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "pardot")
                self.assertEqual(record.token, "test")

    def test_pardot2(self):
        records = self.mock_resolve("example.com", "pardot0123456789=abcdef0123456789")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "pardot")
                self.assertEqual(record.token, "abcdef0123456789")

    def test_postman(self):
        records = self.mock_resolve("example.com", "postman-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Postman")
                self.assertEqual(record.token, "test")

    def test_protonmail(self):
        records = self.mock_resolve("example.com", "protonmail-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "protonmail")
                self.assertEqual(record.token, "test")
                            
    def test_sendinblue(self):
        records = self.mock_resolve("example.com", "Sendinblue-code:123456789abcedf")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "sendinblue")
                self.assertEqual(record.token, "123456789abcedf")   
                             
    def test_segment(self):
        records = self.mock_resolve("example.com", "segment-site-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "segment")
                self.assertEqual(record.token, "test")  

    def test_sendgrid(self):
        records = self.mock_resolve("example.com", "v=spf include:_spf.example.com include:u12345678.wl123.sendgrid.net ~all")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "SendGrid")
                self.assertEqual(record.token, "u12345678.wl123")

    def test_site24x7(self):
        records = self.mock_resolve("example.com", "site24x7-signals-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Site24x7")
                self.assertEqual(record.token, "test")  

    def test_sophos(self):
        records = self.mock_resolve("example.com", "sophos-domain-verification=123456789abcedf")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Sophos")
                self.assertEqual(record.token, "123456789abcedf") 
                           
    def test_spycloud(self):
        records = self.mock_resolve("example.com", "spycloud-domain-verification=123456789-abcedf")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "spycloud")
                self.assertEqual(record.token, "123456789-abcedf") 

    def test_statuspage(self):
        records = self.mock_resolve("example.com", "status-page-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "statuspage")
                self.assertEqual(record.token, "test")  
                   
    def test_swisssign(self):
        records = self.mock_resolve("example.com", "swisssign-check=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "swisssign")
                self.assertEqual(record.token, "test")   
                   
    def test_symantec_mdm(self):
        records = self.mock_resolve("example.com", "OSIAGENTREGURL=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Symantec MDM")
                self.assertEqual(record.token, "test")   
                    
    def test_t_systems(self):
        records = self.mock_resolve("example.com", "_telesec-domain-validation=TEST")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "t-systems")
                self.assertEqual(record.token, "TEST")   
                    
    def test_teamviewer(self):
        records = self.mock_resolve("example.com", "teamviewer-sso-verification=Test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "teamviewer")
                self.assertEqual(record.token, "Test")   
                    
    def test_tinfosecurity(self):
        records = self.mock_resolve("example.com", "tinfoil-site-verification= test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "tinfosecurity")
                self.assertEqual(record.token, "test")

    def test_tmes(self):
        records = self.mock_resolve("example.com", "tmes=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Trend Micro")
                self.assertEqual(record.token, "test")
  
    def test_twilio(self):
        records = self.mock_resolve("example.com", "twilio-domain-verification=0123456789abcdef")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Twilio")
                self.assertEqual(record.token, "0123456789abcdef")

    def test_webaccel1(self):
        records = self.mock_resolve("example.com", "webaccel=0123456789abcdef")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "SAKURA Web Accelerator")
                self.assertEqual(record.token, "0123456789abcdef")

    def test_webaccel2(self):
        records = self.mock_resolve("example.com", "webaccel: 01234; 56789; abcdef;")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "SAKURA Web Accelerator")
                self.assertEqual(record.token, "01234; 56789; abcdef;")

    def test_webex1(self):
        records = self.mock_resolve("example.com", "webexdomainverification.hoge=01234-5678-9abc-def")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "webex")
                self.assertEqual(record.token, "01234-5678-9abc-def")

    def test_webex2(self):
        records = self.mock_resolve("example.com", "ciscocidomainverification=01234-5678-9abc-def")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "webex")
                self.assertEqual(record.token, "01234-5678-9abc-def")

    def test_webex3(self):
        records = self.mock_resolve("example.com", "cisco-ci-domain-verification=0123456789abcdef")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "webex")
                self.assertEqual(record.token, "0123456789abcdef")

    def test_webex4(self):
        records = self.mock_resolve("example.com", "cisco-site-verification=01234-5678-9abc-def")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "webex")
                self.assertEqual(record.token, "01234-5678-9abc-def")

    def test_wmail(self):
        records = self.mock_resolve("example.com", "wmail-verification: 0123456789abcdef")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "wmail")
                self.assertEqual(record.token, "0123456789abcdef")

    def test_workplace(self):
        records = self.mock_resolve("example.com", "workplace-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Workplace")
                self.assertEqual(record.token, "test")

    def test_wrike(self):
        records = self.mock_resolve("example.com", "wrike-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "wrike")
                self.assertEqual(record.token, "test")

    def test_yandex(self):
        records = self.mock_resolve("example.com", "yandex-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Yandex")
                self.assertEqual(record.token, "test")

    def test_zapier(self):
        records = self.mock_resolve("example.com", "zapier-domain-verification-challenge=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Zapier")
                self.assertEqual(record.token, "test")

    def test_zoho(self):
        records = self.mock_resolve("example.com", "zoho-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Zoho Mail")
                self.assertEqual(record.token, "test")

    def test_zoom(self):
        records = self.mock_resolve("example.com", "ZOOM_verify_test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.matches[0].template.name, "Zoom")
                self.assertEqual(record.token, "test")
if __name__ == "__main__":
    unittest.main()
