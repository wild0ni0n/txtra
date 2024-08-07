from txtra.__main__ import (
    Domain,
    Txtra,
    TxtRecord,
    TxtRecords
)

import unittest
from unittest.mock import MagicMock

txtra = Txtra()

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

    def test_adobe_sign(self):
        records = self.mock_resolve("example.com", "adobe-sign-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Adobe Acrobat Sign")
                self.assertEqual(record.token, "test")

    def test_adobe(self):
        records = self.mock_resolve("example.com", "adobe-idp-site-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Adobe")
                self.assertEqual(record.token, "test")

    def test_apple(self):
        records = self.mock_resolve("example.com", "apple-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Apple")
                self.assertEqual(record.token, "test")

    def test_atlassian(self):
        records = self.mock_resolve("example.com", "atlassian-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Atlassian")
                self.assertEqual(record.token, "test")

    def test_aws_ses(self):
        records = self.mock_resolve("example.com", "amazonses:test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Amazon Simple Email")
                self.assertEqual(record.token, "test")

    def test_azure(self):
        records = self.mock_resolve("example.com", "test.azurewebsites.net")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Azure")
                self.assertEqual(record.token, "test")

    def test_brave(self):
        records = self.mock_resolve("example.com", "brave-ledger-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Brave")
                self.assertEqual(record.token, "test")

    def test_citrix(self):
        records = self.mock_resolve("example.com", "citrix-verification-code=test-1234")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Citrix")
                self.assertEqual(record.token, "test-1234")

    def test_docusign(self):
        records = self.mock_resolve("example.com", "docusign=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "docusign")
                self.assertEqual(record.token, "test")

    def test_dropbox(self):
        records = self.mock_resolve("example.com", "dropbox-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Dropbox")
                self.assertEqual(record.token, "test")

    def test_facebook(self):
        records = self.mock_resolve("example.com", "facebook-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Facebook")
                self.assertEqual(record.token, "test")

    def test_firebase(self):
        records = self.mock_resolve("example.com", "firebase=test-test-123")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Firebase")
                self.assertEqual(record.token, "test-test-123")

    def test_globalsign1(self):
        records = self.mock_resolve(
            "example.com", "_globalsign-domain-verification=test"
        )
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Global Sign")
                self.assertEqual(record.token, "test")

    def test_globalsign2(self):
        records = self.mock_resolve(
            "example.com", "globalsign-domain-verification=test"
        )
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Global Sign")
                self.assertEqual(record.token, "test")

    def test_gmail(self):
        records = self.mock_resolve("example.com", "google-site-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "GMail")
                self.assertEqual(record.token, "test")

    def test_haveibeenpwned(self):
        records = self.mock_resolve("example.com", "have-i-been-pwned-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Have I been pwned")
                self.assertEqual(record.token, "test")

    def test_line_works1(self):
        records = self.mock_resolve("example.com", "worksmobile-certification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "LINE WORKS")
                self.assertEqual(record.token, "test")
          
    def test_line_works2(self):
        records = self.mock_resolve("example.com", "worksmobile.certification.test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "LINE WORKS")
                self.assertEqual(record.token, "test")      
             
    def test_loaderio(self):
        records = self.mock_resolve("example.com", "loaderio=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "loaderio")
                self.assertEqual(record.token, "test") 

    def test_mailru(self):
        records = self.mock_resolve("example.com", "mailru-verification:test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Mail.Ru")
                self.assertEqual(record.token, "test")
        records = self.mock_resolve("example.com", "mailru-verification: test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Mail.Ru")
                self.assertEqual(record.token, "test")    
                              
    def test_o3651(self):
        records = self.mock_resolve("example.com", "ms=12345")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Microsoft Office 365")
                self.assertEqual(record.token, "123456")
                              
    def test_o3652(self):
        records = self.mock_resolve("example.com", "mscid=test123==")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Microsoft Office 365")
                self.assertEqual(record.token, "test123==")                              
    def test_pardot(self):
        records = self.mock_resolve("example.com", "pardot_foo.bar=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "pardot")
                self.assertEqual(record.token, "test")
                         
    def test_sendinblue(self):
        records = self.mock_resolve("example.com", "Sendinblue-code:123456789abcedf")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "sendinblue")
                self.assertEqual(record.token, "123456789abcedf")                             
    def test_tmes(self):
        records = self.mock_resolve("example.com", "tmes=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Trend Micro")
                self.assertEqual(record.token, "test")
  
    def test_twilio(self):
        records = self.mock_resolve("example.com", "twilio-domain-verification=0123456789abcdef")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Twilio")
                self.assertEqual(record.token, "0123456789abcdef")

    def test_webaccel(self):
        records = self.mock_resolve("example.com", "webaccel=0123456789abcdef")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "SAKURA Web Accelerator")
                self.assertEqual(record.token, "0123456789abcdef")

    def test_webex1(self):
        records = self.mock_resolve("example.com", "webexdomainverification.hoge=01234-5678-9abc-def")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "webex")
                self.assertEqual(record.token, "01234-5678-9abc-def")

    def test_webex_2(self):
        records = self.mock_resolve("example.com", "ciscocidomainverification=01234-5678-9abc-def")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "webex")
                self.assertEqual(record.token, "01234-5678-9abc-def")

    def test_wmail(self):
        records = self.mock_resolve("example.com", "wmail-verification: 0123456789abcdef")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "wmail")
                self.assertEqual(record.token, "0123456789abcdef")

    def test_workplace(self):
        records = self.mock_resolve("example.com", "workplace-domain-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Workplace")
                self.assertEqual(record.token, "test")

    def test_wrike(self):
        records = self.mock_resolve("example.com", "wrike-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "wrike")
                self.assertEqual(record.token, "test")

    def test_yandex(self):
        records = self.mock_resolve("example.com", "yandex-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Yandex")
                self.assertEqual(record.token, "test")

    def test_zapier(self):
        records = self.mock_resolve("example.com", "zapier-domain-verification-challenge=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Zapier")
                self.assertEqual(record.token, "test")

    def test_zoho(self):
        records = self.mock_resolve("example.com", "zoho-verification=test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Zoho Mail")
                self.assertEqual(record.token, "test")

    def test_zoom(self):
        records = self.mock_resolve("example.com", "ZOOM_verify_test")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Zoom")
                self.assertEqual(record.token, "test")
if __name__ == "__main__":
    unittest.main()
