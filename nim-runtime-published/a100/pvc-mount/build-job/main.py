#!/usr/bin/env python3
from kubernetes import client, config, watch
import os

JOB_NAME = 'ngcpull-job'


def create_job_object():
    # Create environment variables
    (environment_ngc_cli_org, environment_ngc_cli_team,
     environment_ngc_cli_version, environment_ngc_model_name,
     environment_ngc_model_version, environment_var_store_mount_path) = (
        create_environment_vars()
    )

    # Create volume definition
    volume_defs = [client.V1Volume(
        name="my-pvc",
        persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
            claim_name=os.environ.get("NGC_PVC")
        )
    )]

    # Create toleration
    toleration1, toleration2 = getTolerations()

    # Configure Pod template container

    container = client.V1Container(
        name='main',
        image='quay.io/mpaulgreen/ngc-pull:0.6', # TODO: make it come from ENV variable
        command=["/bin/sh", "-c"],
        args=["/scripts/ngc-pull.sh;"],
        image_pull_policy="Always",
        env=[
            environment_var_store_mount_path,
            environment_ngc_cli_org,
            environment_ngc_cli_team,
            environment_ngc_cli_version,
            environment_ngc_model_name,
            environment_ngc_model_version
        ],
        volume_mounts=[client.V1VolumeMount(
            name="my-pvc",
            mount_path="/mnt/models"
        )],
    )
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={'name': JOB_NAME}),
        spec=client.V1PodSpec(
            restart_policy='OnFailure',
            containers=[container],
            volumes=volume_defs,
            tolerations=[toleration1, toleration2],
            # This is not required for storage initializer
            image_pull_secrets=[{"name": "mpaulgreen-mpaulrobo-pull-secret"}], # TODO: make it come from ENV variable
            node_selector=dict(
                {"node.kubernetes.io/instance-type": "p4d.24xlarge"}) # TODO: make it come from ENV variable
            # this is not required for storage initializer
        )
    )
    # Create the specification of deployment
    spec = client.V1JobSpec(template=template)
    # Instantiate the job object
    job = client.V1Job(
        api_version='batch/v1',
        kind='Job',
        metadata=client.V1ObjectMeta(name=JOB_NAME),
        spec=spec)

    return job


def getTolerations(): # TODO : This should be dynamically obtained
    toleration1 = client.V1Toleration(
        key="nvidia.com/gpu",
        operator="Exists",
        effect="NoSchedule"
    )
    toleration2 = client.V1Toleration(
        key="odh-notebook",
        operator="Exists",
        effect="NoSchedule"
    )
    return toleration1, toleration2


def create_job(api_instance, job):
    api_response = api_instance.create_namespaced_job(
        body=job,
        namespace=get_current_namespace()
    )

    print("Job created. status='%s'" % str(api_response.status))


def create_environment_vars():
    # Create env variables
    environment_var_store_mount_path = client.V1EnvVar(
        name="STORE_MOUNT_PATH", value=os.environ.get("STORE_MOUNT_PATH")
    )
    environment_ngc_cli_org = client.V1EnvVar(
        name="NGC_CLI_ORG", value=os.environ.get("NGC_CLI_ORG")
    )
    environment_ngc_cli_team = client.V1EnvVar(
        name="NGC_CLI_TEAM", value=os.environ.get("NGC_CLI_TEAM")
    )
    environment_ngc_cli_version = client.V1EnvVar(
        name="NGC_CLI_VERSION", value=os.environ.get("NGC_CLI_VERSION")
    )
    environment_ngc_model_name = client.V1EnvVar(
        name="NGC_MODEL_NAME", value=os.environ.get("NGC_MODEL_NAME")
    )
    environment_ngc_model_version = client.V1EnvVar(
        name="NGC_MODEL_VERSION", value=os.environ.get("NGC_MODEL_VERSION")
    )
    return (environment_ngc_cli_org, environment_ngc_cli_team,
            environment_ngc_cli_version, environment_ngc_model_name,
            environment_ngc_model_version, environment_var_store_mount_path)


def get_current_namespace():
    ns_path = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"
    if os.path.exists(ns_path):
        with open(ns_path) as f:
            return f.read().strip()
    try:
        _, active_context = config.list_kube_config_contexts()
        return active_context["context"]["namespace"]
    except KeyError:
        return "default"


def main():
    config.load_incluster_config()
    batch_v1 = client.BatchV1Api()
    job = create_job_object()
    create_job(batch_v1, job)


if __name__ == '__main__':
    main()
