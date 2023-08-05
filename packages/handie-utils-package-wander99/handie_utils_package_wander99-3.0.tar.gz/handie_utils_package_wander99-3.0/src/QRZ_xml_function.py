# © 2022 George Fenn
# V2 Changed to raise a RuntimeError Exception when errors like
# call sign not there occur.

import xml.etree.ElementTree as ET
import xmltodict
import requests
import dialogs
from arctic_key import arctic_key

def status_check(code):
	if code==200:
		pass
	else:
		print(f'Status code returned: {code}')
			
def QRZ_lookup(call_sign):
			
	ak=arctic_key()
	ak.get_key()

# Disable the InsecureRequestWarning with the following statement
	requests.packages.urllib3.disable_warnings()

	qrz=requests.get(f'https://xmldata.qrz.com/xml/?username=%s;password=%s'% (ak.key_dict['Userid'], ak.key_dict['Password']),verify=False)
	status_check(qrz.status_code)

	xml_root_dict=xmltodict.parse(qrz.text)
	if 'Session' in xml_root_dict['QRZDatabase']:
	  if 'Error' in xml_root_dict['QRZDatabase']['Session']:
	    raise RuntimeError(xml_root_dict['QRZDatabase']['Session']['Error'])
          
	key=xml_root_dict['QRZDatabase']['Session']['Key']

	c_sign=requests.get(f'https://xmldata.qrz.com/xml/current/?s=%s;callsign=%s'% (key,call_sign),verify=False)
	status_check(c_sign.status_code)
	
	xml_dict=xmltodict.parse(c_sign.text)
	if 'Session' in xml_dict['QRZDatabase']:
	  if 'Error' in xml_dict['QRZDatabase']['Session']:
	    raise RuntimeError(xml_dict['QRZDatabase']['Session']['Error'])
      
	lat=xml_dict['QRZDatabase']['Callsign']['lat']
	lon=xml_dict['QRZDatabase']['Callsign']['lon']

	return(float(lat),float(lon))
	
if __name__ == '__main__':
	
	a_sign=input('Enter Call sign to look up : ')
	try:
	  lat,lon=QRZ_lookup(a_sign)
	  print(f'Latitude: {lat} Longitude: {lon}')
	except RuntimeError as exc_args:
	  print(str(exc_args))
