#!/bin/bash 

master_address="${1:-flux-user000000}"
nodes="${2:-2}"
proc_per_node="${3:-4}"
batch_size="${4:-32}"

# Note that this isn't used, see main.py.
# The pytorch dist automatically provides it
world_size="${6:-1}"

export LOCAL_RANK=${FLUX_TASK_RANK}
export RANK=${LOCAL_RANK}
export OMPI_COMM_WORLD_SIZE=$(nproc)
export WORLD_SIZE=${world_size}
export MASTER_ADDR=${master_address}
export BATCH_SIZE=$batch_size
echo $MASTER_ADDR
echo $FLUX_TASK_RANK

# These are the variables the script can see
# "LOCAL_RANK", "RANK", "GROUP_RANK", "ROLE_RANK", "LOCAL_WORLD_SIZE", "WORLD_SIZE", "ROLE_WORLD_SIZE", "MASTER_ADDR", "MASTER_PORT" BATCH_SIZE

if [[ "${FLUX_TASK_RANK}" == "0" ]]; then
  echo "Torchrun for lead node"
  torchrun \
  --nproc_per_node=${proc_per_node} --nnodes=${nodes} --node_rank=${LOCAL_RANK} \
  --master_addr=$MASTER_ADDR --master_port=8080 \
  /opt/main.py

else
  echo "Torchrun for follower node"
  torchrun \
  --nproc_per_node=${proc_per_node} --nnodes=${nodes} --node_rank=${LOCAL_RANK} \
  --master_addr=$MASTER_ADDR --master_port=8080 \
  /opt/main.py
fi
