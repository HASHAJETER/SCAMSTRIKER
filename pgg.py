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

#print(json.dumps(parsed_eml["header"], default=json_serial, indent=2))

for p in parsed_eml["header"]:
  if p in ["subject", "from", "to", "received_domain", "received_ip" ]:
    print(p, "->", parsed_eml['header'][p])

print( "\n\n--- Attachement ---" )
for i in parsed_eml["attachment"]:
  print( "\n\tfilename ->", i["filename"] )

  for s in i["hash"].keys():
    print( s, "->", i["hash"][s] )
