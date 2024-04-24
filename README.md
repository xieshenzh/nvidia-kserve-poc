# POC for NIM on OpenshiftAI
- The base NIM image is ```nvcr.io/ohlfw0olaadg/ea-participants/nemollm-inference-ms:24.01``
- The model deployed is ```llama-2-7b-chat:LLAMA-2-7B-CHAT-4K-FP16-1-A100.24.01```
- Deployed the above using Openshift AI UI and CLI
- Tested scalability( All pods did not come up due to resource constraints on cluster)


## Open Issues

### Issue 1 - Image update from NVIDIA to include --models-store as startup arg
- A patch as been implemented at this time (https://github.com/mpaulgreen/nvidia-kserve-poc/blob/main/nim-runtime-published/a100/openshift-ai-ui/nimruntime.yaml#L40)
- NVIDA plans to have this param added in future versions of NIM.

### Issue 2 - Nemo container generated more than 4000 threads, wheread limit of threads in Openshift containers is set to 4096
- The limit of threads in the Openshift containers is set to 4096. However, the NeMo container generates more than 4,000 threads before crashing. To mitigate this, we modified the configuration file for the Triton Inference Server by reducing the process count from 128 to 1. Each process can have multiple threads. This worked because it kept the thread count around 300 and prevented exceeding the thread limit of 4096. Nvidia team is going to look on their side how to resolve this issue
- The issue is expectd to resolve with 24.04 version of models


### Issue 3 - Disk pressure & OOMKilled
- Currently models are mounted on ephermal volumes of kserve-container  and as you create more replicas it results in disk pressure on the nodes. The storage-initializer pod is being terminated(OOMKilled) due to insufficient capacity assigned by node to ephermal storage

### Issue 4 - Pods take too long to start up
- NIM pods takes too long to start up. This is an issue if we have to address scalability. 