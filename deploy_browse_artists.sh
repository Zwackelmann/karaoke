#!/bin/bash
BASEDIR=$(dirname "$0")

(cd $BASEDIR/browse_artists && zip -r /tmp/app.zip .)
aws lambda update-function-code --function-name browse_artists --zip-file fileb:///tmp/app.zip
rm /tmp/app.zip
