import aiocoap.resource as resource
import aiocoap
import json
import modules.dbConnector as dbConnector

class SignIn(resource.Resource):

    def __init__(self):
        super().__init__()
        self.set_content("Login Account\n")

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
            isLogin, token = dbConnector.loginUser(payload['email'], payload['password'])
            if isLogin:
                localstring = "{\"status\": \"200\", \"token\": \"" + token + "\"}"
                self.set_content(str.encode(localstring))
            else:   
                self.set_error(501, "[Warning] Wrong User Credentials")
        else:
            self.set_error(400, "[Error] Not found Key (s) in SignUp")
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)