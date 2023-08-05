# © 2022 George Fenn
# V2 Cleaned up the interface and put in code to check for nothing 
# entered from the form
# V3 Added the hidden function that is when coord is DD and latitude
# is Here, then latitude 1 and longitude 1 will be filled in with
# the current location as determined by the location package.
# Added the hidden function that is when coord is DD and latitude
# is Call and longitude is a call sign, then latitude 1 and 
# longitude 1 will be filled in with the coordinates for the home
# location of that operator.
# Kilometers flag is now used to display kilometers instead of miles.
# V4 When used with POTA_park_lookup V5 and SOTA_summit_lookup V3,
# there is a new hidden function added. When coord is DD and latitude
# is Clip, then latitude 2 and longitude 2 will be filled in with the
# latitude and longitude posted to the clipboard on the last park or
# summit lookup.
# V5 Added a check so that Here &/or Clip only work when using 
# degrees decimal input.
# Removed End Section text from display.
# Made directions uppercase so dms_convert works correctly.
# Added input verification for both DD and DMS inputs.
# V6 Changed to use a pyui user interface to 
#     1) get the decimal degrees and have buttons to indicate if
#       the dd is latitude or longitude
#     2) get the degs mins secs direc and have buttons to indicate if
#      that is latitude or longitude
# V7 Changed to allow DD input with a comma and to convert that character
# to a period. Reworked the input verification on latitude and longitude 2
# to clean that up. 
# Changed to handle the RuntimeError Exception that can be raised by 
# lat_long_distance V2 when any of the longitudes or the latitudes are
# out of range.
# V8 Changed DMS input to change comma's in input fields to a period.
# V9 Using imported routines from dms_convert_frontend, added checks to make 
# sure the entered directions are correct for latitude and longitude.
# Changed to handle the RuntimeError Exception that occurs on errors during
# call sign lookup.
# V10 Added a method call to the lat1_inp TextField to give the keyboard focus 
# in that field for input.

from lat_long_distance import distance
from dms_convert import dms2dd
from QRZ_xml_function import QRZ_lookup
from dms_convert_frontend import lon_direction_check
from dms_convert_frontend import lat_direction_check

import ui
import location
import dialogs
import clipboard

def distance_results(inputs,rdis):
	if inputs['is_kms'] is False:
		units='Miles'
	else:
		units='Kilometers'
	
	if inputs['coord']=='DD':
	  i = dialogs.alert(f'Distance Between\n{inputs["lat1"]}, {inputs["lon1"]}\nand\n{inputs["lat2"]}, {inputs["lon2"]}\n is {rdis} {units}','','OK',hide_cancel_button=True)
	else:
	  i = dialogs.alert(f'Distance Between\n{inputs["lat1"][:-2]} {inputs["lat1"][-1].upper()},\n {inputs["lon1"][:-2]} {inputs["lon1"][-1].upper()}\nand\n{inputs["lat2"][:-2]} {inputs["lat2"][-1].upper()},\n {inputs["lon2"][:-2]} {inputs["lon2"][-1].upper()}\n is {rdis} {units}','','OK',hide_cancel_button=True)
	
