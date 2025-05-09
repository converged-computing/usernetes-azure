# AKS setup

```
az aks create \
    --resource-group flux-usernetes-2  \
    --name aks-gpu-vmss \
    --ppg /subscriptions/3e173a37-8f81-492f-a234-ca727b72e6f8/resourceGroups/flux-usernetes-2/providers/Microsoft.Compute/proximityPlacementGroups/flux-usernetes-pg \
    --network-plugin azure \
    --node-count 1 \
    --location southcentralus \
    --enable-node-public-ip \
    --node-vm-size standard_nd40rs_v2 \
    --vm-set-type VirtualMachineScaleSets \
    --load-balancer-sku standard \
    --generate-ssh-keys \
    --aks-custom-headers "ContainerRuntime=containerd" \
    --node-resource-group aks-gpu-pytorch-cluster_nodes_northcentralus
az aks get-credentials --resource-group aks-gpu-pytorch --name aks-gpu-vmss

az aks get-credentials --name "aks-gpu-vmss" --resource-group "flux-usernetes-2"

#az feature register --namespace Microsoft.ContainerService --name AKSInfinibandSupport
#az provider register --namespace Microsoft.ContainerService

...

az aks delete --name "aks-gpu-vmss" --resource-group "flux-usernetes-2"
```


```
kubectl describe node aks-nodepool1-36654457-vmss000000
System Info:
  Machine ID:                 a77a00b8dc274b6099ff199745b5de8d
  System UUID:                ee588be7-2af4-45d0-a9ed-06a40305133c
  Boot ID:                    b3f50fe8-4e0f-4c2f-b42b-5cc37a7b1c14
  Kernel Version:             5.15.0-1084-azure
  OS Image:                   Ubuntu 22.04.5 LTS
  Operating System:           linux
  Architecture:               amd64
  Container Runtime Version:  containerd://1.7.27-1
  Kubelet Version:            v1.31.7
```

```
kubectl get nodes
kubectl apply -f nvidia-device-plugin.yaml
kubectl get nodes -o json | jq .items[].status.allocatable

#from https://github.com/converged-computing/google-performance-study/tree/main/experiments/usernetes/mnist-gpu/gke/size-2

kubectl get nodes -o json > nodes-$(date +%s).json
```

## Experiments

```
kubectl apply --server-side -k "github.com/kubeflow/training-operator.git/manifests/overlays/standalone?ref=v1.8.1"
(simple.yaml from https://github.com/converged-computing/google-performance-study/blob/main/experiments/usernetes/mnist-gpu/gke/size-2/simple.yaml)
```

### 1 node
```
cd size-1/data

for i in $(seq 1 5); do     
  echo "Running iteration $i"
  kubectl apply -f ../../../simple-1node.yaml
  sleep 20
  kubectl logs pytorch-mnist-master-0 -f | tee mnist-master-1-iter-${i}.out
  kubectl wait --for=condition=succeeded --timeout=1200s pytorchjobs.kubeflow.org/pytorch-mnist
  kubectl delete -f ../../../simple-1node.yaml --wait
done

```

### 2 nodes
```
#git clone https://github.com/converged-computing/aks-infiniband-install ./infiniband
#kubectl apply -f infiniband/driver-installation-with-gpu.yaml
#kubectl apply -f infiniband/daemonset/
#we don't need this, just security context

cd size-2/data

for i in $(seq 1 5); do     
  echo "Running iteration $i"
  kubectl apply -f ../../../simple-2nodes.yaml
  sleep 20
  kubectl logs pytorch-mnist-master-0 -f | tee mnist-master-2-iter-${i}.out
  kubectl wait --for=condition=succeeded --timeout=1200s pytorchjobs.kubeflow.org/pytorch-mnist
  kubectl delete -f ../../../simple-2nodes.yaml --wait
done
```

