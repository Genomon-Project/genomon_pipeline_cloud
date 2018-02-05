FROM ubuntu:16.04
MAINTAINER Yuichi Shiraishi <friend1ws@gmail.com> 


RUN apt-get update && apt-get install -y \
    git \
    wget \
    bzip2 \
    make \
    gcc \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    python \
    python-pip


RUN wget https://github.com/samtools/htslib/releases/download/1.7/htslib-1.7.tar.bz2 && \
    tar jxvf htslib-1.7.tar.bz2 && \
    cd htslib-1.7 && \
    make && \
    make install

RUN wget https://github.com/arq5x/bedtools2/releases/download/v2.27.0/bedtools-2.27.0.tar.gz && \
    tar zxvf bedtools-2.27.0.tar.gz && \
    cd bedtools2 && make
ENV PATH $PATH:/bedtools2/bin 

RUN wget https://github.com/mengyao/Complete-Striped-Smith-Waterman-Library/archive/v1.1.tar.gz && \
    tar zxvf v1.1.tar.gz && cd Complete-Striped-Smith-Waterman-Library-1.1/src && \
    gcc -Wall -O3 -pipe -fPIC -shared -rdynamic -o libssw.so ssw.c ssw.h
ENV LD_LIBRARY_PATH /Complete-Striped-Smith-Waterman-Library-1.1/src

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install pysam==0.13
RUN pip install annot_utils==0.2.0
RUN pip install intron_retention_utils==0.4.0

