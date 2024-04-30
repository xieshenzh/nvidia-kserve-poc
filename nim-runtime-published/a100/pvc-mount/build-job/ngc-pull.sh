echo "Starting NGC download script....."
DIRECTORY="${STORE_MOUNT_PATH}/${NGC_MODEL_NAME}_v${NGC_MODEL_VERSION}"

if [ -d "$DIRECTORY" ]; then
    echo "Model is already downloaded...."
else
  wget "https://api.ngc.nvidia.com/v2/resources/nvidia/ngc-apps/ngc_cli/versions/${NGC_CLI_VERSION}/files/ngccli_linux.zip" -O ngccli_linux.zip && unzip ngccli_linux.zip
  chmod u+x ngc-cli/ngc

  NGC_EXE=$(pwd)/ngc-cli/ngc

  if [ "$NGC_EXE" = "ngc" ]; then
    NGC_EXE=$(which ngc)
  fi
  echo "downloading model......"
  $NGC_EXE registry model download-version --dest "$STORE_MOUNT_PATH" "${NGC_CLI_ORG}/${NGC_CLI_TEAM}/${NGC_MODEL_NAME}:${NGC_MODEL_VERSION}"
  echo "$STORE_MOUNT_PATH/${NGC_MODEL_VERSION}"
  tar -xvf "$DIRECTORY/${NGC_MODEL_VERSION}.tar.gz" -C ${DIRECTORY}
fi
echo "Model is mounted on $STORE_MOUNT_PATH"