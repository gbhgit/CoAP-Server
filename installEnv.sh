#!/bin/bash
virtualenv .env -p python2
. .env/bin/activate && pip install CoAPthon