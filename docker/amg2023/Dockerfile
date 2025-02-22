FROM ghcr.io/converged-computing/flux-tutorials:azure-2404-base

# WARNING: This image does not work - hypre segfaults
# We are using amg vanilla from 2013 instead, which runs OK
# AMD
#  docker build -t ghcr.io/converged-computing/metric-amg2023:azure-int64-zen3 .
#  docker push ghcr.io/converged-computing/metric-amg:azure-hpc-int64-zen3 

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /opt
RUN git clone https://github.com/hypre-space/hypre && \
        cd hypre/src/ && ./configure && \
        make -j 4 && \
        make install

COPY Makefile .
RUN git clone https://github.com/LLNL/AMG2023 && \
        cd AMG2023/ && cp /opt/Makefile . && make -j 4
RUN cp /opt/AMG2023/amg /usr/bin/amg
