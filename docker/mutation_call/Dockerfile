FROM python:2.7.14
# debian 8.9

MAINTAINER kchiba <kechiba@ncc.go.jp>

RUN echo "deb http://deb.debian.org/debian stretch main" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian stretch-updates main" >> /etc/apt/sources.list && \
    echo "deb http://security.debian.org stretch/updates main" >> /etc/apt/sources.list && \
    apt-get -y update && \
    apt-get install -y dpkg-dev gcc g++ libc6-dev make patch tar unzip uuid-dev rsync && \
    \ 
    mkdir -p /tools && \
    \
    cd /tools && \
    echo "build BLAT v.35" && \
    wget http://hgdownload.soe.ucsc.edu/admin/exe/userApps.v359.src.tgz && \
    tar -xzvf userApps.v359.src.tgz && \
    rm -f userApps.v359.src.tgz && \
    cd userApps && \
    make && \
    \
    cd /tools && \
    echo "build samtools-1.8" && \
    wget -nc https://sourceforge.net/projects/samtools/files/samtools/1.8/samtools-1.8.tar.bz2 && \
    tar xjvf samtools-1.8.tar.bz2 && \
    rm -f samtools-1.8.tar.bz2 && \
    cd samtools-1.8 && \
    make && \
    make install && \
    \ 
    cd /tools && \
    echo "build htslib-1.8" && \
    wget -nc https://sourceforge.net/projects/samtools/files/samtools/1.8/htslib-1.8.tar.bz2 && \
    tar xvf htslib-1.8.tar.bz2 && \
    rm -f htslib-1.8.tar.bz2 && \
    cd htslib-1.8 && \
    make && \
    make install && \
    \ 
    cd /tools && \
    echo "build bcftools-1.8" && \
    wget -nc https://sourceforge.net/projects/samtools/files/samtools/1.8/bcftools-1.8.tar.bz2 && \
    tar xvf bcftools-1.8.tar.bz2 && \
    rm -f bcftools-1.8.tar.bz2 && \
    cd bcftools-1.8 && \
    make && \
    make install

# python package
RUN pip install --upgrade pip
RUN pip install pysam==0.9.1.4 && \
    pip install numpy==1.12.1 && \
    pip install scipy==0.19.0 && \
    pip install PyVCF==0.6.8 && \
    \
    cd /tools && \
    wget -nc https://github.com/Genomon-Project/GenomonMutationFilter/archive/v0.2.6.zip && \
    unzip v0.2.6.zip && \
    rm -f v0.2.6.zip && \
    cd GenomonMutationFilter-0.2.6 && \
    python setup.py install && \
    \
    cd /tools && \
    wget -nc https://github.com/Genomon-Project/GenomonFisher/archive/v0.4.2.zip && \
    unzip v0.4.2.zip && \
    rm -f v0.4.2.zip && \
    cd GenomonFisher-0.4.2 && \
    python setup.py install && \
    \
    cd /tools && \
    wget -nc https://github.com/Genomon-Project/GenomonMutationAnnotator/archive/v0.1.0.zip && \
    unzip v0.1.0.zip && \
    rm -f v0.1.0.zip && \
    cd GenomonMutationAnnotator-0.1.0 && \
    python setup.py install && \
    \
    cd /tools && \
    wget -nc https://github.com/ken0-1n/mutation_util/archive/v0.5.2.zip && \
    unzip v0.5.2.zip && \
    rm -f v0.5.2.zip && \
    cd mutation_util-0.5.2 && \
    python setup.py install && \
    \
    cd /tools && \
    wget -nc https://github.com/ken0-1n/GenomonHotspotCall/archive/v0.1.0.zip && \
    unzip v0.1.0.zip && \
    rm -f v0.1.0.zip && \
    cd GenomonHotspotCall-0.1.0 && \
    python setup.py install && \
    \
    echo "export LD_LIBRARY_PATH=/usr/local/lib" >> /root/.bashrc

CMD ["/bin/bash"]
