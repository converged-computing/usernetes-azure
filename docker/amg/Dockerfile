FROM ghcr.io/converged-computing/flux-tutorials:azure-2404-base
WORKDIR /opt
RUN git clone https://github.com/LLNL/AMG.git && \
    cd ./AMG && \
    make

ENV PATH=/opt/AMG/test:$PATH
