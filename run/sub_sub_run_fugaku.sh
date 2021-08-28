#!/bin/bash

<< COMMENTOUT
L1ckpt_overhead(int): 1, 2, 4, 8, 16, 32 [7]
L2ckpt_latency(int): 2, 4, 8, 16, 32, 64 [7]
ckptRestartTimes(list): same to L1ckpt_overhead
MTBF(L1) 10, 20, 40, 60, 120, 360, 900, 1440 [9]
MTBF(L2) 60, 120, 360, 720, 1440 [6]
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


# ./sub_run_fugaku.sh ./run_fugaku.sh 16 32 60 360 1024 2 3
O=(1 2 4 8 16 32) # [6]
L=(2 4 8 16 32 64) # [6]
#L=(64)
F1=(10 20 40 60 120 360 900 1440) # [8]
#F1=(10)
F2=(60 120 360 720 1440) #[5]
#F2=(60)

for o in ${O[@]}
do
    for l in ${L[@]}
    do
	for f1 in ${F1[@]}
	do
	    for f2 in ${F2[@]}
	    do
		if test $l -lt $o -o $f2 -lt $f1; then
		    continue
		fi
		com="./sub_run_fugaku.sh ./run_fugaku.sh $o $l $f1 $f2"
		echo $com
		$com
		sleep 1
	    done
	done

    done
done






