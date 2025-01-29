FROM ghcr.io/converged-computing/flux-tutorials:azure-2404-base

ARG PYTHON_VERSION=3.11
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /opt

COPY main.py launch.sh ./
COPY requirements.txt .

RUN /usr/sbin/update-ccache-symlinks
RUN mkdir /opt/ccache && ccache --set-config=cache_dir=/opt/ccache
ENV PATH=/opt/conda/bin:$PATH

RUN curl -fsSL -v -o ~/miniconda.sh -O  "https://repo.anaconda.com/miniconda/Minn
iconda3-latest-Linux-x86_64.sh"
# Manually invoke bash on miniconda script per https://github.com/conda/conda/iss
sues/10431
RUN chmod +x ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda install -y python=${PYTHON_VERSION} cmake conda-build pp
yyaml numpy ipython && \
    /opt/conda/bin/python -mpip install -r requirements.txt && \
    /opt/conda/bin/conda clean -ya

RUN git clone -b v2.3.0 --depth 1 https://github.com/pytorch/pytorch && \
    cd pytorch && \
    conda install pytorch::torchtriton && \
    conda install pytorch torchvision torchaudio cpuonly -c pytorch && \
    git submodule update --init --recursive && \
    PYTORCH_BUILD_VERSION=2.3.0 PYTORCH_BUILD_NUMBER=1 python setup.py bdist_whee
el

RUN chmod a+x /opt/launch.sh
RUN chmod a+x /opt/main.py
