#!/bin/bash
virtualenv .env -p python3
. .env/bin/activate && pip install aiocoap
. .env/bin/activate && pip install mysql-connector-python

# CREATE DATABASE COAP;
# CREATE TABLE COAP.Users (
# id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
# email VARCHAR(50),
# pass VARCHAR(8) NOT NULL,
# token VARCHAR(24)
# );