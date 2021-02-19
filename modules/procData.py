import aiocoap.resource as resource
import aiocoap
import json
import random
import modules.dbConnector as dbConnector

# www.saudeemmovimento.com.br/saude/tabelas/tabela_de_referencia_composicao.htm

data_idade = {
    "0": {"min": 0,  "max": 25},
    "1": {"min": 26, "max": 35},
    "2": {"min": 36, "max": 45},
    "3": {"min": 46, "max": 55},
    "4": {"min": 56, "max": 100}
}

data_tipo = {
    "0": {
        "Excelente": {
            "min": 13, "max": 16
        },
        "Bom": {
            "min": 17, "max": 19
        },
        "Acima do Normal": {
            "min": 20, "max": 22
        },
        "Normal": {
            "min": 23, "max": 25
        },
        "Abaixo do Normal": {
            "min": 26, "max": 28
        },
        "Ruim": {
            "min": 29, "max": 31
        },
        "Muito Ruim": {
            "min": 33, "max": 43
        }
    },

    "1": {
        "Excelente": {
            "min": 14, "max": 16
        },
        "Bom": {
            "min": 18, "max": 20
        },
        "Acima do Normal": {
            "min": 21, "max": 23
        },
        "Normal": {
            "min": 24, "max": 25
        },
        "Abaixo do Normal": {
            "min": 27, "max": 29
        },
        "Ruim": {
            "min": 31, "max": 33
        },
        "Muito Ruim": {
            "min": 36, "max": 49
        }
    },

    "2": {
        "Excelente": {
            "min": 16, "max": 19
        },
        "Bom": {
            "min": 20, "max": 23
        },
        "Acima do Normal": {
            "min": 24, "max": 26
        },
        "Normal": {
            "min": 27, "max": 29
        },
        "Abaixo do Normal": {
            "min": 30, "max": 32
        },
        "Ruim": {
            "min": 33, "max": 36
        },
        "Muito Ruim": {
            "min": 38, "max": 48
        }
    },

    "3": {
        "Excelente": {
            "min": 17, "max": 21
        },
        "Bom": {
            "min": 23, "max": 25
        },
        "Acima do Normal": {
            "min": 24, "max": 26
        },
        "Normal": {
            "min": 29, "max": 31
        },
        "Abaixo do Normal": {
            "min": 32, "max": 34
        },
        "Ruim": {
            "min": 35, "max": 38
        },
        "Muito Ruim": {
            "min": 39, "max": 50
        }
    },
    "4": {
        "Excelente": {
            "min": 18, "max": 22
        },
        "Bom": {
            "min": 24, "max": 26
        },
        "Acima do Normal": {
            "min": 27, "max": 29
        },
        "Normal": {
            "min": 30, "max": 32
        },
        "Abaixo do Normal": {
            "min": 33, "max": 35
        },
        "Ruim": {
            "min": 36, "max": 38
        },
        "Muito Ruim": {
            "min": 39, "max": 49
        }
    }
}

data_tipo_home = {
    "0": {
        "Excelente": {
            "min": 4, "max": 6
        },
        "Bom": {
            "min": 8, "max": 10
        },
        "Acima do Normal": {
            "min": 12, "max": 13
        },
        "Normal": {
            "min": 14, "max": 16
        },
        "Abaixo do Normal": {
            "min": 17, "max": 20
        },
        "Ruim": {
            "min": 20, "max": 24
        },
        "Muito Ruim": {
            "min": 26, "max": 36
        }
    },

    "1": {
        "Excelente": {
            "min": 8, "max": 11
        },
        "Bom": {
            "min": 12, "max": 15
        },
        "Acima do Normal": {
            "min": 16, "max": 18
        },
        "Normal": {
            "min": 18, "max": 20
        },
        "Abaixo do Normal": {
            "min": 22, "max": 24
        },
        "Ruim": {
            "min": 24, "max": 25
        },
        "Muito Ruim": {
            "min": 28, "max": 36
        }
    },

    "2": {
        "Excelente": {
            "min": 10, "max": 14
        },
        "Bom": {
            "min": 16, "max": 18
        },
        "Acima do Normal": {
            "min": 19, "max": 21
        },
        "Normal": {
            "min": 21, "max": 23
        },
        "Abaixo do Normal": {
            "min": 24, "max": 25
        },
        "Ruim": {
            "min": 27, "max": 29
        },
        "Muito Ruim": {
            "min": 30, "max": 39
        }
    },

    "3": {
        "Excelente": {
            "min": 12, "max": 16
        },
        "Bom": {
            "min": 18, "max": 20
        },
        "Acima do Normal": {
            "min": 21, "max": 23
        },
        "Normal": {
            "min": 24, "max": 25
        },
        "Abaixo do Normal": {
            "min": 26, "max": 27
        },
        "Ruim": {
            "min": 28, "max": 30
        },
        "Muito Ruim": {
            "min": 32, "max": 38
        }
    },
    "4": {
        "Excelente": {
            "min": 13, "max": 18
        },
        "Bom": {
            "min": 20, "max": 21
        },
        "Acima do Normal": {
            "min": 22, "max": 23
        },
        "Normal": {
            "min": 24, "max": 25
        },
        "Abaixo do Normal": {
            "min": 26, "max": 27
        },
        "Ruim": {
            "min": 28, "max": 30
        },
        "Muito Ruim": {
            "min": 32, "max": 38
        }
    }
}

 

