import re
import sys
import argparse
import csv
import json

from urllib.parse import urlparse
from typing import List, Optional
from dataclasses import dataclass
from dns import resolver
from colorama import Fore
from importlib import resources
import yaml


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
            for pattern in self.rule["regex"]:
                m = re.search(pattern, value)
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
        self.provider: str = ""
        self.category: str
        self.token: str = ""

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
        try:
            answers = resolver.resolve(self.domain.name, "TXT")
        except resolver.LifetimeTimeout as e:
            raise resolver.LifetimeTimeout from e
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


class Txtra:
    """txtra class"""

    def __init__(self) -> None:
        self.templates = self.load_templates()

    def load_templates(self) -> List[Template]:
        """Load a templates"""
        templates = []
        provider_dir = resources.files('txtra') / 'provider'
        for path in provider_dir.glob('*.yml'):
            _t = Template()
            _t.loads(path)
            templates.append(_t)
        return templates

    def stdout_mode(self, args, domains: List[Domain]):
        """standard output mode"""
        print(f"[INF] Check {len(domains)} domains")
        print("[INF] No Scan Mode") if args.no_scan else ""
        for domain in domains:
            records = TxtRecords(domain=domain)
            try:
                records.resolve()
            except resolver.NoAnswer:
                continue
            except resolver.LifetimeTimeout:
                continue
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                continue  # Optional: handle other exceptions and continue to the next iteration

            if args.no_scan:
                for record in records:
                    print(Fore.YELLOW + f"[{records.domain}] " + f"{record.value}")
            else:
                records.scan(templates=self.templates)
                for record in records:
                    if record.is_matched:
                        token_string = (
                            Fore.CYAN + f" [token={record.token}] "
                            if record.token
                            else ""
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

    def csv_mode(self, args, domains: List[Domain], path="./output.csv"):
        """csv mode"""

        with open(path, "w") as f:
            f.writelines([])

        for domain in domains:
            records = TxtRecords(domain=domain)

            try:
                records.resolve()
            except resolver.LifetimeTimeout:
                continue
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                continue  # Optional: handle other exceptions and continue to the next iteration

            if args.no_scan:
                with open(path, "a") as f:
                    w = csv.writer(f)
                    for record in records:
                        w.writerow([records.domain, record.value])
            else:
                records.scan(templates=self.templates)
                with open(path, "a") as f:
                    w = csv.writer(f)
                    for record in records:
                        w.writerow(
                            [
                                records.domain,
                                record.provider,
                                record.token,
                                record.value,
                            ]
                        )
    
    def json_mode(self, args, domains: List[Domain], path="./output.json"):
        """json mode"""
        output_json = {}
        for domain in domains:
            records = TxtRecords(domain=domain)

            try:
                records.resolve()
            except resolver.LifetimeTimeout:
                continue
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                continue  # Optional: handle other exceptions and continue to the next iteration

            if args.no_scan:
                output_json[str(domain)] = {
                    'raw_records': [ record.value for record in records]
                }
                
            else:
                records.scan(templates=self.templates)
                output_json[str(domain)] = {
                    'raw_records': [ record.value for record in records]
                }
                output_json[str(domain)]['records'] = []
                for record in records:
                    if record.is_matched:
                        token_string = record.token if record.token else ""
                        
                        output_json[str(domain)]['records'].append({
                            "provider": record.provider,
                            "token": token_string,
                            "value": record.value,
                        })
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(output_json))


    def argparse_setup(self, args) -> argparse.Namespace:
        """argparse setup function"""
        p = argparse.ArgumentParser()
        p.add_argument("-d", "--domain", help="Specify domain")
        p.add_argument(
            "-f",
            "--file",
            help="Specify domains file",
            type=argparse.FileType("r", encoding="utf-8"),
        )
        p.add_argument(
            "-s",
            "--no-scan",
            help="No template scan is performed. Txtra returns only txt records",
            action="store_true",
        )
        p.add_argument(
            "-c",
            "--csv",
            help="Output in CSV format. Cannot be used in conjunction with the \
                --json option.",
            action="store_true",
        )
        p.add_argument(
            "-j",
            "--json",
            help="Output in json format. Cannot be used in conjunction with the \
                --csv option.",
            action="store_true",
        )
        # parser.add_argument('-o', 'Specify output file')

        if sys.stdin.isatty() and len(sys.argv) == 1:
            p.print_help()
            sys.exit(1)

        return p.parse_args(args)

def main():
    txtra = Txtra()
    args = txtra.argparse_setup(sys.argv[1:])

    if args.csv and args.json:
        print("`--csv` and `--json` options cannot be used together.")
        sys.exit(0)

    if args.domain:
        domains = [Domain(args.domain)]
    elif args.file is not None:
        lines = args.file.read().splitlines()
        domains = list(map(lambda v: Domain(v), lines))
    elif not sys.stdin.isatty():
        lines = sys.stdin.read().strip().splitlines()
        domains = list(map(lambda v: Domain(v), lines))

    if args.csv:
        txtra.csv_mode(args, domains)
    if args.json:
        txtra.json_mode(args, domains)
    else:
        txtra.stdout_mode(args, domains)
    sys.exit(0)

if __name__ == "__main__":
    main()