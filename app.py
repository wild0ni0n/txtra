import re
import sys
import glob
import argparse
from urllib.parse import urlparse
from typing import List, Optional
from dataclasses import dataclass
from dns import resolver
from colorama import Fore
import yaml


TEMPLATE_DIR = "provider/*.yml"


class Template:
    """txtra provider template class"""

    def __init__(self, name="", author="", category="") -> None:
        self.name: str = name
        self.category: str = category
        self.author: str = author
        self.rule: dict
        self.yaml_data: dict

    def load(self, yaml_data):
        """Load txtra provider template

        Args:
            yaml_data (_type_): raw template data
        """
        self.name = yaml_data["info"]["name"]
        self.category = yaml_data["info"]["category"]
        self.author = yaml_data["info"]["author"]
        self.rule = yaml_data["rule"]

    def loads(self, path: str):
        """Load multiple txtra provider templates

        Args:
            path (str): txtra provider template directory  path
        """
        with open(path, "r", encoding="utf-8") as yml:
            self.yaml_data = yaml.safe_load(yml)
        self.load(self.yaml_data)

    def match(self, value: str) -> Optional[re.Match]:
        """Match txt records with loaded templates

        Args:
            value (str): txt record value

        Returns:
            Optional[re.Match]: If a match is found, re.match is returned. If not,
            return None.
        """
        if self.rule["type"] == "regex":
            m = re.search(self.rule["regex"][0], value)
            if m:
                return m
        return None

    def get_paramname(self) -> Optional[List[str]]:
        """Get the params parameter of the template

        Returns:
            Optional[List[str]]
        """
        if "params" in self.rule:
            return self.rule["params"]
        return None


@dataclass
class Domain:
    """Domain class"""

    name: str

    def __post_init__(self):
        if self.name[:4] == "http":
            o = urlparse(self.name)
            if o.hostname is not None:
                self.name = o.hostname

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class TxtRecord:
    """txt record class"""

    def __init__(self, value: str) -> None:
        self.value = value
        self.is_matched: bool = False
        self.template: Template
        self.provider: str
        self.category: str
        self.token: str

    def scan(self, templates: List[Template]) -> Optional[Template]:
        """Scans txt records to see if the value corresponds to the template

        Args:
            templates (List[Template]): List of Template instances

        Returns:
            Optional[Template]: Applicable Templates, or None
        """
        for template in templates:
            m = template.match(self.value)
            if m:
                self.template = template
                self.provider = self.template.name
                self.category = self.template.category
                self.is_matched = True
                try:
                    self.token = m.group("token")
                except IndexError:
                    self.token = ""
                return template
        return None


class TxtRecords:
    """collective class of txt record class"""

    def __init__(self, domain: Domain) -> None:
        self.domain: Domain = domain
        self.records: List[TxtRecord] = []
        self.is_matched = False

    def resolve(self) -> List[TxtRecord]:
        """Perform DNS resolution of txt records

        Returns:
            List[TxtRecord]: txt record list
        """
        answers = resolver.resolve(self.domain.name, "TXT")
        for rdata in answers:  # type:ignore
            for data in rdata.strings:
                self.records.append(TxtRecord(data.decode("utf-8")))
        return self.records

    def scan(self, templates: List[Template]):
        """Scans txt records to see if the value corresponds to the template

        Args:
            templates (List[Template]): List of Template instances
        """
        for record in self.records:
            record.scan(templates)

    def __iter__(self):
        yield from self.records


def load_templates() -> List[Template]:
    """Load a templates"""
    templates = []
    path_list = glob.glob(TEMPLATE_DIR)
    for path in path_list:
        _t = Template()
        _t.loads(path)
        templates.append(_t)
    return templates


TEMPLATES = load_templates()


def stdout_mode(target_domains: List[Domain]):
    """standard output mode"""
    print(f"[INF] Check {len(target_domains)} domains")
    for target_domain in target_domains:
        records = TxtRecords(domain=target_domain)
        try:
            records.resolve()
        except resolver.NoAnswer:
            continue
        records.scan(templates=TEMPLATES)
        for record in records:
            if record.is_matched:
                token_string = (
                    Fore.CYAN + f" [token={record.token}] " if record.token else ""
                )
                print(
                    Fore.YELLOW
                    + f"[{records.domain}]"
                    + Fore.BLUE
                    + f" [{record.provider}] "
                    + token_string
                    + Fore.YELLOW
                    + f"{record.value}"
                )
            else:
                print(Fore.YELLOW + f"[{records.domain}] {record.value} ")


def argparse_setup() -> argparse.ArgumentParser:
    """argparse setup function"""
    p = argparse.ArgumentParser()
    p.add_argument("-d", "--domain", help="Specify domain")
    p.add_argument(
        "-f",
        "--file",
        help="Specify domains file",
        type=argparse.FileType("r", encoding="utf-8"),
    )
    # parser.add_argument('-o', 'Specify output file')
    return p


if __name__ == "__main__":
    parser = argparse_setup()
    args = parser.parse_args()

    if args.domain:
        domain = Domain(args.domain)
        stdout_mode([domain])
        sys.exit(0)

    if args.file is not None:
        lines = args.file.read().splitlines()
        domains = list(map(lambda v: Domain(v), lines))
        print(domains)
        stdout_mode(domains)
        sys.exit(0)
