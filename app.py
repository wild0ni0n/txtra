from dns import resolver
from urllib.parse import urlparse
from colorama import Fore
import yaml
import re
import glob
from typing import List, Optional
import argparse
from dataclasses import dataclass


TEMPLATE_DIR = "provider/*.yml"


class Template:
    def __init__(self, name="", author="", category="") -> None:
        self.name = name
        self.category = category
        self.author = author

    def load(self, yaml_data):
        self.name = yaml_data["info"]["name"]
        self.category = yaml_data["info"]["category"]
        self.author = yaml_data["info"]["author"]
        self.rule = yaml_data["rule"]

    def loads(self, path: str):
        with open(path, "r") as yml:
            self.yaml_data = yaml.safe_load(yml)
        self.load(self.yaml_data)

    def match(self, value: str) -> Optional[re.Match]:
        if self.rule["type"] == "regex":
            m = re.search(self.rule["regex"][0], value)
            if m:
                return m
        return None

    def get_paramname(self) -> Optional[List[str]]:
        if "params" in self.rule:
            return self.rule["params"]
        else:
            return None


@dataclass
class Domain:
    name: str

    def __post_init__(self):
        if self.name[:4] == "http":
            o = urlparse(self.name)
            self.name = o.hostname

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class TxtRecord:
    def __init__(self, value: str) -> None:
        self.value = value
        self.is_matched = False

    def scan(self, templates: List[Template]) -> Optional[Template]:
        for template in templates:
            m = template.match(self.value)
            if m:
                self.template = template
                self.provider = self.template.name
                self.category = self.template.category
                self.is_matched = True
                try:
                    self.token: str = m.group("token")
                except IndexError:
                    self.token = ""
                return template
        return None


class TxtRecords:
    def __init__(self, domain: Domain) -> None:
        self.domain: Domain = domain
        self.records: List[TxtRecord] = []
        self.is_matched = False

    def resolve(self) -> List[TxtRecord]:
        answers = resolver.resolve(self.domain.name, "TXT")
        for rdata in answers:
            for data in rdata.strings:
                self.records.append(TxtRecord(data.decode("utf-8")))
        return self.records

    def scan(self, templates: List[Template]):
        for record in self.records:
            record.scan(templates)

    def __iter__(self):
        yield from self.records


def load_templates() -> List[Template]:
    templates = []
    path_list = glob.glob(TEMPLATE_DIR)
    for path in path_list:
        _t = Template()
        _t.loads(path)
        templates.append(_t)
    return templates


def detect_provider_from_txt(txt, templates: List[Template]) -> Optional[Template]:
    for t in templates:
        if t.match(txt):
            return t
    return None


def stdout_mode(domains: List[Domain]):
    print("[INF] Check {} domains".format(len(domains)))
    for domain in domains:
        records = TxtRecords(domain=domain)
        try:
            records.resolve()
        except resolver.NoAnswer:
            continue
        records.scan(templates=templates)
        for record in records:
            if record.is_matched:
                token_string = (
                    Fore.CYAN + " [token={}] ".format(record.token)
                    if record.token
                    else ""
                )
                print(
                    Fore.YELLOW
                    + "[{}]".format(records.domain)
                    + Fore.BLUE
                    + " [{}] ".format(record.provider)
                    + token_string
                    + Fore.YELLOW
                    + "{}".format(record.value)
                )
            else:
                print(Fore.YELLOW + "[{}] {} ".format(records.domain, record.value))


def argparse_setup() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", help="Specify domain")
    parser.add_argument(
        "-f",
        "--file",
        help="Specify domains file",
        type=argparse.FileType("r", encoding="utf-8"),
    )
    # parser.add_argument('-o', 'Specify output file')
    return parser


if __name__ == "__main__":
    parser = argparse_setup()
    args = parser.parse_args()

    templates = load_templates()

    if args.domain:
        domain = Domain(args.domain)
        stdout_mode([domain])
        exit()

    if args.file is not None:
        lines = args.file.read().splitlines()
        domains = list(map(lambda v: Domain(v), lines))
        print(domains)
        stdout_mode(domains)
        exit()
