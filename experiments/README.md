# Experiments

### Scale experiments actions
- launch 32 node cluster
- prepull all containers (osu, lammps, amg, minife)
- create save.sh
- oras login ghcr.io --username lisejolicoeur
- launch benchmarks in order with oras push at the end of each
- create Usernetes cluster
- launch benchmarks for each

save.sh
```
#!/bin/bash
output=$1

# When they are done:
for jobid in $(flux jobs -a --json | jq -r .jobs[].id)
  do
    # Get the job study id
    study_id=$(flux job info $jobid jobspec | jq -r ".attributes.user.study_id")    
    if [[ -f "$output/${study_id}-${jobid}.out" ]] || [[ "$study_id" == "null" ]]; then
        continue
    fi
    echo "Parsing jobid ${jobid} and study id ${study_id}"
    flux job attach $jobid &> $output/${study_id}-${jobid}.out 
    echo "START OF JOBSPEC" >> $output/${study_id}-${jobid}.out 
    flux job info $jobid jobspec >> $output/${study_id}-${jobid}.out 
    echo "START OF EVENTLOG" >> $output/${study_id}-${jobid}.out 
    flux job info $jobid guest.exec.eventlog >> $output/${study_id}-${jobid}.out
done
```
check.sh
```
#!/bin/bash
output=$1

# When they are done:
for jobid in $(flux jobs -a --json | jq -r .jobs[].id)
  do
    # Get the job study id
    study_id=$(flux job info $jobid jobspec | jq -r ".attributes.user.study_id")    
    if [[ -f "$output/${study_id}-${jobid}.out" ]] || [[ "$study_id" == "null" ]]; then
        continue
    fi
    flux job info $jobid guest.exec.eventlog
echo "---------------------------------------"
done
```


## OSU

### Test (2 nodes)

#### Container pull
```
cd /opt
time flux exec -r all singularity pull docker://ghcr.io/converged-computing/usernetes-azure:osu
real	2m33.207s
user	0m0.007s
sys	0m0.009s
```

#### Environment variables
```
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx

flux run -N1 -n1 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif env | grep UCX

UCX_NET_DEVICES=mlx5_0:1
UCX_TLS=rc,sm

flux run -N1 -n1 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif env | grep OMPI

OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_btl_vader_backing_directory=/opt/run/flux/jobtmp-0-ƒ4bo9NTSf
OMPI_MCA_pml=ucx
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx
```
#### Bare metal
```
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

time flux run -N2 -n2 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency

[ 3420.098285] infiniband mlx5_1: create_qp:3323:(pid 300371): Create QP type 2 failed
....
# OSU MPI Latency Test v5.8
# Size          Latency (us)
0                       1.61
1                       1.61
2                       1.61
4                       1.61
8                       1.61
16                      1.62
32                      1.75
64                      1.78
128                     1.82
256                     2.35
512                     2.45
1024                    2.59
2048                    2.77
4096                    3.55
8192                    4.09
16384                   5.38
32768                   6.97
65536                   9.46
131072                 14.46
262144                 17.62
524288                 28.48
1048576                49.98
2097152                93.80
4194304               179.11

real    0m2.194s
user    0m0.077s
```
```
time flux run -N2 -n2 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw

[ 3420.098285] infiniband mlx5_1: create_qp:3323:(pid 300371): Create QP type 2 failed
....
# OSU MPI Bandwidth Test v5.8
# Size      Bandwidth (MB/s)
1                       3.88
2                       7.92
4                      16.14
8                      31.91
16                     63.71
32                    127.70
64                    247.02
128                   493.01
256                   940.30
512                  1765.59
1024                 3381.33
2048                 6057.63
4096                 9050.88
8192                13470.27
16384               14390.78
32768               20167.41
65536               22544.32
131072              23722.18
262144              24238.68
524288              24454.23
1048576             24562.45
2097152             24617.71
4194304             24453.38

real    0m1.162s
user    0m0.078s
sys     0m0.024s
```
```
# --env UCX_NET_DEVICES=mlx5_0:1 does not remove the warning thrown at execution
time flux run -N2 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier

[ 3420.098285] infiniband mlx5_1: create_qp:3323:(pid 300371): Create QP type 2 failed
....
# OSU MPI Barrier Latency Test v5.8
# Avg Latency(us)
             8.32

real    0m7.045s
user    0m0.077s
sys     0m0.026s
```
```
time flux run -N2 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce

[ 3420.098285] infiniband mlx5_1: create_qp:3323:(pid 300371): Create QP type 2 failed
....
# OSU MPI Allreduce Latency Test v5.8
# Size       Avg Latency(us)
4                      10.08
8                       9.57
16                      9.18
32                     11.45
64                     12.13
128                    18.39
256                    17.15
512                    19.77
1024                   22.67
2048                   27.75
4096                   54.32
8192                  326.91
16384                 104.84
32768                 418.40
65536                 157.01
131072               2041.94
262144                505.41
524288               1023.61
1048576              2066.89

real    0m9.502s
user    0m0.082s
sys     0m0.027s
```
#### Usernetes

Shell into the Usernetes container once the cluster is up:
```
kubectl apply -f crd/osu.yaml

(Pulling    2m6s   kubelet            Pulling image "ghcr.io/converged-computing/usernetes-azure:osu"
Pulled     37s    kubelet            Successfully pulled image "ghcr.io/converged-computing/usernetes-azure:osu" in 1m29.121s (1m29.121s including waiting). Image size: 2164616929 bytes.)

kubectl exec -ti flux-sample-0-XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local
```

Run the tests:
```
time flux run -N2 -n2 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency

# OSU MPI Latency Test v5.8
# Size          Latency (us)
0                       1.62
1                       1.61
2                       1.61
4                       1.61
8                       1.61
16                      1.62
32                      1.76
64                      1.82
128                     1.86
256                     2.37
512                     2.45
1024                    2.62
2048                    2.81
4096                    3.56
8192                    4.07
16384                   5.37
32768                   6.89
65536                   9.41
131072                 14.17
262144                 17.43
524288                 28.06
1048576                49.68
2097152                92.27
4194304               178.10

real    0m1.996s
user    0m0.073s
sys     0m0.025s
```
```
time flux run -N2 -n2 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw

# OSU MPI Bandwidth Test v5.8
# Size      Bandwidth (MB/s)
1                       3.82
2                       7.62
4                      14.95
8                      30.77
16                     61.87
32                    127.18
64                    242.34
128                   481.50
256                   930.58
512                  1722.17
1024                 3325.32
2048                 5982.11
4096                 9165.93
8192                13353.16
16384               14758.96
32768               21150.72
65536               22706.13
131072              23693.80
262144              24085.29
524288              24440.12
1048576             24552.39
2097152             24641.75
4194304             24648.26

real    0m0.992s
user    0m0.075s
sys     0m0.021s
```
```
time flux run -N2 --tasks-per-node=96 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier

# OSU MPI Barrier Latency Test v5.8
# Avg Latency(us)
             8.94

real    0m3.784s
user    0m0.073s
sys     0m0.029s
```
```
time flux run -N2 --tasks-per-node=96 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce

# OSU MPI Allreduce Latency Test v5.8
# Size       Avg Latency(us)
4                       9.99
8                      10.28
16                      9.79
32                     12.25
64                     12.98
128                    19.79
256                    18.03
512                    20.43
1024                   24.46
2048                   28.55
4096                   63.48
8192                  310.34
16384                 110.35
32768                 422.45
65536                 156.50
131072               1999.21
262144                608.51
524288               1080.29
1048576              2163.43

real    0m7.057s
user    0m0.077s
sys     0m0.029s
```
### Scale

