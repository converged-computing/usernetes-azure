# Experiments

## OSU

### Test (2 nodes)

#### Container pull
```
time flux exec -r all singularity pull docker://ghcr.io/converged-computing/flux-tutorials:azure-2404-osu
```
#### Bare metal
```
time flux run -N2 -n2 -o cpu-affinity=per-task singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency
```
```
time flux run -N2 -n2 -o cpu-affinity=per-task singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bandwidth
```
```
time flux run -N2 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier
```
```
time flux run -N2 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce
```
#### Usernetes
```
time flux run -N2 -n2 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency
```
```
time flux run -N2 -n2 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_barrier
```
```
time flux run -N2 --tasks-per-node=96 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier
```
```
time flux run -N2 --tasks-per-node=96 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce
```
### Scale

#### Bare metal
```
oras login ghcr.io --username lisejolicoeur
app=osu_latency

for ((i=1; i<=20; i++)); do 
	flux run -N 2 --tasks-per-node=96 --setattr=user.study_id=$app-2-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000002] singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency;
	flux run -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000004] singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency;
	flux run -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000008] singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency;
	flux run -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000009],flux-user00000A,flux-user00000B,flux-user00000C,flux-user00000D,flux-user00000E,flux-user00000F,flux-user00000G singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency;
	flux run -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency;
done


./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output
```

```
oras login ghcr.io --username lisejolicoeur
app=osu_bw

for ((i=1; i<=20; i++)); do 
	flux run -N 2 --tasks-per-node=96 --setattr=user.study_id=$app-2-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000002] singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw;
	flux run -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000004] singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw;
	flux run -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000008] singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw;
	flux run -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000009],flux-user00000A,flux-user00000B,flux-user00000C,flux-user00000D,flux-user00000E,flux-user00000F,flux-user00000G singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw;
	flux run -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw;
done

./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output

```

```
oras login ghcr.io --username lisejolicoeur
app=osu_barrier

for ((i=1; i<=20; i++)); do 
        flux run -N 2 --tasks-per-node=96 --setattr=user.study_id=$app-2-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000002] singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier; 
        flux run -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000004] singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier;
        flux run -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000008] singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier; 
        flux run -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000009],flux-user00000A,flux-user00000B,flux-user00000C,flux-user00000D,flux-user00000E,flux-user00000F,flux-user00000G singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier; 
        flux run -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier; 
done

./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output
```

```
oras login ghcr.io --username lisejolicoeur
app=osu_allreduce

for ((i=1; i<=20; i++)); do 
        flux run -N 2 --tasks-per-node=96 --setattr=user.study_id=$app-2-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000002] singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux run -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000004] singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux run -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000008] singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux run -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000009],flux-user00000A,flux-user00000B,flux-user00000C,flux-user00000D,flux-user00000E,flux-user00000F,flux-user00000G singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux run -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
done

./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output
```


#### Usernetes

```
oras login ghcr.io --username lisejolicoeur
app=osu_latency

for ((i=1; i<=20; i++)); do 
	flux run -N 2 --tasks-per-node=96 --setattr=user.study_id=$app-2-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000002] /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency;
	flux run -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000004] /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency;
	flux run -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000008] /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency;
	flux run -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000009],flux-user00000A,flux-user00000B,flux-user00000C,flux-user00000D,flux-user00000E,flux-user00000F,flux-user00000G /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency;
	flux run -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency;
done


./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output
```

```
oras login ghcr.io --username lisejolicoeur
app=osu_bw

for ((i=1; i<=20; i++)); do 
	flux run -N 2 --tasks-per-node=96 --setattr=user.study_id=$app-2-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000002] /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw;
	flux run -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000004] /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw;
	flux run -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000008] /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw;
	flux run -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000009],flux-user00000A,flux-user00000B,flux-user00000C,flux-user00000D,flux-user00000E,flux-user00000F,flux-user00000G /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw;
	flux run -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw;
done

./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output

```

