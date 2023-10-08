import dns.resolver
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

    def match(self, value) -> Optional[str]:
        if self.rule['type'] == 'regex':
            r = self.rule['regex']
            if re.search(r[0], value):
                return value
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
        return  self.name


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
        try:
            answers = dns.resolver.resolve(domain.name, "TXT")
            for rdata in answers:
                for data in rdata.strings:
                    txtval = data.decode('utf-8')
                    t = detect_provider_from_txt(txtval, templates)
                    if t is not None:
                        print(Fore.YELLOW +
                              "[{}]".format(domain) + Fore.BLUE + " [{}] ".format(t.name) + Fore.YELLOW + "{}".format(txtval))
                    else:
                        print(Fore.YELLOW +
                              "[{}] {} ".format(domain, txtval))

        except:
            continue


def load_list(file, limit=None):
    with open(file, "r") as f:
        lines = f.readlines()

    p_lines = []
    try:
        for line in lines[:limit]:
            if line[:4] == "http":
                o = urlparse(line)
                p_lines.append(o.hostname)
            else:
                p_lines.append(line)
    except:
        print("Some domains cannot be parsed.")

    return p_lines

def argparse_setup() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', help='Specify domain')
    parser.add_argument('-f', '--file', help='Specify domains file', type=argparse.FileType("r", encoding="utf-8"))
    #parser.add_argument('-o', 'Specify output file')
    return parser

if __name__ == "__main__":
    parser = argparse_setup()
    args = parser.parse_args()

    templates = load_templates()

    if args.domain:
        domain = Domain(args.domain)
        stdout_mode([domain])
        exit()
    
    if args.file != None:
        lines = args.file.read().splitlines()
        domains = list(map(lambda v: Domain(v), lines))
        print(domains)
        stdout_mode(domains)
        exit()
