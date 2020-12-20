#!/bin/bash
virtualenv .env -p python3
. .env/bin/activate && pip install aiocoap
. .env/bin/activate && pip install mysql-connector-python