import requests
import argparse
import colorama
from colorama import Fore, Back, Style
import json
import subprocess

colorama.init(autoreset=True)

parser = argparse.ArgumentParser(description='Security header scanner')
parser.add_argument('url', help='URL to scan (e.g., https://example.com)')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

url = args.url
verbose = args.verbose

security_headers = {}
with open("security-headers.json", "r") as config_file:
    security_headers = json.load(config_file)

file = open("log.txt", "w", encoding="utf-8")

count = len(security_headers)
implemented = 0

try:
    response = requests.get(url, timeout=5)
    print(f"Status Code: {response.status_code}")
    file.write(f"Status Code: {response.status_code}\n")
    headers = response.headers
    if  verbose == True:
        for header, value in headers.items():
            print(f"{header}: {value}")
    print()
    for header_name, correct_value in security_headers.items():    
        if header_name in headers:
            value = headers[header_name]
            print(f"{Fore.GREEN}✓ {header_name}", end="")
            file.write(f"✓ {header_name}")
            if value in correct_value:
                print(f"{Fore.GREEN} is implemented with the right value\n")
                file.write(f"is implemented with the right value\n")
            else:
                print(f"{Fore.RED} is implemented with has the wrong value\n")
                file.write(f"is implemented with has the wrong value\n")
            implemented += 1
        else: 
            print(f"{Fore.RED}✗ {header_name}")
            file.write(f"✗ {header_name}\n")

    print(f"{implemented} out of {count} recommended security headers have been detected")
    file.write(f"{implemented} out of {count} recommended security headers have been detected\n")

except requests.exceptions.RequestException as e:
    raise SystemExit(f"{Fore.RED}{e}")

file.close()

