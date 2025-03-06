export OMPI_MCA_pml=ucx
export UCX_TLS=rc,sm
export OMPI_MCA_btl=^vader,tcp,openib,uct
OMPI_MCA_spml=ucx
OMPI_MCA_osc=ucx

for ((i=1; i<=5; i++)); do 
        flux submit -N 4 --tasks-per-node=96 --setattr=user.study_id=$app-4-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux submit -N 8 --tasks-per-node=96 --setattr=user.study_id=$app-8-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux submit -N 16 --tasks-per-node=96 --setattr=user.study_id=$app-16-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
        flux submit -N 32 --tasks-per-node=96 --setattr=user.study_id=$app-32-iter-$i -o cpu-affinity=per-task singularity exec /opt/usernetes-azure_osu.sif /opt/osu-benchmark/build.openmpi/mpi/collective/osu_allreduce;
done
