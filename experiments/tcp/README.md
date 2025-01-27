# Experiments

## Bare metal

### latency
```
unset OMPI_MCA_pml
export UCX_TLS=tcp
time flux run -N2 -n2 -o cpu-affinity=per-task singularity exec --env=UCX_NET_DEVICES=eth0 /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency
# OSU MPI Latency Test v5.8
# Size          Latency (us)
0                       1.82
1                       1.77
2                       1.76
4                       1.76
8                       1.76
16                      1.93
32                      1.95
64                      2.01
128                     2.46
256                     2.50
512                     2.60
1024                    2.77
2048                    2.86
4096                    3.23
8192                    3.77
16384                   7.49
32768                   8.37
65536                  10.95
131072                 16.17
262144                 26.61
524288                 47.50
1048576                89.13
2097152               172.54
4194304               341.20

real	0m3.120s
user	0m0.076s
sys	0m0.021s
```

### bandwidth
```
unset OMPI_MCA_pml
export UCX_TLS=tcp
#/opt/flux-tutorials_azure-2404-osu.sif
time flux run -N2 -n2 -o cpu-affinity=per-task singularity exec --env=UCX_NET_DEVICES=eth0 /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw
time flux run -N2 -n2 -o cpu-affinity=per-task singularity exec --env=UCX_NET_DEVICES=eth0 /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw
# OSU MPI Bandwidth Test v5.8
# Size      Bandwidth (MB/s)
1                       2.99
2                       5.98
4                      11.64
8                      24.33
16                     49.46
32                     97.14
64                    183.39
128                   352.40
256                   690.76
512                  1282.18
1024                 2428.13
2048                 3550.39
4096                 7116.18
8192                10586.74
16384               10091.80
32768               11818.33
65536               12224.25
131072              12397.54
262144              12486.41
524288              12533.83
1048576             12536.67
2097152             12568.19
4194304             12453.77

real	0m2.645s
user	0m0.067s
sys	0m0.029s

```

### iperf
We use iperf and not iperf3 to use multithreading and test the bandwidth with multiple streams.
Install iperf:
```
flux exec -r all sudo apt install iperf

```
```
#first terminal on node 1
iperf -s

#second terminal on node 2
iperf -c IP-node-1

------------------------------------------------------------
Client connecting to 172.16.0.4, TCP port 5001
TCP window size: 16.0 KByte (default)
------------------------------------------------------------
[  1] local 172.16.0.5 port 43172 connected with 172.16.0.4 port 5001 (icwnd/mss/irtt=13/1398/891)
[ ID] Interval       Transfer     Bandwidth
[  1] 0.0000-10.0117 sec  27.3 GBytes  23.5 Gbits/sec

[  1] 0.0000-10.0050 sec  29.5 GBytes  25.3 Gbits/sec

[  1] 0.0000-10.0024 sec  25.3 GBytes  21.7 Gbits/sec

[  1] 0.0000-10.0132 sec  17.0 GBytes  14.6 Gbits/sec

[  1] 0.0000-10.0115 sec  25.5 GBytes  21.9 Gbits/sec
```

With multiple streams:
```
#first terminal on node 1
iperf -s

#second terminal on node 2
iperf -c IP-node-1 -P 30

[SUM] 0.0000-10.0078 sec  44.4 GBytes  38.1 Gbits/sec

[SUM] 0.0000-10.0027 sec  44.4 GBytes  38.1 Gbits/sec

[SUM] 0.0000-10.0149 sec  44.4 GBytes  38.1 Gbits/sec

[SUM] 0.0000-10.0067 sec  44.4 GBytes  38.1 Gbits/sec

[SUM] 0.0000-10.0078 sec  44.4 GBytes  38.1 Gbits/sec
```


## Usernetes

### OSU container

We use the same container as from the experiments folder for OSU.
We use this CRD :
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
        UCX_TLS: tcp
      securityContext:
        privileged: true
```

Launch and enter the container to run the commands:
```
kubectl apply -f minicluster.yaml
kubectl exec -ti flux-sample-0-XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local
```

### latency
```
unset UCX_NET_DEVICES
time flux run -N2 -n2 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency

# OSU MPI Latency Test v5.8
# Size          Latency (us)
0                     147.07
1                     145.58
2                     146.81
4                     143.86
8                     139.90
16                    140.53
32                    140.18
64                    133.28
128                   140.23
256                   140.80
512                   138.64
1024                  140.14
2048                  167.21
4096                  187.06
8192                  305.24
16384                 461.80
32768                1066.31
65536                1788.14
131072               3320.30
262144               6153.32
524288              10355.21
1048576             15749.88
2097152             24450.76
4194304             49079.73

real	4m35.461s
user	0m0.080s
sys	0m0.022s
```

### bandwidth
```
unset UCX_NET_DEVICES
time flux run -N2 -n2 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw

# OSU MPI Bandwidth Test v5.8
# Size      Bandwidth (MB/s)
1                       0.03
2                       0.05
4                       0.12
8                       0.31
16                      0.62
32                      1.24
64                      2.57
128                     4.00
256                    10.06
512                    13.96
1024                   28.60
2048                   34.70
4096                   46.47
8192                   49.51
16384                  82.76
32768                  88.25
65536                  56.15
131072                 79.94
262144                 79.69
524288                 74.28
1048576                70.91
2097152                73.91
4194304                76.02

real	2m43.376s
user	0m0.075s
sys	0m0.025s
```

### iperf container

We use a container with the same base image as the other benchmarks, and install iperf. See the Dockerfile 
from this repository.
We use this CRD :
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
    - image: docker.io/milkshake113/iperf:azure-hpc-2404
      volumes:
        memory-dir:
          emptyDir: true
          emptyDirMedium: "memory"
      securityContext:
        privileged: true
```

### iperf
We use iperf and not iperf3 to use multithreading and test the bandwidth with multiple streams.
```
#first terminal on pod 1
iperf -s

#second terminal on pod 2
iperf -c IP-pod-1

[  1] 0.0000-10.0592 sec   678 MBytes   566 Mbits/sec

[  1] 0.0000-10.0530 sec   696 MBytes   581 Mbits/sec

[  1] 0.0000-10.0893 sec   679 MBytes   565 Mbits/sec

[  1] 0.0000-10.0420 sec   601 MBytes   502 Mbits/sec

[  1] 0.0000-10.0809 sec   710 MBytes   591 Mbits/sec
```

With multiple streams:
```
#first terminal on pod 1
iperf -s

#second terminal on pod 2
iperf -c IP-pod-1 -P 30

[SUM] 0.0000-10.1431 sec   526 MBytes   435 Mbits/sec

[SUM] 0.0000-10.2030 sec   568 MBytes   467 Mbits/sec

[SUM] 0.0000-10.1870 sec   513 MBytes   422 Mbits/sec

[SUM] 0.0000-10.1378 sec   610 MBytes   504 Mbits/sec

[SUM] 0.0000-10.1715 sec   545 MBytes   449 Mbits/sec
```
