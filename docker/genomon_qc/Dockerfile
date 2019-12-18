FROM genomon/genomon_qc:0.1.0
# debian 8.9

MAINTAINER aokad <aokad@hgc.jp> 

RUN cd /tools && \
    wget -nc https://github.com/Genomon-Project/GenomonQC/archive/v2.1.1.zip && \
    unzip v2.1.1.zip && \
    rm -f v2.1.1.zip && \
    cd GenomonQC-2.1.1 && \
    python setup.py install
    
CMD ["/bin/bash"]
