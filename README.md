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
//to continue