#### Bare metal

flux-run-combinations.sh
```
app=osu_latency
output=./results/$app
mkdir -p $output

# At most 28 combinations, 8 nodes 2 at a time
hosts=$(flux run -N 32 hostname | shuf -n 8 | tr '\n' ' ')
list=${hosts}

dequeue_from_list() {
  shift;
  list=$@
}

iter=0
for i in $hosts; do
  dequeue_from_list $list
  for j in $list; do
    echo "${i} ${j}"
    time flux submit run -N 2 -n 2 \
      --setattr=user.study_id=$app-2-iter-$iter \
      --requires="hosts:${i},${j}" \
      -o cpu-affinity=per-task \
      singularity exec /opt/usernetes-azure_osu.sif \
      /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency
    time flux submit -N 2 -n 2 \
      --setattr=user.study_id=$app-2-iter-$iter \
      --requires="hosts:${i},${j}" \
      -o cpu-affinity=per-task \
      singularity exec /opt/usernetes-azure_osu.sif \
      /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw
    iter=$((iter+1))
done
done

./check.sh
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output
```

```
oras login ghcr.io --username lisejolicoeur
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

./check.sh
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output
```

```
oras login ghcr.io --username lisejolicoeur
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

./check.sh
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output
```


#### Usernetes

```
oras login ghcr.io --username lisejolicoeur
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

./check.sh
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output
```

```
oras login ghcr.io --username lisejolicoeur
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

./check.sh
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output
```

## LAMMPS

### Test (2 nodes)

#### Container pull
```
cd /opt
time flux exec -r all singularity pull docker://ghcr.io/converged-computing/usernetes-azure:lammps
real	2m5.881s
user	0m0.006s
sys	0m0.011s
```
#### Bare metal
```
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx

#from flux-usernetes aws experiments
time flux run -N 2 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec --pwd /opt/lammps/examples/reaxff/HNS --env UCX_NET_DEVICES=mlx5_0:1 usernetes-azure_lammps.sif /usr/bin/lmp -v x 16 -v y 16 -v z 8 -in ./in.reaxff.hns -nocite

[ 3420.098285] infiniband mlx5_1: create_qp:3323:(pid 300371): Create QP type 2 failed
....
WARNING on proc 0: Cannot open log.lammps for writing: Read-only file system (src/lammps.cpp:511)
LAMMPS (17 Apr 2024 - Development - a8687b5)
OMP_NUM_THREADS environment is not set. Defaulting to 1 thread. (src/comm.cpp:98)
  using 1 OpenMP thread(s) per MPI task
Reading data file ...
  triclinic box = (0 0 0) to (22.326 11.1412 13.778966) with tilt (0 -5.02603 0)
  8 by 4 by 6 MPI processor grid
  reading atoms ...
  304 atoms
  reading velocities ...
  304 velocities
  read_data CPU = 0.127 seconds
Replication is creating a 16x16x8 = 2048 times larger system...
  triclinic box = (0 0 0) to (357.216 178.2592 110.23173) with tilt (0 -40.20824 0)
  8 by 6 by 4 MPI processor grid
  bounding box image = (0 -1 -1) to (0 1 1)
  bounding box extra memory = 0.03 MB
  average # of replicas added to proc = 46.75 out of 2048 (2.28%)
  622592 atoms
  replicate CPU = 0.015 seconds
Neighbor list info ...
  update: every = 20 steps, delay = 0 steps, check = no
  max neighbors/atom: 2000, page size: 100000
  master list distance cutoff = 11
  ghost atom cutoff = 11
  binsize = 5.5, bins = 73 33 21
  2 neighbor lists, perpetual/occasional/extra = 2 0 0
  (1) pair reaxff, perpetual
      attributes: half, newton off, ghost
      pair build: half/bin/ghost/newtoff
      stencil: full/ghost/bin/3d
      bin: standard
  (2) fix qeq/reax, perpetual, copy from (1)
      attributes: half, newton off
      pair build: copy
      stencil: none
      bin: none
Setting up Verlet run ...
  Unit style    : real
  Current step  : 0
  Time step     : 0.1
Per MPI rank memory allocation (min/avg/max) = 252.5 | 252.7 | 253 Mbytes
   Step          Temp          PotEng         Press          E_vdwl         E_coul         Volume    
         0   300           -113.27833      439.01454     -111.57687     -1.7014647      7019230      
        10   300.6458      -113.28009      687.89553     -111.57866     -1.7014301      7019230      
        20   302.20326     -113.2846       1467.4879     -111.58328     -1.701318       7019230      
        30   302.31937     -113.28481      4051.081      -111.58371     -1.7010939      7019230      
        40   300.51347     -113.27935      6235.4715     -111.57858     -1.7007736      7019230      
        50   297.61214     -113.27065      6426.6131     -111.57024     -1.7004134      7019230      
        60   295.0453      -113.26295      6236.1432     -111.5629      -1.7000496      7019230      
        70   294.72697     -113.26195      6937.5805     -111.56227     -1.6996827      7019230      
        80   297.50375     -113.27022      8342.3188     -111.57091     -1.6993152      7019230      
        90   301.3484      -113.28168      9484.1542     -111.5827      -1.6989854      7019230      
       100   302.48622     -113.28501      10463.506     -111.58627     -1.6987438      7019230      
Loop time of 37.0552 on 192 procs for 100 steps with 622592 atoms

Performance: 0.023 ns/day, 1029.311 hours/ns, 2.699 timesteps/s, 1.680 Matom-step/s
99.9% CPU use with 192 MPI tasks x 1 OpenMP threads

MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 20.653     | 23.087     | 25.919     |  20.5 | 62.30
Neigh   | 0.36974    | 0.37636    | 0.3904     |   0.6 |  1.02
Comm    | 0.043263   | 2.4378     | 5.2333     |  65.7 |  6.58
Output  | 0.0013471  | 0.11683    | 0.28654    |  20.5 |  0.32
Modify  | 10.7       | 11.035     | 11.913     |  10.9 | 29.78
Other   |            | 0.002731   |            |       |  0.01

Nlocal:        3242.67 ave        3264 max        3217 min
Histogram: 13 27 21 2 2 10 38 49 22 8
Nghost:        12106.8 ave       12139 max       12070 min
Histogram: 3 9 24 20 20 27 40 32 14 3
Neighs:    1.07024e+06 ave  1.0764e+06 max 1.06275e+06 min
Histogram: 15 24 19 5 2 8 47 41 21 10

Total # of neighbors = 2.0548535e+08
Ave neighs/atom = 330.04817
Neighbor list builds = 5
Dangerous builds not checked
Total wall time: 0:00:38

real    0m44.051s
user    0m0.080s
sys     0m0.059s

```
```
#from performance study experiments
time flux run -N 2 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec --pwd /opt/lammps/examples/reaxff/HNS usernetes-azure_lammps.sif /usr/bin/lmp -v x 64 -v y 64 -v z 32 -in ./in.reaxff.hns -nocite

230.432s: flux-shell[1]: ERROR: oom: Memory cgroup out of memory: killed 1 task on flux-user000001.
230.474s: flux-shell[1]: ERROR: oom: memory.peak = 444.927G
261.098s: flux-shell[0]: FATAL: doom: rank 102 on host flux-user000001 exited and exit-timeout=30s has expired
261.446s: job.exception type=exec severity=0 rank 102 on host flux-user000001 exited and exit-timeout=30s has expired
flux-job: task(s) Killed

real	4m46.656s
user	0m0.076s
sys	0m0.086s
```

