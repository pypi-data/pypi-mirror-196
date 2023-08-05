# © 2022 George Fenn
# V3 Write to clipboard the summit latitude and longitude
# so it can be used in the distance calculator module.
# Added the summit_results routine to reduce duplicate code.
# Changed the results function to not put the My Points
# number on another line; used 2 tabs instead.
# V4 Changed encoding from ASCII to UTF-8 for the summitslist
# CSV file. The first row in that spreadsheet does need to be
# deleted and the spreadsheet re-exported to CSV before import
# into Pythonista. This is necessary so summit lookups work.
# V5 Added a check so the asociation indicator can be looked for, 
# like W4G for the Georgia association.
# Added a ui method call to check for screen size so the dialog
# header can be adjusted to fit on an iPhone screen.
# V6 Changed to check if the csv filename 'summitslist.csv' exists.
# V7 Changed to use the handie common interface to get call sign lookup
# input.

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
		self.last_summit=''
		self.count=0
	
	def add_parms(self,name_assc,name,code,assoc,region,altm,altft,long,lat,pts,bonuspts):
	    	self.parms_data[name_assc]=(name,code,assoc,region,altm,altft,long,lat,pts,bonuspts)
	    	self.param_list.append(dict(title=name_assc,accessory_type='none'))
	    	self.count+=1
	    	self.last_summit=name+' '+code.split('/')[1]
	    	
def summit_results(summit_data):
	xname,xcode, xassoc, xregion, xaltm, xaltft, xlong, xlat, xpts,xbonuspts = summit_data
	lat_long=str(xlat+','+xlong)
	clipboard.set(lat_long)
	i = dialogs.alert(f'SUMMIT FOUND\n\nCode:\t{xcode}\nName:\t{xname}\nAssociation:\t{xassoc}\nRegion:\t{xregion}\nAlt Meters:\t{xaltm}\nAlt Feet:\t{xaltft}\nLat:\t{xlat}\nLon:\t{xlong}\nPoints:\t\t{xpts}\nBonus Points:\t\t{xbonuspts}','',  'OK',hide_cancel_button=True)
	    	
def SOTA_summit_lookup(summit_list,dialog_hdr):
	    		
	    vi=ci_init(dialog_hdr)
	    
	    while True:
	      vi.ci_text_input=''
	      ci_view_present()
	      
	      if vi.ci_text_input == '':
	        break
	      elif vi.ci_done_button_pressed == True:
	        parmsc = parameter_item()
	        
	        for code,assoc,region,name,altm,altft,_,_,long,lat,pts,bonuspts,actcount,actdate,actcall in summit_list:
	          checkl=vi.ci_text_input.lower()
	          if code.lower()==checkl or name.lower().find(checkl)!= -1 or code.split('/')[0].lower()==checkl:
	            name_rid=name+' '+code.split('/')[1]
	            parmsc.add_parms(name_rid,name,code,assoc,region,altm,altft,long,lat,pts,bonuspts)
	          else:
	            pass
	            
	        if parmsc.count>1:
	          choices = dialogs.list_dialog('Select Summit', parmsc.param_list)
	          if choices is None:
	            continue
	          xname_rid=choices["title"]
	          summit_results(parmsc.parms_data[xname_rid])
	        elif parmsc.count==1:
	          summit_results(parmsc.parms_data[parmsc.last_summit])
	        else:
	          i = dialogs.alert(f'Summit Not Found\n{vi.ci_text_input}','',  'OK',hide_cancel_button=True)
	    

def main(summit_list):
  
  summit_file='summitslist.csv'
  
  if min(ui.get_screen_size()) >= 768:
    # iPad
    dialog_hdr='Summit, Assoc or Name for Lookup'
  else:
    # iPhone
    dialog_hdr='Summit or Name for Lookup'
    
  if not(file_exists(summit_file)):
    i = dialogs.alert(f'Summits File Not Found!\nDownload from sotadata.org.uk','',  'OK',hide_cancel_button=True)
    return
      
  if not summit_list:
    i=dialogs.alert('Reading Summit List...','','OK',hide_cancel_button=True)
    with open(summit_file,encoding='utf-8') as csv_file :
      csv_reader = csv.DictReader(csv_file, delimiter=',')
      for row in csv_reader:
          next_summit=[(row["SummitCode"],row["AssociationName"],row["RegionName"],row["SummitName"],row["AltM"],row["AltFt"],row["GridRef1"],row["GridRef2"],row["Longitude"],row["Latitude"],row["Points"],row["BonusPoints"],row["ActivationCount"],row["ActivationDate"],row["ActivationCall"])]
          summit_list.extend(next_summit)
          
  SOTA_summit_lookup(summit_list,dialog_hdr)

if __name__ == '__main__':
	summit_list=[]
	main(summit_list)
    
