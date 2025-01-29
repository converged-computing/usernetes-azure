# Experiments

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

Usernetes CRD for these tests:
```
apiVersion: flux-framework.org/v1alpha2
kind: MiniCluster
metadata:
  name: flux-sample
spec:
  size: 2
  interactive: true
  flux:
    container:
      disable: true
  containers:
    - image: ghcr.io/converged-computing/usernetes-azure:osu
      volumes:
        memory-dir:
          emptyDir: true
          emptyDirMedium: "memory"
      environment:
        UCX_TLS: rc,sm
	OMPI_MCA_btl: ^vader,tcp,openib,uct
	OMPI_MCA_pml: ucx
        UCX_NET_DEVICES: mlx5_0:1
	OMPI_MCA_spml: ucx
	OMPI_MCA_osc: ucx
      securityContext:
        privileged: true
```

Shell into the Usernetes container once the cluster is up:
```
kubectl apply -f minicluster.yaml

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
```
oras login ghcr.io --username lisejolicoeur
app=osu_latency

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

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

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

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

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

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

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

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

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

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

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

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

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

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

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

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

#### Usernetes

Usernetes CRD for these tests:
```
apiVersion: flux-framework.org/v1alpha2
kind: MiniCluster
metadata:
  name: flux-sample
spec:
  size: 2
  interactive: true
  flux:
    container:
      disable: true
  containers:
    - image: ghcr.io/converged-computing/usernetes-azure:lammps
      volumes:
        memory-dir:
          emptyDir: true
          emptyDirMedium: "memory"
      environment:
        UCX_TLS: rc,sm
	OMPI_MCA_btl: ^vader,tcp,openib,uct
	OMPI_MCA_pml: ucx
        UCX_NET_DEVICES: mlx5_0:1
	OMPI_MCA_spml: ucx
	OMPI_MCA_osc: ucx
      securityContext:
        privileged: true
```

Shell into the Usernetes container once the cluster is up:
```
kubectl apply -f minicluster.yaml

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
#from performance study experiments
time flux run -N 2 --tasks-per-node=96 -o cpu-affinity=per-task /usr/bin/lmp -v x 64 -v y 64 -v z 32 -in ./in.reaxff.hns -nocite

 1984.637562] Out of memory: Killed process 16060 (lmp) total-vm:9388380kB, anon-rss:5008112kB, file-rss:9984kB, shmem-rss:20736kB, UID:1000 pgtables:10528kB oom_score_adj:1000
```


### Scale
#### Bare metal
TODO
#### Usernetes
TODO


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

Usernetes CRD for these tests:
```
apiVersion: flux-framework.org/v1alpha2
kind: MiniCluster
metadata:
  name: flux-sample
spec:
  size: 2
  interactive: true
  flux:
    container:
      disable: true
  containers:
    - image: ghcr.io/converged-computing/usernetes-azure:minife
      volumes:
        memory-dir:
          emptyDir: true
          emptyDirMedium: "memory"
      environment:
        UCX_TLS: rc,sm
	OMPI_MCA_btl: ^vader,tcp,openib,uct
	OMPI_MCA_pml: ucx
        UCX_NET_DEVICES: mlx5_0:1
	OMPI_MCA_spml: ucx
	OMPI_MCA_osc: ucx
      securityContext:
        privileged: true
```

Shell into the Usernetes container once the cluster is up:
```
kubectl apply -f minicluster.yaml

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
TODO
#### Usernetes
TODO


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
time flux run --env OMP_NUM_THREADS=3 -N 2 --tasks-per-node=4 -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_amg.sif amg -n 256 256 128 -P 2 2 2 -problem 2

Running with these driver parameters:
  solver ID    = 3

  Laplacian_27pt:
    (Nx, Ny, Nz) = (512, 512, 256)
    (Px, Py, Pz) = (2, 2, 2)

=============================================
Generate Matrix:
=============================================
Spatial Operator:
  wall clock time = 0.840630 seconds
  wall MFLOPS     = 0.000000
  cpu clock time  = 2.329313 seconds
  cpu MFLOPS      = 0.000000

  RHS vector has unit components
  Initial guess is 0
=============================================
IJ Vector Setup:
=============================================
RHS and Initial Guess:
  wall clock time = 0.099909 seconds
  wall MFLOPS     = 0.000000
  cpu clock time  = 0.142580 seconds
  cpu MFLOPS      = 0.000000

=============================================
Problem 2: Cumulative AMG-GMRES Solve Time:
=============================================
GMRES Solve:
  wall clock time = 194.876108 seconds
  wall MFLOPS     = 0.000000
  cpu clock time  = 570.104697 seconds
  cpu MFLOPS      = 0.000000


No. of Time Steps = 6
Cum. No. of Iterations = 215
Final Relative Residual Norm = 3.916826e-14


nnz AP * (Iterations + time_steps) / Total Time: 

Figure of Merit (FOM_2): 2.234090e+09



real    3m16.702s
user    0m0.072s
sys     0m0.038s
```

#### Usernetes

Usernetes CRD for these tests:
```
apiVersion: flux-framework.org/v1alpha2
kind: MiniCluster
metadata:
  name: flux-sample
spec:
  size: 2
  interactive: true
  flux:
    container:
      disable: true
  containers:
    - image: ghcr.io/converged-computing/usernetes-azure:amg
      volumes:
        memory-dir:
          emptyDir: true
          emptyDirMedium: "memory"
      environment:
        UCX_TLS: rc,sm
	OMPI_MCA_btl: ^vader,tcp,openib,uct
	OMPI_MCA_pml: ucx
        UCX_NET_DEVICES: mlx5_0:1
	OMPI_MCA_spml: ucx
	OMPI_MCA_osc: ucx
      securityContext:
        privileged: true
```

Shell into the Usernetes container once the cluster is up:
```
kubectl apply -f minicluster.yaml

(Pulling    46s   kubelet            Pulling image "ghcr.io/converged-computing/usernetes-azure:amg"
  Normal  Pulled     44s   kubelet            Successfully pulled image "ghcr.io/converged-computing/usernetes-azure:amg" in 1.405s (1.405s including waiting). Image size: 1800886203 bytes.)

kubectl exec -ti flux-sample-0-XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local
```

```
#from performance study experiments
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



real    3m19.647s
user    0m0.064s
sys     0m0.038s
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
#docker.io/milkshake113/resnet:azure-hpc-2404
cd /opt
time flux exec -r 0,1 singularity pull docker://ghcr.io/converged-computing/usernetes-azure:resnet
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
