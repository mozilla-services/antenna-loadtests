#!/bin/bash

# Sends a fake crash report to the host specified in $HOST 
# defaulting to http://localhost:8000 .
HOST=$1
if [ -z "${HOST}" ]; then
    HOST="http://localhost:8000"
fi

URL="https://${HOST}/submit"

curl -L -XPOST  \
     -F 'Content-Type=multipart/form-data' \
     -F 'ProductName=Firefox' \
     -F 'Version=1' \
     -v -H 'Host: antenna.stage.mozaws.net' \
     -F upload_file_minidump2=@small.dmp \
     "$URL"

