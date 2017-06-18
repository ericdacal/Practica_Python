import argparse as AP
import xml.etree.ElementTree as ET
import urllib.request as UL
from ast import literal_eval
from math import sin,cos,sqrt,asin,pi


class Out:
    'classe que conte sortida del programa dividida'
    def __init__(self,llarga, curta, content_before, content_after):
        self.llarga = llarga
        self.curta = curta
        self.content_before = content_before
        self.content_after = content_after
    def mostrarOut(self):
        final = ""
        if len(self.llarga) == 1:
            final = self.content_before[0] + self.llarga[0] +  self.content_after[0]
        else:
            i = 0
            while i < len(self.llarga):
                #print(self.content_before[i] + self.curta[i] + self.content_after[i])
                final = final + self.content_before[i] + self.curta[i] +  self.content_after[i]
                i = i + 1
        return final
    
    def sumar_sortida(self,out):
        i = 0
        while i < len(out.llarga):
            self.llarga.append(out.llarga[i])
            self.curta.append(out.curta[i])
            self.content_before.append(out.content_before[i])
            self.content_after.append(out.content_after[i])
            i = i + 1


def process_keys(keys, container):
    out = Out([],[],[],[])
    inter_points = select_intereset_point_lan(parser.parse_args().lan)
    bicing = bicing_stations()   
    html = ""
    if container == "list":
        if isinstance(keys[0],list): 
            out.sumar_sortida(process_keys(keys[0],"list"))
        elif isinstance(keys[0],tuple): 
            out.sumar_sortida(process_keys(keys[0],"tuple"))
        elif isinstance(keys[0],dict):
            out.sumar_sortida(process_keys(keys[0],"dict"))
        else:
            out.sumar_sortida(process_keys(keys[0], "string"))
        del keys[0]
        if len(keys) == 0: return out
        out.sumar_sortida(process_keys(keys,"list"))
        return out

    elif container == "tuple":
        if isinstance(keys[0],list): 
            out.sumar_sortida(process_keys(keys[0],"list"))
        elif isinstance(keys[0],tuple): 
            out.sumar_sortida(process_keys(keys[0],"tuple"))
        elif isinstance(keys[0],dict):
            out.sumar_sortida(process_keys(keys[0],"dict"))
        else:
            out.sumar_sortida(process_keys(keys[0], "string"))
        del keys[0]
        if len(keys) == 0: return out
        out.sumar_sortida(process_keys(keys,"tuple"))
        return out
    elif container == "dict":
        for row in inter_points.iter('row'):
            entra = False
            stations = []
            htmlrow = """
            <tr>
                """
            i = 0
            dic_values = list(keys.values())
            dic_keys = list(keys.keys())
            while(i < len(dic_values)):
                if dic_keys[i] == 'location':
                    if (row.find('addresses').find('item').find('address').text.find(dic_values[i].capitalize()) > -1 or row.find('addresses').find('item').find('address').text.find(dic_values[i]) > - 1): entra  = True
                    elif (row.find('addresses').find('item').find('district') != None): 
                        if row.find('addresses').find('item').find('district').text.find(dic_values[i].capitalize()) > -1 or row.find('addresses').find('item').find('district').text.find(dic_values[i]) > - 1: entra = True
                    elif (row.find('addresses').find('item').find('barri') != None): 
                        if(row.find('addresses').find('item').find('barri').text.find(dic_values[i].capitalize()) > -1 or row.find('addresses').find('item').find('barri').text.find(dic_values[i]) > - 1): entra = True
                else: 
                    if row.find(dic_keys[i]).text.find(dic_values[i].capitalize()) > -1 or row.find(dic_keys[i]).text.find(dic_values[i]) > - 1: entra = True
                    
                if entra:
                    htmlrow = htmlrow + """<td>""" + row.find('name').text + """</td>
                    """
                    htmlrow = htmlrow + """<td>""" + row.find('addresses').find('item').find('address').text + """</td>
                    """
                    out.content_before.append(htmlrow)
                    out.curta.append("""<td>""" + row.find('custom_fields').find('descripcio-curta-pics').text + """</td>""")
                    out.llarga.append("""<td>""" + row.find('content').text + """</td>""")
                    for station in bicing.iter('station'):
                            long1 = row.find('addresses').find('item').find('gmapy').text
                            lat1 = row.find('addresses').find('item').find('gmapx').text
                            long2 = station.find('long').text
                            lat2 = station.find('lat').text
                            d = Haversine_distance(float(long1),float(lat1),float(long2),float(lat2))
                            if d <= 500 and len(stations) <= 5: stations.append(station.find('street').text)
                    htmlrow = """
                    <td><table>"""
                    #station.sort()
                    for station in stations:
                        htmlrow = htmlrow + """<tr><td>"""+ station + """</td></tr>
                        """
                    html = htmlrow  + """
                    </table></td>"""
                    out.content_after.append(html)
                i = i + 1
        return out

    else:
        for row in inter_points.iter('row'):
            stations = []
            htmlrow = """
            <tr>
                """
            if row.find('name').text.find(keys.capitalize()) > -1:
                htmlrow = htmlrow + """<td>""" + row.find('name').text + """</td>
                """
                htmlrow = htmlrow + """<td>""" + row.find('addresses').find('item').find('address').text + """</td>
                """
                out.content_before.append(htmlrow)
                out.curta.append("""<td>""" + row.find('custom_fields').find('descripcio-curta-pics').text + """</td>""")
                out.llarga.append("""<td>""" + row.find('content').text + """</td>""")
                for station in bicing.iter('station'):
                        long1 = row.find('addresses').find('item').find('gmapy').text
                        lat1 = row.find('addresses').find('item').find('gmapx').text
                        long2 = station.find('long').text
                        lat2 = station.find('lat').text
                        d = Haversine_distance(float(long1),float(lat1),float(long2),float(lat2))
                        if d <= 500 and len(stations) <= 5: stations.append(station.find('street').text)
                htmlrow = """
                <td><table>"""
                #station.sort()
                for station in stations:
                    htmlrow = htmlrow + """<tr><td>"""+ station + """</td></tr>
                    """
                html = htmlrow  + """
                </table></td>"""
                out.content_after.append(html)
        return out


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
        background-color: #ffffff;
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
        
keys = literal_eval(keys)
if isinstance(keys,list): container = "list"
elif isinstance(keys,tuple): container = "tuple"
elif isinstance(keys,dict): container = "dict"
else: container = "string"
out = process_keys(keys, container)
thtml = thtml + out.mostrarOut()  
thtml = thtml + """
</tr>
</table>
</body>      
</html>"""
f.write(thtml)
f.close()



