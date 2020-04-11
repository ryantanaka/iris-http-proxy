#/bin/bash

INPUT=$1
OUTPUT=$2

for input in "${@:1:$#-1}"
do
    /usr/bin/wc -c < "$input" >> ${!#}
done

