# © 2022 George Fenn
# V2 This version changed the Call sign display from a dialogs.alert
# display to instead use a pyui UI file. This allowed the addition 
# of a map button to the display, using Google maps in Safari, to
# display the home QTH of the operator that was looked up.
# The latitude and longitude to use will be determined using
# location.geocode if all parts of the address are there.
# This is more accurate; for instance with KI4ASK the
# derived latitude and longitude is returned, since they aren't 
# included in the XML data, which puts the location on the street 
# in front of the house. Using geocode, it puts the location right 
# at the house. 
# V3 Added a check for an exception that is the result of an invalid
# userid or password for XML access.
# V4 Added a check for exceptions raised by the requests module
# that are inherited from requests.exceptions.RequestException.
# Added a check for internet before going off to render a map using
# the browser. This is done even if there was a successfull call sign
# retrieval in case of a dropped connection in the interval time.
# Cleaned up the redundant code that was used in the call to the 
# map_presentation function.
# V5 Added Done button logic to handle the addition of a Done button
# in the output ui. Increased the height of the frame to 550 to 
# accomodate this on an iPad.
# Changed to use the handie common interface to get call sign lookup
# input.
# V6 Changed to check if 'country' is there in the returned data from
# qrz.com. In testing, tried a bogus call sign of kkk but it redirected 
# to IT9ICR. The qrz page for this even says it is an incomplete record 
# with no 'country'.
# V7 Changed to check if 'name' is there in the returned data from
# qrz.com. Found when doing a lookup for V85A, who doesn't have a 
# name, but only a nickname and fname. Also started using name_fmt for 
# a more consistent output if it is available.

import xml.etree.ElementTree as ET
import xmltodict
import requests
from arctic_key import arctic_key
from handie_ci import *
import ui
import clipboard
import location
import webbrowser
import sys
import http.client as httplib

map_requested=0

def have_internet():
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()

def status_check(code):
	if code==200:
		pass
	else:
		print(f'Status code returned: {code}')
		
def main():
  global map_requested
  
  def done_button_pressed(sender):
    vs.close()
  
  def qrz_view_present(vs):
    global map_requested
    
    if min(ui.get_screen_size()) >= 768:
      # iPad
      vs.frame = (0, 0, 360, 550)
      vs.present('sheet')
      vs.wait_modal()
    else:
      # iPhone
      vs.present(orientations=['portrait'])
      vs.wait_modal()

  def field_fill(field,value):
    label=vs[field]
    label.text=value
    
  def field_get(field,value):
    label=vs[field]
    value=label.text
    
  def map_button_pressed(sender):
    global map_requested
    
    map_requested=1
    vs.close()
    
  def map_presentation(lat,lon,addr_dict):
    if len(addr_dict)==4:
      results=location.geocode(addr_dict)
      if results:
        lat=results[0]['latitude']
        lon=results[0]['longitude']
    if have_internet():
      webbrowser.open(f'safari-https://maps.google.com/?q={lat},{lon}')
    else:
      i=dialogs.alert('No Internet Connection - Connect to a network!','','OK',hide_cancel_button=True)
      sys.exit()
    
  vs = ui.load_view('QRZ_output_ui')
  
  ak=arctic_key()
  ak.get_key()
  
  param_list=[]
  param_list2=[]
  addr_dict={}
  state=addr1=addr2=country=''

