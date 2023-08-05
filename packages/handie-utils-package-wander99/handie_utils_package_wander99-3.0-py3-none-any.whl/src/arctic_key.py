# © 2022 George Fenn
# V2 Changed all interactions to use dialogs for input and
# alerts for output. Console interaction should not be used
# for the distributed version.

import sys
import csv
import dialogs
import ui

class my_file_context:
	
	def __init__(self):
		self.debug=0
		
	def __enter__(self):
		try:
			self.file = open('Big_key.csv')
			return self.file
		except FileNotFoundError:
		  i=dialogs.alert('\n Arctic key file not found','','OK',hide_cancel_button=True)
		except IOError as err:
			i=dialogs.alert(err,'','OK',hide_cancel_button=True)
		
	def __exit__(self, type, value, traceback):
		if all((type, value, traceback)):
		  dialogs.alert('\n Unable to instantiate arctic key class','','OK',hide_cancel_button=True)
		  if self.debug:
		    i=dialogs.alert(f'Type: {type} Value: {value} Traceback: {traceback}','','OK',hide_cancel_button=True)
		  sys.exit()
		else:
		  self.file.close()

class arctic_key:
	
    def __init__(self):
    	self.key_dict = {}
    	
    def get_key(self):
    	
    	with my_file_context() as csv_file:
    		
    		csv_reader = csv.DictReader(csv_file, delimiter=',')
    		row=(next(csv_reader))
    		self.key_dict['Userid']=row['Userid']
    		self.key_dict['Password']=row['Password']
    		
    def init_key(self):
    	
    	param_list=[]
    	ans=''
    	arctic_title=' Initialize Arctic Key File'
    	arctic_field_title_uid='Enter user id for new user   '
    	arctic_field_title_pword='Enter password for new user    '
    	
    	with open('Big_key.csv',mode='w') as csv_out :
    		file_header=['Userid','Password']
    		csv_writer = csv.writer(csv_out,delimiter=',',quotechar='"')
    		csv_writer.writerow(file_header)
    		param_list.append(dict(type='text',title=arctic_field_title_uid,key='arctic_uid',accessory_type='none',autocapitalization=ui.AUTOCAPITALIZE_NONE))
    		param_list.append(dict(type='password',title=arctic_field_title_pword,key='arctic_password',accessory_type='none',autocapitalization=ui.AUTOCAPITALIZE_NONE))
    		ans=dialogs.form_dialog(title=arctic_title,fields=param_list)
    		uid=ans['arctic_uid']
    		pword=ans['arctic_password']
    		csv_writer.writerow([uid,pword])
    		
    		i=dialogs.alert('\n Done with Arctic Key File Initialize','','OK',hide_cancel_button=True)

def main():
	ak=arctic_key()
	ak.init_key()	
    			
if __name__ == '__main__':
	main()