def main():
  
  def lat_lon_dms_button_pressed(sender):
    label = sender.superview['label1']
    label.text= '\n\tDegrees Minutes Seconds\n\t\t\t\tEntry'
    inputs['coord']='DMS'
    
  def lat_lon_dd_button_pressed(sender):
    label = sender.superview['label1']
    label.text= '\tDecimal Degrees Options\n\t  Here in Latitude 1 and \n  Clip or Call in Latitude 2 and \nCall sign in Longitude 2 w/ Call'
    inputs['coord']='DD'
    
  def lat_lon_km_switch(sender):
    switch = sender.superview['switch1']
    inputs['is_kms']=switch.value
    
  def lat_lon_done_button_pressed(sender):
    label = sender.superview['lat1_inp']
    inputs['lat1']=label.text
    if label.text == '':
      pass
    else:
      label = sender.superview['lon1_inp']
      inputs['lon1']=label.text
      label = sender.superview['lat2_inp']
      inputs['lat2']=label.text
      label = sender.superview['lon2_inp']
      inputs['lon2']=label.text
    v.close()
    
  def lat_lon_view_present():
    
    v_focus=v['lat1_inp']
    v_focus.begin_editing()
    if min(ui.get_screen_size()) >= 768:
      # iPad
      v.frame = (0, 0, 360, 400)
      v.present('sheet')
      v.wait_modal()
    else:
      # iPhone
      v.present(orientations=['portrait'])
      v.wait_modal()
      
  def field_fill(field,value):
    label=v[field]
    label.text=value
    
  def field_get(field,value):
    label=v[field]
    value=label.text
      
  v = ui.load_view('lat_lon_ui')
  
  inputs={}
  inputs['coord']='DMS'
  
  inputs['is_kms']=False
  while True:
    inputs['lat1']=inputs['lon1']=inputs['lat2']=inputs['lon2']=''
    field_fill('lat1_inp','')
    field_fill('lon1_inp','')
    field_fill('lat2_inp','')
    field_fill('lon2_inp','')
    lat_lon_view_present()
    
    if inputs['lat1'] == '':
      break
    elif inputs['coord'] == 'DMS':
      if inputs['lat1']=='Here' or inputs['lat2']=='Clip':
        i=dialogs.alert('Here and Clip only work with DD!','','OK',hide_cancel_button=True)
        continue
      try:
        inputs['lat1']=inputs['lat1'].replace(',','.')
        degs,minutes,seconds,direc=inputs['lat1'].split()
      except:
        i=dialogs.alert('Latitude 1 is not Degrees Minutes Seconds Direction!','','OK',hide_cancel_button=True)
        continue
      if not(lat_direction_check(direc.upper())):
        i = dialogs.alert('Latitude 1 must be either N or S','','OK',hide_cancel_button=True)
        continue
      lat11=dms2dd(degs,minutes,seconds,direc.upper())
      try:
        inputs['lon1']=inputs['lon1'].replace(',','.')
        degs,minutes,seconds,direc=inputs['lon1'].split()
      except:
        i=dialogs.alert('Longitude 1 is not Degrees Minutes Seconds Direction!','','OK',hide_cancel_button=True)
        continue
      if not(lon_direction_check(direc.upper())):
        i = dialogs.alert('Longitude 1 must be either E or W','','OK',hide_cancel_button=True)
        continue
      lon12=dms2dd(degs,minutes,seconds,direc.upper())
      try:
        inputs['lat2']=inputs['lat2'].replace(',','.')
        degs,minutes,seconds,direc=inputs['lat2'].split()
      except:
        i=dialogs.alert('Latitude 2 is not Degrees Minutes Seconds Direction!','','OK',hide_cancel_button=True)
        continue
      if not(lat_direction_check(direc.upper())):
        i = dialogs.alert('Latitude 2 must be either N or S','','OK',hide_cancel_button=True)
        continue
      lat21=dms2dd(degs,minutes,seconds,direc.upper())
      try:
        inputs['lon2']=inputs['lon2'].replace(',','.')
        degs,minutes,seconds,direc=inputs['lon2'].split()
      except:
        i=dialogs.alert('Longitude 2 is not Degrees Minutes Seconds Direction!','','OK',hide_cancel_button=True)
        continue
      if not(lon_direction_check(direc.upper())):
        i = dialogs.alert('Longitude 2 must be either E or W','','OK',hide_cancel_button=True)
        continue
      lon22=dms2dd(degs,minutes,seconds,direc.upper())
      if inputs['is_kms'] is False:
        r=3959
      else:
        r=6371
      try:
        rdis=round(distance(str(lat11),str(lat21),str(lon12),str(lon22),r),3)
        distance_results(inputs,rdis)
      except RuntimeError as exc_args:
        i=dialogs.alert(str(exc_args),'','OK',hide_cancel_button=True)
        continue
    elif inputs['coord'] == 'DD':
      if inputs['lat1']=='Here':
        here=location.get_location()
        inputs['lat1']=round(here['latitude'],5)
        inputs['lon1']=round(here['longitude'],5)
      else:
        try:
          degs,minutes,seconds,direc=inputs['lat1'].split()
          i=dialogs.alert('Latitude 1 is not Decimal Degrees!','','OK',hide_cancel_button=True)
          continue
        except:
          inputs['lat1']=inputs['lat1'].replace(',','.')
        try:
          degs,minutes,seconds,direc=inputs['lon1'].split()
          i=dialogs.alert('Longitude 1 is not Decimal Degrees!','','OK',hide_cancel_button=True)
          continue
        except:
          inputs['lon1']=inputs['lon1'].replace(',','.')
      if inputs['lat2']=='':
        dialogs.alert('Latitude 2 has no entered input!','','OK',hide_cancel_button=True)
        continue
      elif inputs['lat2']=='Call':
        if inputs['lon2']=='':
          dialogs.alert('When using Call put the call sign in Second longitude!','','OK',hide_cancel_button=True)
          continue
        else:
          try:
            inputs['lat2'],inputs['lon2']=QRZ_lookup(inputs['lon2'])
          except RuntimeError as exc_args:
            i=dialogs.alert(str(exc_args),'','OK',hide_cancel_button=True)
            continue        
      elif inputs['lat2']=='Clip':
        clipit=clipboard.get()
        if clipit == '':
          i=dialogs.alert('Clipboard is empty!','','OK',hide_cancel_button=True)
          continue
        else:
          inputs['lat2'],inputs['lon2']=clipit.split(',')
      else:
        if inputs['lon2']=='':
          dialogs.alert('Longitude 2 has no entered input!','','OK',hide_cancel_button=True)
          continue
        try:
          degs,minutes,seconds,direc=inputs['lat2'].split()
          i=dialogs.alert('Latitude 2 is not Decimal Degrees!','','OK',hide_cancel_button=True)
          continue
        except:
          inputs['lat2']=inputs['lat2'].replace(',','.')
        try:
          degs,minutes,seconds,direc=inputs['lon2'].split()
          i=dialogs.alert('Longitude 2 is not Decimal Degrees!','','OK',hide_cancel_button=True)
          continue
        except:
          inputs['lon2']=inputs['lon2'].replace(',','.')
          
      if inputs['is_kms'] is False:
        r=3959
      else:
        r=6371

      try:
        rdis=round(distance(str(inputs['lat1']),str(inputs['lat2']),str(inputs['lon1']),str(inputs['lon2']),r),3)
        distance_results(inputs,rdis)
      except ValueError:
        i=dialogs.alert('Input is not formatted correctly!','','OK',hide_cancel_button=True)
        continue
      except RuntimeError as exc_args:
        i=dialogs.alert(str(exc_args),'','OK',hide_cancel_button=True)
        continue        
    else:
      break
	
if __name__ == '__main__':

	main()
