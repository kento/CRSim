#!/bin/bash

<< COMMENTOUT
L1ckpt_overhead(int): 0, 1, 2, 4, 8, 16, 32 [7]
L2ckpt_latency(int): 0, 2, 4, 8, 16, 32, 64 [7]
ckptRestartTimes(list): same to L1ckpt_overhead
MTBF(L1) 0, 10, 20, 40, 60, 120, 360, 900, 1440 [8]
MTBF(L2) 0, 60, 120, 360, 720, 1440 [5]
N(int): 1024 2048 4096 8192 16384 32768 65536 131072 [8]
G(int): (group size) 1 2 4 8  [4]
g(int): 1 2 4 [3]
alpha(float): 0.1

usage: CRtool.py opt [-h] -o L1_OVERHEAD -l L2_LATENCY -r RECOVERY
                     [RECOVERY ...] -f MTBF [MTBF ...] -n NODES -s SPARES -g
                     GROUP_SIZE -t GROUP_TOLERANCE -a ALPHA
                     [-e CHECK_INTERVAL] [-c CHECK_CONTIGUOUS]
                     [-m FAILURE_MAX] [-p STEPS] [-v VERBOSE]
COMMENTOUT

crtool=../src/CRtool.py

O=(1 2 4 8 16 32) #
if [ $# -gt 0 ]; then
    O=($1)
fi    
L=(2 4 8 16 32 64)
if [ $# -gt 1 ]; then
    L=($2)
fi    
F1=(10 20 40 60 120 360 900 1440) #
if [ $# -gt 2 ]; then
    F1=($3)
fi    
F2=(60 120 360 720 1440)
if [ $# -gt 3 ]; then
    F2=($4)
fi    
N=(1024 2048 4096 8192 16384 32768 65536 131072)
if [ $# -gt 4 ]; then
    N=($5)
fi    
S=999999
G=(1 2 4 8) #
if [ $# -gt 5 ]; then
    G=($6)
fi    
T=(1 2 4) #
if [ $# -gt 6 ]; then
    T=($7)
fi    
A=0.01
E=100
C=2
M=500000
P=5000



for o in ${O[@]}
do
    for l in ${L[@]}
    do
	for f1 in ${F1[@]}
	do
	    for f2 in ${F2[@]}
	    do
		for n in ${N[@]}
		do
		    for g in ${G[@]}
		    do
			for t in ${T[@]}
			do
			    if test $l -lt $o -o $f2 -lt $f1; then
				continue
			    fi
			    com="$crtool opt -o $o -l $l -r $o $l -f $f1 $f2 -n $n -s $S -g $g -t $t -a $A -e $E -c $C -m $M -p $P -v 100"
			    echo $com
			    $com >> ./data/crtool-$o-$l-$o-$l-$f1-$f2-$n-$S-$g-$t-$A-$E-$C-$M-$P.txt &
			done
		    done
		done
	    done
	done
	
    done
done












