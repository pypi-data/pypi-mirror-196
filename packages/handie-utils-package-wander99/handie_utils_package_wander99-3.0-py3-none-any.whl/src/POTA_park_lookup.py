# © 2022 George Fenn
# V5 Write to clipboard the park entity latitude and longitude
# so it can be used in the distance calculator module.
# Added the park_results routine to reduce duplicate code.
# Changed the check for multiple activations for a park from
# Many to Manyme to allow for park names with many in them.
# Changed the results function to not put the My Activations
# number on another line; used a tab instead.
# V6 Changed csv filename to 'United States Of America.csv', 
# exactly as it comes from POTA.app. Also, changed encoding
# from ASCII to UTF-8 so no exporting is necessary.
# V7 Added a ui method call to check for screen size so the dialog
# header can be adjusted to fit on an iPhone screen.
# V8 Changed to check which csv filename exists, first for
# 'United States of America (K).csv' or if that doesn't exist
# 'United States Of America.csv', which is a subcategory 
# under (K) which doesn't include Alaska, Hawaii, Puerto Rico, 
# and some islands. 
# V9 Changed to use the handie common interface to get call sign lookup
# input.
# V10 Added logic, like what is in SOTA Summit Lookup, to be able to
# differentiate between Parks with the same name e.g. Natural Bridge.
# This is done by adding the location to the dictionary key e.g. US-VA.

from handie_ci import *
import csv
import dialogs
import clipboard
import ui
from os.path import exists as file_exists

class parameter_item():
	
	def __init__(self):
		self.param_list=[]
		self.parms_data={}
		self.last_name=''
		self.count=0
	
	def add_parms(self,name_qth,name,ref,qth,lat,lon,my_acts,my_hunts):
	    	self.parms_data[name_qth]=(name,ref,qth,lat,lon,my_acts,my_hunts)
	    	self.param_list.append(dict(title=name_qth,accessory_type='none'))
	    	self.count+=1
	    	self.last_name=name_qth
	    	
def park_results(park_data,name):
	xname,xref, xqth, xlat, xlong, xmy_acts,xmy_hunts = park_data
	lat_long=str(xlat+','+xlong)
	clipboard.set(lat_long)
	i = dialogs.alert(f'PARK FOUND\n\nReference:\t{xref}\nPark:\t{name}\nLocation:\t{xqth}\nLat:\t{xlat}\nLon:\t{xlong}\nMy Activations:\t{xmy_acts}\nMy Hunted QSOs:\t{xmy_hunts}','',  'OK',hide_cancel_button=True)
	    	
def POTA_park_lookup(park_list,dialog_hdr):
      
      vi=ci_init(dialog_hdr)
      
      while True:
        vi.ci_text_input=''
        ci_view_present()
        
        if vi.ci_text_input == '':
          break
        elif vi.ci_done_button_pressed == True:
          parmsc = parameter_item()
          
          for ref,name,lat,long,grid,qth,my_acts,my_hunts in park_list:
            checkl=vi.ci_text_input.lower()
            if vi.ci_text_input == 'Manyme':
              if int(my_hunts) > 1:
                name_qth=name+' '+qth
                parmsc.add_parms(name_qth,name,ref,qth,lat,long,my_acts,my_hunts)
              else:
                pass
            elif ref.lower()==checkl or name.lower().find(checkl)!= -1:
              name_qth=name+' '+qth
              parmsc.add_parms(name_qth,name,ref,qth,lat,long,my_acts,my_hunts)
            else:
              pass
              
          if parmsc.count>1:
            choices = dialogs.list_dialog('Select Park', parmsc.param_list)
            if choices is None:
              continue
            xname_qth=choices["title"]
            park_results(parmsc.parms_data[xname_qth],parmsc.parms_data[xname_qth][0])
          elif parmsc.count==1:
            xname_qth=parmsc.last_name
            park_results(parmsc.parms_data[xname_qth],parmsc.parms_data[xname_qth][0])
          else:
            i = dialogs.alert(f'Park Not Found\n{vi.ci_text_input}','',  'OK',hide_cancel_button=True)

def main(park_list):
  
  USA_K_file = 'United States of America (K).csv'
  USA_file = 'United States Of America.csv'
  
  if min(ui.get_screen_size()) >= 768:
    # iPad
    dialog_hdr='Park reference or Name for Lookup'
  else:
    # iPhone
    dialog_hdr='Park ref or Name for Lookup'
    
  if file_exists(USA_K_file):
    file_name=USA_K_file
  elif file_exists(USA_file):
    file_name=USA_file
  else:
    i = dialogs.alert(f'Park File Not Found!\nDownload from pota.app','',  'OK',hide_cancel_button=True)
    return
    
  if not park_list:
    with open(file_name,encoding='utf-8') as csv_file :
      csv_reader = csv.DictReader(csv_file, delimiter=',')
      for row in csv_reader:
        next_park=[(row["reference"],row["name"],row["latitude"],row["longitude"],row["grid"],row["locationDesc"],row["my_activations"],row["my_hunted_qsos"])]
        park_list.extend(next_park)
    
  POTA_park_lookup(park_list,dialog_hdr)

if __name__ == '__main__':
	park_list=[]
	main(park_list)
