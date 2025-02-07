job_name="${1:-flux-sample-}"
nodes="${2:-2}"
proc_per_node="${3:-4}"
batch_size="${4:-32}"
dns_suffix="${5:-}"

export LOCAL_RANK=${FLUX_TASK_RANK}
export RANK=-1
#${FLUX_TASK_RANK}
export WORLD_SIZE=-1
#$((nodes * proc_per_node))
#.flux-service.default.svc.cluster.local
MASTER_ADDR=${job_name}0${dns_suffix}

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
