# At most 28 combinations, 8 nodes 2 at a time
hosts=$(flux run -N 32 hostname | shuf -n 8 | tr '\n' ' ')
list=${hosts}

dequeue_from_list() {
  shift;
  list=$@
}

iter=0
for i in $hosts; do
  dequeue_from_list $list
  for j in $list; do
    echo "${i} ${j}"
    time flux submit --exclusive -N 2 -n 2 \
      --setattr=user.study_id=osu_latency-2-iter-$iter \
      --requires="hosts:${i},${j}" \
      -o cpu-affinity=per-task \
      singularity exec /opt/usernetes-azure_osu.sif \
      /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_latency
    time flux submit --exclusive -N 2 -n 2 \
      --setattr=user.study_id=osu_bw-2-iter-$iter \
      --requires="hosts:${i},${j}" \
      -o cpu-affinity=per-task \
      singularity exec /opt/usernetes-azure_osu.sif \
      /opt/osu-benchmark/build.openmpi/mpi/pt2pt/osu_bw
    iter=$((iter+1))
done
done
