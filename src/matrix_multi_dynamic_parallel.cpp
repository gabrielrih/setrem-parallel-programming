#include <iostream>
#include <chrono>
#include <thread>
#include <vector>
#include <mutex>

#define MX 1000
#define THREADS 5

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

long int iterator=MX;
std::mutex m;
void parallel_multiply() {
	while (iterator > 0) {
		m.lock();
		iterator--;
		long int i=iterator;
		m.unlock();
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
	std::vector<std::thread> th;
    for(size_t id = 0; id < THREADS; id++){
		//std::cout << "Starting thread: " << id;
		th.push_back(std::thread(parallel_multiply));
    }
    for(auto &t : th)
        t.join();

	auto t_end = std::chrono::high_resolution_clock::now();

 	// for debugging
	//printMatrix(final_matrix);

	std::cout << "Parallel Dynamic DotProduct Execution time(s): " << std::chrono::duration<double>(t_end-t_start).count() << std::endl;
	printf("SIZE= %d\n", MX);

	delete final_matrix;
	delete matrix_one;
	delete matrix_two;
}
