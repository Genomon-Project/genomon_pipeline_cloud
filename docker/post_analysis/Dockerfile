FROM python:3.7.5-buster
MAINTAINER aokad <aokad@hgc.jp>

RUN apt-get -y update && \
    apt-get install -y wget unzip && \
    \
    wget -nc https://github.com/aokad/GenomonPostAnalysis/archive/v1.5.0.zip && \
    unzip v1.5.0.zip && \
    rm -f v1.5.0.zip && \
    cd GenomonPostAnalysis-1.5.0 && \
    python setup.py build install

CMD ["/bin/bash"]
