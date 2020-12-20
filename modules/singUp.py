import aiocoap.resource as resource
import aiocoap
import json
import modules.dbConnector as dbConnector

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
            if dbConnector.createUser(payload['email'],payload['password']):
                self.set_success("[Success] Created User")
            else:
                self.set_error(500, "[Warning] User already exists")
        else:
             self.set_error(400, "[Error] Not found Key (s) in SignUp")
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)