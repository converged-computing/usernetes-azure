# 32 node experiments commands and results

## Environment variables
```
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx

oras login ghcr.io --username lisejolicoeur

```
## OSU pt2pt

### Bare metal
```
mkdir -p ./results/osu_latency
mkdir -p ./results/osu_bw

./flux-pt2pt-bare-combinations.sh

#wait until all jobs are finished
flux jobs

#look at the results see if they're coherent before pushing
./check.sh ./results/osu_latency
./check.sh ./results/osu_bw

./save.sh ./results/osu_latency
./save.sh ./results/osu_bw

oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-osu_latency ./results/osu_latency
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-osu_bw ./results/osu_bw

```
### Usernetes 
```
mkdir -p ./results/osu_latency
mkdir -p ./results/osu_bw

./flux-pt2pt-usernetes-combinations.sh

#wait until all jobs are finished
flux jobs

#look at the results see if they're coherent before pushing
./check.sh ./results/osu_latency
./check.sh ./results/osu_bw

./save.sh ./results/osu_latency
./save.sh ./results/osu_bw

oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-osu_latency ./results/osu_latency
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-osu_bw ./results/osu_bw
```


## OSU allreduce

### Bare metal
```
app=osu_allreduce
output=./results/$app
mkdir -p $output

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

for ((i=1; i<=5; i++)); do 
        flux submit -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux submit -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux submit -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux submit -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
done

#wait until all jobs are finished
flux jobs

./check.sh $output
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output
```
### Usernetes 
```
kubectl apply -f osu.yaml
kubectl exec -ti XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local

app=osu_allreduce
output=./results/$app
mkdir -p $output

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

for ((i=1; i<=5; i++)); do 
        flux submit -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux submit -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux submit -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux submit -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
done

#wait until all jobs are finished
flux jobs

./check.sh $output
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output
```
## OSU barrier

### Bare metal
```
app=osu_barrier
output=./results/$app
mkdir -p $output

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

for ((i=1; i<=5; i++)); do 
        flux submit -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier;
        flux submit -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier;
        flux submit -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier;
        flux submit -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier;
done

#wait until all jobs are finished
flux jobs

./check.sh $output
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output
```

### Usernetes 

```
kubectl apply -f osu.yaml
kubectl exec -ti XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local

app=osu_barrier
output=./results/$app
mkdir -p $output

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

for ((i=1; i<=5; i++)); do 
        flux submit -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier;
        flux submit -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier; 
        flux submit -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier; 
        flux submit -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier; 
done

#wait until all jobs are finished
flux jobs

./check.sh $output
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output
```

## LAMMPS

### Bare metal
```
app=lammps
output=./results/$app
mkdir -p $output

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

for ((i=1; i<=5; i++)); do 
        flux submit -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task singularity exec --pwd /opt/lammps/examples/reaxff/HNS /opt/usernetes-azure_lammps.sif /usr/bin/lmp -v x 64 -v y 64 -v z 32 -in ./in.reaxff.hns -nocite;
        flux submit -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task singularity exec --pwd /opt/lammps/examples/reaxff/HNS /opt/usernetes-azure_lammps.sif /usr/bin/lmp -v x 64 -v y 64 -v z 32 -in ./in.reaxff.hns -nocite; 
        flux submit -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task singularity exec --pwd /opt/lammps/examples/reaxff/HNS /opt/usernetes-azure_lammps.sif /usr/bin/lmp -v x 64 -v y 64 -v z 32 -in ./in.reaxff.hns -nocite; 
        flux submit -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task singularity exec --pwd /opt/lammps/examples/reaxff/HNS /opt/usernetes-azure_lammps.sif /usr/bin/lmp -v x 64 -v y 64 -v z 32 -in ./in.reaxff.hns -nocite; 
done


#wait until all jobs are finished
flux jobs

./check.sh $output
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output
```
### Usernetes 
```
kubectl apply -f lammps.yaml
kubectl exec -ti XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local

app=lammps
output=./results/$app
mkdir -p $output

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

for ((i=1; i<=5; i++)); do 
        flux submit -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task /usr/bin/lmp -v x 64 -v y 32 -v z 32 -in ./in.reaxff.hns -nocite;
        flux submit -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task /usr/bin/lmp -v x 64 -v y 32 -v z 32 -in ./in.reaxff.hns -nocite; 
        flux submit -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task /usr/bin/lmp -v x 64 -v y 32 -v z 32 -in ./in.reaxff.hns -nocite; 
        flux submit -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task /usr/bin/lmp -v x 64 -v y 32 -v z 32 -in ./in.reaxff.hns -nocite; 
done

#wait until all jobs are finished
flux jobs

./check.sh $output
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output
```

