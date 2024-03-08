from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
numProc = comm.Get_size()


if rank == 0:
    dado = "eu "
    for destino in range(1, numProc):
        comm.send(dado+str(destino), dest=destino)

else:
    data = comm.recv(source=0)
    print("I am ", rank, "Received: ", data)
