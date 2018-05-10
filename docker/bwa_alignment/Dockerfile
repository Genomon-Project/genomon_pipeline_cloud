FROM python:2.7.14
# debian 8.9

MAINTAINER aokad <aokad@hgc.jp>

RUN echo "deb http://deb.debian.org/debian stretch main" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian stretch-updates main" >> /etc/apt/sources.list && \
    echo "deb http://security.debian.org stretch/updates main" >> /etc/apt/sources.list && \
    apt-get -y update && \
    apt-get install -y dpkg-dev gcc g++ libc6-dev make patch tar unzip && \
    \
    mkdir -p /tools && \
    \
    cd /tools && \
    echo "build bwa-0.7.8" && \
    wget http://sourceforge.net/projects/bio-bwa/files/bwa-0.7.8.tar.bz2 && \
    tar xjvf bwa-0.7.8.tar.bz2 && \
    cd bwa-0.7.8 && \
    make && \
    \ 
    cd /tools && \
    echo "build samtools-1.2" && \
    wget -nc https://sourceforge.net/projects/samtools/files/samtools/1.2/samtools-1.2.tar.bz2 && \
    tar xjvf samtools-1.2.tar.bz2 && \
    rm -f samtools-1.2.tar.bz2 && \
    cd samtools-1.2 && \
    make && \
    make install && \
    \ 
    cd /tools && \
    echo "build libmaus-0.0.196" && \
    wget https://github.com/gt1/libmaus/archive/0.0.196-release-20150326095654.tar.gz && \
    tar xzvf 0.0.196-release-20150326095654.tar.gz && \
    rm -f 0.0.196-release-20150326095654.tar.gz && \
    cd libmaus-0.0.196-release-20150326095654 && \
    autoreconf -i -f && \
    ./configure && \
    make && \
    make install && \
    \ 
    cd /tools && \
    echo "build biobambam-0.0.191" && \
    wget -nc https://github.com/gt1/biobambam/archive/0.0.191-release-20150401083643.tar.gz && \
    tar xzvf 0.0.191-release-20150401083643.tar.gz && \
    rm -f 0.0.191-release-20150401083643.tar.gz && \
    cd biobambam-0.0.191-release-20150401083643 && \
    autoreconf -i -f && \
    ./configure && \
    make && \
    make install && \
    \ 
    echo "export LD_LIBRARY_PATH=/usr/local/lib" >> /root/.bashrc

CMD ["/bin/bash"]