```
#real	4m17.421s
user	0m0.078s
sys	0m0.028s
time flux run -N 4 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec --pwd /opt/lammps/examples/reaxff/HNS usernetes-azure_lammps.sif /usr/bin/lmp -v x 32 -v y 32 -v z 32 -in ./in.reaxff.hns -nocite
LAMMPS (17 Apr 2024 - Development - a8687b5)
OMP_NUM_THREADS environment is not set. Defaulting to 1 thread. (src/comm.cpp:98)
  using 1 OpenMP thread(s) per MPI task
Reading data file ...
  triclinic box = (0 0 0) to (22.326 11.1412 13.778966) with tilt (0 -5.02603 0)
  8 by 6 by 8 MPI processor grid
  reading atoms ...
  304 atoms
  reading velocities ...
  304 velocities
  read_data CPU = 0.290 seconds
Replication is creating a 32x32x32 = 32768 times larger system...
  triclinic box = (0 0 0) to (714.432 356.5184 440.92691) with tilt (0 -160.83296 0)
  8 by 6 by 8 MPI processor grid
  bounding box image = (0 -1 -1) to (0 1 1)
  bounding box extra memory = 0.03 MB
  average # of replicas added to proc = 203.02 out of 32768 (0.62%)
  9961472 atoms
  replicate CPU = 0.094 seconds
Neighbor list info ...
  update: every = 20 steps, delay = 0 steps, check = no
  max neighbors/atom: 2000, page size: 100000
  master list distance cutoff = 11
  ghost atom cutoff = 11
  binsize = 5.5, bins = 160 65 81
  2 neighbor lists, perpetual/occasional/extra = 2 0 0
  (1) pair reaxff, perpetual
      attributes: half, newton off, ghost
      pair build: half/bin/ghost/newtoff
      stencil: full/ghost/bin/3d
      bin: standard
  (2) fix qeq/reax, perpetual, copy from (1)
      attributes: half, newton off
      pair build: copy
      stencil: none
      bin: none
Setting up Verlet run ...
  Unit style    : real
  Current step  : 0
  Time step     : 0.1
Per MPI rank memory allocation (min/avg/max) = 1077 | 1077 | 1078 Mbytes
   Step          Temp          PotEng         Press          E_vdwl         E_coul         Volume    
         0   300           -113.27833      439.02012     -111.57687     -1.7014647      1.1230768e+08
        10   300.79322     -113.28052      814.31332     -111.57908     -1.7014379      1.1230768e+08
        20   302.45257     -113.28533      1685.6286     -111.584       -1.7013293      1.1230768e+08
        30   302.59441     -113.28563      4263.3992     -111.58452     -1.7011034      1.1230768e+08
        40   300.64312     -113.27973      6364.2243     -111.57896     -1.7007792      1.1230768e+08
        50   297.45605     -113.27019      6459.1292     -111.56978     -1.7004157      1.1230768e+08
        60   294.76611     -113.26213      6171.9565     -111.56208     -1.7000481      1.1230768e+08
        70   294.67237     -113.26181      6799.0872     -111.56213     -1.6996741      1.1230768e+08
        80   297.76439     -113.271        8195.6183     -111.5717      -1.6992976      1.1230768e+08
        90   301.6648      -113.28262      9358.909      -111.58366     -1.6989612      1.1230768e+08
       100   302.60489     -113.28537      10365.143     -111.58666     -1.6987176      1.1230768e+08
Loop time of 245.531 on 384 procs for 100 steps with 9961472 atoms

Performance: 0.004 ns/day, 6820.318 hours/ns, 0.407 timesteps/s, 4.057 Matom-step/s
100.0% CPU use with 384 MPI tasks x 1 OpenMP threads

MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 140.9      | 152.05     | 161.33     |  27.1 | 61.93
Neigh   | 1.6944     | 1.7248     | 1.7666     |   1.4 |  0.70
Comm    | 0.34477    | 7.5669     | 20.352     | 140.9 |  3.08
Output  | 0.037987   | 0.68973    | 1.3134     |  34.4 |  0.28
Modify  | 81.436     | 83.486     | 87.029     |  20.0 | 34.00
Other   |            | 0.01206    |            |       |  0.00

Nlocal:        25941.3 ave       26032 max       25878 min
Histogram: 31 123 92 10 0 0 0 14 75 39
Nghost:        36530.5 ave       36577 max       36479 min
Histogram: 14 21 35 46 31 74 75 54 26 8
Neighs:    7.53368e+06 ave 7.55943e+06 max 7.51606e+06 min
Histogram: 27 133 89 7 0 0 0 15 80 33

Total # of neighbors = 2.8929346e+09
Ave neighs/atom = 290.41237
Neighbor list builds = 5
Dangerous builds not checked
Total wall time: 0:04:11
```

