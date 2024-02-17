/* ***************************************************************************
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License version 2 as
 *  published by the Free Software Foundation.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 *
 *  As a special exception, you may use this file as part of a free software
 *  library without restriction.  Specifically, if other files instantiate
 *  templates or use macros or inline functions from this file, or you compile
 *  this file and link it with other files to produce an executable, this
 *  file does not by itself cause the resulting executable to be covered by
 *  the GNU General Public License.  This exception does not however
 *  invalidate any other reasons why the executable file might be covered by
 *  the GNU General Public License.
 *
 ****************************************************************************
 *  Authors: Dalvan Griebler <dalvangriebler@gmail.com>
 *         
 *  Copyright: GNU General Public License
 *  Description: This is a simple matrix multiplication algorithm. 
 *  File Name: matrix_multi.cpp
 *  Version: 1.0 (25/05/2018)
 *  Compilation Command: g++ -std=c++1y matrix_multi.cpp -o exe
 ****************************************************************************
*/

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
