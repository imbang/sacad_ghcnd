#!/usr/bin/python

# ==============================================
# created by Bayu Imbang L, 11 March 2013 @KNMI
# ++++++++++++++++++++++++++++++++++++++++++++++
# make keyfile and prepare for ingesting
# ==============================================

import os
import sys
from glob import glob
import MySQLdb as mdb
from ghcnd import ghcnd

if len(sys.argv)<5:
	print "ghcn_preparetosacad.py <IN-DIR> <OUT-KEY-FILE> <OUT-SQL-DIR> <SUMMARY-FILE>"
	print "needs 4 parameters :"
	print "          IN-DIR"
	print "          OUT-KEY-FILE"
	print "          OUT-SQL-DIR"
	print "          SUMMARY-FILE"
	print "==========================================================="
	sys.exit()

ghcnsta="/usr/people/imbangla/didah/official/ghcnd/GHCND_update_SACA_sta_id.txt"
#ghcnsta="GHCND_update_SACA_sta_id.txt"

if (not os.path.isfile(ghcnsta)):
	print "file GHCND_update_SACA_sta_id.txt not found."
	sys.exit()

indir=sys.argv[1]
keyfile=sys.argv[2]
outsqldir=sys.argv[3]
sumfile=sys.argv[4]

listcode={}
fid = open(ghcnsta,'r')
fid.readline()
while True:
	line = fid.readline().strip()
	dt =line.split()
	if len(dt)<=1:
		break
	counid = dt[1]	
	staid = dt[2]
	tn = dt[3]
	tx = dt[4]
	rr = dt[5]	
	dic={}
	dic['staid'] = staid
	dic['tn'] = tn
	dic['tx'] = tx
	dic['rr'] = rr
	listcode[counid] = dic
	del dic
fid.close()

#print listcode['32078']
#sys.exit()

if not os.path.isdir(outsqldir):
	print "creating directory",outsqldir
	os.mkdir(outsqldir)
else:
	print "Deleting files in directory",outsqldir
	os.chdir(outsqldir)
	for the_file in os.listdir('.'):
		file_path = os.path.join(the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception, e:
			print e
	os.chdir('..')


fid = open(keyfile,'w')
fsm = open(sumfile,'w')
fsm.write("staid\ttx\ttn\trr\n")

listing=glob(indir+'/*.dly')
berhasil=0
gagal=0
for fl in listing:
	print "Processing file",fl
	fls = os.path.basename(fl)
	code=str(int(fls[3:11]))
	for key,value in listcode.iteritems():
		if code==key:
			[totx,itx,totn,itn,torr,irr] = ghcnd(fl,outsqldir,value)
			if totx>0:	
				psntx = (totx-itx) / float(totx) * 100.0
			else:
				psntx = 0
		
			if totn>0:
				psntn = (totn-itn) / float(totn) * 100.0
			else:
				psntn = 0
		
			if torr>0:		
				psnrr = (torr-irr)/ float(torr) * 100.0
			else:
				psnrr = 0
	
			fsm.write("%s\t%.2f\t%.2f\t%.2f\n" % (listcode[code]['staid'],psntx,psntn,psnrr))

fsm.close()
fid.close() # fid creating keyfile
#sys.stderr.write("berhasil: %d | gagal: %d\n" % (berhasil,gagal))