# Disable the InsecureRequestWarning with the following statement

  requests.packages.urllib3.disable_warnings()
  
  try:
    qrz=requests.get(f'https://xmldata.qrz.com/xml/?username=%s;password=%s'% (ak.key_dict['Userid'], ak.key_dict['Password']),verify=False)
  except requests.exceptions.ConnectionError:
    i=dialogs.alert('No Internet Connection - Connect to a network!','','OK',hide_cancel_button=True)
    sys.exit()
  except requests.exceptions.Timeout:
    i=dialogs.alert('Internet Connection Timed Out - Try Again!','','OK',hide_cancel_button=True)
    sys.exit()
  status_check(qrz.status_code)

  xml_root_dict=xmltodict.parse(qrz.text)
  try:
    key=xml_root_dict['QRZDatabase']['Session']['Key']
  except:
    i=dialogs.alert('QRZ Database Access Failed - Check Userid/Password!','','OK',hide_cancel_button=True)
    sys.exit()
  
  call_sign_dialog=1
  inp_hdr='Enter Call sign to look up'
  vi=ci_init(inp_hdr)
  
  while True:
    
    if call_sign_dialog:
      vi.ci_text_input=''
      ci_view_present()
    else:
      call_sign_dialog=1
    
    if vi.ci_text_input == '':
	    break
    elif vi.ci_done_button_pressed == True:
      c_sign=requests.get(f'https://xmldata.qrz.com/xml/current/?s=%s;callsign=%s'% (key,vi.ci_text_input),verify=False)
      status_check(c_sign.status_code)
      
      xml_dict=xmltodict.parse(c_sign.text)
      if 'Session' in xml_dict['QRZDatabase']:
        if 'Error' in xml_dict['QRZDatabase']['Session']:
          i=dialogs.alert(xml_dict['QRZDatabase']['Session']['Error'],'','OK',hide_cancel_button=True)
          continue
          
      call=xml_dict['QRZDatabase']['Callsign']['call']
      if 'fname' in xml_dict['QRZDatabase']['Callsign']:
        fname=xml_dict['QRZDatabase']['Callsign']['fname']+' '
      else:
        fname=''
      if 'name' in xml_dict['QRZDatabase']['Callsign']:
        name=xml_dict['QRZDatabase']['Callsign']['name']
      else:
        name=''
      if 'name_fmt' in xml_dict['QRZDatabase']['Callsign']:
        name_fmt=xml_dict['QRZDatabase']['Callsign']['name_fmt']
      else:
        name_fmt=''
      if 'addr1' in xml_dict['QRZDatabase']['Callsign']:
        addr1=xml_dict['QRZDatabase']['Callsign']['addr1']
        addr_dict['Street']=addr1
      else:
        addr1=''
      if 'addr2' in xml_dict['QRZDatabase']['Callsign']:
        addr2=xml_dict['QRZDatabase']['Callsign']['addr2']
        addr_dict['City']=addr2
      else:
        addr2=''
      if 'state' in xml_dict['QRZDatabase']['Callsign']:
        state=xml_dict['QRZDatabase']['Callsign']['state']
        addr_dict['State']=state
        comma=','
      else:
        comma=state=''
      if 'zip' in xml_dict['QRZDatabase']['Callsign']:
        qthzip=xml_dict['QRZDatabase']['Callsign']['zip']
      else:
        qthzip=''
      
      grid=xml_dict['QRZDatabase']['Callsign']['grid']
      if 'country' in xml_dict['QRZDatabase']['Callsign']:
        country=xml_dict['QRZDatabase']['Callsign']['country']
      else:
        country=''
      
      lat=xml_dict['QRZDatabase']['Callsign']['lat']
      lon=xml_dict['QRZDatabase']['Callsign']['lon']
      
      if 'class' in xml_dict['QRZDatabase']['Callsign']:
        lic_class=xml_dict['QRZDatabase']['Callsign']['class']
      else:
        lic_class='None'
      if country=='United States':
        addr_dict['Country']='USA'
        if lic_class=='T':
          pr_class='Technician'
        elif lic_class=='G':
          pr_class='General'
        elif lic_class=='N':
          pr_class='Novice'
        elif lic_class=='A':
          pr_class='Advanced'
        elif lic_class=='E':
          pr_class='Amateur Extra'
        elif lic_class=='C':
          pr_class='Club'
        else:
          pr_class=lic_class
      else:
        addr_dict['Country']=country
        pr_class=''
      
      try:
        email=xml_dict['QRZDatabase']['Callsign']['email']
      except KeyError:
        email=' '
        
      lat_long=str(lat+','+lon)
      clipboard.set(lat_long)
      
      field_fill('label2',call)
      field_fill('label4',pr_class)
      if name_fmt=='':
        field_fill('label6',fname+name)
      else:
        field_fill('label6',name_fmt)
      field_fill('label8',addr1)
      field_fill('label9',addr2+comma+' '+state+'   '+qthzip)
      field_fill('label11',country)
      field_fill('label13',grid)
      field_fill('label15',lat)
      field_fill('label17',lon)
      field_fill('label19',email)
      map_requested=0
      qrz_view_present(vs)
      if map_requested == 1:
        map_presentation(lat,lon,addr_dict)
        map_requested=0
        vs = ui.load_view('QRZ_output_ui')
        call_sign_dialog=0

if __name__ == '__main__':
  main()
