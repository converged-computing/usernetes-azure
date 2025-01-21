FROM ghcr.io/converged-computing/flux-tutorials:azure-2404-base
WORKDIR /opt
COPY ./gke.cmake /opt/gke.cmake

RUN git clone https://github.com/LLNL/Kripke && \
    cd Kripke && \
    git submodule update --init --recursive && \
    mkdir build && \
    mv /opt/gke.cmake /opt/Kripke/host-configs/gke.cmake && \
    cd /opt/Kripke/build && \
    cmake  -C../host-configs/gke.cmake ../ && make && \
    mv /opt/Kripke/build/kripke.exe /usr/local/bin/kripke && \
    rm -rf /opt/Kripke

ENV PATH=/opt/Kripke:/opt/Kripke/build/bin:$PATH
