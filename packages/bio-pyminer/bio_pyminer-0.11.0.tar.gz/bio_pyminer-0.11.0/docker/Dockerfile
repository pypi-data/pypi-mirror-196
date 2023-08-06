FROM ubuntu:20.04
RUN apt-get upgrade && \
    apt-get update && \
    #apt-get install -y python3.7 python3-pip && \
    apt-get install -y python3-pip && \
    python3 -V && \
    python3 -m pip install numpy chardet==3.0.4 && \
    python3 -m pip install  bio-pyminer==0.9.8
