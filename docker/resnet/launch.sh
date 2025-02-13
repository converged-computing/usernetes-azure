master="${1:-flux-user000000}"
nodes="${2:-2}"
proc_per_node="${3:-96}"
batch_size="${4:-128}"

export LOCAL_RANK=${FLUX_TASK_RANK}
MASTER_ADDR=${master}

if [[ "${FLUX_TASK_RANK}" == "0" ]]; then
  echo "Torchrun for lead node"
  torchrun \
  --nproc_per_node=${proc_per_node} --nnodes=${nodes} --node_rank=${LOCAL_RANK} \
  --master_addr=$MASTER_ADDR --master_port=8080 \
  main.py \
  --backend=gloo --use_syn --batch_size=${batch_size} --arch=resnet18

else
  echo "Torchrun for follower node"
  torchrun \
  --nproc_per_node=${proc_per_node} --nnodes=${nodes} --node_rank=${LOCAL_RANK} \
  --master_addr=$MASTER_ADDR --master_port=8080 \
  main.py \
  --backend=gloo --use_syn --batch_size=${batch_size} --arch=resnet18
fi
