# © 2022 George Fenn
# V1 Initial version to use dialogs for information
# input and results output.
# V2 Done checking doesn't work for ans
# V3 Change to use list_dialog and just pick which format for input.
# V4 Changed to use a pyui user interface to 
#     1) get the decimal degrees and have buttons to indicate if
#       the dd is latitude or longitude
#     2) get the degs mins secs direc and have buttons to indicate if
#      that is latitude or longitude
# V5 Added input verification using try, except
# V6 Changed dialog input location so if there is an error on
# input it will stay in that conversion input ui instead of 
# returning to the main input dialog
# V7 Added an option to convert Degrees Decimal Minutes to
# Degrees Minutes Seconds Direction and Decimal Degrees.
# V8 Changed the dialog header to be consistent with dialog
# options to to have no redundancy in statement of purpose.
# V9 Added range checks for when any of the longitudes or any 
# of the latitudes are out of range. 
# V10 Added option to convert Decimal Degrees to the corresponding
# Gridsquare
# V11 Changed to use a pyui interface for function selection.
# V12 Added checks to make sure the entered directions are correct
# for latitude and longitude. 
# Changed to use the handie common interface to get grid square
# input for conversion.
# V13 Added a method call to the dd_inp, dms_input, and ddm_input 
# TextFields in their respective present module to give the keyboard 
# focus in that field for input. 
# Cleaned up interface when checking for no input indicated by None to
# ''. Also changed the 3 pyui files for coordinates input to have an 
# initial value in the first input field as '' versus ' '.

from handie_ci import *
from dms_convert import dms2dd
from dms_convert import dd2dms
from dms_convert import ddm2dd
from dd2grid import to_grid
import dialogs
import ui

def lon_range_check(lon):
  if (-180<=lon<180):
    return True
  else:
    return False
      
def lat_range_check(lat):
  if (-90<=lat<90):
    return True
  else:
    return False
    
def lon_direction_check(lon):
  if (lon == 'E') or (lon == 'W'):
    return True
  else:
    return False
      
def lat_direction_check(lat):
  if (lat == 'N') or (lat == 'S'):
    return True
  else:
    return False
      
