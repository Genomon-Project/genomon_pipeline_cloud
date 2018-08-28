FROM genomon/genomon_qc:0.1.0
# debian 8.9

MAINTAINER aokad <aokad@hgc.jp> 

RUN cd /tools && \
    wget -nc https://github.com/Genomon-Project/GenomonQC/archive/v2.0.3.zip && \
    unzip v2.0.3.zip && \
    rm -f v2.0.3.zip && \
    cd GenomonQC-2.0.3 && \
    python setup.py install
    
CMD ["/bin/bash"]
