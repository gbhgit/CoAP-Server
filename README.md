# CoAP-Server
CoAP-Server using python

Requisitos:
      
  * Ubuntu 16.04 ou 20.04:
  
  * Python 3

Para realizar a criação da base de dados rode os seguintes comandos:

```mysql
CREATE DATABASE COAP;
CREATE TABLE COAP.Users (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(50),
    pass VARCHAR(8) NOT NULL,
    token VARCHAR(24)
);
```

Para Instalar é necessário que os requisitos acima tenham sido contemplados:

  * Baixar o presente projeto.
  
  * Entrar na pasta raiz rodar o comando: `./install_env.sh`
  
Para Rodar Servidor:

  * Abrir terminal.
  
  * Ativar a env: `. .env/bin/activate`
  
  * Rodar code: `python server.py`