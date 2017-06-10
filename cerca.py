import argparse as AP
import xml.etree.ElementTree as ET
import urllib.request as UL


def process_keys(keys):
  keys = keys.split(",")
  index = keys[0].find("'[")
  keys[0] = keys[0][index+2:]
  index = keys[1].find("]'")
  keys[1] = keys[1][:index]
  return keys


def select_intereset_point_lan (lan):
  if lan == 'cat': url ='http://www.bcn.cat/tercerlloc/pits_opendata.xml'
  elif lan == 'es': url = 'http://www.bcn.cat/tercerlloc/pits_opendata_es.xml'
  elif lan == 'en': url = 'http://www.bcn.cat/tercerlloc/pits_opendata_en.xml'
  else : url ='http://www.bcn.cat/tercerlloc/pits_opendata_fr.xml'
  fp = UL.urlopen(url)
  doc = ET.parse(fp)
  fp.close()
  return (doc.getroot())











parser = AP.ArgumentParser(description='Process input language and input key')
parser.add_argument('--lan', dest='lan', default='cat',
                    help='language to search')
parser.add_argument('--key', dest='key', 
                    help='key to search')
 
keys = parser.parse_args().key
keys = process_keys(keys)
inter_points = select_intereset_point_lan(parser.parse_args().lan)

print(inter_points[0][0].text)