def main():
  
  def dd_lat_button_pressed(sender):
    label = sender.superview['label2']
    label.text= 'Latitude'
    v.dms_coord_input='LA'
    
  def dd_lon_button_pressed(sender):
    label = sender.superview['label2']
    label.text= 'Longitude'
    v.dms_coord_input='LO'
    
  def dd_text_received(sender):
    dms_input = sender.superview['dd_inp']
    v.dms_text_input=dms_input.text
    dms_input.text=''
    
  def dd_done_button_pressed(sender):
    v.close()
  
  def dd_view_present():
    
    v_focus=v['dd_inp']
    v_focus.begin_editing()
    if min(ui.get_screen_size()) >= 768:
      # iPad
      v.frame = (0, 0, 360, 400)
      v.present('sheet')
    else:
      # iPhone
      v.present(orientations=['portrait'])
    v.wait_modal()
      
  def dms_lat_button_pressed(sender):
    label = sender.superview['label2']
    label.text= 'Latitude'
    vs.dms_coord_input='LA'
    
  def dms_lon_button_pressed(sender):
    label = sender.superview['label2']
    label.text= 'Longitude'
    vs.dms_coord_input='LO'
    
  def dms_text_received(sender):
    dms_input = sender.superview['dms_inp']
    vs.dms_text_input=dms_input.text
    dms_input.text=''
    
  def dms_done_button_pressed(sender):
    vs.close()
    
  def dms_view_present():
    
    vs_focus=vs['dms_inp']
    vs_focus.begin_editing()
    if min(ui.get_screen_size()) >= 768:
      # iPad
      vs.frame = (0, 0, 360, 400)
      vs.present('sheet')
    else:
      # iPhone
      vs.present(orientations=['portrait'])
    vs.wait_modal()
      
  def ddm_lat_button_pressed(sender):
    label = sender.superview['label2']
    label.text= 'Latitude'
    vm.dms_coord_input='LA'
    
  def ddm_lon_button_pressed(sender):
    label = sender.superview['label2']
    label.text= 'Longitude'
    vm.dms_coord_input='LO'
      
  def ddm_text_received(sender):
    dms_input = sender.superview['ddm_inp']
    vm.dms_text_input=dms_input.text
    dms_input.text=''
      
  def ddm_done_button_pressed(sender):
    vm.close()

  def ddm_view_present():
    
    vm_focus=vm['ddm_inp']
    vm_focus.begin_editing()
    if min(ui.get_screen_size()) >= 768:
      # iPad
      vm.frame = (0, 0, 360, 400)
      vm.present('sheet')
    else:
      # iPhone
      vm.present(orientations=['portrait'])
    vm.wait_modal()
  
  def dms_button_pressed(sender):
    vo.close()
    vo.choices=dd_dms_field_title_dms
    
  def dd_button_pressed(sender):
    vo.close()
    vo.choices=dd_dms_field_title_dd
    
  def ddm_button_pressed(sender):
    vo.close()
    vo.choices=dd_dms_field_title_ddm
    
  def gs_button_pressed(sender):
    vo.close()
    vo.choices=dd_dms_field_title_to_grid
    
  def convert_done_button_pressed(sender):
    vo.close()
    vo.done_button=True
    
  def convert_view_present():
    
    if min(ui.get_screen_size()) >= 768:
      # iPad
      vo.frame = (0, 0, 360, 400)
      vo.present('sheet')
    else:
      # iPhone
      vo.present(orientations=['portrait'])
    vo.wait_modal()
    
  dialog_hdr='Decimal Degrees to Grid Square'
  
  v = ui.load_view('dms_convert_dd_ui')
  vs= ui.load_view('dms_convert_dms_ui')
  vm= ui.load_view('dms_convert_ddm_ui')
  vo= ui.load_view('dms_convert_ui')
  vo.done_button = ''
  
  v.dms_coord_input=None
  vs.dms_coord_input=None
  vm.dms_coord_input=None
  
  dd_dms_title='Convert Coordinates'  
  dd_dms_field_title_dms='From Degrees Mins Secs  '
  dd_dms_field_title_dd='From Decimal Degrees  '
  dd_dms_field_title_ddm='From Degrees Decimal Mins  '
  dd_dms_field_title_to_grid='To Grid Square  '
  
  while True:
	  vo.choices=''
	  convert_view_present()
	  
	  if vo.choices == '' or vo.done_button == True:
	    break
	  else:
	    direc=' '
	    if vo.choices==dd_dms_field_title_dms:
	      vs.dms_text_input=''
	      dms_view_present()
	      ans2=vs.dms_text_input
	      if ans2=='':
	        pass
	      else:
	        try:
	          degs,minutes,seconds_str,direc=ans2.split()
	          seconds=seconds_str.replace(',','.')
	        except:
	          i=dialogs.alert('Coordinate input is not Degrees Minutes Seconds Direction!','','OK',hide_cancel_button=True)
	          continue
	        dd1=dms2dd(degs,minutes,seconds,direc.upper())
	        dd1_round=round(dd1,5)
	        if vs.dms_coord_input == None:
	          i=dialogs.alert('Neither Latitude nor Longitude Has Been Selected!','','OK',hide_cancel_button=True)
	          continue
	        elif vs.dms_coord_input == 'LO':
	          if lon_range_check(dd1):
	            coord_pr='Longitude'
	          else:
	            i = dialogs.alert('Longitude must be between -180 & 180','','OK',hide_cancel_button=True)
	            continue
	          if not(lon_direction_check(direc.upper())):
	            pass
	            i = dialogs.alert('Longitude must be either E or W','','OK',hide_cancel_button=True)
	            continue
	        elif vs.dms_coord_input == 'LA':
	          if lat_range_check(dd1):
	            coord_pr='Latitude'
	          else:
	            i = dialogs.alert('Latitude must be between -90 & 90','','OK',hide_cancel_button=True)
	            continue
	          if not(lat_direction_check(direc.upper())):
	            i = dialogs.alert('Latitude must be either N or S','','OK',hide_cancel_button=True)
	            continue
	        i = dialogs.alert(f'CONVERT {coord_pr} FROM\n\n{degs} {minutes} {seconds} {direc.upper()}\nto\n{dd1_round}','','OK',hide_cancel_button=True)
	    elif vo.choices==dd_dms_field_title_dd:
	      v.dms_text_input=''
	      dd_view_present()
	      dd1=v.dms_text_input
	      v.dms_text_input=''
	      if dd1=='':
	        pass
	      else:
	        try:
	          degs,minutes,seconds,direc=dd1.split()
	          i=dialogs.alert('Coordinate input is not Decimal Degrees!','','OK',hide_cancel_button=True)
	          continue
	        except:
	          pass
	        ans3=dd1.strip().replace(',','.')
	        try:
	          d,m,s = dd2dms(float(ans3))
	        except ValueError:
	          i=dialogs.alert('Input is not formatted correctly!','','OK',hide_cancel_button=True)
	          continue
	        s_round=round(s,3)
	        if v.dms_coord_input == None:
	          i=dialogs.alert('Neither Latitude nor Longitude Has Been Selected!','','OK',hide_cancel_button=True)
	          continue
	        elif v.dms_coord_input == 'LO':
	          if lon_range_check(d):
	            coord_pr='Longitude'
	          else:
	            i = dialogs.alert('Longitude must be between -180 & 180','','OK',hide_cancel_button=True)
	            continue
	          if d>0:
	            direc='E'
	          else:
	            direc='W'
	            d=abs(d)
	        elif v.dms_coord_input == 'LA':
	          if lat_range_check(d):
	            coord_pr='Latitude'
	          else:
	            i = dialogs.alert('Latitude must be between -90 & 90','','OK',hide_cancel_button=True)
	            continue
	          if d>0:
	            direc='N'
	          else:
	            direc='S'
	            d=abs(d)
	        i = dialogs.alert(f'CONVERT {coord_pr} FROM\n\n{ans3}\nto\n{d} {m} {s_round} {direc}','','OK',hide_cancel_button=True)
	    elif vo.choices==dd_dms_field_title_ddm:
	      vm.dms_text_input=''
	      ddm_view_present()
	      dd2=vm.dms_text_input
	      vm.dms_text_input=''
	      if dd2=='':
	        pass
	      else:
	        try:
	          degs,minutes_str,direc=dd2.split()
	          minutes=minutes_str.replace(',','.')
	        except:
	          i=dialogs.alert('Coordinate input is not Degrees Decimal Minutes Direction!','','OK',hide_cancel_button=True)
	          continue
	        try:
	          dd_list=ddm2dd(degs,minutes,direc.upper())
	        except :
	          i=dialogs.alert('Input is not formatted correctly!','','OK',hide_cancel_button=True)
	          continue
	        s_round=round(dd_list[1][2],3)
	        d=dd_list[1][0]
	        if vm.dms_coord_input == None:
	          i=dialogs.alert('Neither Latitude nor Longitude Has Been Selected!','','OK',hide_cancel_button=True)
	          continue
	        elif vm.dms_coord_input == 'LO':
	          if lon_range_check(d):
	            coord_pr='Longitude'
	          else:
	            i = dialogs.alert('Longitude must be between -180 & 180','','OK',hide_cancel_button=True)
	            continue
	          if not(lon_direction_check(direc.upper())):
	            i = dialogs.alert('Longitude must be either E or W','','OK',hide_cancel_button=True)
	            continue
	          if d>0:
	            direc='E'
	          else:
	            direc='W'
	            d=abs(d)
	        elif vm.dms_coord_input == 'LA':
	          if lat_range_check(d):
	            coord_pr='Latitude'
	          else:
	            i = dialogs.alert('Latitude must be between -90 & 90','','OK',hide_cancel_button=True)
	            continue
	          if not(lat_direction_check(direc.upper())):
	            i = dialogs.alert('Latitude must be either N or S','','OK',hide_cancel_button=True)
	            continue
	          if d>0:
	            direc='N'
	          else:
	            direc='S'
	            d=abs(d)
	        d2=round(dd_list[0],3)
	        i = dialogs.alert(f'CONVERT {coord_pr} FROM\n\n{degs} {minutes} {direc.upper()}\nto\n{d} {dd_list[1][1]} {s_round} {direc}\n&\n{d2}','','OK',hide_cancel_button=True)
	    elif vo.choices==dd_dms_field_title_to_grid:
	      vi=ci_init(dialog_hdr)
	      vi.ci_text_input=''
	      ci_view_present()
	      if vi.ci_text_input == '':
	        pass
	      elif vi.ci_done_button_pressed == True:
	        try:
	          lat,lon=vi.ci_text_input.split(',')
	        except:
	          i=dialogs.alert('Latitude and Longitude must both be specified!','','OK',hide_cancel_button=True)
	          continue
	        float_lat=float(lat.strip())
	        float_lon=float(lon.strip())
	        if not(lat_range_check(float_lat)):
	          i = dialogs.alert('Latitude must be between -90 & 90','','OK',hide_cancel_button=True)
	          continue
	        if not(lon_range_check(float_lon)):
	          i = dialogs.alert('Longitude must be between -180 & 180','','OK',hide_cancel_button=True)
	          continue
	        grid_square=to_grid(float_lat,float_lon)
	        i = dialogs.alert(f'CONVERT\n{float_lat}, {float_lon}\nto\n{grid_square}','','OK',hide_cancel_button=True)

# end of While True
	  
if __name__ == '__main__':

	main()
	
