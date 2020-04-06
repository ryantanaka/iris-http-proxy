#/bin/bash

INPUT=$1
OUTPUT=$2

/usr/bin/wc -c < $INPUT >> $OUTPUT

