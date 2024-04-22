#!/bin/bash
echo "url : ${1}"
for i in {1..50}
do
curl --insecure \
-k "${1}" \
-d "@mistral.json" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC" &
done
