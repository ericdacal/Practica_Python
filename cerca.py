import argparse as AP
import xml.etree.ElementTree as ET
import urllib.request as UL
from math import sin,cos,sqrt,asin,pi


def process_keys(keys):
  keys = keys.split(",")
  keys[0] = keys[0][2:]
  size = len(keys) - 1
  sizek = len(keys[size]) - 1
  keys[size] = keys[size][:sizek - 2]
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

def bicing_stations ():
  url = 'http://wservice.viabicing.cat/v1/getstations.php?v=1'
  fp = UL.urlopen(url)
  doc = ET.parse(fp)
  fp.close()
  return (doc.getroot())

def Haversine_distance(long1,lat1,long2,lat2):
    r = 6371000 #median radio terrestrial
    c = pi/180 #constant to transform grades on radians
    return 2*r*asin(sqrt(sin(c*(lat2-lat1)/2)**2 + cos(c*lat1)*cos(c*lat2)*sin(c*(long2-long1)/2)**2))
    
    
    
parser = AP.ArgumentParser(description='Process input language and input key')
parser.add_argument('--lan', dest='lan', default='cat',help='language to search')
parser.add_argument('--key', dest='key', help='key to search')

keys = parser.parse_args().key
keys = process_keys(keys)
inter_points = select_intereset_point_lan(parser.parse_args().lan)
bicing = bicing_stations()


f = open('table.html','w')

thtml = """ 
    <!DOCTYPE html>
    <html>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <head>
    <style>
    table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
    }

    td, th {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }

    tr:nth-child(even) {
        background-color: #dddddd;
    }
    </style>
    </head>
    <body>

    <table>"""
    
    
if parser.parse_args().lan == 'fr': 
    thtml = thtml + """
        <tr>
            <th>Nom</th>
            <th>Adresse</th>
            <th>Description</th>
            <th>Stations de Bicing à proximité</th>
        </tr>
        """
   
elif parser.parse_args().lan == 'es':
    thtml = thtml + """
        <tr>
            <th>Nombre</th>
            <th>Dirección</th>
            <th>Descripción</th>
            <th>Estaciones de Bicing Cercanas</th>
        </tr>
        """
elif parser.parse_args().lan == 'en':
    thtml = thtml + """
        <tr>
            <th>Name</th>
            <th>Address</th>
            <th>Description</th>
            <th>Bicing Stations Nearby</th>
        </tr>
        """
else:
     thtml = thtml + """
        <tr>
            <th>Nom</th>
            <th>Adreça</th>
            <th>Descripció</th>
            <th>Estacions de Bicing Properes</th>
        </tr>
        """
for row in inter_points.iter('row'):
    stations = []
    for key in keys:
        htmlrow = """
        <tr>
            """  
        if row.find('name').text.capitalize().find(key) > -1: 
            htmlrow = htmlrow + """<td>""" + row.find('name').text + """</td>
            """
            htmlrow = htmlrow + """<td>""" + row.find('addresses').find('item').find('address').text + """</td>
            """
            if len(keys) == 1: 
                htmlrow = htmlrow + """<td>""" + row.find('content').text + """</td>"""
            else: 
                htmlrow = htmlrow + """<td>""" + row.find('custom_fields').find('descripcio-curta-pics').text + """</td>"""
            for station in bicing.iter('station'):
                    long1 = row.find('addresses').find('item').find('gmapy').text
                    lat1 = row.find('addresses').find('item').find('gmapx').text
                    long2 = station.find('long').text
                    lat2 = station.find('lat').text
                    d = Haversine_distance(float(long1),float(lat1),float(long2),float(lat2))
                    if d <= 500 and len(stations) <= 5: stations.append(station.find('street').text)
            htmlrow = htmlrow + """
            <td>"""
            for station in stations:
                htmlrow = htmlrow + station + """ 
                """
            htmlrow = htmlrow  + """
            </td>"""
            thtml = thtml + htmlrow
            
thtml = thtml + """
</tr>
</table>
</body>      
</html>"""
f.write(thtml)
f.close()



