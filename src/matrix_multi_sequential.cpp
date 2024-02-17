#include <iostream>
#include <chrono>

//Matrix sizes
#define MX	2000

//all the matrix
long int **matrix1, **matrix2, **matrix;

void val(){
	long int i, j;
	for(i=0; i<MX; i++){
		for(j=0; j<MX; j++){
			matrix1[i][j] = 4;
			matrix2[i][j] = 5;
			matrix[i][j] = 0;
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

//matrix multiplication algorithm
void multiply(){
	for(long int i=0; i<MX; i++){
		for(long int j=0; j<MX; j++){
			for(long int k=0; k<MX; k++){
				matrix[i][j] += (matrix1[i][k] * matrix2[k][j]);
			}
		}
	}	
}

//main function
int main(int argc, char const *argv[]){

	matrix = new long int*[MX];
	matrix1 = new long int*[MX];
	matrix2 = new long int*[MX];

	for (long int i=0; i < MX; i++){
	    matrix[i] = new long int[MX];
	    matrix1[i] = new long int[MX];
	    matrix2[i] = new long int[MX];
	}
	
	//assigning fixed values to the matrix			
	val();

	auto t_start = std::chrono::high_resolution_clock::now();
	//matrix multiplication algorithm call
	multiply();
	auto t_end = std::chrono::high_resolution_clock::now();
	std::cout << "DotProduct Execution time(s): " << std::chrono::duration<double>(t_end-t_start).count() << std::endl;
	
	printf("SIZE= %d\n", MX);
	//printing the resultant matrix (you may comment when bigger sizes will be set-up)
	//printMatrix(matrix);

	delete matrix;
	delete matrix1;
	delete matrix2;
}
