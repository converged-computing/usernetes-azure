FROM ghcr.io/converged-computing/flux-tutorials:azure-2404-base
WORKDIR /opt
RUN mkdir lammps && \
   cd lammps && \
   git init && \
   git remote add origin https://github.com/lammps/lammps.git && \
   git fetch --depth 1 origin a8687b53724b630fb5f454c8d7be9f9370f8bb3b && \
   git checkout FETCH_HEAD && \
   mkdir build && \
   cd build && \
   cmake \
  -D CMAKE_INSTALL_PREFIX=/usr \
  -D CMAKE_BUILD_TYPE=Release \
  -D MPI_CXX_COMPILER=mpicxx \
  -D BUILD_MPI=yes \
  -D PKG_ML-SNAP=yes \
  -D PKG_GPU=no \
  -D PKG_REAXFF=on \
  ../cmake && make && make install
RUN chown -R 100 /opt/lammps/examples/reaxff/HNS/
WORKDIR /opt/lammps/examples/reaxff/HNS/
