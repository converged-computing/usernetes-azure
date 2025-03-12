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

Edit the Usernetes Makefile to have :
```
export HOSTNAME ?= $(shell hostname | tr 'A-Z' 'a-z')
```

```
Prepull all the containers:
cd /opt
time flux exec -r all singularity pull docker://ghcr.io/converged-computing/usernetes-azure:osu
time flux exec -r all singularity pull docker://ghcr.io/converged-computing/usernetes-azure:lammps
time flux exec -r all singularity pull docker://ghcr.io/converged-computing/usernetes-azure:minife
time flux exec -r all singularity pull docker://ghcr.io/converged-computing/usernetes-azure:amg2023
```
## OSU pt2pt

### Bare metal
```
mkdir -p ./results/osu_pt2pt

chmod +x flux-pt2pt-bare-combinations.sh
./flux-pt2pt-bare-combinations.sh

#wait until all jobs are finished
flux jobs -a

#look at the results see if they're coherent before pushing
./check.sh ./results/osu_pt2pt

./save.sh ./results/osu_pt2pt

oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-osu_pt2pt ./results/osu_pt2pt

```
### Usernetes 
```
mkdir -p ./results/osu_latency
mkdir -p ./results/osu_bw

./flux-pt2pt-usernetes-combinations.sh

#wait until all jobs are finished
flux jobs -a

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
flux jobs -a

./check.sh
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

./check.sh
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
        flux run -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier;
        flux run -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier;
        flux run -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier;
        flux run -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier;
done

#wait until all jobs are finished
flux jobs -a

./check.sh
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

./check.sh
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

#divided into 4 loops to have all the 4 node jobs running at the same time to save time
#flux would not schedule them otherwise
for ((i=1; i<=5; i++)); do 
        flux submit -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task singularity exec --pwd /opt/lammps/examples/reaxff/HNS /opt/usernetes-azure_lammps.sif /usr/bin/lmp -v x 64 -v y 64 -v z 32 -in ./in.reaxff.hns -nocite;
done
for ((i=1; i<=5; i++)); do 
        flux submit -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task singularity exec --pwd /opt/lammps/examples/reaxff/HNS /opt/usernetes-azure_lammps.sif /usr/bin/lmp -v x 64 -v y 64 -v z 32 -in ./in.reaxff.hns -nocite;
done
for ((i=1; i<=5; i++)); do
        flux submit -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task singularity exec --pwd /opt/lammps/examples/reaxff/HNS /opt/usernetes-azure_lammps.sif /usr/bin/lmp -v x 64 -v y 64 -v z 32 -in ./in.reaxff.hns -nocite;
done
for ((i=1; i<=5; i++)); do
        flux submit -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task singularity exec --pwd /opt/lammps/examples/reaxff/HNS /opt/usernetes-azure_lammps.sif /usr/bin/lmp -v x 64 -v y 64 -v z 32 -in ./in.reaxff.hns -nocite; 
done


#wait until all jobs are finished
flux jobs

./check.sh
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
done
for ((i=1; i<=5; i++)); do 
        flux submit -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task /usr/bin/lmp -v x 64 -v y 32 -v z 32 -in ./in.reaxff.hns -nocite;
done
for ((i=1; i<=5; i++)); do 
        flux submit -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task /usr/bin/lmp -v x 64 -v y 32 -v z 32 -in ./in.reaxff.hns -nocite;
done
for ((i=1; i<=5; i++)); do 
        flux submit -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task /usr/bin/lmp -v x 64 -v y 32 -v z 32 -in ./in.reaxff.hns -nocite; 
done

#wait until all jobs are finished
flux jobs

./check.sh
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
flux exec -r XX cat miniFE... > miniFE...

#move output files to output folder
cp miniFE*.yaml $output

./check.sh
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
cp miniFE*.yaml $output

./check.sh
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output
```

## AMG

### Preliminary tests
```
#test without OMP_NUM_THREADS=3 first and look at FOM : if it is better, use this configuration (remove OMP_NUM_THREADS, -n * 3 and adjust -P)

#real	2m44.246s
user	0m0.073s
sys	0m0.033s
time flux run --exclusive -N 4 -n 384 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg2023.sif amg -n 256 256 128 -P 8 8 6 -problem 2
Running with these driver parameters:
  Problem ID    = 2

=============================================
Hypre init times:
=============================================
Hypre init:
  wall clock time = 0.000029 seconds
  Laplacian_7pt:
    (Nx, Ny, Nz) = (2048, 2048, 768)
    (Px, Py, Pz) = (8, 8, 6)

=============================================
Generate Matrix:
=============================================
Spatial Operator:
  wall clock time = 4.368174 seconds
  RHS vector has unit components
  Initial guess is 0
=============================================
IJ Vector Setup:
=============================================
RHS and Initial Guess:
  wall clock time = 0.215981 seconds
=============================================
Problem 2: AMG Setup Time:
=============================================
PCG Setup:
  wall clock time = 62.721547 seconds

FOM_Setup: nnz_AP / Setup Phase Time: 6.199187e+08

=============================================
Problem 2: AMG-PCG Solve Time:
=============================================
PCG Solve:
  wall clock time = 86.212000 seconds

Iterations = 28
Final Relative Residual Norm = 5.829667e-09
FOM_Solve: nnz_AP * iterations / Solve Phase Time: 4.510075e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 1.209938e+08

#real	0m48.913s
user	0m0.074s
sys	0m0.026s
time flux run --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 4 -n 128 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg2023.sif amg -n 256 256 128 -P 8 8 2 -problem 2
Running with these driver parameters:
  Problem ID    = 2

=============================================
Hypre init times:
=============================================
Hypre init:
  wall clock time = 0.000027 seconds
  Laplacian_7pt:
    (Nx, Ny, Nz) = (2048, 2048, 256)
    (Px, Py, Pz) = (8, 8, 2)

=============================================
Generate Matrix:
=============================================
Spatial Operator:
  wall clock time = 1.585996 seconds
  RHS vector has unit components
  Initial guess is 0
=============================================
IJ Vector Setup:
=============================================
RHS and Initial Guess:
  wall clock time = 0.074409 seconds
=============================================
Problem 2: AMG Setup Time:
=============================================
PCG Setup:
  wall clock time = 21.651406 seconds

FOM_Setup: nnz_AP / Setup Phase Time: 5.989061e+08

=============================================
Problem 2: AMG-PCG Solve Time:
=============================================
PCG Solve:
  wall clock time = 23.428831 seconds

Iterations = 22
Final Relative Residual Norm = 9.729440e-09
FOM_Solve: nnz_AP * iterations / Solve Phase Time: 5.534702e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 1.410426e+08

```

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

for ((i=1; i<=5; i++)); do 
        flux submit --setattr=user.study_id=$app-4-iter-$i --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 4 -n 128 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg2023.sif amg -n 256 256 128 -P 8 8 2 -problem 2;
	flux submit --setattr=user.study_id=$app-8-iter-$i --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 8 -n 256 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg2023.sif amg -n 256 256 128 -P 8 8 4 -problem 2;
	flux submit --setattr=user.study_id=$app-16-iter-$i --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 16 -n 512 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg2023.sif amg -n 256 256 128 -P 8 8 8 -problem 2;
	flux submit --setattr=user.study_id=$app-32-iter-$i --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 32 -n 1024 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg2023.sif amg -n 256 256 128 -P 16 8 8 -problem 2;
done

./check.sh
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

./check.sh
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output
```