```
oras login ghcr.io --username lisejolicoeur
app=osu_barrier

for ((i=1; i<=20; i++)); do 
        flux run -N 2 --tasks-per-node=96 --setattr=user.study_id=$app-2-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000002] /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier; 
        flux run -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000004] /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier;
        flux run -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000008] /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier; 
        flux run -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000009],flux-user00000A,flux-user00000B,flux-user00000C,flux-user00000D,flux-user00000E,flux-user00000F,flux-user00000G /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier; 
        flux run -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier; 
done

./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output
```

```
oras login ghcr.io --username lisejolicoeur
app=osu_allreduce

for ((i=1; i<=20; i++)); do 
        flux run -N 2 --tasks-per-node=96 --setattr=user.study_id=$app-2-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000002] /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux run -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000004] /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux run -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000008] /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux run -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task --requires=hosts:flux-user[000001-000009],flux-user00000A,flux-user00000B,flux-user00000C,flux-user00000D,flux-user00000E,flux-user00000F,flux-user00000G /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux run -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
done

./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output
```

## LAMMPS

### Test (2 nodes)

#### Container pull
```
time flux exec -r all singularity pull docker.io/milkshake113/lammps:azure-hpc-2404
```
#### Bare metal
```
#from flux-usernetes aws experiments
time flux run -N 2 --tasks-per-node=96 -c 1 -o cpu-affinity=per-task singularity exec lammps_azure-hpc-2404.sif /usr/bin/lmp -v x 16 -v y 16 -v z 8 -in ./in.reaxff.hns -nocite
```
```
#from performance study experiments
time flux run -N 2 --tasks-per-node=96 -c 1 -o cpu-affinity=per-task singularity exec lammps_azure-hpc-2404.sif /usr/bin/lmp -v x 64 -v y 64 -v z 32 -in ./in.reaxff.hns -nocite
```

#### Usernetes
```
#from flux-usernetes aws experiments
time flux run -N 2 --tasks-per-node=96 -c 1 -o cpu-affinity=per-task /usr/bin/lmp -v x 16 -v y 16 -v z 8 -in ./in.reaxff.hns -nocite
```
```
#from performance study experiments
time flux run -N 2 --tasks-per-node=96 -c 1 -o cpu-affinity=per-task /usr/bin/lmp -v x 64 -v y 64 -v z 32 -in ./in.reaxff.hns -nocite
```
### Scale
#### Bare metal
TODO
#### Usernetes
TODO


## MiniFE

### Test (2 nodes)

#### Container pull
```
time flux exec -r all singularity pull docker.io/milkshake113/minife:azure-hpc-2404
```
#### Bare metal
```
#from performance study experiments
time flux run -N2 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec minife_azure-hpc-2404.sif miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0
```
#### Usernetes
```
#from performance study experiments
time flux run -N2 --tasks-per-node=96 -o cpu-affinity=per-task miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0
```

### Scale
#### Bare metal
TODO
#### Usernetes
TODO


## AMG

### Test (2 nodes)

#### Container pull
```
time flux exec -r all singularity pull docker.io/milkshake113/amg:azure-hpc-2404
```

#### Bare metal
```
#from performance study experiments
time flux run --env OMP_NUM_THREADS=3 -N 2 --tasks-per-node=4 -o cpu-affinity=per-task singularity exec amg_azure-hpc-2404.sif amg -n 32 32 32 -P 2 2 2 -problem 2
```

#### Usernetes
```
#from performance study experiments
time flux run --env OMP_NUM_THREADS=3 -N 2 --tasks-per-node=4 -o cpu-affinity=per-task amg -n 32 32 32 -P 2 2 2 -problem 2
```
### Scale
#### Bare metal
TODO
#### Usernetes
TODO


## RESNET

### Test (2 nodes)

#### Container pull
```
time flux exec -r all singularity pull docker.io/milkshake113/resnet:azure-hpc-2404
```

#### Bare metal
TODO
#### Usernetes
TODO
### Scale
#### Bare metal
TODO
#### Usernetes
TODO