```
#real	8m19.793s
user	0m0.079s
sys	0m0.028s
time flux run -N 4 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec --pwd /opt/lammps/examples/reaxff/HNS usernetes-azure_lammps.sif /usr/bin/lmp -v x 64 -v y 32 -v z 32 -in ./in.reaxff.hns -nocite
LAMMPS (17 Apr 2024 - Development - a8687b5)
OMP_NUM_THREADS environment is not set. Defaulting to 1 thread. (src/comm.cpp:98)
  using 1 OpenMP thread(s) per MPI task
Reading data file ...
  triclinic box = (0 0 0) to (22.326 11.1412 13.778966) with tilt (0 -5.02603 0)
  8 by 6 by 8 MPI processor grid
  reading atoms ...
  304 atoms
  reading velocities ...
  304 velocities
  read_data CPU = 0.308 seconds
Replication is creating a 64x32x32 = 65536 times larger system...
  triclinic box = (0 0 0) to (1428.864 356.5184 440.92691) with tilt (0 -160.83296 0)
  16 by 4 by 6 MPI processor grid
  bounding box image = (0 -1 -1) to (0 1 1)
  bounding box extra memory = 0.03 MB
  average # of replicas added to proc = 336.76 out of 65536 (0.51%)
  19922944 atoms
  replicate CPU = 0.104 seconds
Neighbor list info ...
  update: every = 20 steps, delay = 0 steps, check = no
  max neighbors/atom: 2000, page size: 100000
  master list distance cutoff = 11
  ghost atom cutoff = 11
  binsize = 5.5, bins = 290 65 81
  2 neighbor lists, perpetual/occasional/extra = 2 0 0
  (1) pair reaxff, perpetual
      attributes: half, newton off, ghost
      pair build: half/bin/ghost/newtoff
      stencil: full/ghost/bin/3d
      bin: standard
  (2) fix qeq/reax, perpetual, copy from (1)
      attributes: half, newton off
      pair build: copy
      stencil: none
      bin: none
Setting up Verlet run ...
  Unit style    : real
  Current step  : 0
  Time step     : 0.1
Per MPI rank memory allocation (min/avg/max) = 1847 | 1853 | 1859 Mbytes
   Step          Temp          PotEng         Press          E_vdwl         E_coul         Volume    
         0   300           -113.27833      439.02035     -111.57687     -1.7014647      2.2461536e+08
        10   300.76787     -113.28045      806.9458      -111.57901     -1.7014353      2.2461536e+08
        20   302.41893     -113.28523      1697.8505     -111.5839      -1.701324       2.2461536e+08
        30   302.57545     -113.28557      4298.4964     -111.58447     -1.7010952      2.2461536e+08
        40   300.64331     -113.27974      6396.8071     -111.57897     -1.7007683      2.2461536e+08
        50   297.45504     -113.27019      6484.7256     -111.56979     -1.7004027      2.2461536e+08
        60   294.75203     -113.26209      6200.4902     -111.56205     -1.7000332      2.2461536e+08
        70   294.65378     -113.26175      6838.3808     -111.56209     -1.6996571      2.2461536e+08
        80   297.75343     -113.27097      8234.8411     -111.57169     -1.6992793      2.2461536e+08
        90   301.65876     -113.28261      9374.4735     -111.58366     -1.6989423      2.2461536e+08
       100   302.57974     -113.2853       10365.474     -111.5866      -1.6986993      2.2461536e+08
Loop time of 483.1 on 384 procs for 100 steps with 19922944 atoms

Performance: 0.002 ns/day, 13419.449 hours/ns, 0.207 timesteps/s, 4.124 Matom-step/s
99.9% CPU use with 384 MPI tasks x 1 OpenMP threads

MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 274.59     | 289.07     | 303.78     |  31.5 | 59.84
Neigh   | 2.9703     | 3.0443     | 3.1347     |   2.0 |  0.63
Comm    | 0.54145    | 13.594     | 29.741     | 149.9 |  2.81
Output  | 0.0048463  | 1.1647     | 2.193      |  47.4 |  0.24
Modify  | 172.74     | 176.19     | 180.64     |  16.4 | 36.47
Other   |            | 0.03491    |            |       |  0.01

Nlocal:        51882.7 ave       52023 max       51763 min
Histogram: 90 38 0 95 33 0 0 0 21 107
Nghost:          53775 ave       54266 max       53187 min
Histogram: 128 0 0 0 0 1 127 0 0 128
Neighs:    1.45786e+07 ave 1.46117e+07 max 1.45471e+07 min
Histogram: 77 51 0 2 104 22 0 0 62 66

Total # of neighbors = 5.5981697e+09
Ave neighs/atom = 280.99109
Neighbor list builds = 5
Dangerous builds not checked
Total wall time: 0:08:13
```
#### Usernetes

Shell into the Usernetes container once the cluster is up:
```
kubectl apply -f crd/lammps.yaml

(Pulling    3m1s   kubelet            Pulling image "ghcr.io/converged-computing/usernetes-azure:lammps"
Pulled     2m45s  kubelet            Successfully pulled image "ghcr.io/converged-computing/usernetes-azure:lammps" in 15.026s (15.026s including waiting). Image size: 2103022386 bytes.)

kubectl exec -ti flux-sample-0-XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local
```

