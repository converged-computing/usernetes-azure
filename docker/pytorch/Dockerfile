FROM ghcr.io/converged-computing/flux-tutorials:azure-2404-base

# docker build -t ghcr.io/converged-computing/usernetes-azure:pytorch .
# docker push ghcr.io/converged-computing/usernetes-azure:pytorch

ARG PYTHON_VERSION=3.11
ENV DEBIAN_FRONTEND=noninteractive
ENV UCX_NET_DEVICES=mlx5_0:1
ENV UCX_TLS=ib
ENV OMPI_MCA_btl_openib_warn_no_device_params_found=0

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        ccache \
        cmake \
        curl \
        git \
        libjpeg-dev \
        libpng-dev && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=/opt/conda/bin:$PATH

RUN curl -fsSL -v -o ~/miniconda.sh -O  "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"

COPY requirements.txt .
RUN chmod +x ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda install -y python=${PYTHON_VERSION} cmake conda-build pyyaml numpy ipython && \
    /opt/conda/bin/python -mpip install -r requirements.txt && \
    /opt/conda/bin/conda clean -ya

WORKDIR /opt
COPY main.py launch.sh ./

RUN git clone -b v2.3.0 --depth 1 https://github.com/pytorch/pytorch && \
    cd pytorch && \
    conda install pytorch::torchtriton && \
    conda install torchvision && \
    git submodule update --init --recursive && \
    PYTORCH_BUILD_VERSION=2.3.0 PYTORCH_BUILD_NUMBER=1 CMAKE_C_COMPILER=$(which mpicc) CMAKE_CXX_COMPILER=$(which mpicxx) python setup.py build develop && \
    python setup.py install
   
ENTRYPOINT ["/bin/bash", "/opt/launch.sh"]
