#include <iostream>
#include <chrono>
#include <thread>
#include <vector>

#define MX 2000
#define CORES 6

long int **matrix_one, **matrix_two, **final_matrix;

void initialize_matrices(){
	long int i, j;
	for(i=0; i<MX; i++){
		for(j=0; j<MX; j++){
			matrix_one[i][j] = 4;
			matrix_two[i][j] = 5;
			final_matrix[i][j] = 0;
		}
	}	
}

void printMatrix(long int **matrix){		
	int i, j;
	for(i=0; i<MX; i++){
		printf("\n");
		for(j=0; j<MX; j++){
			printf("%ld ", matrix[i][j]);
		}
	}
	printf("\n");				
}

void parallel_multiply(long int start, long int end) {
	for(long int i=start; i<=end; i++){
		for(long int j=0; j<MX; j++){
			for(long int k=0; k<MX; k++){
				final_matrix[i][j] += (matrix_one[i][k] * matrix_two[k][j]);
			}
		}
	}	
}

int main(int argc, char const *argv[]){

	//define matrices
	final_matrix = new long int*[MX];
	matrix_one = new long int*[MX];
	matrix_two = new long int*[MX];

	for (long int i=0; i < MX; i++){
	    final_matrix[i] = new long int[MX];
	    matrix_one[i] = new long int[MX];
	    matrix_two[i] = new long int[MX];
	}
	
	//assigning fixed values to the matrixes SEQUENTIALLY
	initialize_matrices();

	//matrix multiplication algorithm IN PARALLEL
	auto t_start = std::chrono::high_resolution_clock::now();
	long int start;
	long int end;
	long int factor = MX / CORES;
	std::vector<std::thread> th;
    for(size_t id = 0; id < CORES; id++){
		start = id * factor;
		end = ((id + 1) * factor) - 1;
		if (id == CORES - 1) {  // it is the last core
			if (MX % CORES != 0 ) {  // mod
				end = MX - 1;
			}
		}
		th.push_back(std::thread(parallel_multiply, start, end));
    }
    for(auto &t : th)
        t.join();

	auto t_end = std::chrono::high_resolution_clock::now();
	std::cout << "Parallel DotProduct Execution time(s): " << std::chrono::duration<double>(t_end-t_start).count() << std::endl;
	
	printMatrix(final_matrix);
	printf("SIZE= %d\n", MX);

	delete final_matrix;
	delete matrix_one;
	delete matrix_two;
}
