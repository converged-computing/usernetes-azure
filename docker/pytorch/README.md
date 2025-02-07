# Pytorch testing

This is a derivative of resnet, but using a model that we can control (and a simpler script to debug). It is currently running 8 epocs at a reasonable time for 1 and 2 nodes, but the time increases with 2 nodes so likely we want to debug that.

## Items to do! 📝

0. First we should reproduce what I did - both 1/2 nodes should work, and the second is slower.
1. Next, I think we want to adjust the dataset loader batch size to be world size divided by procs per one worker (right now it is set to the batch size, which could explain not scaling).
2. When it is working, we can try switching batch to the official resnet model to try. If it doesn't work, we might compare the init params, and maximally get it working, minimally could conclude it is something about the model.
3. When that is working, think about the dataset.
  - If we download the dataset here, let's wrap that command to time it.
  - If it's slow (or just to save time/money) we might consider a download and then save to an ORAS archive
  - We can exec download to all nodes to avoid needing to download (I saw errors with download on a worker once and I think we should avoid that)
4. Are there other operations we want to wrap to time?
5. Figure out the right parameters to adjust (e.g., 2 nodes should not be slower)
6. Compare our model to Resnet to assess similarity
7. When all is good, rebuild container and update instructions in main experiment README.

## Usage 🧐

### Container pull

I testing with `docker://ghcr.io/converged-computing/usernetes-azure:resnet` and built this container (should be the same) that adds the launch.sh and main.py scripts here.

```console
cd /opt
time flux exec -r 0,1 singularity pull docker://ghcr.io/converged-computing/usernetes-azure:resnet
```

### 1 node

```console
# One node (52 seconds)

# This is what I tested
container=/opt/usernetes-azure_pytorch.sif

time flux run --requires="host:flux-user000000" -N 1 singularity exec --bind /tmp:/tmp --bind /opt/run/flux:/opt/run/flux --bind /opt/usernetes-azure/docker/resnet/launch.sh:/opt/launch.sh --bind /opt/usernetes-azure/docker/resnet/main-test.py:/opt/main.py $container /bin/bash /opt/launch.sh flux-user00000 1 $(nproc) 128

# But I think we can try this to use the script in the container
time flux run --requires="host:flux-user000000" -N 1 singularity exec --bind /tmp:/tmp --bind /opt/run/flux:/opt/run/flux $container /bin/bash /opt/launch.sh flux-user00000 1 $(nproc) 128
```

### 2 nodes 

```console
# Two nodes (1m 24 seconds)

# This is what I tested
container=/opt/usernetes-azure_pytorch.sif

time flux run -N 2 singularity exec --bind /tmp:/tmp --bind /opt/run/flux:/opt/run/flux --bind /opt/usernetes-azure/docker/resnet/launch.sh:/opt/launch.sh --bind /opt/usernetes-azure/docker/resnet/main-test.py:/opt/main.py $container /bin/bash /opt/launch.sh flux-user00000 2 192 128

# And we can try this to use the scripts in the container
time flux run -N 2 singularity exec --bind /tmp:/tmp --bind /opt/run/flux:/opt/run/flux $container /bin/bash /opt/launch.sh flux-user00000 2 192 128
```

### MPI (not tested)

<details>

<summary>Instructions for MPI</summary>

Note that I did export these envars for the first run, but using gloo I don't think it would matter. If there are issues above we should try exporting them.

```console
export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx
```

Here are the original notes from Lise.

```console
#backend=mpi
flux run -N 1 -o cpu-affinity=per-task --tasks-per-node=1 -o mpi=none -o pmi=pmix singularity exec --bind /tmp:/tmp --bind /opt/run/flux:/opt/run/flux --bind launch.sh:/opt/launch.sh --bind main.py:/opt/main.py /opt/usernetes-azure_resnet.sif /bin/bash /opt/launch.sh flux-user00000 1 8 128
Torchrun for lead node
W0207 11:51:48.344000 133469446010688 torch/distributed/run.py:757] 
W0207 11:51:48.344000 133469446010688 torch/distributed/run.py:757] *****************************************
W0207 11:51:48.344000 133469446010688 torch/distributed/run.py:757] Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
W0207 11:51:48.344000 133469446010688 torch/distributed/run.py:757] *****************************************
Rank 0 initialized, WORLD SIZE: 1
Rank 0 initialized, WORLD SIZE: 1
Rank 0 initialized, WORLD SIZE: 1
Rank 0 initialized, WORLD SIZE: 1
Rank 0 initialized, WORLD SIZE: 1
Rank 0 initialized, WORLD SIZE: 1
Rank 0 initialized, WORLD SIZE: 1
Rank 0 initialized, WORLD SIZE: 1
epoch : 0.0000
epoch : 0.0000
epoch : 0.0000
epoch : 0.0000
epoch : 0.0000
epoch : 0.0000
epoch : 0.0000
epoch : 0.0000

#backend=gloo
flux run -N 1 -o cpu-affinity=per-task --tasks-per-node=1 -o mpi=none -o pmi=pmix singularity exec --bind /tmp:/tmp --bind /opt/run/flux:/opt/run/flux --bind launch.sh:/opt/launch.sh --bind main.py:/opt/main.py /opt/usernetes-azure_resnet.sif /bin/bash /opt/launch.sh flux-user00000 1 8 128
Torchrun for lead node
W0207 11:52:25.138000 135745581799232 torch/distributed/run.py:757] 
W0207 11:52:25.138000 135745581799232 torch/distributed/run.py:757] *****************************************
W0207 11:52:25.138000 135745581799232 torch/distributed/run.py:757] Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
W0207 11:52:25.138000 135745581799232 torch/distributed/run.py:757] *****************************************
Rank 0 initialized, WORLD SIZE: 8
Rank 1 initialized, WORLD SIZE: 8
Rank 2 initialized, WORLD SIZE: 8
Rank 3 initialized, WORLD SIZE: 8
Rank 4 initialized, WORLD SIZE: 8
Rank 5 initialized, WORLD SIZE: 8
Rank 6 initialized, WORLD SIZE: 8
Rank 7 initialized, WORLD SIZE: 8
epoch : 0.0000
epoch : 0.0000
epoch : 0.0000
epoch : 0.0000
epoch : 0.0000
epoch : 0.0000
epoch : 0.0000
epoch : 0.0000
```

</details>
