#!/usr/bin/python

import os
from ftplib import FTP


ghcnsta="/usr/people/imbangla/didah/official/ghcnd/GHCND_update_SACA_sta_id.txt"

 
ftp = FTP("ftp.ncdc.noaa.gov")
ftp.login()
ftp.cwd("pub")
ftp.cwd("data")
ftp.cwd("ghcn")
ftp.cwd("daily")
ftp.cwd("all")
#ftp.retrlines("LIST")
#pub/data/ghcn/daily

#ftp.cwd("folderOne")
#ftp.cwd("subFolder") # or ftp.cwd("folderOne/subFolder")
 
#listing = []
#ftp.retrlines("LIST", listing.append)
#words = listing[0].split(None, 8)
#filename = words[-1].lstrip()
#print filename

listing = ftp.nlst("*")
print listing

#fid = open(ghcnsta,'r')
#line = fid.readline()
#while True:
#	line = fid.readline().strip()
#	dt = line.split()
#	
#fid.close()

#filename="ASN00040284.dly" 
#local_filename = os.path.join("tmp", filename)
#lf = open(local_filename, "wb")
#ftp.retrbinary("RETR " + filename, lf.write, 8*1024)
#lf.close()

ftp.quit()
