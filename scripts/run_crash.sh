#!/bin/bash

# Sends a fake crash report to the host specified in $HOST 
# defaulting to http://localhost:8000 .
HOST=$1
if [ -z "${HOST}" ]; then
    HOST="http://localhost:8000"
fi

URL="${HOST}/submit"

curl -L -v -H 'Host: crash-reports' \
     -F 'ProductName=Firefox' \
     -F 'uuid=a448814e-16dd-45fb-b7dd-b0b522161010' \
     -F 'Version=1' \
     -F upload_file_minidump2=@small.dmp \
     "$URL"

