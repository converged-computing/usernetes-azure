# usernetes-azure


## Launching a cluster

The method described here to launch a cluster uses the Azure interface directly, not Terraform.
After logging into the Azure portal, create a new VMSS with the following attributes (if not mentionned then not modified):

Basic menu:
* name of the VMSS : flux-usernetes
* orchestration mode : Uniform
* number of instances : 2 (or more)
* image : from local azure images ('My Images'), select flux-usernetes-ubuntu-2404
* license type : Other

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

```
cd usernetes
make up
make kubeadm-init
make install-flannel
make kubeconfig
export KUBECONFIG=/home/ubuntu/usernetes/kubeconfig
make join-command
```

Copy the join-command file to all other VMs:
```
flux archive create --name=join-command --mmap -C /home/azureuser/usernetes join-command
flux exec -r 1 flux archive extract --overwrite --name=join-command -C /home/azureuser/usernetes
```
Launch Usernetes on the others VMs:
```
flux exec -r 1 --dir /home/azureuser/usernetes make up
flux exec -r 1 --dir /home/azureuser/usernetes make kubeadm-join
```
Finalize installation of Usernetes, and install the Flux Operator:
```
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
