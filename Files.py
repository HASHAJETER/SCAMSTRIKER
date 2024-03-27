import datetime
import eml_parser
import json
import requests
from colorama import init, Fore

init(autoreset=True)
API_KEY = "CLEAPI"

def json_serial(obj):
  if isinstance(obj, datetime.datetime):
      serial = obj.isoformat()
      return serial

with open('mail3.eml', 'rb') as fhdl:
  raw_email = fhdl.read()

ep = eml_parser.EmlParser()
parsed_eml = ep.decode_email_bytes(raw_email)
#print(json.dumps(parsed_eml["header"], default=json_serial, indent=2))


def get_header():
  for p in parsed_eml["header"]:
    if p in ["subject", "from", "to", "received_domain", "received_ip" ]:
      print(p, "->", parsed_eml['header'][p])

def verif_atachement():
  print( "\n\n--- Attachement ---" )
  for i in parsed_eml["attachment"]:
    print( "\nfilename ->", i["filename"] )
    
    print("---- Verify hash ----")
    for s in i["hash"].keys():
      #hash.append(i["hash"][s])

      url = f'https://api.metadefender.com/v4/hash/{i["hash"][s]}'
      headers = {
        "apikey" : API_KEY
      }
      response = requests.get(url, headers=headers)

      if response.status_code == 200:
        data = response.json()
        if 'scan_results_i' in data and data['scan_results_i']['scan_all_result_a'] == 'clean':
          print(f" {s} [ {Fore.GREEN}Clean{Fore.RESET} ]")
        else:
          print(f" {s} [ {Fore.RED}Detected as malicious{Fore.RESET} ]")
      else:
          print(f" {s} [ {Fore.BLUE}Not found, unknow{Fore.RESET} ]")