### 4 nodes
```
cd size-4/data

for i in $(seq 1 5); do     
  echo "Running iteration $i"
  kubectl apply -f ../../../simple-4nodes.yaml
  sleep 20
  kubectl logs pytorch-mnist-master-0 -f | tee mnist-master-4-iter-${i}.out
  kubectl wait --for=condition=succeeded --timeout=1200s pytorchjobs.kubeflow.org/pytorch-mnist
  kubectl delete -f ../../../simple-4nodes.yaml --wait
done
```

# Usernetes GPU azure

## Lauching the VMs
- Same setup as regular Usernetes in Azure interface
- change start_script.sh to remove DefaultLimitMEMLOCK=infinity (start-script file will be created here)

## Installing GPU drivers in Ubuntu on Azure
#https://learn.microsoft.com/en-us/azure/virtual-machines/linux/n-series-driver-setup#install-cuda-drivers-on-n-series-vms
Probably this tutorial works : it didn’t work for me the first time because I had already installed things which may have conflicted but in the end, it was those steps that lead to a working setup. The takeaway is we need version 535, 550 won’t work the versions will not match between the client and the kernel

```
sudo apt update && sudo apt install -y ubuntu-drivers-common
sudo ubuntu-drivers install
sudo reboot
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo apt install -y ./cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt -y install cuda-toolkit-12-5

sudo reboot
nvidia-smi
```

Working setup:
```
cat /proc/driver/nvidia/version
NVRM version: NVIDIA UNIX x86_64 Kernel Module  535.183.01  Sun May 12 19:39:15 UTC 2024
GCC version:
```

```
sudo dmesg | grep NVRM
[   11.402126] NVRM: loading NVIDIA UNIX x86_64 Kernel Module  535.183.01  Sun May 12 19:39:15 UTC 2024
```

```
nvidia-smi
Mon Apr  7 19:32:25 2025       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.183.01             Driver Version: 535.183.01   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  Tesla V100-SXM2-32GB           Off | 00000001:00:00.0 Off |                    0 |
| N/A   29C    P0              40W / 300W |      0MiB / 32768MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
|   1  Tesla V100-SXM2-32GB           Off | 00000002:00:00.0 Off |                    0 |
| N/A   31C    P0              42W / 300W |      0MiB / 32768MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
|   2  Tesla V100-SXM2-32GB           Off | 00000003:00:00.0 Off |                    0 |
| N/A   28C    P0              41W / 300W |      0MiB / 32768MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
|   3  Tesla V100-SXM2-32GB           Off | 00000004:00:00.0 Off |                    0 |
| N/A   30C    P0              40W / 300W |      0MiB / 32768MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
|   4  Tesla V100-SXM2-32GB           Off | 00000005:00:00.0 Off |                    0 |
| N/A   28C    P0              40W / 300W |      0MiB / 32768MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
|   5  Tesla V100-SXM2-32GB           Off | 00000006:00:00.0 Off |                    0 |
| N/A   30C    P0              41W / 300W |      0MiB / 32768MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
|   6  Tesla V100-SXM2-32GB           Off | 00000007:00:00.0 Off |                    0 |
| N/A   29C    P0              41W / 300W |      0MiB / 32768MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
|   7  Tesla V100-SXM2-32GB           Off | 00000008:00:00.0 Off |                    0 |
| N/A   30C    P0              40W / 300W |      0MiB / 32768MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
                                                                                         
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|  No running processes found                                                           |
+---------------------------------------------------------------------------------------+
```

