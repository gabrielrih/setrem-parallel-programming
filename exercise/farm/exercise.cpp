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

// Farm pattern: ranks
const int EMMITER_RANK = 0;
const int COLLECTOR_RANK = 1;
const int WORKERS_QUANTITY = 2;

const int MESSAGE_TAG=0;

int main(int argc, char *argv []){
    int myrank, //who am i
    numprocs; //how many process
    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&myrank);
    MPI_Comm_size(MPI_COMM_WORLD,&numprocs);

    // Validation
    int min_of_processes=WORKERS_QUANTITY + 2;  // emitter, collector and workers
    if (numprocs < min_of_processes) {
        throw std::invalid_argument("The quantity of informed processes are to low!");
        MPI_Finalize();
        return 1;
        //exit(1);
    }

    // Create the workers rank
    if (myrank == EMMITER_RANK) { // Run on emitter, send message to the workers
        std::cout << "Number of processes " << numprocs << std::endl;
        int worker_rank;
        for(int worker = 0; worker < WORKERS_QUANTITY; worker++) { // send message to each work
            worker_rank = worker + 2;  // this is because the rank 0 and 1 are used by the emitter and collector
            int message = 2;  // any message, just for testing
            MPI_Send(&message, 1, MPI_INT, worker_rank, MESSAGE_TAG, MPI_COMM_WORLD);
            std::cout << "I am the emitter, sending to the worker " << worker_rank << " this message: " << message << std::endl;
        }
    }
    else if (myrank == COLLECTOR_RANK) { // Run on collector, it's done
        //MPI_Status status;
        //int message = 0;
        //for(auto worker: WORKERS_RANK) {  // receive message from every single worker
            //MPI_Recv(&message, 1, MPI_INT, worker, MESSAGE_TAG, MPI_COMM_WORLD, &status);
            //std::cout << "I am the collector and I received from worker " << worker << " this message: " << message << std::endl;
        //}
        std::cout << "I am the collector!" << std::endl;
    }
    else { // Run on workers, send message to collector
        MPI_Status status;
        int message = 0;
        MPI_Recv(&message, 1, MPI_INT, EMMITER_RANK, MESSAGE_TAG, MPI_COMM_WORLD, &status);
        std::cout << "I am the worker " << myrank << ", receiving this message: " << message << std::endl;
        // Do the work
        //int final_message = message * 10;
        // Sending message to the collector
        //MPI_Send(&final_message, 1, MPI_INT, COLLECTOR_RANK, MESSAGE_TAG, MPI_COMM_WORLD);
        //std::cout << "I am the worker " << myrank << " and the message was sent to the collector" << std::endl;
    }
    MPI_Finalize();
    return 0;
}