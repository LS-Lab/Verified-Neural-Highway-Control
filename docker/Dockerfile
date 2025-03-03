# Uses a digest instead of a version number to be as exact as possible.
# This ensures CI doesn't unexpectedly break as a result of a new release.
# However, the version should be manually bumped from time to time.
#
# See also:
# https://www.wolfram.com/engine/
# https://hub.docker.com/r/wolframresearch/wolframengine
# https://docs.docker.com/engine/reference/builder/#from
#
# Digest from version 13.3.0
FROM wolframresearch/wolframengine@sha256:3ff9460b7c53a66f4eb5528e066a40293f3ad935c85f12353ad3dc9fe121c127

# Install KeYmaera X dependencies

USER root

RUN apt-get --yes update
RUN apt-get --yes upgrade
RUN apt-get --yes install openjdk-21-jre-headless bash

##### Install NCubeV

ARG NB_USER="dockeruser"
ARG NB_UID="1000"
ARG NB_GID="100"
RUN useradd --no-log-init --create-home --shell /bin/bash --uid "${NB_UID}" --no-user-group "${NB_USER}"

RUN apt-get install --yes --no-install-recommends git curl build-essential g++
#nano-tiny tzdata unzip make g++ build-essential

# Install Anaconda
USER ${NB_UID}
RUN mkdir -p ~/miniconda3 && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh && bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3 && rm ~/miniconda3/miniconda.sh
ENV PATH="/home/dockeruser/miniconda3/bin:${PATH}"
RUN conda init --all

RUN conda create -y --name versaille python=3.8
RUN conda run -n versaille pip install numpy==1.22.4 &&\
    conda run -n versaille pip install torch==2.4 --index-url https://download.pytorch.org/whl/cpu &&\
    conda run -n versaille pip install onnx==1.12 onnxruntime==1.18.0
#conda run -n versaille pip install stable-baselines3>=2.3 gymnasium    &&\
#conda install -n versaille -y -c anaconda ipykernel &&\
#conda run -n versaille pip install moviepy pygame
USER root

# Julia dependencies
# install Julia packages in /opt/julia instead of ${HOME}
ENV CONDA_DIR=/home/dockeruser/miniconda3 \
    JULIA_DEPOT_PATH=/opt/julia \
    JULIA_PKGDIR=/opt/julia \
    JULIA_CPU_TARGET=generic

RUN mkdir -p /opt/setup-scripts
COPY ./setup_julia.py /opt/setup-scripts/setup_julia.py
COPY ./fix-permissions /opt/setup-scripts/fix-permissions
RUN chmod +x /opt/setup-scripts/setup_julia.py && chmod +x /opt/setup-scripts/fix-permissions && /opt/setup-scripts/setup_julia.py


# Download & Install NCubeV
RUN mkdir /software && chown ${NB_UID}:${NB_GID} /software

USER ${NB_UID}

ENV NCUBEV_VERSION=0c3c65b
RUN cd /software &&\
    git clone https://github.com/samysweb/NCubeV &&\
    cd NCubeV &&\
    git checkout $NCUBEV_VERSION

RUN cd /software/NCubeV/ &&\
    ./build.sh $(which julia)

USER root
RUN ln -s /software/NCubeV/deps/NCubeV/bin/NCubeV /usr/local/bin/NCubeV

RUN mkdir /proofs && mkdir /spec && mkdir /nets
RUN chown ${NB_UID}:${NB_GID} /proofs &&\
    chown ${NB_UID}:${NB_GID} /spec &&\
    chown ${NB_UID}:${NB_GID} /nets

ENV JULIA_PROJECT=/software/NCubeV/

USER ${NB_UID}
WORKDIR /home/dockeruser/
# Custom Data KeYmaera X
COPY *.kyx /proofs
COPY run_benchmark.sh /home/dockeruser/run_benchmark.sh

RUN wget https://github.com/LS-Lab/Verified-Neural-Highway-Control/releases/download/0.9/keymaerax.tar
RUN tar -xzvf keymaerax.tar

# Custom Data NCubeV
COPY /spec /spec
COPY /nets /nets
COPY run_nnv.sh /home/dockeruser/run_nnv.sh

ENTRYPOINT ["/bin/bash"]
