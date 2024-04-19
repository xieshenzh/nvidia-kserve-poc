# POC for NIM on OpenshiftAI
- The base NIM image is ```nvcr.io/ohlfw0olaadg/ea-participants/nemollm-inference-ms:24.01``
- The model deployed is ```llama-2-7b-chat:LLAMA-2-7B-CHAT-4K-FP16-1-A100.24.01```
- The image used for ```InferenceService``` CR - ```quay.io/mpaulgreen/nim-kserve-poc:24.01```
## TODO
- Scalibility script 
- Kserve minReplicas = 0 and with adjusted KServe target


