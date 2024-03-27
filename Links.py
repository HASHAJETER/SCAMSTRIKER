
from phishtank import PhishTank
import os
import ssl
import email
import re
import base64
from urllib.parse import urlparse

api_key = "CLEAPI"


def extract_links_from_eml(eml_file):
    links = []
    with open(eml_file, 'r', encoding='utf-8') as file:
        msg = email.message_from_file(file)
        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                links.extend(re.findall(r'href=["\'](.*?)["\']', html_content))
    return [link for link in links if urlparse(link).scheme and urlparse(link).netloc]


def check_phishtank(domain_name, api_key):
    pt = PhishTank(api_key)
    response = pt.check(domain_name)
    if response.in_database:
        print("Incorrecte")
    else:
        print("Correcte")


links = extract_links_from_eml("mail.eml")
print("\n\n---- Links founds ----\n")
for link in links:
    print(link)
    check_phishtank(link, api_key)


