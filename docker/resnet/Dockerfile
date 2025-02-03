FROM ghcr.io/converged-computing/flux-tutorials:azure-2404-base

ARG PYTHON_VERSION=3.11
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /opt

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

COPY main.py launch.sh ./
COPY requirements.txt .

ENV PATH=/opt/conda/bin:$PATH

RUN curl -fsSL -v -o ~/miniconda.sh -O  "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"

RUN chmod +x ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda install -y python=${PYTHON_VERSION} cmake conda-build pyyaml numpy ipython && \
    /opt/conda/bin/python -mpip install -r requirements.txt && \
    /opt/conda/bin/conda clean -ya
    
RUN git clone -b v2.3.0 --depth 1 https://github.com/pytorch/pytorch && \
    cd pytorch && \
    conda install pytorch::torchtriton && \
    git submodule update --init --recursive && \
    PYTORCH_BUILD_VERSION=2.3.0 PYTORCH_BUILD_NUMBER=1 python setup.py bdist_wheel
    
RUN conda install -y python=${PYTHON_VERSION} torchvision
