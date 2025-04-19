# AKS setup and preliminary tests

```
az aks create \
    --resource-group aks-gpu-pytorch  \
    --name aks-gpu-vmss \
    --ppg /subscriptions/3e173a37-8f81-492f-a234-ca727b72e6f8/resourceGroups/aks-gpu-pytorch/providers/Microsoft.Compute/proximityPlacementGroups/aks-pytorch \
    --network-plugin azure \
    --node-count 1 \
    --location northcentralus \
    --enable-node-public-ip \
    --node-vm-size standard_nc64as_t4_v3 \
    --vm-set-type VirtualMachineScaleSets \
    --load-balancer-sku standard \
    --generate-ssh-keys \
    --aks-custom-headers "ContainerRuntime=containerd" \
    --node-resource-group aks-gpu-pytorch-cluster_nodes_northcentralus
az aks get-credentials --resource-group aks-gpu-pytorch --name aks-gpu-vmss

az aks get-credentials --name "aks-gpu-vmss" --resource-group "aks-gpu-pytorch"

#az feature register --namespace Microsoft.ContainerService --name AKSInfinibandSupport
#az provider register --namespace Microsoft.ContainerService

...

az aks delete --name "aks-gpu-vmss" --resource-group "aks-gpu-pytorch"
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
kubectl apply -f flux-operator.yaml

#from https://github.com/converged-computing/google-performance-study/tree/main/experiments/usernetes/mnist-gpu/gke/size-2

kubectl create namespace monitoring
kubectl apply -f ../kubernetes-event-monitor
mkdir -p ./data/metadata
kubectl get nodes -o json > ./data/metadata/nodes-$NODES-$(date +%s).json

git clone https://github.com/converged-computing/aks-infiniband-install ./infiniband
kubectl apply -f infiniband/driver-installation-with-gpu.yaml
...TODO on 2 nodes

```
## mnist
```
#from https://github.com/converged-computing/google-performance-study/blob/main/experiments/usernetes/mnist-gpu/gke/size-2/simple.yaml
kubectl apply -f 1node.yaml
kubectl apply -f 1node.yaml
sleep 30
kubectl logs pytorch-mnist-master-0 -f | tee ./$outdir/mnist-master-$size-iter-1.out
kubectl delete -f simple.yaml --wait

```
## resnet
```
#https://github.com/converged-computing/usernetes-azure/blob/main/experiments/crd/resnet.yaml
kubectl apply -f resnet.yaml
kubectl exec -ti flux-sample-0-kqs4p -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local
git clone https://github.com/converged-computing/usernetes-azure

export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
export OMPI_MCA_spml=ucx
export OMPI_MCA_osc=ucx
time flux run -N1 -n 40 -o cpu-affinity=per-task python /opt/usernetes-azure/docker/resnet-mpi/main.py --backend=nccl --use_syn --batch_size=128 --arch=resnet18
//not meant for GPUs

#https://github.com/converged-computing/performance-study/blob/45642807dcc995669cda53230a0a94bfe6c833a0/experiments/aws/eks/gpu/crd/resnet.yaml#L16
kubectl apply -f resnet.yaml
kubectl exec -ti flux-sample-0-kqs4p -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local
flux submit ...
//torchvision is not installed, does not work
//trying with the image from the above resnet.yaml gives this error:
//job.exception type=alloc severity=0 sched-simple does not support resource type 'gpu'
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

## Usernetes on 1 node
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
simple.yaml

```

```
kubectl apply --server-side -k "github.com/kubeflow/training-operator.git/manifests/overlays/standalone?ref=v1.8.1"
kubectl apply -f simple.yaml (simple.yaml from flux-usernetes/google/gpu)
```

```


```
