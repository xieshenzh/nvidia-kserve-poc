- Pre-reqs
    - Have persistent volume claim
    - Create a secret named ```registry-secret``` ngc registry
    - Create a secret named ```mpaulgreen-mpaulrobo-pull-secret``` to access images from private image registry
    - This is a POC and hence some values are hardcoded
# Create the PVC
```
oc apply -f pvc.yaml
```
# Build the ngc pull image
```
sudo podman build -t quay.io/mpaulgreen/ngc-pull:0.6 -f ./ngcpull_Dockerfile
sudo podman push quay.io/mpaulgreen/ngc-pull:0.6
```

# Build the image to run the job
```
sudo podman build -t quay.io/mpaulgreen/ngc-job:0.6 -f ./createjob_Dockerfile
sudo podman push quay.io/mpaulgreen/ngc-job:0.6
```

# Create role, role bindings and sa for creating an deleting the job
```
oc apply -f jobrobot_rolebinding.yaml
oc apply -f jobrobot_role.yaml
oc apply -f jobrobot_sa.yaml
```


# Create a pod to start the job 
- This was done in this way to plug this in an initContainer if available
```
oc apply -f pod.yaml
```