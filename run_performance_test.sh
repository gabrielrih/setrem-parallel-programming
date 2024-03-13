#!/bin/bash

processes=$1
until_number=$2

command="mpirun -np $processes python app.py --mode parallel --until-number $until_number"
echo "Running: $command"

echo "Try 1"
$command > /tmp/result.txt

echo "Try 2"
$command > /tmp/result.txt

echo "Try 3"
$command > /tmp/result.txt

echo "Try 4"
$command > /tmp/result.txt

echo "Try 5"
$command > /tmp/result.txt

exit 0
