BEFORE OPTIMIZE COLLECTOR

python app.py --mode sequential --until-number 100000
77,74
71,39
67,82

mpirun -np 3 --use-hwthread-cpus python app.py --mode parallel --until-number 100000
54,45
79,92
95,60

mpirun -np 3 --use-hwthread-cpus python app.py --mode parallel --until-number 100000 --light-way True
84,26