def processInputData(inputData):
    sexo, idade, altura, peso, imagem = inputData.split(";")
    sexo = int(sexo.split("=")[1])
    idade = int(idade.split("=")[1])
    altura = float(altura.split("=")[1])/100
    peso = float(peso.split("=")[1])
    b64_string = str(imagem.split("=")[1])
    value = random.uniform(20.5, 38.5)
    # calcular IMC
    IMC = peso/(altura*altura)
    IMC = round(IMC,2)
    IMC_classe = ""

    if IMC < 18.5:
        IMC_classe = "Magreza"
    if IMC >= 18.5 and IMC < 24.9:
        IMC_classe = "Normal"
    if IMC >= 24.9 and IMC < 30:
        IMC_classe = "Sobrepeso"
    if IMC >= 30:
        IMC_classe = "Obesidade"
    
    if sexo == 1: # homem
        class_idade = 0
        for index in range(len(data_idade)):
            if idade >= data_idade[str(index)]['min'] and idade <= data_idade[str(index)]['max']:
                class_idade = str(index)
        
        class_typo = 0
        for typ in data_tipo_home[class_idade]:
            print(typ, data_tipo_home[class_idade][typ], value)
            if value >= data_tipo_home[class_idade][typ]['min'] and value <= data_tipo_home[class_idade][typ]['max']:
                class_typo = typ
        
        if class_typo == 0:
            min_dist = 1000
            for typ in data_tipo_home[class_idade]:
                mean = (data_tipo_home[class_idade][typ]['min'] + data_tipo_home[class_idade][typ]['max'])/2
                dist = abs(mean - value)
                if dist <= min_dist:
                    class_typo = typ

        message = "Resultado " + class_typo 
        message = message + ", considerando sexo masculino e idade entre " + str(data_idade[class_idade]['min']) + "-" + str(data_idade[class_idade]['max']) + "."
        message = message + " Enquanto o IMC deu " + str(IMC) + " que se classifica como " + IMC_classe
        localstring = "{\"value\": \"" + str(value) + "\", \"message\": \"" + message + "\"}"
        return localstring, value
    else:
        class_idade = 0
        for index in range(len(data_idade)):
            if idade >= data_idade[str(index)]['min'] and idade <= data_idade[str(index)]['max']:
                class_idade = str(index)
        
        class_typo = 0
        for typ in data_tipo[class_idade]:
            print(typ, data_tipo[class_idade][typ], value)
            if value >= data_tipo[class_idade][typ]['min'] and value <= data_tipo[class_idade][typ]['max']:
                class_typo = typ
        
        if class_typo == 0:
            min_dist = 1000
            for typ in data_tipo[class_idade]:
                mean = (data_tipo[class_idade][typ]['min'] + data_tipo[class_idade][typ]['max'])/2
                dist = abs(mean - value)
                if dist <= min_dist:
                    class_typo = typ

        message = "Resultado " + class_typo 
        message = message + ", considerando sexo feminino e idade entre " + str(data_idade[class_idade]['min']) + "-" + str(data_idade[class_idade]['max']) + "."
        message = message + " Enquanto o IMC deu " + str(IMC) + " que se classifica como " + IMC_classe
        localstring = "{\"value\": \"" + str(value) + "\", \"message\": \"" + message + "\"}"
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