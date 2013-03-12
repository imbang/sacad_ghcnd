#!/usr/bin/python

import os
import time
import sys
from ftplib import FTP

if len(sys.argv)<2:
	print "update_ghcn.py <OUT-DIR>"
	print "needs 1 parameters :"
	print "          OUT-DIR"
	print "========================"
	sys.exit()

start_time = time.time()

#outdir="scratch"
outdir=$1

ghcnsta="/usr/people/imbangla/didah/official/ghcnd/GHCND_update_SACA_sta_id.txt"

if not os.path.isdir(outdir):
	print "creating directory",outdir
	os.mkdir(outdir)
else:
	print "Deleting existing files in directory",outdir
	os.chdir(outdir)
	for the_file in os.listdir('.'):
		file_path = os.path.join(the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception, e:
			print e
	os.chdir('..')
 
ftp = FTP("ftp.ncdc.noaa.gov")
ftp.login()
ftp.cwd("pub")
ftp.cwd("data")
ftp.cwd("ghcn")
ftp.cwd("daily")
ftp.cwd("all")

#=================================================================
#ftp.retrlines("LIST")
#pub/data/ghcn/daily

#ftp.cwd("folderOne")
#ftp.cwd("subFolder") # or ftp.cwd("folderOne/subFolder")
 
#listing = []
#ftp.retrlines("LIST", listing.append)
#words = listing[0].split(None, 8)
#filename = words[-1].lstrip()
#print filename
#=================================================================

print "Trying to list the files...."
listing = ftp.nlst("*")
print "Ready to download...."
fid = open(ghcnsta,'r')
line = fid.readline()
while True:
	line = fid.readline().strip()
	dt = line.split()
	if len(dt)<=1:
		break
	coun = dt[0]
	if coun=='ID':
		continue
	ghcnid = dt[1]
	#make looks like file ghcnd
	lnght = 8 - len(ghcnid)
	g0 = lnght*"0"
	ghcnid = g0 + ghcnid
	isketemu=False
	print "downloading",ghcnid,
	for i in range(len(listing)):
		if listing[i].find(ghcnid)>=0:
			filename = listing[i]
			local_filename = os.path.join(outdir, filename)
			lf = open(local_filename, "wb")
			ftp.retrbinary("RETR " + filename, lf.write, 8*1024)
			lf.close()
			print "YES"
			isketemu=True
			break
	if isketemu==False:
		print "NO"
		sys.stderr.write(ghcnid+"\n")
fid.close()
# 00914690
#=================================================================
#filename="ASN00040284.dly" 
#local_filename = os.path.join("tmp", filename)
#lf = open(local_filename, "wb")
#ftp.retrbinary("RETR " + filename, lf.write, 8*1024)
#lf.close()
#=================================================================
ftp.quit()

elapsed_time = time.time() - start_time
print "Elapsed time: %.4f" % elapsed_time

