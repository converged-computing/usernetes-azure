# Pytorch testing

This is a derivative of resnet, but using a model that we can control (and a simpler script to debug). We did this for initial testing when resnet was having trouble. It creates a Multi layer perceptron (MLP) instead.

## Items to do! 📝

- We are going to use gloo, it will show there is overhead but it works
- Lise is going to look into running an LLM (e.g., training-operator)
- Look into boosting mtu (currently at 1500)
- Try Resnet, fewer iterations (less than 10 minutes)
- Downloading the dataset

## Usage 🧐

### Container pull

I testing with `docker://ghcr.io/converged-computing/usernetes-azure:resnet` and built this container (should be the same) that adds the launch.sh and main.py scripts here.

```console
# Takes 8m44.692s
cd /opt
time flux exec -r 0,1 singularity pull docker://ghcr.io/converged-computing/usernetes-azure:pytorch
```

### Run directory

Make a directory to run the experiment from.

```bash
mkdir experiment
cd experiment
```

### 1 node

```console
# One node (52 seconds with download of data)
# 47.7 already with data

# This is what I tested
container=/opt/usernetes-azure_pytorch.sif

time flux run --requires="host:flux-user000000" -N 1 singularity exec --bind /tmp:/tmp --bind /opt/run/flux:/opt/run/flux $container /bin/bash /opt/launch.sh flux-user00000 1 $(nproc) 128 1

time flux run --requires="host:flux-user000000" -N 1 singularity exec --bind /tmp:/tmp --bind /opt/run/flux:/opt/run/flux --bind /opt/experiment/launch.sh:/opt/launch.sh --bind /opt/experiment/main.py:/opt/main.py  $container /bin/bash /opt/launch.sh flux-user000000 1 $(nproc) 128 1
```

### 2 nodes 

```console
# Two nodes (54 seconds) (including download of data for one)
# Two nodes (43.8 seconds) (not needing to download data)

# This is what I tested
container=/opt/usernetes-azure_pytorch.sif

time flux run -N 2 singularity exec --bind /tmp:/tmp --bind /opt/run/flux:/opt/run/flux --bind /opt/experiment/launch.sh:/opt/launch.sh --bind /opt/experiment/main.py:/opt/main.py $container /bin/bash /opt/launch.sh flux-user000000 2 $(nproc) 128 1

time flux run -N 2 singularity exec --bind /tmp:/tmp --bind /opt/run/flux:/opt/run/flux --bind /opt/usernetes-azure/docker/resnet/launch.sh:/opt/launch.sh --bind /opt/usernetes-azure/docker/resnet/main-test.py:/opt/main.py $container /bin/bash /opt/launch.sh flux-user00000 2 128 1
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
# This is the only setup we got working, with run.py
mpirun -n 96 singularity exec --bind /tmp:/tmp --bind /opt/run/flux:/opt/run/flux --bind /opt/mlnx/ /opt/usernetes-azure_resnet.sif python3 ./run.py 
```

</details>
