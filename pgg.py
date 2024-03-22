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

print(eml_parser)

parsed_eml = ep.decode_email_bytes(raw_email)

print(json.dumps(parsed_eml, default=json_serial, indent=2))