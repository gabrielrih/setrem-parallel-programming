# Using multiple VMs to run parallel code (Cluster of workstations)

We are basically deploying a cluster of workstations to run and test parallel code.

## Stack:
- [Oracle Virtual Box](https://www.virtualbox.org/)
- [Network: Host-Only Adapter and NAT](https://download.virtualbox.org/virtualbox/7.0.14/UserManual.pdf)
- [Ubuntu Server 22.04.3](https://ubuntu.com/download/server)
- [NFS](https://en.wikipedia.org/wiki/Network_File_System)
- [OpenMPI](https://github.com/open-mpi/ompi)

## Architecture:

![](.drawio.png)

## Virtual Machines setup

### Network configuration
First of all, we must create, on Virtual Box, two network interfaces in each Virtual Machine:
- The first one must use the "Host-Only Adapter". This interface is to allow the machines to communicate between each other using _Static IP Addresses_.
- And the second one should use NAT. This interface is necessary to virtual machines communicate with the Internet.

On each virtual machine, we must configure an Static IP Address for the first interface and configure DHCP to the second one (NAT interface).

To identify the interfaces just run:
```sh
ls /sys/class/net
```

Then...
```sh
cd /etc/netplan
sudo cp 00-installer-config.yaml 00-installer-config.yaml.old
sudo vim 00-installer-config.yaml
```

Within the _00-installer-config.yaml_ you must define a YAML configuring the desired configuration.

> You must change the interface names and the IP address as needed.

```yaml
network:
	ethernets:
		enp0s3:
			dhcp4: false
			addresses: [192.168.56.101/24]
		enp0s8:
			dhcp4: true
			nameservers:
				addresses: [1.1.1.1,8.8.8.8]
```

Finally, just apply the changes and you can check the changes:
```sh
sudo netplan apply
ifconfig
```

When you have the network configuration configured in all the virtual machines you can change the hostname of each machine and change the _/etc/hosts_ file:

> Here, you can put meaninfull names. Like, primary, secondary1, secondary2, etc.

```sh
sudo vim /etc/hostname
```

Then, you can set the hostname VS ip address in the _/etc/hosts_ file and then restart the vm.

```sh
sudo vim /etc/hosts
```

```conf
# workstation cluster
192.168.56.101	secondary1
192.168.56.102	secondary2
192.168.56.103	secondary3
192.168.56.200	primary
```

### Creating user for OpenMPI

We must create a new user to be used by OpenMPI.

```sh
sudo adduser mpihpc --uid 7777
sudo usermod -aG sudo mpihpc
```

Then, you must login with this new user and create a SSH key.

> You must keep the SSH key without password.

```sh
su - mpihpc
ssh-keygen -t rsa -b 4096
```

Now, you must send this key to the others virtual machines. For example, if you are using the _primary_, we commands you should run are:
```sh
su - mpihpc
ssh-copy-id secondary1
ssh-copy-id secondary2
ssh-copy-id secondary3
```

> Note that to run ssh-copy-id command, the user mpihpc should be created in all the vms.

To try the connection you must run the command below. Note that it shouldn't ask you for the password.
```sh
ssh <hostname>
```

### NFS server

We must configure a NFS server in the _primary_ vm and NFS client on the _secondaries_.

__On the primary__, we should install _nfs-kernel-server_:

```sh
su - mpihpc
sudo apt-get install nfs-kernel-server
```

Then, you should create a folder called _shared_ on _/home/mpihpc/_ and then configure this folder has a shared storage available in the LAN:
```sh
su - mpihpc
mkdir shared
sudo vim /etc/exports
exportfs -a
```

This is the content to put inside _exportfs -a_
```conf
/home/mpihpc/shared *(rw,sync,no_root_squash,no_subtree_check)
```

Restart NFS service:
```sh
sudo service nfs-kernel-server restart
```

To show the shared folders run:
```sh
exportfs -s
```

### NFS client

__On each secondary__, we should install _nfs-common_:
```sh
su - mpihpc
sudo apt-get install nfs-common
```

Create the _shared_ folder, the same way we did on primary, and then map it on _/etc/fstab_.
```sh
su - mpihpc
mkdir shared
sudo vim /etc/fstab
```

This is the content to put inside _/etc/fstab_:
```conf
primary:/home/mpihpc/shared /home/mpihpc/shared nfs
```

Finally, we just mount the volumes using this command:
```sh
sudo mount -a
```

To check if it worked just run the command below. You should be able to see the _/home/mpihpc/shared_ folder.
```sh
df -h
```

### OpenMPI

__In all machines__, we must install the OpenMPI library.
```sh
sudo apt-get install openmpi-bin openmpi-common libopenmpi-dev
```


__On the primary__, we must install the OpenMPI library.
... and must create a _.cluster_hostfile_ to be used by OpenMPI.
```sh
su - mpihpc
cat <<EOT >> /home/mpihpc/.cluster_hostfile
primary
secondary1
secondary2
secondary3
EOT
```

#### Running code in the same machine

Creating the source code:
```sh
su - mpihpc
vi example.cpp
```

```c++
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
```

Compiling:
```sh
mpic++ -O3 -Wall -std=c++1y example.cpp -o output
```

Running the code in the same machine:
```sh
mpirun -np 3 ./output
```

> Note that in this case the _mpirun_ are running the code in three different processes but all of them in the same machine. Another important thing is that each process is created in a differente vCore, so, in the case, the VM must have thre or more vCores.


#### Running code to run in multiple machines

Creating the source code:
```sh
su - mpihpc
vi example_cluster.cpp
```

```c++
#include <mpi.h>
#include <iostream>
#include <stdlib.h>
#include <string.h>

char *getCommandResult(const char *cmd){
	if (cmd == NULL) return NULL;
	FILE *pipe = popen(cmd, "r");
	char *data = (char *) malloc(sizeof(char) * 2566);
	char *bf = (char *) malloc(sizeof(char) * 256);
	if (pipe) {
		while (fgets(bf, 256, pipe) != NULL) strcat(data,bf);
		pclose(pipe);
	}else{
		perror("popen");
		pclose(pipe);
		return NULL;
	}
	free(bf);
	return data;
}
int main(int argc, char **argv){
	int myrank, //who am i
	numprocs; //how many process

	MPI_Init(&argc,&argv);
	MPI_Comm_rank(MPI_COMM_WORLD,&myrank);
	MPI_Comm_size(MPI_COMM_WORLD,&numprocs);

	char buff[256];
	sprintf(buff,"hostname && gcc --version");
	char *dat = getCommandResult("hostname && gcc --version");
	std::cout << "myrank: " << myrank << " of " << numprocs << " -> " << dat << std::endl;

	MPI_Finalize();
	return 0;
}
```

Compiling:
```sh
mpic++ -O3 -Wall -std=c++1y example_cluster.cpp -o output
```

Running the code in multiple machines:
```sh
mpirun -np 4 --machinefile /home/mpihpc/.cluster_hostfile ./output
```

> Note that in this case the _mpirun_ are running using four different processes. By default, each process are allocated in a different vCore. If the -np value is bigger than the number of vCores in all the cluster, the default behavior is to generate an error.