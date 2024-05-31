FROM registry.access.redhat.com/ubi9/python-311:1-52.1712567218 as model

USER 0

ENV STORE_MOUNT_PATH=/mnt/models
ENV NGC_CLI_ORG=''
ENV NGC_CLI_TEAM=ea-participants
ENV NGC_CLI_VERSION=3.41.3
ENV NGC_MODEL_NAME=llama-2-7b-chat
ENV NGC_MODEL_VERSION=LLAMA-2-7B-CHAT-4K-FP16-1-A100.24.01

COPY ngc-pull.sh /scripts/ngc-pull.sh

RUN yum install unzip wget -y && \
    chmod +x /scripts/ngc-pull.sh

RUN /scripts/ngc-pull.sh


FROM nvcr.io/nvaie/nemollm-inference-ms:24.01

COPY --from=model $STORE_MOUNT_PATH /model-store/

