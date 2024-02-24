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
 *  Authors: Gabriel Richter <gabrielrih@gmail.com>
 *         
 *  Copyright: GNU General Public License
 *  Description: 
 *  File Name: exercise.cpp
 *  Version: 1.0 (24/02/2024)
 *  Compilation Command: mpic++ -O3 -std=c++1y -Wall exercise.cpp -o exe
 *	Exacution Command: mpirun -np 4 ./exe
*/
#include <iostream>
#include <mpi.h>

const int MESSAGE_TAG=0;
const int MASTER_RANK=0;

int main(int argc, char *argv []){
    int myrank, //who am i
    numprocs; //how many process
    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&myrank);
    MPI_Comm_size(MPI_COMM_WORLD,&numprocs);
    if (myrank == MASTER_RANK) {
        std::cout << "Number of processes " << numprocs << std:endl;
       for(int source = 1; source < numprocs; source++){
            MPI_Send(&source, 1, MPI_INT, source, MESSAGE_TAG, MPI_COMM_WORLD);
            std::cout << "I am the Master, sending to " << source << " this integer: " << source << std::endl;
        }
    }else{
        MPI_Status status;
        int message=0;
        MPI_Recv(&message, 1, MPI_INT, MASTER_RANK, MESSAGE_TAG, MPI_COMM_WORLD, &status );
        std::cout << "I am the Slave " << myrank << " Receiving this integer: " << message << std::endl;
    }
    MPI_Finalize();
    return 0;
}