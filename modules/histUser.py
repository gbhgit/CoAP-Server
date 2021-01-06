import aiocoap.resource as resource
import aiocoap
import json
import modules.dbConnector as dbConnector

class HistoryUser(resource.Resource):

    def __init__(self):
        super().__init__()
        self.set_content("History User\n")

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
        if "token" in payload:
            user_id = dbConnector.checkToken(payload['token'])
            if user_id == -1:
                self.set_error(502, "[Warning] Wrong User Credentials")
            else:
                history = dbConnector.getHistory(str(user_id))
                self.set_content(str.encode(history))   
        else:
            self.set_error(400, "[Error] Not found Key (s) in HistoryUser")
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)