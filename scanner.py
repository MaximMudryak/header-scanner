import requests
import argparse
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

parser = argparse.ArgumentParser(description='Security header scanner')
parser.add_argument('url', help='URL to scan (e.g., https://example.com)')
args = parser.parse_args()

url = args.url

security_headers = {
    "X-Frame-Options": "Clickjacking protection",
    "Strict-Transport-Security": "HTTPS enforcement",
    "X-Content-Type-Options": "MIME guessing protection",
    "X-XSS-Protection": " the browser’s built-in protection against reflected XSS attacks" 
}

count = len(security_headers)
implemented = 0

try:
    response = requests.get(url, timeout=5)
    print(f"Status Code: {response.status_code}")
    headers = response.headers
    #Left out part lists all the headers with their values, which seemed excessive for a quick scan.
    # for header, value in headers.items():
        #print(f"{header}: {value}")
    #print()
    for header_name, description in security_headers.items():    
        if header_name in headers:
            print(f"{Fore.GREEN}✓ {description}")
            implemented += 1
        else: 
            print(f"{Fore.RED}✗ {description}")
    print(f"{implemented} out of {count} recommended security headers have been detected")
except requests.exceptions.RequestException as e:
    raise SystemExit(f"{Fore.RED}{e}")