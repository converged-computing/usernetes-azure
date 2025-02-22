## OSU barrier
### Bare metal
```
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx
time flux run -N4 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier
# OSU MPI Barrier Latency Test v5.8
# Avg Latency(us)
            12.57

real	0m5.711s
user	0m0.083s
sys	0m0.021s
```
### Usernetes
```
time flux run -N4 --tasks-per-node=96 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_barrier
```
## OSU allreduce

### Bare metal 
```
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx
time flux run -N4 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce
# OSU MPI Allreduce Latency Test v5.8
# Size       Avg Latency(us)
4                      12.45
8                      12.41
16                     12.44
32                     14.05
64                     15.48
128                    18.82
256                    20.31
512                    21.52
1024                   22.69
2048                   26.29
4096                   33.94
8192                   62.87
16384                  57.83
32768                  70.72
65536                 124.29
131072                234.21
262144                497.70
524288               1065.87
1048576              2159.77

real	0m7.902s
user	0m0.079s
sys	0m0.027s
```
### Usernetes
```
time flux run -N4 --tasks-per-node=96 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce

```
## LAMMPS
### Bare metal 
```
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx

#real	1m20.276s
user	0m0.080s
sys	0m0.026s
time flux run -N 4 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec --pwd /opt/lammps/examples/reaxff/HNS usernetes-azure_lammps.sif /usr/bin/lmp -v x 32 -v y 32 -v z 8 -in ./in.reaxff.hns -nocite
WARNING on proc 0: Cannot open log.lammps for writing: Read-only file system (src/lammps.cpp:511)
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
  read_data CPU = 0.285 seconds
Replication is creating a 32x32x8 = 8192 times larger system...
  triclinic box = (0 0 0) to (714.432 356.5184 110.23173) with tilt (0 -40.20824 0)
  16 by 8 by 3 MPI processor grid
  bounding box image = (0 -1 -1) to (0 1 1)
  bounding box extra memory = 0.03 MB
  average # of replicas added to proc = 70.31 out of 8192 (0.86%)
  2490368 atoms
  replicate CPU = 0.087 seconds
Neighbor list info ...
  update: every = 20 steps, delay = 0 steps, check = no
  max neighbors/atom: 2000, page size: 100000
  master list distance cutoff = 11
  ghost atom cutoff = 11
  binsize = 5.5, bins = 138 65 21
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
Per MPI rank memory allocation (min/avg/max) = 391.9 | 394.2 | 397.1 Mbytes
   Step          Temp          PotEng         Press          E_vdwl         E_coul         Volume    
         0   300           -113.27833      439.01896     -111.57687     -1.7014647      28076920     
        10   300.71016     -113.28028      750.05397     -111.57884     -1.701434       28076920     
        20   302.35333     -113.28504      1556.0215     -111.58372     -1.7013225      28076920     
        30   302.53416     -113.28545      4098.1346     -111.58435     -1.701096       28076920     
        40   300.65409     -113.27977      6228.4845     -111.57899     -1.7007733      28076920     
        50   297.54539     -113.27045      6405.5372     -111.57004     -1.7004123      28076920     
        60   294.88375     -113.26247      6229.5675     -111.56243     -1.7000474      28076920     
        70   294.75512     -113.26205      6922.7674     -111.56237     -1.6996773      28076920     
        80   297.80546     -113.27113      8318.7557     -111.57182     -1.6993057      28076920     
        90   301.70681     -113.28275      9502.0118     -111.58378     -1.6989743      28076920     
       100   302.69039     -113.28563      10531.679     -111.58689     -1.698735       28076920     
Loop time of 71.8396 on 384 procs for 100 steps with 2490368 atoms

Performance: 0.012 ns/day, 1995.544 hours/ns, 1.392 timesteps/s, 3.467 Matom-step/s
99.9% CPU use with 384 MPI tasks x 1 OpenMP threads

MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 39.021     | 42.284     | 45.638     |  19.7 | 58.86
Neigh   | 0.58735    | 0.60194    | 0.62263    |   0.9 |  0.84
Comm    | 0.20753    | 3.0458     | 6.5916     |  79.6 |  4.24
Output  | 0.001593   | 0.13333    | 0.23893    |  17.7 |  0.19
Modify  | 23.929     | 25.768     | 27.086     |  14.1 | 35.87
Other   |            | 0.005638   |            |       |  0.01

Nlocal:        6485.33 ave        6521 max        6449 min
Histogram: 95 33 0 0 7 72 47 29 79 22
Nghost:          16964 ave       17192 max       16789 min
Histogram: 127 1 81 47 0 0 0 0 0 128
Neighs:    2.03165e+06 ave   2.043e+06 max 2.02209e+06 min
Histogram: 95 33 0 19 73 34 4 44 65 17

Total # of neighbors = 7.8015293e+08
Ave neighs/atom = 313.26813
Neighbor list builds = 5
Dangerous builds not checked
Total wall time: 0:01:13
```
### Usernetes
```

```
## AMG 2023
### Bare metal 
```

```
### Usernetes
```

```
## MiniFE
### Bare metal 

### Usernetes