```
sudo apt list --installed | grep nvidia

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

libnvidia-cfg1-535/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 amd64 [installed,automatic]
libnvidia-common-535/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 all [installed,automatic]
libnvidia-compute-535/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 amd64 [installed,automatic]
libnvidia-container-tools/unknown,now 1.17.5-1 amd64 [installed,automatic]
libnvidia-container1/unknown,now 1.17.5-1 amd64 [installed,automatic]
libnvidia-decode-535/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 amd64 [installed,automatic]
libnvidia-encode-535/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 amd64 [installed,automatic]
libnvidia-extra-535/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 amd64 [installed,automatic]
libnvidia-fbc1-535/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 amd64 [installed,automatic]
libnvidia-gl-535/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 amd64 [installed,automatic]
linux-modules-nvidia-535-6.11.0-1012-azure/noble-updates,noble-security,now 6.11.0-1012.12~24.04.1+1 amd64 [installed,automatic]
linux-modules-nvidia-535-azure/noble-updates,noble-security,now 6.11.0-1012.12~24.04.1+1 amd64 [installed]
linux-objects-nvidia-535-6.11.0-1012-azure/noble-updates,noble-security,now 6.11.0-1012.12~24.04.1+1 amd64 [installed,automatic]
linux-objects-nvidia-550-6.11.0-1012-azure/noble-updates,noble-security,now 6.11.0-1012.12~24.04.1+1 amd64 [installed,automatic]
linux-signatures-nvidia-6.11.0-1012-azure/noble-updates,noble-security,now 6.11.0-1012.12~24.04.1+1 amd64 [installed,automatic]
nvidia-compute-utils-535/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 amd64 [installed,automatic]
nvidia-container-toolkit-base/unknown,now 1.17.5-1 amd64 [installed,automatic]
nvidia-container-toolkit/unknown,now 1.17.5-1 amd64 [installed]
nvidia-driver-535/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 amd64 [installed]
nvidia-firmware-535-535.183.01/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 amd64 [installed,automatic]
nvidia-firmware-550-550.144.03/unknown,now 550.144.03-0ubuntu1 amd64 [installed,auto-removable]
nvidia-kernel-common-535/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 amd64 [installed,automatic]
nvidia-kernel-source-535/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 amd64 [installed,automatic]
nvidia-prime/noble,now 0.8.17.2 all [installed,automatic]
nvidia-settings/unknown,now 570.124.06-0ubuntu1 amd64 [installed,automatic]
nvidia-utils-535/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 amd64 [installed,automatic]
xserver-xorg-video-nvidia-535/noble-updates,noble-security,now 535.183.01-0ubuntu0.24.04.1 amd64 [installed,automatic]
```

## Launch Usernetes
```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

#uncomment line about envvars at top here:
#the top two lines of this file /etc/nvidia-container-runtime/config.toml

sudo nvidia-ctk runtime configure --runtime=docker --cdi.enabled --config=/etc/docker/daemon.json
sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml --device-name-strategy=uuid
nvidia-ctk cdi list
sudo nvidia-ctk config --in-place --set nvidia-container-runtime.mode=cdi

#IMPORTANT! The last line before the bracket of /usr/bin/dockerd-rootless.sh needs to be
#exec "$dockerd" "--config-file"	"/etc/docker/daemon.json" "$@"

systemctl restart --user docker.service

docker info | grep -i runtimes OK
docker info | grep root OK
```
```
[In a VM after saving the image, we can not do the cp and just run the make from the folder /home/azureuser/usernetes/gpu]
cd /home/azureuser/
git clone https://github.com/converged-computing/flux-usernetes/

#this block only if we changed the number of GPUs
#sudo nvidia-ctk runtime configure --runtime=docker --cdi.enabled --config=/etc/docker/daemon.json
#sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml --device-name-strategy=uuid
#nvidia-ctk cdi list
#sudo nvidia-ctk config --in-place --set nvidia-container-runtime.mode=cdi
#systemctl restart --user docker.service

cd flux-usernetes/google/gpu
cp -R ../../../usernetes/Dockerfile.d .
cp -R ../../../usernetes/Makefile.d .
make up
make nvidia

cp ../../../usernetes/kubeadm-config.yaml .
make kubeadm-init

cp -R ../../../usernetes/init-host .
cp -R ../../../usernetes/hack .
cp -R ../../../usernetes/LICENSE .

make install-flannel
make kubeconfig
export KUBECONFIG=/home/azureuser/flux-usernetes/google/gpu/kubeconfig
kubectl get pods -A

#if we have more than 1 instance
make join-command
flux archive create --name=join-command --mmap -C /home/azureuser/flux-usernetes/google/gpu join-command
flux exec -r 1 flux archive extract --overwrite --name=join-command -C /home/azureuser/flux-usernetes/google/gpu
flux exec -r 1 --dir /home/azureuser/flux-usernetes/google/gpu make up
flux exec -r 1 --dir /home/azureuser/flux-usernetes/google/gpu make nvidia
flux exec -r 1 --dir /home/azureuser/flux-usernetes/google/gpu make kubeadm-join

make sync-external-ip

kubectl taint node u7s-flux-usernetes node-role.kubernetes.io/control-plane:NoSchedule-

kubectl apply -f nvidia-device-plugin.yaml
```

