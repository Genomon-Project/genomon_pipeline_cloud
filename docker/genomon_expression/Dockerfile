FROM ubuntu:16.04
MAINTAINER Yuichi Shiraishi <friend1ws@gmail.com> 

RUN apt-get update && apt-get install -y \
    git \
    wget \
    bzip2 \
    make \
    gcc \
    zlib1g-dev \
    python \
    python-pip \
    bedtools=2.25.0-1

RUN wget https://github.com/samtools/htslib/releases/download/1.3.2/htslib-1.3.2.tar.bz2 && \
    tar jxvf htslib-1.3.2.tar.bz2 && \
    cd htslib-1.3.2 && \
    make && \
    make install

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install pysam==0.11.2.1

RUN pip install annot-utils==0.2.0

Run pip install genomon-expression==0.4.0

