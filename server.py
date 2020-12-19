import datetime
import logging
import asyncio
from re import T
from typing import Tuple
import aiocoap.resource as resource
import aiocoap
import json

# == DATABASE ==
import mysql.connector
import random
import string

mydb = mysql.connector.connect(host="localhost", user="root", password="",database="COAP")
# mydb.close()

def create_token(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
def checkEmailExist(email):
    checkemail = False
    mycursor = mydb.cursor()
    query = "SELECT email FROM Users WHERE email = '" + email + "'"
    print(query)
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    if len(myresult)  > 0:
        checkemail = True
    mycursor.close()
    return checkemail
def insertUser(email, password):
    if checkEmailExist(email):
        return False
    else:
        token = create_token(23)
        mycursor = mydb.cursor()
        sql = "INSERT INTO Users (email, pass, token) VALUES (%s, %s, %s)"
        val = (email, password, token)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        return True
# == DATABASE ==

# class SignUp(resource.Resource):

#     def __init__(self):
#         super().__init__()
#         self.set_content(b"Create Account\n")

#     def set_content(self, content):
#         self.content = content
#         while len(self.content) <= 1024:
#             self.content = self.content + b"0123456789\n"
    
#     async def render_get(self, request):
#         return aiocoap.Message(payload=self.content)

#     async def render_put(self, request):
#         print('PUT payload: %s' % request.payload)
#         self.set_content(request.payload)
#         return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)
        
class SignUp(resource.Resource):

    def __init__(self):
        super().__init__()
        self.set_content("Create Account\n")

    def set_content(self, content):
        self.content = content
    
    def set_error(self, status, message):
        localstring = "{\"status\": \"" + str(status) + "\", \"message\": \"" + str(message) + "\"}" 
        self.content = str.encode(localstring)
    
    def set_success(self, message):
        localstring = "{\"status\": \"200\", \"message\": \"" + message + "\"}"
        self.content = str.encode(localstring)

    async def render_put(self, request):
        payload = request.payload
        payload = json.loads(payload.decode('utf-8'))
        if "email" in payload and "password" in payload:
            if insertUser(payload['email'],payload['password']):
                self.set_success("[Success] Created User")
            else:
                self.set_error(500, "[Warning] User already exists")
        else:
             self.set_error(400, "[Error] Not found Key (s) in SignUp")
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)

# Logging Setup
logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['signup'], SignUp())
    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()