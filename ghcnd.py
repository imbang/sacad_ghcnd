#!/usr/bin/python

#=============================================
#created by Bayu Imbang
#edited by Aris Suwondo
#Objective : GHCND data into txt
#KNMI Utrecht Februari 2013
#=============================================  

import sys
import os
from calendar import monthrange

def is_number(cellvalue):
    try:
        float (cellvalue)
        return True
    except ValueError:
        return False

ofset=1
namafile = sys.argv[1]

def ghcnd(namafile,outdir,series,offset=1):
	#offset=1    
	f=open(namafile)
	filetx = os.path.join(outdir,"GHCN_%s_TX.txt" % series['staid'])
	filetn = os.path.join(outdir,"GHCN_%s_TN.txt" % series['staid'])
	filerr = os.path.join(outdir,"GHCN_%s_RR.txt" % series['staid'])
	if series['tx']<>'-1':
		ftx=open(filetx,'w')
	if series['tn']<>'-1':
		ftn=open(filetn,'w')
	if series['rr']<>'-1':
		frr=open(filerr,'w')
	itx=0;itn=0;irr=0
	totx=0;totn=0;torr=0
	while True:
		baris=f.readline()
		isi=baris.split()
		if len(isi)==0:
			break
		code=isi[0]
		coun=code.split()[0][0:2]
		nosta=code.split()[0][2:11]
		thn=int(code.split()[0][11:15])
		bln=int(code.split()[0][15:17])
		ele=code.split()[0][17:21]
		ranges=monthrange(thn,bln)[1]
		if (ele=="TMAX" or ele=="TMIN" or ele=="PRCP"):
			for tgl in range(1,ranges+1):
				tmp=tgl*2-1
				if tmp>=len(isi):
					break				
				#print namafile,"->",isi,tgl,bln,thn,\
				#	isi[(tgl-1)*2-1],isi[(tgl-2)*2-1],isi[(tgl-3)*2-1],len(isi),tmp
				val1=isi[tgl*2-1]
				#print coun,nosta,thn,bln,tgl,ele,val1
				if ele=='TMAX':
					totx=totx+1
					try:
						val = int(val1)
					except:
						val = -9999
						itx=itx+1						
					tmp="%s,'%d-%d-%d',%d,-9,-9,-9\n" % (series['tx'],thn,bln,tgl,val)
					if series['tx']<>'-1':
						ftx.write(tmp)
				elif ele=='TMIN':
					totn=totn+1
					try:
						val = int(val1)
					except:
						val = -9999
						itn=itn+1
					tmp="%s,'%d-%d-%d',%d,-9,-9,-9\n" % (series['tn'],thn,bln,tgl,val)
					if series['tn']<>'-1':
						ftn.write(tmp)
				elif ele=='PRCP':
					torr=torr+1
					try:
						val = int(val1)
					except:
						val = -9999
						irr=irr+1
					tmp="%s,'%d-%d-%d',%d,-9,-9,-9\n" % (series['rr'],thn,bln,tgl,val)
					if series['rr']<>'-1':
						frr.write(tmp)
	if series['tx']<>'-1':
		ftx.close()
	if series['tn']<>'-1':		
		ftn.close()
	if series['rr']<>'-1':
		frr.close()

	f.close()
	#print namafile,totx,itx,totn,itn,torr,irr
	return totx,itx,totn,itn,torr,irr

	
