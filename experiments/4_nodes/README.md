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
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx

#real	0m56.021s
user	0m0.076s
sys	0m0.025s
time flux run --env OMP_NUM_THREADS=3 --cores-per-task 3 --exclusive -N 4 -n 128 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg2023.sif amg -n 256 256 128 -P 8 8 2 -problem 2
Running with these driver parameters:
  Problem ID    = 2

=============================================
Hypre init times:
=============================================
Hypre init:
  wall clock time = 0.002653 seconds
  Laplacian_7pt:
    (Nx, Ny, Nz) = (2048, 2048, 256)
    (Px, Py, Pz) = (8, 8, 2)

=============================================
Generate Matrix:
=============================================
Spatial Operator:
  wall clock time = 1.123729 seconds
  RHS vector has unit components
  Initial guess is 0
=============================================
IJ Vector Setup:
=============================================
RHS and Initial Guess:
  wall clock time = 0.069868 seconds
=============================================
Problem 2: AMG Setup Time:
=============================================
PCG Setup:
  wall clock time = 34.791758 seconds

FOM_Setup: nnz_AP / Setup Phase Time: 3.727079e+08

=============================================
Problem 2: AMG-PCG Solve Time:
=============================================
PCG Solve:
  wall clock time = 19.264474 seconds

Iterations = 22
Final Relative Residual Norm = 4.265372e-09
FOM_Solve: nnz_AP * iterations / Solve Phase Time: 6.731127e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 1.400566e+08

```
### Usernetes
```

```
## MiniFE
### Bare metal 
```
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx

#real	0m7.573s
user	0m0.085s
sys	0m0.021s
time flux run -N4 --tasks-per-node=96 -o cpu-affinity=per-task singularity exec --bind /opt:/opt /opt/usernetes-azure_minife.sif miniFE.x nx=230 ny=230 nz=230 use_locking=1 elem_group_size=10 use_elem_mat_fields=300 verify_solution=0
MiniFE Mini-App, OpenMP Peer Implementation
Creating OpenMP Thread Pool...
Counted: 384 threads.
Running MiniFE Mini-App...
      creating/filling mesh...0.056628s, total time: 0.056628
generating matrix structure...0.0331519s, total time: 0.0897799
         assembling FE data...0.061553s, total time: 0.151333
      imposing Dirichlet BC...0.010272s, total time: 0.161605
      imposing Dirichlet BC...0.000727177s, total time: 0.162332
making matrix indices local...0.0952201s, total time: 0.257552
Starting CG solver ... 
Initial Residual = 231.002
Iteration = 20   Residual = 0.121724
Iteration = 40   Residual = 0.0251405
Iteration = 60   Residual = 0.015028
Iteration = 80   Residual = 0.0100868
Iteration = 100   Residual = 0.00715833
Iteration = 120   Residual = 0.0387415
Iteration = 140   Residual = 0.00387161
Iteration = 160   Residual = 0.00277456
Iteration = 180   Residual = 0.00196057
Iteration = 200   Residual = 0.00137808
Final Resid Norm: 0.00137808

real	0m7.573s
user	0m0.085s
sys	0m0.021s

cat miniFE.230x230x230.P384.T1.2025\:02\:22-11\:28\:14.yaml

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
  number of processors: 384
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
Run Date/Time: 2025-02-22, 11-28-13
Rows-per-proc Load Imbalance: 
  Largest (from avg, %): 6.17046
  Std Dev (%): 2.79606
Matrix structure generation: 
  Mat-struc-gen Time: 0.0331519
FE assembly: 
  FE assembly Time: 0.061553
Matrix attributes: 
  Global Nrows: 12326391
  Global NNZ: 329939371
  Global Memory (GB): 3.7792
  Pll Memory Overhead (MB): 25.4045
  Rows per proc MIN: 29792
  Rows per proc MAX: 33640
  Rows per proc AVG: 32100
  NNZ per proc MIN: 804384
  NNZ per proc MAX: 908280
  NNZ per proc AVG: 859217
CG solve: 
  Iterations: 200
  Final Resid Norm: 0.00137808
  WAXPY Time: 0.0185571
  WAXPY Flops: 2.19736e+10
  WAXPY Mflops: 1.18411e+06
  DOT Time: 0.177008
  DOT Flops: 9.7336e+09
  DOT Mflops: 54989.5
  MATVEC Time: 0.168564
  MATVEC Flops: 1.32636e+11
  MATVEC Mflops: 786857
  Total: 
    Total CG Time: 0.36647
    Total CG Flops: 1.64343e+11
    Total CG Mflops: 448448
  Time per iteration: 0.00183235
Global All-RSS (kB): 51540580
Global Max-RSS (kB): 145420
Total Program Time: 0.93045

```
### Usernetes
```

```
