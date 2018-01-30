FROM python:2.7.14
MAINTAINER aokad <aokad@hgc.jp>

RUN apt-get -y update && \
    apt-get -y install apt-transport-https ca-certificates curl gnupg2 software-properties-common && \
    apt-get -y install vim && \
    \
    curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | apt-key add - && \
    apt-key fingerprint 0EBFCD88 && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") $(lsb_release -cs) stable" && \
    apt-get -y update && \
    apt-get -y install docker-ce && \
    apt-get -y install docker-ce=17.12.0~ce-0~debian && \
    \
    curl -L https://github.com/docker/machine/releases/download/v0.13.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine && chmod +x /tmp/docker-machine && cp /tmp/docker-machine /usr/local/bin/docker-machine && \
    \
    mkdir /tools && \
    cd /tools && \
    wget https://github.com/otiai10/awsub/releases/download/v0.0.3/awsub.linux_amd64.tar.gz && \
    tar -zxvf awsub.linux_amd64.tar.gz; rm awsub.linux_amd64.tar.gz && \
    mv awsub /usr/local/bin/ && \
    git clone https://github.com/otiai10/awsub.git && \
    \
    cd /tools && \
    git clone https://github.com/Genomon-Project/genomon_pipeline_cloud.git && \
    cd genomon_pipeline_cloud && \
    pip install . --upgrade

CMD ["bin/bash"]

# for example
# docker build -t gcloud .
# docker run -it --name gcloud-a -e AWS_ACCESS_KEY_ID={your ID} -e AWS_SECRET_ACCESS_KEY={your KEY} gcloud
