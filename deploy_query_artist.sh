#!/bin/bash
BASEDIR=$(dirname "$0")

cp $BASEDIR/data/rds_config.py $BASEDIR/query_artist
(cd $BASEDIR/query_artist && zip -r /tmp/app.zip .)
aws lambda update-function-code --function-name query_artist --zip-file fileb:///tmp/app.zip
rm /tmp/app.zip
