#!/bin/bash
BASEDIR=$(dirname "$0")

cp $BASEDIR/data/rds_config.py $BASEDIR/text_query
(cd $BASEDIR/text_query && zip -r /tmp/app.zip .)
aws lambda update-function-code --function-name text_query --zip-file fileb:///tmp/app.zip
rm /tmp/app.zip
