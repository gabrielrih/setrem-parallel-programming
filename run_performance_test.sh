#!/bin/bash

processes=$1
until_number=$2

command="mpirun -np $processes python app.py --mode parallel --until-number $until_number"
echo "Running: $command"

$command > /tmp/result.txt
echo "Try 1"
cat /tmp/result.txt | grep Took

$command > /tmp/result.txt
echo "Try 2"
cat /tmp/result.txt | grep Took

$command > /tmp/result.txt
echo "Try 3"
cat /tmp/result.txt | grep Took

$command > /tmp/result.txt
echo "Try 4"
cat /tmp/result.txt | grep Took

$command > /tmp/result.txt
echo "Try 5"
cat /tmp/result.txt | grep Took

exit 0
