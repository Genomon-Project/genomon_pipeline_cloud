FROM python:3.8.3-slim-buster AS builder
WORKDIR /root
RUN apt-get update && \
  apt-get install -y --no-install-recommends git=1:2.* && \
  pip install awscli==1.18.91 boto3==1.14.14 pyyaml==5.3.1 && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  git clone --depth=1 -b v0.0.18 https://github.com/aokad/ecsub.git && \
  rm -rf /root/ecsub/.git

FROM python:3.8.3-slim-buster AS genomon_pipeline_cloud
LABEL maintainer="aokad <aokad@hgc.jp>"
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /root/ecsub /root/ecsub
WORKDIR /root/ecsub
RUN python setup.py build install
WORKDIR /root/genomon_pipeline_cloud
COPY . /root/genomon_pipeline_cloud
RUN python setup.py build install
WORKDIR /root
RUN rm -rf /root/ecsub /root/genomon_pipeline_cloud
ENTRYPOINT ["genomon_pipeline_cloud", "--engine", "ecsub"]
