# flag wifi names that should be ignored, because they come from cell phones

import sys
import xmltodict
import os
import json
from optparse import OptionParser

def read_xml(opts):
  #Setting up vendor directory
  if not os.path.isfile(opts.xml_file):
    sys.stderr.write("XML file not found at %s\n" % opts.xml_file)
    sys.exit(-1)
  xml_dict = {}
  with open(opts.xml_file, 'r') as f:
    data=f.read()
  return data

def parse_xml(xml_data, opts):
  if opts.verbose:
    print(json.dumps(xmltodict.parse(xml_data), indent=4, sort_keys=True))
  return json.dumps(xmltodict.parse(xml_data), indent=4, sort_keys=True)

def write_json(json_data, output_file):
  with open(output_file, 'w') as f:
    f.write(json_data)

def main():
  op = OptionParser()
  op.add_option("-v", "--verbose", action="store_true", help="verbose", default=False)
  op.add_option("-f", "--xmlfile", dest="xml_file", help="XML file to convert to json", default=None)
  (opts, args) = op.parse_args()
  if not opts.xml_file:   # if filename is not given
    op.error('XML Filename not given')
  data = read_xml(opts)
  json_data = parse_xml(xml_data=data, opts=opts)
  if opts.xml_file.endswith('.xml'):
    json_file = opts.xml_file[:-4] + ".json"
  else:
    json_file = opts.xml_file + ".json"
  write_json(json_data=json_data, output_file=json_file)

if __name__ == '__main__':
  main()