```
azureuser@flux-usernetes:~/flux-usernetes/google/gpu$ kubectl  get pods -n kube-system
NAME                                         READY   STATUS    RESTARTS   AGE
coredns-668d6bf9bc-b88tj                     1/1     Running   0          7m54s
coredns-668d6bf9bc-nr7g2                     1/1     Running   0          7m54s
etcd-u7s-flux-usernetes                      1/1     Running   0          8m2s
kube-apiserver-u7s-flux-usernetes            1/1     Running   0          8m1s
kube-controller-manager-u7s-flux-usernetes   1/1     Running   0          8m1s
kube-proxy-dsvcn                             1/1     Running   0          7m55s
kube-scheduler-u7s-flux-usernetes            1/1     Running   0          8m1s
nvidia-device-plugin-daemonset-5rsnb         1/1     Running   0          35s
```

```
kubectl  logs -n kube-system nvidia-device-plugin-daemonset-2vxcv
Running with config:
{
  "version": "v1",
  "flags": {
    "migStrategy": "none",
    "failOnInitError": false,
    "mpsRoot": "",
    "nvidiaDriverRoot": "/",
    "nvidiaDevRoot": "/",
    "gdsEnabled": false,
    "mofedEnabled": false,
    "useNodeFeatureAPI": null,
    "deviceDiscoveryStrategy": "auto",
    "plugin": {
      "passDeviceSpecs": false,
      "deviceListStrategy": [
        "envvar"
      ],
      "deviceIDStrategy": "uuid",
      "cdiAnnotationPrefix": "cdi.k8s.io/",
      "nvidiaCTKPath": "/usr/bin/nvidia-ctk",
      "containerDriverRoot": "/driver-root"
    }
  },
  "resources": {
    "gpus": [
      {
        "pattern": "*",
        "name": "nvidia.com/gpu"
      }
    ]
  },
  "sharing": {
    "timeSlicing": {}
  },
  "imex": {}
}
I0407 19:26:00.879227       1 main.go:356] Retrieving plugins.
I0407 19:26:20.833934       1 server.go:195] Starting GRPC server for 'nvidia.com/gpu'
I0407 19:26:20.835119       1 server.go:139] Starting to serve 'nvidia.com/gpu' on /var/lib/kubelet/device-plugins/nvidia-gpu.sock
I0407 19:26:20.840687       1 server.go:146] Registered device plugin for 'nvidia.com/gpu' with Kubelet
```

```
kubectl  get nodes -o json | jq -r .items[].status.capacity
{
  "cpu": "40",
  "ephemeral-storage": "128917488Ki",
  "hugepages-1Gi": "0",
  "hugepages-2Mi": "0",
  "memory": "693499704Ki",
  "nvidia.com/gpu": "8",
  "pods": "110"
}
```

## Experiments

```
kubectl apply --server-side -k "github.com/kubeflow/training-operator.git/manifests/overlays/standalone?ref=v1.8.1"
(simple.yaml from https://github.com/converged-computing/google-performance-study/blob/main/experiments/usernetes/mnist-gpu/gke/size-2/simple.yaml)
```

### 1 node
```
outdir=./data
size=1
mkdir -p $outdir

for i in $(seq 1 5); do     
  echo "Running iteration $i"
  kubectl apply -f ./simple-1node.yaml
  sleep 20
  kubectl logs pytorch-mnist-master-0 -f | tee ./$outdir/mnist-master-$size-iter-${i}.out
  kubectl wait --for=condition=succeeded --timeout=1200s pytorchjobs.kubeflow.org/pytorch-mnist
  kubectl delete -f ./simple-1node.yaml --wait
done

```