## MiniFE

### Bare metal
```
app=minife
output=./results/$app
mkdir -p $output

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

for ((i=1; i<=5; i++)); do 
        flux submit -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task singularity exec --bind /opt:/opt /opt/usernetes-azure_minife.sif miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0;
        flux submit -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task singularity exec --bind /opt:/opt /opt/usernetes-azure_minife.sif miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0; 
        flux submit -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task singularity exec --bind /opt:/opt /opt/usernetes-azure_minife.sif miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0; 
        flux submit -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task singularity exec --bind /opt:/opt /opt/usernetes-azure_minife.sif miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0; 
done

#fetch all yaml output files from nodes on the cluster
flux exec -r all ...

#move output files to output folder
mv miniFE*.yaml $output

./check.sh $output
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output
```
### Usernetes
```
kubectl apply -f minife.yaml
kubectl exec -ti XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local

app=minife
output=./results/$app
mkdir -p $output

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

for ((i=1; i<=5; i++)); do 
        flux submit -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0;
        flux submit -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0; 
        flux submit -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0; 
        flux submit -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0; 
done

#fetch all yaml output files from nodes on the cluster
flux exec -r all ...

#move output files to output folder
mv miniFE*.yaml $output

./check.sh $output
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output
```

## AMG

### Bare metal
```
app=amg
output=./results/$app
mkdir -p $output

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

#test without OMP_NUM_THREADS=3 first and look at FOM : if it is better, use this configuration (remove OMP_NUM_THREADS, -n * 3 and adjust -P)
flux run --cores-per-task 3 --exclusive -N 4 -n 384 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg2023.sif amg -n 256 256 128 -P 8 8 6 -problem 2;

for ((i=1; i<=5; i++)); do 
        flux submit --setattr=user.study_id=$app-4-iter-$i --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 4 -n 128 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg2023.sif amg -n 256 256 128 -P 8 8 2 -problem 2;
	flux submit --setattr=user.study_id=$app-8-iter-$i --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 8 -n 256 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg2023.sif amg -n 256 256 128 -P 8 8 4 -problem 2;
	flux submit --setattr=user.study_id=$app-16-iter-$i --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 16 -n 512 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg2023.sif amg -n 256 256 128 -P 8 8 8 -problem 2;
	flux submit --setattr=user.study_id=$app-32-iter-$i --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 32 -n 1024 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg2023.sif amg -n 256 256 128 -P 16 8 8 -problem 2;
done

./check.sh $output
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output
```
### Usernetes
```
kubectl apply -f amg.yaml
kubectl exec -ti XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local

app=amg
output=./results/$app
mkdir -p $output

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

for ((i=1; i<=5; i++)); do 
  flux submit --setattr=user.study_id=$app-4-iter-$i --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 4 -n 128 -o cpu-affinity=per-task amg -n 256 256 128 -P 8 8 2 -problem 2;
	flux submit --setattr=user.study_id=$app-8-iter-$i --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 8 -n 256 -o cpu-affinity=per-task amg -n 256 256 128 -P 8 8 4 -problem 2;
	flux submit --setattr=user.study_id=$app-16-iter-$i --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 16 -n 512 -o cpu-affinity=per-task amg -n 256 256 128 -P 8 8 8 -problem 2;
	flux submit --setattr=user.study_id=$app-32-iter-$i --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 32 -n 1024 -o cpu-affinity=per-task amg -n 256 256 128 -P 16 8 8 -problem 2;
done

./check.sh $output
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output
```
