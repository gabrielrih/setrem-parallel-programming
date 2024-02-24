# setrem-parallel-programming

## dependencies
Common
```sh
sudo apt install screen
```

C++ compiler
```sh
sudo apt install g++
```

TBB library
```sh
sudo apt install libtbb-dev
```

## compiling the code
```sh
g++ -O3 file.cpp -o output -pthread
```

Using tbb
```sh
g++ -O3 -std=c++1y file.cpp -o output -tbb
```

Using OpenMp
```sh
g++ -Wall -std=c++1y -O3 file.cpp -o output -fopenlomp
```

## running it
```sh
./output
```
