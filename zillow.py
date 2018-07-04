#http://www.zillow.com/webservice/GetSearchResults.htm?zws-id='+ZWSID+'&address=carnegie%20hill&citystatezip=10128
import requests
import xmltodict
import xml.etree.ElementTree as ET
import xmljson
import json


with open('zwsid','r') as f:
    ZWSID = f.readline().strip()

Z_address = 'http://www.zillow.com/webservice/'

addr = 'carnegie%20hill'

zipcode = '10128'

r1 = requests.get(Z_address + 'GetDeepSearchResults.htm?zws-id=' +ZWSID+ '&address=' + addr + '&citystatezip=' + zipc)
root = ET.fromstring(r1.text)
#js = json.dumps(xmljson.abdera.data(root[2][0]))
print json.dumps(xmljson.abdera.data(root[2][0]), indent=4, sort_keys=True)
