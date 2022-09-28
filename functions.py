class Usuario:
    def __init__(self, nome, telefone, endereco):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco

def formtCPF(cpf: str):
  for n in cpf:
    if n in [' ', '.', '-']:
      cpf = cpf.replace(n, '')
  return cpf



def buildResponse(responseText = None, contexts: list = None):
  
  resposta = {}

  if responseText and contexts:
    resposta["fulfillmentMessages"] = [
              {
                "text": {
                  "text": [
                    responseText
                  ]
                }
              }
            ]
    resposta["outputContexts"] = contexts
    

  elif responseText:
    resposta["fulfillmentMessages"] = [
              {
                "text": {
                  "text": [
                    responseText
                  ]
                }
              }
            ]

  # contexts é uma lista de dicionários
  elif contexts:
    resposta["outputContexts"] = contexts


  return resposta