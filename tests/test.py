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

    def test_apple_vusiness_manager(self):
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

    def test_globalsign(self):
        records = self.mock_resolve(
            "example.com", "_globalsign-domain-verification=test"
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

    def test_o365(self):
        records = self.mock_resolve("example.com", "ms=12345")
        records.scan(templates=txtra.templates)
        for record in records:
            if record.is_matched:
                self.assertEqual(records.domain.name, "example.com")
                self.assertEqual(record.provider, "Microsoft Office 365")
                self.assertEqual(record.token, "123456")


if __name__ == "__main__":
    unittest.main()