```
#from flux-usernetes aws experiments
time flux run -N 2 --tasks-per-node=96 -o cpu-affinity=per-task /usr/bin/lmp -v x 16 -v y 16 -v z 8 -in ./in.reaxff.hns -nocite

LAMMPS (17 Apr 2024 - Development - a8687b5)
OMP_NUM_THREADS environment is not set. Defaulting to 1 thread. (src/comm.cpp:98)
  using 1 OpenMP thread(s) per MPI task
Reading data file ...
  triclinic box = (0 0 0) to (22.326 11.1412 13.778966) with tilt (0 -5.02603 0)
  8 by 4 by 6 MPI processor grid
  reading atoms ...
  304 atoms
  reading velocities ...
  304 velocities
  read_data CPU = 0.124 seconds
Replication is creating a 16x16x8 = 2048 times larger system...
  triclinic box = (0 0 0) to (357.216 178.2592 110.23173) with tilt (0 -40.20824 0)
  8 by 6 by 4 MPI processor grid
  bounding box image = (0 -1 -1) to (0 1 1)
  bounding box extra memory = 0.03 MB
  average # of replicas added to proc = 46.75 out of 2048 (2.28%)
  622592 atoms
  replicate CPU = 0.016 seconds
Neighbor list info ...
  update: every = 20 steps, delay = 0 steps, check = no
  max neighbors/atom: 2000, page size: 100000
  master list distance cutoff = 11
  ghost atom cutoff = 11
  binsize = 5.5, bins = 73 33 21
  2 neighbor lists, perpetual/occasional/extra = 2 0 0
  (1) pair reaxff, perpetual
      attributes: half, newton off, ghost
      pair build: half/bin/ghost/newtoff
      stencil: full/ghost/bin/3d
      bin: standard
  (2) fix qeq/reax, perpetual, copy from (1)
      attributes: half, newton off
      pair build: copy
      stencil: none
      bin: none
Setting up Verlet run ...
  Unit style    : real
  Current step  : 0
  Time step     : 0.1
Per MPI rank memory allocation (min/avg/max) = 252.5 | 252.7 | 253 Mbytes
   Step          Temp          PotEng         Press          E_vdwl         E_coul         Volume    
         0   300           -113.27833      439.01454     -111.57687     -1.7014647      7019230      
        10   300.6458      -113.28009      687.89553     -111.57866     -1.7014301      7019230      
        20   302.20326     -113.2846       1467.4879     -111.58328     -1.701318       7019230      
        30   302.31937     -113.28481      4051.081      -111.58371     -1.7010939      7019230      
        40   300.51347     -113.27935      6235.4715     -111.57858     -1.7007736      7019230      
        50   297.61214     -113.27065      6426.6131     -111.57024     -1.7004134      7019230      
        60   295.0453      -113.26295      6236.1432     -111.5629      -1.7000496      7019230      
        70   294.72697     -113.26195      6937.5805     -111.56227     -1.6996827      7019230      
        80   297.50375     -113.27022      8342.3188     -111.57091     -1.6993152      7019230      
        90   301.3484      -113.28168      9484.1542     -111.5827      -1.6989854      7019230      
       100   302.48622     -113.28501      10463.506     -111.58627     -1.6987438      7019230      
Loop time of 37.6902 on 192 procs for 100 steps with 622592 atoms

Performance: 0.023 ns/day, 1046.950 hours/ns, 2.653 timesteps/s, 1.652 Matom-step/s
99.9% CPU use with 192 MPI tasks x 1 OpenMP threads

MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 20.69      | 22.842     | 25.285     |  19.6 | 60.60
Neigh   | 0.3672     | 0.3724     | 0.38777    |   0.4 |  0.99
Comm    | 0.14968    | 2.3516     | 4.6025     |  62.8 |  6.24
Output  | 0.0014315  | 0.093636   | 0.24207    |  20.4 |  0.25
Modify  | 11.859     | 12.028     | 12.673     |   7.4 | 31.91
Other   |            | 0.003204   |            |       |  0.01

Nlocal:        3242.67 ave        3264 max        3217 min
Histogram: 13 27 21 2 2 10 38 49 22 8
Nghost:        12106.8 ave       12139 max       12070 min
Histogram: 3 9 24 20 20 27 40 32 14 3
Neighs:    1.07024e+06 ave  1.0764e+06 max 1.06275e+06 min
Histogram: 15 24 19 5 2 8 47 41 21 10

Total # of neighbors = 2.0548535e+08
Ave neighs/atom = 330.04817
Neighbor list builds = 5
Dangerous builds not checked
Total wall time: 0:00:38

real    0m42.552s
user    0m0.073s
sys     0m0.027s
```
```
#real	8m20.674s
user	0m0.077s
sys	0m0.030s
time flux run -N 4 --tasks-per-node=96 -o cpu-affinity=per-task /usr/bin/lmp -v x 64 -v y 32 -v z 32 -in ./in.reaxff.hns -nocite
LAMMPS (17 Apr 2024 - Development - a8687b5)
OMP_NUM_THREADS environment is not set. Defaulting to 1 thread. (src/comm.cpp:98)
  using 1 OpenMP thread(s) per MPI task
Reading data file ...
  triclinic box = (0 0 0) to (22.326 11.1412 13.778966) with tilt (0 -5.02603 0)
  8 by 6 by 8 MPI processor grid
  reading atoms ...
  304 atoms
  reading velocities ...
  304 velocities
  read_data CPU = 0.358 seconds
Replication is creating a 64x32x32 = 65536 times larger system...
  triclinic box = (0 0 0) to (1428.864 356.5184 440.92691) with tilt (0 -160.83296 0)
  16 by 4 by 6 MPI processor grid
  bounding box image = (0 -1 -1) to (0 1 1)
  bounding box extra memory = 0.03 MB
  average # of replicas added to proc = 336.76 out of 65536 (0.51%)
  19922944 atoms
  replicate CPU = 0.106 seconds
Neighbor list info ...
  update: every = 20 steps, delay = 0 steps, check = no
  max neighbors/atom: 2000, page size: 100000
  master list distance cutoff = 11
  ghost atom cutoff = 11
  binsize = 5.5, bins = 290 65 81
  2 neighbor lists, perpetual/occasional/extra = 2 0 0
  (1) pair reaxff, perpetual
      attributes: half, newton off, ghost
      pair build: half/bin/ghost/newtoff
      stencil: full/ghost/bin/3d
      bin: standard
  (2) fix qeq/reax, perpetual, copy from (1)
      attributes: half, newton off
      pair build: copy
      stencil: none
      bin: none
Setting up Verlet run ...
  Unit style    : real
  Current step  : 0
  Time step     : 0.1
Per MPI rank memory allocation (min/avg/max) = 1847 | 1853 | 1859 Mbytes
   Step          Temp          PotEng         Press          E_vdwl         E_coul         Volume    
         0   300           -113.27833      439.02035     -111.57687     -1.7014647      2.2461536e+08
        10   300.76787     -113.28045      806.9458      -111.57901     -1.7014353      2.2461536e+08
        20   302.41893     -113.28523      1697.8505     -111.5839      -1.701324       2.2461536e+08
        30   302.57545     -113.28557      4298.4964     -111.58447     -1.7010952      2.2461536e+08
        40   300.64331     -113.27974      6396.8071     -111.57897     -1.7007683      2.2461536e+08
        50   297.45504     -113.27019      6484.7256     -111.56979     -1.7004027      2.2461536e+08
        60   294.75203     -113.26209      6200.4902     -111.56205     -1.7000332      2.2461536e+08
        70   294.65378     -113.26175      6838.3808     -111.56209     -1.6996571      2.2461536e+08
        80   297.75343     -113.27097      8234.8411     -111.57169     -1.6992793      2.2461536e+08
        90   301.65876     -113.28261      9374.4735     -111.58366     -1.6989423      2.2461536e+08
       100   302.57974     -113.2853       10365.474     -111.5866      -1.6986993      2.2461536e+08
Loop time of 486.293 on 384 procs for 100 steps with 19922944 atoms

Performance: 0.002 ns/day, 13508.138 hours/ns, 0.206 timesteps/s, 4.097 Matom-step/s
99.9% CPU use with 384 MPI tasks x 1 OpenMP threads

MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 276.23     | 289.49     | 302.65     |  31.0 | 59.53
Neigh   | 2.9643     | 3.0405     | 3.1477     |   2.1 |  0.63
Comm    | 0.99824    | 12.412     | 26.624     | 143.9 |  2.55
Output  | 0.034299   | 0.40063    | 1.2512     |  44.5 |  0.08
Modify  | 179.22     | 180.92     | 183.98     |  10.4 | 37.20
Other   |            | 0.03343    |            |       |  0.01

Nlocal:        51882.7 ave       52023 max       51763 min
Histogram: 90 38 0 95 33 0 0 0 21 107
Nghost:          53775 ave       54266 max       53187 min
Histogram: 128 0 0 0 0 1 127 0 0 128
Neighs:    1.45786e+07 ave 1.46117e+07 max 1.45471e+07 min
Histogram: 77 51 0 2 104 22 0 0 62 66

Total # of neighbors = 5.5981697e+09
Ave neighs/atom = 280.99109
Neighbor list builds = 5
Dangerous builds not checked
Total wall time: 0:08:16
```

### Scale
#### Bare metal
```
oras login ghcr.io --username lisejolicoeur
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

./check.sh
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output
```

#### Usernetes
```
oras login ghcr.io --username lisejolicoeur
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

./check.sh
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output
```

## MiniFE

### Test (2 nodes)

### Container pull
```
#docker.io/milkshake113/minife:azure-hpc-2404
cd /opt
time flux exec -r all singularity pull docker://ghcr.io/converged-computing/usernetes-azure:minife
real	1m51.646s
user	0m0.008s
sys	0m0.006s
```

