FROM ghcr.io/converged-computing/flux-tutorials:azure-2404-base
WORKDIR /opt
ENV MAKE_CXX_FLAG="MPICXX=mpic++"

WORKDIR /opt
RUN mkdir minife && \
    cd minife && \
    git init && \
    git remote add origin https://github.com/Mantevo/minife && \
    git fetch --depth 1 origin abe328816d84afc319c482d6bc8df414b8f90d79 && \
    git checkout FETCH_HEAD

# We are adding this to be able to customize parameters moreso
RUN cd /opt/minife/openmp/src && make && cp miniFE.x /usr/local/bin/miniFE.x
WORKDIR /opt/minife
