# setrem-parallel-programming

## Index
- [Purpose](#purpose)
- [Development stack](#development-stack)
- [Local testing](#local-testing)
- [Environment for testing](#environment-for-testing)
    - [Running parallel code in the same machine](#running-parallel-code-in-the-same-machine)
    - [Running parallel code in multiple machines](#running-parallel-code-in-multiple-machines)
    - [Running sequential code](#running-sequential-code)
- [Performance tests](#performance-tests)
- [Other things](#other-things)

## Purpose
Given an initial number, the main purpose of this automation is to calculate the quantity of prime numbers in this range.

Example: Given the number 10, the algorithm will return that there are 4 prime numbers until 10.

You can run this algorithm:
- ... in sequential mode
- ... in paralell mode

For parallel mode we are using the farm pattern, which is compose by an emitter, a collector and one or more workers. The emitter organize the work and send tasks to the workers (distributing the tasks evenly). Then, the worker performs the actual work and send the result to collector. Finally, the collector merges this data and presents it to the user.

![](.docs/img/.pattern.drawio.png)

The main idea of this architecture is to scale the number of workers to achieve more speed. The more workers we have, the higher the performance (in theory). We'll see more about this in the [performance test](#performance-tests).

## Development stack
- Python: 3.11
- Libraries:
    - [mpi4py](https://pypi.org/project/mpi4py/)
    - [click](https://pypi.org/project/click/)
- Dev libraries:
    - [pytest](https://pypi.org/project/pytest/)
    - [coverage](https://pypi.org/project/coverage/)
    - [flake8](https://pypi.org/project/flake8/)

## Local testing

I'm using [pipenv](https://pipenv.pypa.io/en/latest/) to create and manage Python virtual environments. It helps us to isolate the libraries and differents Python versions.

To initialize the virtual environment just run:
```sh
pipenv install -d
pipenv shell
```

To run code using __sequential mode__:
```sh
python app.py --mode sequential --until-number 1000
```

> Where 1000 represents the max number to search for prime numbers.

It's important to comment that to run this code in parallel mode I'm using [OpenMPI](https://www.open-mpi.org/). In case you are using Windows in your development environment, even if you will run this code in sequential mode, you must [install Microsoft MPI](https://learn.microsoft.com/en-us/message-passing-interface/microsoft-mpi). If you don't, a common error that may happen is:
```
ImportError: DLL load failed while importing MPI: Não foi possível encontrar o módulo especificado.
```


## Environment for testing

To run this code in a testing environment, we first need to create this environment following [these steps](./.docs/ENVIRONMENT.md).

The next steps, you must run just on __primary__.

You must access the shared folder and clone this repository:
```sh
cd /home/mpihpc/shared
git clone https://github.com/gabrielrih/setrem-parallel-programming.git
```

Then you can finally run the code inside the repo:
```sh
cd setrem-parallel-programming
```

### Running parallel code in the same machine

Running the code in the same machine:
```sh
mpirun -np 3 python app.py --mode parallel --until-number 10000
```

> Note that in this case the _mpirun_ are running the code in three different processes but all of them in the same machine. Another important thing is that each process is created in a differente vCore, so, in this case, the VM must have three or more vCores.


### Running parallel code in multiple machines

Running the code in multiple machines:
```sh
mpirun -np 3 --machinefile /home/mpihpc/.cluster_hostfile python app.py --mode parallel --until-number 10000
```

> Note that in this case the _mpirun_ are running using three different processes. By default, each process are allocated in a different vCore. If the -np value is bigger than the number of vCores in all the cluster, the default behavior is generate an error.

### Running sequential code

Running the sequential code. It uses just a single vCore.
```sh
python app.py --mode sequential --until-number 10000
```

## Performance tests

COLOCAR AQUI


## Other things
[Here](./cpp/CPP.md) you can see some example using C++.