#### Bare metal
```
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx

#from performance study experiments
time flux run -N2 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec --bind /opt:/opt /opt/usernetes-azure_minife.sif miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0

MiniFE Mini-App, OpenMP Peer Implementation
Creating OpenMP Thread Pool...
Counted: 192 threads.
Running MiniFE Mini-App...
      creating/filling mesh...0.00914598s, total time: 0.00914598
generating matrix structure...0.07336s, total time: 0.0825059
         assembling FE data...0.132909s, total time: 0.215415
      imposing Dirichlet BC...0.026612s, total time: 0.242027
      imposing Dirichlet BC...0.0016129s, total time: 0.24364
making matrix indices local...0.04285s, total time: 0.28649
Starting CG solver ... 
Initial Residual = 231.002
Iteration = 20   Residual = 0.0808553
Iteration = 40   Residual = 0.0251403
Iteration = 60   Residual = 0.015028
Iteration = 80   Residual = 0.0101214
Iteration = 100   Residual = 0.00840999
Iteration = 120   Residual = 0.00529916
Iteration = 140   Residual = 0.0038704
Iteration = 160   Residual = 0.00279602
Iteration = 180   Residual = 0.00212219
Iteration = 200   Residual = 0.00140664
Final Resid Norm: 0.00140664

real    0m7.393s
user    0m0.071s
sys     0m0.034s

YAML file content:

Mini-Application Name: miniFE
Mini-Application Version: 2.0
Global Run Parameters: 
  dimensions: 
    nx: 230
    ny: 230
    nz: 230
  load_imbalance: 0
  mv_overlap_comm_comp: 0 (no)
  OpenMP Max Threads:: 1
  number of processors: 192
  ScalarType: double
  GlobalOrdinalType: int
  LocalOrdinalType: int
Platform: 
  hostname: buildkitsandbox
  kernel name: 'Linux'
  kernel release: '6.8.0-1017-azure'
  processor: 'x86_64'
Build: 
  CXX: '/usr/local/bin/mpicxx'
  compiler version: 'g++ (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0'
  CXXFLAGS: '-O3 -fopenmp'
  using MPI: yes
Run Date/Time: 2025-01-28, 15-21-24
Rows-per-proc Load Imbalance: 
  Largest (from avg, %): 6.17046
  Std Dev (%): 2.51343
Matrix structure generation: 
  Mat-struc-gen Time: 0.07336
FE assembly: 
  FE assembly Time: 0.132909
Matrix attributes: 
  Global Nrows: 12326391
  Global NNZ: 329939371
  Global Memory (GB): 3.7792
  Pll Memory Overhead (MB): 19.929
  Rows per proc MIN: 60648
  Rows per proc MAX: 67280
  Rows per proc AVG: 64200
  NNZ per proc MIN: 1637496
  NNZ per proc MAX: 1816560
  NNZ per proc AVG: 1.71843e+06
CG solve: 
  Iterations: 200
  Final Resid Norm: 0.00140664
  WAXPY Time: 0.0402985
  WAXPY Flops: 2.19736e+10
  WAXPY Mflops: 545271
  DOT Time: 0.148738
  DOT Flops: 9.7336e+09
  DOT Mflops: 65441.1
  MATVEC Time: 0.540604
  MATVEC Flops: 1.32636e+11
  MATVEC Mflops: 245347
  Total: 
    Total CG Time: 0.73506
    Total CG Flops: 1.64343e+11
    Total CG Mflops: 223577
  Time per iteration: 0.0036753
Global All-RSS (kB): 28375868
Global Max-RSS (kB): 159840
Total Program Time: 1.34695
```
#### Usernetes


Shell into the Usernetes container once the cluster is up:
```
kubectl apply -f crd/minife.yaml

(Pulling    2m16s  kubelet            Pulling image "ghcr.io/converged-computing/usernetes-azure:minife"
Normal  Pulled     2m14s  kubelet            Successfully pulled image "ghcr.io/converged-computing/usernetes-azure:minife" in 1.99s (1.99s including waiting). Image size: 1802286887 bytes.)

kubectl exec -ti flux-sample-0-XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local
```

```
#from performance study experiments
time flux run -N2 --tasks-per-node=96 -o cpu-affinity=per-task miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0

MiniFE Mini-App, OpenMP Peer Implementation
Creating OpenMP Thread Pool...
Counted: 192 threads.
Running MiniFE Mini-App...
      creating/filling mesh...0.0119441s, total time: 0.011945
generating matrix structure...0.07165s, total time: 0.083595
         assembling FE data...0.13135s, total time: 0.214945
      imposing Dirichlet BC...0.0271759s, total time: 0.242121
      imposing Dirichlet BC...0.00164008s, total time: 0.243761
making matrix indices local...0.0423589s, total time: 0.28612
Starting CG solver ... 
Initial Residual = 231.002
Iteration = 20   Residual = 0.0808553
Iteration = 40   Residual = 0.0251403
Iteration = 60   Residual = 0.015028
Iteration = 80   Residual = 0.0101214
Iteration = 100   Residual = 0.00840999
Iteration = 120   Residual = 0.00529916
Iteration = 140   Residual = 0.0038704
Iteration = 160   Residual = 0.00279602
Iteration = 180   Residual = 0.00212219
Iteration = 200   Residual = 0.00140664
Final Resid Norm: 0.00140664

real    0m4.800s
user    0m0.076s
sys     0m0.032s

YAML file output:

Mini-Application Name: miniFE
Mini-Application Version: 2.0
Global Run Parameters: 
  dimensions: 
    nx: 230
    ny: 230
    nz: 230
  load_imbalance: 0
  mv_overlap_comm_comp: 0 (no)
  OpenMP Max Threads:: 1
  number of processors: 192
  ScalarType: double
  GlobalOrdinalType: int
  LocalOrdinalType: int
Platform: 
  hostname: buildkitsandbox
  kernel name: 'Linux'
  kernel release: '6.8.0-1017-azure'
  processor: 'x86_64'
Build: 
  CXX: '/usr/local/bin/mpicxx'
  compiler version: 'g++ (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0'
  CXXFLAGS: '-O3 -fopenmp'
  using MPI: yes
Run Date/Time: 2025-01-29, 08-57-16
Rows-per-proc Load Imbalance: 
  Largest (from avg, %): 6.17046
  Std Dev (%): 2.51343
Matrix structure generation: 
  Mat-struc-gen Time: 0.07165
FE assembly: 
  FE assembly Time: 0.13135
Matrix attributes: 
  Global Nrows: 12326391
  Global NNZ: 329939371
  Global Memory (GB): 3.7792
  Pll Memory Overhead (MB): 19.929
  Rows per proc MIN: 60648
  Rows per proc MAX: 67280
  Rows per proc AVG: 64200
  NNZ per proc MIN: 1637496
  NNZ per proc MAX: 1816560
  NNZ per proc AVG: 1.71843e+06
CG solve: 
  Iterations: 200
  Final Resid Norm: 0.00140664
  WAXPY Time: 0.0386293
  WAXPY Flops: 2.19736e+10
  WAXPY Mflops: 568833
  DOT Time: 0.17013
  DOT Flops: 9.7336e+09
  DOT Mflops: 57212.9
  MATVEC Time: 0.532768
  MATVEC Flops: 1.32636e+11
  MATVEC Mflops: 248956
  Total: 
    Total CG Time: 0.746711
    Total CG Flops: 1.64343e+11
    Total CG Mflops: 220089
  Time per iteration: 0.00373356
Global All-RSS (kB): 28378544
Global Max-RSS (kB): 159840
Total Program Time: 1.35242
```

### Scale
#### Bare metal
```
oras login ghcr.io --username lisejolicoeur
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

mv miniFE*.yaml $output

./check.sh
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output
```
#### Usernetes
```
oras login ghcr.io --username lisejolicoeur
app=lammps
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

mv miniFE*.yaml $output

./check.sh
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app $output
```


## AMG

### Test (2 nodes)

