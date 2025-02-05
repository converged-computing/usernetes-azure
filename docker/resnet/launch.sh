job_name="${1:-flux-sample-}"
nodes="${2:-2}"
proc_per_node="${3:-4}"
batch_size="${4:-32}"
dns_suffix="${5:-}"

export LOCAL_RANK=${FLUX_TASK_RANK}
export RANK=${FLUX_TASK_RANK}
export WORLD_SIZE=${nodes}
#.flux-service.default.svc.cluster.local
MASTER_ADDR=${job_name}0${dns_suffix}

if [[ "${FLUX_TASK_RANK}" == "0" ]]; then
  echo "Torchrun for lead node"
  torchrun \
  --nproc_per_node=${proc_per_node} --nnodes=${nodes} --node_rank=${RANK} \
  --master_addr=$MASTER_ADDR --master_port=8080 \
  main.py \
  --backend=mpi --use_syn --batch_size=${batch_size} --arch=resnet152

else
  echo "Torchrun for follower node"
  torchrun \
  --nproc_per_node=${proc_per_node} --nnodes=${nodes} --node_rank=${RANK} \
  --master_addr=$MASTER_ADDR --master_port=8080 \
  main.py \
  --backend=mpi --use_syn --batch_size=${batch_size} --arch=resnet152
fi
