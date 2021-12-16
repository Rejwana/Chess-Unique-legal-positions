FROM nvidia/cuda:10.0-cudnn7-devel as builder

COPY . /

## Install Prerequisites

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git wget unzip ninja-build python3.8 python3-pip gcc-8 g++-8 libeigen3-dev clang libopenblas-dev vim && \
    pip3 install meson

RUN apt-get install -y mysql-client
RUN apt-get install -y mysql-server

WORKDIR /Py
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
RUN pip3 install pipenv && pipenv install --system --deploy --ignore-pipfile

WORKDIR /
