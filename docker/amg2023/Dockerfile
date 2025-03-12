FROM ghcr.io/converged-computing/flux-tutorials:azure-2404-base

# WARNING: This image does not work - hypre segfaults
# We are using amg vanilla from 2013 instead, which runs OK
# AMD
#  docker build -t ghcr.io/converged-computing/metric-amg2023:azure-int64-zen3 .
#  docker push ghcr.io/converged-computing/metric-amg:azure-hpc-int64-zen3 

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN sudo apt-get update && sudo apt-get install -y cmake

WORKDIR /opt/spack-environment
COPY ./spack.yaml ./spack.yaml

# IMPORTANT: you MUST use this version of spack, as later
# versions will segfault when you run flux + amg
RUN cd /opt/spack-environment \
    && git clone --depth 1 --branch v0.22.1 https://github.com/spack/spack.git \
    && . spack/share/spack/setup-env.sh \
    && spack env activate . \
    && spack install --reuse --fail-fast \
    && spack gc -y

# Modifications to the environment that are necessary to run
RUN cd /opt/spack-environment \
    && . spack/share/spack/setup-env.sh \
    && spack env activate --sh -d . >> /etc/profile.d/z10_spack_environment.sh

ENV PATH=/opt/view/linux-ubuntu24.04-zen2/gcc-13.3.0/amg2023-develop-brv2voedjtlmypn75itlbzp5oamtn6fj/bin:$PATH
