#!/bin/bash
BASEDIR=$(dirname "$0")

(cd $BASEDIR/query_song && zip -r /tmp/app.zip .)
aws lambda update-function-code --function-name query_song --zip-file fileb:///tmp/app.zip
rm /tmp/app.zip