#### Container pull
```
#docker.io/milkshake113/amg:azure-hpc-2404
cd /opt
time flux exec -r all singularity pull docker://ghcr.io/converged-computing/usernetes-azure:amg
real	2m6.814s
user	0m0.005s
sys	0m0.009s
```

#### Bare metal
```
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx

#from performance study experiments
time flux run --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 2 -n 64 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg.sif amg -n 256 256 128 -P 8 4 2 -problem 2
Running with these driver parameters:
  solver ID    = 3

  Laplacian_27pt:
    (Nx, Ny, Nz) = (2048, 1024, 256)
    (Px, Py, Pz) = (8, 4, 2)

=============================================
Generate Matrix:
=============================================
Spatial Operator:
  wall clock time = 3.000220 seconds
  wall MFLOPS     = 0.000000
  cpu clock time  = 8.478691 seconds
  cpu MFLOPS      = 0.000000

  RHS vector has unit components
  Initial guess is 0
=============================================
IJ Vector Setup:
=============================================
RHS and Initial Guess:
  wall clock time = 0.116649 seconds
  wall MFLOPS     = 0.000000
  cpu clock time  = 0.224480 seconds
  cpu MFLOPS      = 0.000000

=============================================
Problem 2: Cumulative AMG-GMRES Solve Time:
=============================================
GMRES Solve:
  wall clock time = 813.874858 seconds
  wall MFLOPS     = 0.000000
  cpu clock time  = 2412.747225 seconds
  cpu MFLOPS      = 0.000000


No. of Time Steps = 6
Cum. No. of Iterations = 215
Final Relative Residual Norm = 1.607252e-13


nnz AP * (Iterations + time_steps) / Total Time: 

Figure of Merit (FOM_2): 4.287041e+09

real	13m40.343s
user	0m0.077s
sys	0m0.023s
```

#### Usernetes

Shell into the Usernetes container once the cluster is up:
```
kubectl apply -f crd/amg.yaml

(Pulling    46s   kubelet            Pulling image "ghcr.io/converged-computing/usernetes-azure:amg"
  Normal  Pulled     44s   kubelet            Successfully pulled image "ghcr.io/converged-computing/usernetes-azure:amg" in 1.405s (1.405s including waiting). Image size: 1800886203 bytes.)

kubectl exec -ti flux-sample-0-XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local
```
```
#from performance study experiments
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx

#real    3m19.647s
user    0m0.064s
sys     0m0.038s
time flux run --env OMP_NUM_THREADS=3 -N 2 --tasks-per-node=4 -o cpu-affinity=per-task amg -n 256 256 128 -P 2 2 2 -problem 2

Running with these driver parameters:
  solver ID    = 3

  Laplacian_27pt:
    (Nx, Ny, Nz) = (512, 512, 256)
    (Px, Py, Pz) = (2, 2, 2)

=============================================
Generate Matrix:
=============================================
Spatial Operator:
  wall clock time = 0.851080 seconds
  wall MFLOPS     = 0.000000
  cpu clock time  = 2.344703 seconds
  cpu MFLOPS      = 0.000000

  RHS vector has unit components
  Initial guess is 0
=============================================
IJ Vector Setup:
=============================================
RHS and Initial Guess:
  wall clock time = 0.086135 seconds
  wall MFLOPS     = 0.000000
  cpu clock time  = 0.130718 seconds
  cpu MFLOPS      = 0.000000

=============================================
Problem 2: Cumulative AMG-GMRES Solve Time:
=============================================
GMRES Solve:
  wall clock time = 197.980853 seconds
  wall MFLOPS     = 0.000000
  cpu clock time  = 574.031475 seconds
  cpu MFLOPS      = 0.000000


No. of Time Steps = 6
Cum. No. of Iterations = 215
Final Relative Residual Norm = 3.895199e-14


nnz AP * (Iterations + time_steps) / Total Time: 

Figure of Merit (FOM_2): 2.199055e+09
```

## AMG2023

### Test (2 nodes)

#### Container pull
```
cd /opt
time flux exec -r all singularity pull docker://ghcr.io/converged-computing/usernetes-azure:amg2023
real	2m15.967s
user	0m0.012s
sys	0m0.005s
```

#### Bare metal
```
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx

#real	0m54.587s
user	0m0.076s
sys	0m0.021s
time flux run --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 2 -n 64 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg2023.sif amg -n 256 256 128 -P 8 4 2 -problem 2
Running with these driver parameters:
  Problem ID    = 2

=============================================
Hypre init times:
=============================================
Hypre init:
  wall clock time = 0.002488 seconds
  Laplacian_7pt:
    (Nx, Ny, Nz) = (2048, 1024, 256)
    (Px, Py, Pz) = (8, 4, 2)

=============================================
Generate Matrix:
=============================================
Spatial Operator:
  wall clock time = 1.046138 seconds
  RHS vector has unit components
  Initial guess is 0
=============================================
IJ Vector Setup:
=============================================
RHS and Initial Guess:
  wall clock time = 0.069057 seconds
=============================================
Problem 2: AMG Setup Time:
=============================================
PCG Setup:
  wall clock time = 32.242117 seconds

FOM_Setup: nnz_AP / Setup Phase Time: 2.010611e+08

=============================================
Problem 2: AMG-PCG Solve Time:
=============================================
PCG Solve:
  wall clock time = 19.244267 seconds

Iterations = 22
Final Relative Residual Norm = 3.610765e-09
FOM_Solve: nnz_AP * iterations / Solve Phase Time: 3.368605e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 7.204935e+07

```

#### Usernetes

Shell into the Usernetes container once the cluster is up:
```
kubectl apply -f crd/amg.yaml

(Pulling    2m7s   kubelet            Pulling image "ghcr.io/converged-computing/usernetes-azure:amg2023"
  Normal  Pulled     44s    kubelet            Successfully pulled image "ghcr.io/converged-computing/usernetes-azure:amg2023" in 1m23.57s (1m23.57s including waiting). Image size: 2053770085 bytes.)

kubectl exec -ti flux-sample-0-XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local
```

```
#real	0m54.427s
user	0m0.074s
sys	0m0.028s
time flux run --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 2 -n 64 -o cpu-affinity=per-task amg -n 256 256 128 -P 8 4 2 -problem 2
Running with these driver parameters:
  Problem ID    = 2

=============================================
Hypre init times:
=============================================
Hypre init:
  wall clock time = 0.000009 seconds
  Laplacian_7pt:
    (Nx, Ny, Nz) = (2048, 1024, 256)
    (Px, Py, Pz) = (8, 4, 2)

=============================================
Generate Matrix:
=============================================
Spatial Operator:
  wall clock time = 1.041354 seconds
  RHS vector has unit components
  Initial guess is 0
=============================================
IJ Vector Setup:
=============================================
RHS and Initial Guess:
  wall clock time = 0.069725 seconds
=============================================
Problem 2: AMG Setup Time:
=============================================
PCG Setup:
  wall clock time = 32.574849 seconds

FOM_Setup: nnz_AP / Setup Phase Time: 1.990073e+08

=============================================
Problem 2: AMG-PCG Solve Time:
=============================================
PCG Solve:
  wall clock time = 19.242726 seconds

Iterations = 22
Final Relative Residual Norm = 3.610765e-09
FOM_Solve: nnz_AP * iterations / Solve Phase Time: 3.368875e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 7.178756e+07
```
### Scale
#### Bare metal
```
oras login ghcr.io --username lisejolicoeur
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

./check.sh
./save.sh $output
oras push ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app $output
```
#### Usernetes
```
oras login ghcr.io --username lisejolicoeur
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


## RESNET

### Test (2 nodes)

#### Container pull
```
cd /opt
time flux exec -r 0,1 singularity pull docker://ghcr.io/converged-computing/usernetes-azure:pytorch

