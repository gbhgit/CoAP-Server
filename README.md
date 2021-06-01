# CoAP-Server
CoAP-Server using python
Constrained Application Protocol (CoAP), to connect users to db.

### Requirements
      
  * Ubuntu 16.04 or 20.04:
  * Python 3
  * Install [Mysql](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04-pt)

### Installation
- 1: Using the terminal enter in repository folder and type the command:

		`./install_env.sh`
- 2: To create db just run the following commands:
```mysql
CREATE DATABASE COAP;
CREATE TABLE COAP.Users (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(50),
    pass VARCHAR(8) NOT NULL,
    token VARCHAR(24)
);
CREATE TABLE COAP.Hist (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT(6) UNSIGNED,
    data_value FLOAT,
    date_value DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE COAP.Images (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT(6) UNSIGNED,
    data_block LONGTEXT
);
```

### Usage
  
  * Activate env: `. .env/bin/activate`
  
  * Run code: `python server.py`
