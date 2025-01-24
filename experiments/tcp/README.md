# Experiments

## Bare metal

### latency
```
export OMPI_MCA_pml=ucx
export UCX_TLS=tcp
time flux run -N2 -n2 -o cpu-affinity=per-task singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency
```

### bandwidth
```
export OMPI_MCA_pml=ucx
export UCX_TLS=tcp
time flux run -N2 -n2 -o cpu-affinity=per-task singularity exec /opt/flux-tutorials_azure-2404-osu.sif /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw
```

### iperf
We use iperf and not iperf3 to use multithreading and test the bandwidth with multiple streams.
```
#first terminal on node 1
iperf3 -s

#second terminal on node 2
iperf -c IP-node-1
```

With multiple streams (30 is arbitrary, TODO test mutliple ones to max out and pick this number):
```
#first terminal on node 1
iperf3 -s

#second terminal on node 2
iperf -P 30 -c IP-node-1
```


## Usernetes

### latency
```
export OMPI_MCA_pml=ucx
export UCX_TLS=tcp
time flux run -N2 -n2 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency
```

### bandwidth
```
export OMPI_MCA_pml=ucx
export UCX_TLS=tcp
time flux run -N2 -n2 -o cpu-affinity=per-task /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw
```

### iperf
We use iperf and not iperf3 to use multithreading and test the bandwidth with multiple streams.
```
#first terminal on pod 1
iperf3 -s

#second terminal on pod 2
iperf -c IP-pod-1
```

With multiple streams (30 is arbitrary, TODO test mutliple ones to max out and pick this number):
```
#first terminal on pod 1
iperf3 -s

#second terminal on pod 2
iperf -P 30 -c IP-pod-1
```
