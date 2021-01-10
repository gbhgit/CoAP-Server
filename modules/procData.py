import aiocoap.resource as resource
import aiocoap
import json
import random
import modules.dbConnector as dbConnector

def processInputData(inputData):
    print(inputData)
    value = random.uniform(20.5, 38.5)
    localstring = "{\"value\": \"" + str(value) + "\"}"
    return localstring, value

class ProcessData(resource.Resource):

    def __init__(self):
        super().__init__()
        self.set_content("Process Data\n")

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
        if "token" in payload and "inputData" in payload and "dataStatus" in payload:
            user_id = dbConnector.checkToken(payload['token'])
            if user_id == -1:
                self.set_error(502, "[Warning] Wrong User Credentials")
            else:
                if payload['dataStatus'] == 'create':
                    dataId = dbConnector.insertImage(user_id, payload['inputData'])
                    localstring = "{\"dataId\": \"" + str(dataId) + "\"}"
                    self.set_content(str.encode(localstring))
                elif payload['dataStatus'] == 'update':
                    dbConnector.updateImage(user_id, payload['dataId'],  payload['inputData'])
                    localstring = "{\"dataId\": \"" + str(payload['dataId'],) + "\"}"
                    self.set_content(str.encode(localstring))
                elif payload['dataStatus'] == 'end':
                    dbConnector.updateImage(user_id, payload['dataId'],  payload['inputData'])
                    inputData = dbConnector.getImage(user_id, payload['dataId'])
                    procResult, data_value = processInputData(inputData)
                    dbConnector.insertInHistory(user_id, data_value)
                    self.set_content(str.encode(procResult)) 
        else:
            self.set_error(400, "[Error] Not found Key (s) in HistoryUser")
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)