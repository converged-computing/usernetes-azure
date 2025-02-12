# usernetes-azure


## Launching a cluster

The method described here to launch a cluster uses the Azure interface directly, not Terraform.
After logging into the Azure portal, create a new VMSS with the following attributes (if not mentioned then not modified):

Basic menu:
* name of the VMSS : flux-usernetes
* Resource group : create a new one (flux-usernetes)
* Region : US South Central US (choose a region you have quota for)
* Availability zone: None
* Orchestration mode : Uniform
* Security type: Standard
* Scaling mode: Manually update the capacity
* Number of instances : 2 (or more)
* Image : from local azure images ('My Images'), select flux-usernetes-ubuntu-2404
* Size: Standard_HB120-96RS_V3 96 Vcpu 456 gIb
* SSH choose a pem key or make one
* license type : Other
* Ignore / nothing to change for: spot, disks, management, health
* Networking: virtual network: allow to create new Vnet

When using SSH to connect to the instances, in Networking menu:
* edit network interface to allow SSH
* enable public IP address

Advanced menu:
* enable user data
* in user data, copy paste the start-script.sh file content
* select a placement group (optional)

Once the VMSS is created, you can log into the first VM.

## Installing Usernetes

On the first VM, run the typical steps to install Usernetes:

```console
# git commit we used 1d3956cdfc141bfab1c04a613fa4601ed2474418
cd usernetes
make up
make kubeadm-init
make install-flannel
make kubeconfig
KUBECONFIG=$(pwd)/kubeconfig kubectl get nodes
export KUBECONFIG=$(pwd)/kubeconfig
make join-command
```

Copy the join-command file to all other VMs:

```bash
flux archive create --name=join-command --mmap -C /home/azureuser/usernetes join-command

# The -r refers to ranks, and you should only select the ones active for the instance (flux resource list)
flux exec -r 1 flux archive extract --overwrite --name=join-command -C /home/azureuser/usernetes
```

Launch Usernetes on the others VMs:

```bash
flux exec -r 1 --dir /home/azureuser/usernetes make up
flux exec -r 1 --dir /home/azureuser/usernetes make kubeadm-join
```

Finalize installation of Usernetes, and install the Flux Operator:

```console
make sync-external-ip
echo "export KUBECONFIG=/home/azureuser/usernetes/kubeconfig" >> ~/.bashrc
export KUBECONFIG=/home/azureuser/usernetes/kubeconfig
kubectl get nodes -o wide
kubectl apply -f https://raw.githubusercontent.com/flux-framework/flux-operator/refs/heads/main/examples/dist/flux-operator.yaml
(optional)
On a 2 node cluster, allow pods to be scheduled to the controller node:
kubectl taint node u7s-flux-user000000 node-role.kubernetes.io/control-plane:NoSchedule-
```

From here, we can use Usernetes as normal and create MiniClusters. Example of the minicluster definition I used in my tests is in minicluster.yaml.

```
kubectl apply -f minicluster.yaml
kubectl get pods
kubectl exec -ti flux-sample-XXX -- /bin/bash
export FLUX_URI=local:///mnt/flux/view/run/flux/local
```
