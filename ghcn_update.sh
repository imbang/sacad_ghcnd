#!/bin/bash

// menggunakan direktori scratch
// ghcn_update.sh <out-dir> <out-keyfile> <out-sql-dir> <avail-file>

outdir=$1
keyfile=$2
outsqldir=$3
availfile=$4

./update_ghcn.py $outdir 2> update_ghcn.err
./ghcn_preparetosacad.py $outdir $keyfile $outsqldir $availfile 2> ghcn_preparetosacad.err

echo "please check files : update_ghcn.err and ghcn_preparetosacad.err
