#!/bin/bash

id=`date '+%Y%m%d%H%M%S'`
mkdir ./tmp
file="./tmp/ssub_run_fugaku.${id}.$$.sh"

touch $file
chmod +x ./$file
echo "#!/bin/bash" > $file
echo "$@" >> $file
echo "rm $file" >> $file

com="pjsub -L "node=1" -L "rscgrp=small" -L "elapse=12:00:00" $file"
echo $com
$com












