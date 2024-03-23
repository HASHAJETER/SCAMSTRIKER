import datetime
import json
import eml_parser

def json_serial(obj):
  if isinstance(obj, datetime.datetime):
      serial = obj.isoformat()
      return serial

with open('mail.eml', 'rb') as fhdl:
  raw_email = fhdl.read()

ep = eml_parser.EmlParser()

parsed_eml = ep.decode_email_bytes(raw_email)

hash = []
#print(json.dumps(parsed_eml["header"], default=json_serial, indent=2))

for p in parsed_eml["header"]:
  if p in ["subject", "from", "to", "received_domain", "received_ip" ]:
    print(p, "->", parsed_eml['header'][p])

print( "\n\n--- Attachement ---" )
for i in parsed_eml["attachment"]:
  print( "\n\tfilename ->", i["filename"] )

  for s in i["hash"].keys():
    print( s, "->", i["hash"][s] )
    hash.append(i["hash"][s])



print("\n\n\n------- VERIFIE HASH -------")
API_KEY = ''

import requests

for h in hash:
  print("\n----------------------------")
  url = f'https://api.metadefender.com/v4/hash/{h}'
  headers = {
    "apikey" : API_KEY
  }
  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    data = response.json()
    if 'scan_results_i' in data and data['scan_results_i']['scan_all_result_a'] == 'clean':
      print(f"Metadefender: Hash {hash} is clean.")
    else:
      print(f"Metadefender: Hash {hash} is detected as malicious.")
  else:
      print("Error querying Metadefender API:", response.status_code)
