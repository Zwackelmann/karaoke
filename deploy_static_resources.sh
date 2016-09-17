#!/bin/bash
BASEDIR=$(dirname "$0")

(cd $BASEDIR/static_resources && zip -r /tmp/app.zip .)
aws lambda update-function-code --function-name static_resources --zip-file fileb:///tmp/app.zip
rm /tmp/app.zip
