# © 2022 George Fenn

def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction == 'W' or direction == 'S':
        dd *= -1
    return dd

def dd2dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]

def ddm2dd(degrees, minutes, direction):
    dd = float(degrees) + float(minutes)/60
    if direction == 'W' or direction == 'S':
        dd *= -1
    d,m,s = dd2dms(dd)
    return [dd,[d,m,s]]
    
def main():
	ans=input('Enter coordinates as Degs Mins Secs, Degs Decimal Minutes, or Decimal Degrees <dms>/ddm/dd')
	if ans== 'dms' or ans=='':
		degs,minutes,seconds,direc=input('Enter : Degrees Minutes Seconds Direction ').split()
		dd1=dms2dd(degs,minutes,seconds,direc)
		print(dd1)
	elif ans=='ddm':
	  degs,minutes,direc=input('Enter : Degs Decimal Mins Direction').split()
	  dd_list=ddm2dd(degs,minutes,direc)
	  print(dd_list)
	else:
		dd1=input('Enter : Decimal Degrees')
		d,m,s = dd2dms(float(dd1))
		print(str(d)+' '+str(m)+' '+str(s))
	
if __name__ == '__main__':

	main()
	