### 2 nodes
```
outdir=./data
size=2
mkdir -p $outdir

for i in $(seq 1 5); do     
  echo "Running iteration $i"
  kubectl apply -f ./simple-2nodes.yaml
  sleep 20
  kubectl logs pytorch-mnist-master-0 -f | tee ./$outdir/mnist-master-$size-iter-${i}.out
  kubectl wait --for=condition=succeeded --timeout=1200s pytorchjobs.kubeflow.org/pytorch-mnist
  kubectl delete -f ./simple-2nodes.yaml --wait
done
```

### 4 nodes
```
outdir=./data
size=4
mkdir -p $outdir

for i in $(seq 1 5); do     
  echo "Running iteration $i"
  kubectl apply -f ./simple-4nodes.yaml
  sleep 20
  kubectl logs pytorch-mnist-master-0 -f | tee ./$outdir/mnist-master-$size-iter-${i}.out
  kubectl wait --for=condition=succeeded --timeout=1200s pytorchjobs.kubeflow.org/pytorch-mnist
  kubectl delete -f ./simple-4nodes.yaml --wait
done
```

### Debugging
Look at what's going on:
```
export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=INIT,NET
ibv_devinfo
ofed_info -s
```
Result:
```
Using CUDA
Using distributed PyTorch with nccl backend
2025-04-24T15:44:04Z INFO     Added key: store_based_barrier_key:1 to store for rank: 0
2025-04-24T15:44:04Z INFO     Rank 0: Completed store-based barrier for key:store_based_barrier_key:1 with 2 nodes.
pytorch-mnist-master-0:40:40 [0] NCCL INFO Bootstrap : Using eth0:10.244.1.4<0>
pytorch-mnist-master-0:40:40 [0] NCCL INFO NET/Plugin : No plugin found (libnccl-net.so), using internal implementation

pytorch-mnist-master-0:40:40 [0] misc/ibvwrap.cc:63 NCCL WARN Failed to open libibverbs.so[.1]
pytorch-mnist-master-0:40:40 [0] NCCL INFO NET/Socket : Using [0]eth0:10.244.1.4<0>
pytorch-mnist-master-0:40:40 [0] NCCL INFO Using network Socket
NCCL version 2.10.3+cuda10.2
pytorch-mnist-master-0:40:125 [0] NCCL INFO Channel 00/02 :    0   1
pytorch-mnist-master-0:40:125 [0] NCCL INFO Channel 01/02 :    0   1
pytorch-mnist-master-0:40:125 [0] NCCL INFO Trees [0] 1/-1/-1->0->-1 [1] -1/-1/-1->0->1
pytorch-mnist-master-0:40:125 [0] NCCL INFO Setting affinity for GPU 0 to 0fffff
pytorch-mnist-master-0:40:125 [0] NCCL INFO Channel 00 : 1[100000] -> 0[100000] [receive] via NET/Socket/0
pytorch-mnist-master-0:40:125 [0] NCCL INFO Channel 01 : 1[100000] -> 0[100000] [receive] via NET/Socket/0
pytorch-mnist-master-0:40:125 [0] NCCL INFO Channel 00 : 0[100000] -> 1[100000] [send] via NET/Socket/0
pytorch-mnist-master-0:40:125 [0] NCCL INFO Channel 01 : 0[100000] -> 1[100000] [send] via NET/Socket/0
pytorch-mnist-master-0:40:125 [0] NCCL INFO Connected all rings
pytorch-mnist-master-0:40:125 [0] NCCL INFO Connected all trees
pytorch-mnist-master-0:40:125 [0] NCCL INFO threadThresholds 8/8/64 | 16/8/64 | 8/8/512
pytorch-mnist-master-0:40:125 [0] NCCL INFO 2 coll channels, 2 p2p channels, 1 p2p channels per peer
pytorch-mnist-master-0:40:125 [0] NCCL INFO comm 0x7a9f48001360 rank 0 nranks 2 cudaDev 0 busId 100000 - Init COMPLETE
pytorch-mnist-master-0:40:40 [0] NCCL INFO Launch mode Parallel
```


