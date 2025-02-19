# 32 node experiments commands and results

## Environment variables
```
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx
```
## OSU allreduce

### Bare metal
```
time flux run -N32 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce
```
### Usernetes 
```
kubectl apply -f osu.yaml

time flux run -N32 --tasks-per-node=96 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce
```
## OSU barrier

### Bare metal
```
time flux run -N32 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier
```
### Usernetes 
```
kubectl apply -f osu.yaml

time flux run -N32 --tasks-per-node=96 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier
```

## LAMMPS

### Bare metal
```
time flux run -N 32 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec --pwd /opt/lammps/examples/reaxff/HNS --env UCX_NET_DEVICES=mlx5_0:1 usernetes-azure_lammps.sif /usr/bin/lmp -v x 64 -v y 64 -v z 32 -in ./in.reaxff.hns -nocite
```
### Usernetes 
```
kubectl apply -f lammps.yaml

time flux run -N 32 --tasks-per-node=96 -o cpu-affinity=per-task /usr/bin/lmp -v x 64 -v y 64 -v z 32 -in ./in.reaxff.hns -nocite
```

## MiniFE

### Bare metal
```
time flux run -N32 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec --bind /opt:/opt /opt/usernetes-azure_minife.sif miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0
```
### Usernetes
```
kubectl apply -f minife.yaml

time flux run -N32 --tasks-per-node=96 -o cpu-affinity=per-task miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0
```

## AMG

### Bare metal
```
time flux run --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 32 -n 1024 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg.sif amg -n 256 256 128 -P 8 4 2 -problem 2
```
### Usernetes
```
kubectl apply -f amg.yaml

time flux run --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 32 -n 1024 -o cpu-affinity=per-task amg -n 256 256 128 -P 8 4 2 -problem 2
```

## Resnet

### Bare metal
```
time flux run -N32 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec --bind /opt/usernetes-azure --bind /tmp --bind /dev/shm --bind /opt/run/flux --env LOCAL_RANK=0 /opt/usernetes-azure_pytorch.sif python /opt/usernetes-azure/docker/resnet/main.py --backend=mpi --use_syn --batch_size=128 --arch=resnet18
```
### Usernetes
```
kubectl apply -f amg.yaml

time flux run -N32 --tasks-per-node=96 -o cpu-affinity=per-task python /opt/usernetes-azure/docker/resnet-mpi/main.py --backend=mpi --use_syn --batch_size=128 --arch=resnet18
```
