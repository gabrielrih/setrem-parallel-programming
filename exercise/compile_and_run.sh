#!/bin/bash
num_processes=$1
if ! [ "$num_processes" ]; then num_processes=4; fi  # default value
run_on_cluster=$2
if ! [ "$run_on_cluster" ]; then run_on_cluster=1; fi  # default value

exe_file='tmp_exe'
file='farm/exercise.cpp'

echo "(+) Compiling"
if [ -f "$exe_file" ]; then rm $exe_file; fi
mpic++ -Wall -std=c++1y -O3 $file -o $exe_file

if [ $run_on_cluster == 1 ]; then
    echo "(+) Running on cluster..."
    mpirun -np $num_processes --machinefile /home/mpihpc/.cluster_hostfile $exe_file
else
    echo "(+) Running on the current machine..."
    mpirun -np $num_processes $exe_file
fi

exit 0