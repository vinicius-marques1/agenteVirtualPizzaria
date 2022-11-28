from flask import Flask, request, jsonify
from functions import Usuario, buildResponse

app = Flask(__name__)

pedidos = []

usuario1 = Usuario('Lucas', '11987654243', 'rua sebastião cardoso')
usuarios = {usuario1.telefone: usuario1}


# rota para lidar com as chamadas da API do Dialogflow
@app.route('/webhook', methods=['POST',])
def main():

    dados = request.get_json()
    #print(dados)

    responseText = ""
    intent = dados["queryResult"]["intent"]["displayName"]


    # Intent ""
    if intent == "pizza.pedido":
      telefone = dados['queryResult']['parameters']['telefone']
      
      if telefone in usuarios:
        usuario = usuarios[telefone]
        
        responseText = f'''Seja bem vindo {usuario.nome}. Qual é o seu pedido?'''
        
        contexts = [
          {
            "name": 
            'projects/project-test-agentvirtual/agent/sessions//contexts/contexto-pedido',
            "lifespanCount": 10, 
            "parameters": {
                          'telefone': telefone
                          }
          }
        ]
        
        res = buildResponse(responseText=responseText, contexts=contexts)

      
      else:
        responseText = 'Você ainda não é nosso cliente! gostaria de fazer um cadastro?'
        contexts = [
          {
            "name": 'projects/project-test-agentvirtual/agent/sessions//contexts/inscricao',
            "lifespanCount": 5, 
            "parameters": {
                          'telefone': telefone
                          }
          }
        ]
        
        res = buildResponse(responseText=responseText, contexts=contexts)


    if intent == "cadastro":
      parametros_ = dados['queryResult']['parameters']
      nome = parametros_['nome']
      telefone = parametros_['telefone']
      cidade = parametros_['cidade']

      usuario2 = Usuario(nome, telefone, cidade)
      usuarios[usuario2.telefone] = usuario2

      print(usuarios)

      responseText = f'Tudo certo {usuario2.nome}, você foi cadastrado no nosso sistema'
      res = buildResponse(responseText=responseText)

        
    # intent ""
    if intent == 'pizza.pedido-follow-up':
      contexts_list = dados['queryResult']['outputContexts']

      for context in contexts_list:
        if 'contexto-pedido' in context['name']:
          parametros = context['parameters']
          telefone = parametros['telefone']
          sabor = parametros['sabor']

          usuario = usuarios[telefone]
          nome = usuario.nome
          pedidos.append({ 'nome': nome, 'sabor': sabor })
          print(pedidos)

    
      responseText = f'Tudo certo {usuario.nome}, o seu pedido sera entregue em 30 minutos'
      res = buildResponse(responseText=responseText)


    # Retornando a resposta
    return jsonify(res)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)