## Get data
```
mkdir -p data/bare
mkdir -p data/usernetes
oras pull ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-osu_allreduce
oras pull ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-osu_pt2pt_exclusive
oras pull ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-lammps
oras pull ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-amg
oras pull ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-minife
mv results/* data/bare/
oras pull ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-osu_allreduce
oras pull ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-osu_pt2pt_exclusive
oras pull ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-lammps
oras pull ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-amg
oras pull ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-minife
mv results/* data/usernetes/
```

```
python3 analysis.py
```

