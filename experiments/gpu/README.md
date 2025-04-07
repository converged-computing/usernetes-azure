# Usernetes GPU azure

- Same setup as regular Usernetes in Azure interface

## GPU drivers in Ubuntu on Azure
#https://learn.microsoft.com/en-us/azure/virtual-machines/linux/n-series-driver-setup#install-cuda-drivers-on-n-series-vms
Mostly this but didn’t work the first time… we need version 535 basically, 550 won’t work the versions will not match

```
sudo apt install nvidia-driver-550 nvidia-dkms-550
sudo apt update && sudo apt install -y ubuntu-drivers-common
sudo ubuntu-drivers install
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo apt install -y ./cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt -y install cuda-toolkit-12-5

sudo reboot
nvidia-smi
```

Working setup:
cat /proc/driver/nvidia/version
NVRM version: NVIDIA UNIX x86_64 Kernel Module  535.183.01  Sun May 12 19:39:15 UTC 2024
GCC version:

sudo dmesg | grep NVRM
[   11.402126] NVRM: loading NVIDIA UNIX x86_64 Kernel Module  535.183.01  Sun May 12 19:39:15 UTC 2024



## Usernetes on 1 node
```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```
#uncomment line about envvars at top here:
#the top two lines of this file /etc/nvidia-container-runtime/config.toml
```
sudo nvidia-ctk runtime configure --runtime=docker --cdi.enabled --config=/etc/docker/daemon.json
sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml --device-name-strategy=uuid
nvidia-ctk cdi list
sudo nvidia-ctk config --in-place --set nvidia-container-runtime.mode=cdi
```
#IMPORTANT! The last line of /usr/bin/dockerd-rootless.sh needs to be
#exec "$dockerd" "--config-file"	"/etc/docker/daemon.json" "$@"
#replaces an existing line, actually second to last line
```
systemctl restart --user docker.service

docker info | grep -i runtimes OK
docker info | grep root OK

cd /home/azureuser/
git clone https://github.com/converged-computing/flux-usernetes/
```
```
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
