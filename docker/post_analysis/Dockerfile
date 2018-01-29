FROM python:2.7.14
MAINTAINER aokad <aokad@hgc.jp>

RUN apt-get -y update && \
    apt-get install -y wget unzip && \
    \
    wget -nc https://github.com/aokad/GenomonPostAnalysis/archive/v1.4.1.zip && \
    unzip v1.4.1.zip && \
    rm -f v1.4.1.zip && \
    cd GenomonPostAnalysis-1.4.1 && \
    python setup.py build install

CMD ["/bin/bash"]