real    7m1.034s
user    0m0.008s
sys     0m0.163s
```

#### Bare metal

Clone this repo to get newer version of main.py and launch.sh
```
cd /opt
git clone https://github.com/converged-computing/usernetes-azure
mkdir experiment
cd experiment
cp ../usernetes-azure/docker/resnet/main.py .
cp ../usernetes-azure/docker/resnet/launch.sh .

container=/opt/usernetes-azure_pytorch.sif
```

```
#1 node
real	7m57.739s
user	0m0.100s
sys	0m0.047s
time flux run -N 1 singularity exec --bind /tmp:/tmp --bind /opt/run/flux:/opt/run/flux --bind /opt/experiment/launch.sh --bind /opt/experiment/main.py $container /bin/bash /opt/experiment/launch.sh flux-user000000 1 $(nproc) 128
samples_per_sec: 268.1390

#2 nodes
#real	8m2.749s
user	0m0.096s
sys	0m0.053s
time flux run -N 2 singularity exec --bind /tmp:/tmp --bind /opt/run/flux:/opt/run/flux --bind /opt/experiment/launch.sh --bind /opt/experiment/main.py $container /bin/bash /opt/experiment/launch.sh flux-user000000 2 $(nproc) 128
samples_per_sec: 532.8424
```

#### Usernetes

Shell into the Usernetes container once the cluster is up:
```
kubectl apply -f crd/resnet.yaml
kubectl get pods -o wide

(  Normal  Pulling    7m26s  kubelet            Pulling image "ghcr.io/converged-computing/usernetes-azure:pytorch"
  Normal  Pulled     2m19s  kubelet            Successfully pulled image "ghcr.io/converged-computing/usernetes-azure:pytorch" in 5m6.579s (5m6.579s including waiting). Image size: 7642462941 bytes.)

kubectl exec -ti flux-sample-0-XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local
```
Retreive the updated two files necessary for running resnet:
```
flux exec -r 0,1 git clone https://github.com/converged-computing/usernetes-azure
flux exec -r 0,1 mkdir /opt/experiment
cd experiment
flux exec -r 0,1 cp /opt/usernetes-azure/docker/resnet/main.py .
flux exec -r 0,1 cp /opt/usernetes-azure/docker/resnet/launch.sh .
> modify launch.sh to have : MASTER_ADDR=${master}.flux-service.default.svc.cluster.local
flux archive create --name launch --dir /opt/experiment/ launch.sh
flux exec -r 1 flux archive extract --dir /opt/experiment/ --overwrite --name launch

flux exec -r 0,1 chmod +x /opt/experiment/launch.sh 
flux exec -r 0,1 chmod +x /opt/experiment/main.py
```

```
cd /opt/experiment

#1 node
real	7m46.435s
user	0m0.079s
sys	0m0.023s
time flux run -N 1 /opt/experiment/launch.sh flux-sample-0 1 $(nproc) 128
samples_per_sec: 267.8348
samples_per_sec: 268.4161
samples_per_sec: 267.6725
samples_per_sec: 269.5900

#2 nodes
real	15m20.375s
user	0m0.073s
sys	0m0.035s

time flux run -N 2 /opt/experiment/launch.sh flux-sample-0 2 $(nproc) 128
samples_per_sec: 515.7026
samples_per_sec: 518.0394
samples_per_sec: 520.0916
samples_per_sec: 519.0018
```

## RESNET MPI

### Test (2 nodes)

#### Container pull
```
#This won't work for now, I was unsuccessful pushing the image...
#use regular pytorch/resnet image and modify main.py to match the one from resnet-mpi
cd /opt
time flux exec -r 0,1 singularity pull docker://ghcr.io/converged-computing/usernetes-azure:pytorch-mpi

real    7m1.034s
user    0m0.008s
sys     0m0.163s
```
#### Bare metal
```
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx

#real	9m15.529s
user	0m0.095s
sys	0m0.041s
time flux run -N1 -n 96 -o cpu-affinity=per-task singularity exec --bind /opt/usernetes-azure --bind /tmp --bind /dev/shm --bind /opt/run/flux --env LOCAL_RANK=0 /opt/usernetes-azure_pytorch.sif python /opt/usernetes-azure/docker/resnet/main.py --backend=mpi --use_syn --batch_size=128 --arch=resnet18
samples_per_sec: 224.8194
samples_per_sec: 225.0790
samples_per_sec: 226.6073
samples_per_sec: 226.9088

#does not work if LOCAL_RANK is not passed, but it is also reassigned in the python script so it doesnt matter which value we pass
#real	9m20.726s
user	0m0.127s
sys	0m0.090s
time flux run -N2 -n 192 -o cpu-affinity=per-task singularity exec --bind /opt/usernetes-azure --bind /tmp --bind /dev/shm --bind /opt/run/flux --env LOCAL_RANK=0 /opt/usernetes-azure_pytorch.sif python /opt/usernetes-azure/docker/resnet/main.py --backend=mpi --use_syn --batch_size=128 --arch=resnet18
samples_per_sec: 447.5474
```

#### Usernetes
```
#for now, use resnet.yaml until image is successfully pushed
kubectl apply -f crd/resnet-mpi.yaml
kubectl get pods -o wide

(  Normal  Pulling    7m26s  kubelet            Pulling image "ghcr.io/converged-computing/usernetes-azure:pytorch"
  Normal  Pulled     2m19s  kubelet            Successfully pulled image "ghcr.io/converged-computing/usernetes-azure:pytorch" in 5m6.579s (5m6.579s including waiting). Image size: 7642462941 bytes.)

kubectl exec -ti flux-sample-0-XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local
flux exec -r 0,1 git clone https://github.com/converged-computing/usernetes-azure
```

```
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx

#real	9m13.769s
user	0m0.074s
sys	0m0.030s
time flux run -N1 -n 96 -o cpu-affinity=per-task python /opt/usernetes-azure/docker/resnet-mpi/main.py --backend=mpi --use_syn --batch_size=128 --arch=resnet18
samples_per_sec: 222.2845
samples_per_sec: 224.7697
samples_per_sec: 224.9327
samples_per_sec: 226.0100

#real	9m21.389s
user	0m0.071s
sys	0m0.036s
time flux run -N2 -n 192 -o cpu-affinity=per-task python /opt/usernetes-azure/docker/resnet-mpi/main.py --backend=mpi --use_syn --batch_size=128 --arch=resnet18
samples_per_sec: 440.8316
samples_per_sec: 443.3149
samples_per_sec: 444.3847
samples_per_sec: 446.0719

```
