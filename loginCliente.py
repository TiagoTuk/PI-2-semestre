from pymongo import MongoClient


# conectando ao banco de dados
connection_string = "mongodb+srv://tiago:tiago123@projetointegrador.hstyqui.mongodb.net/"
client = MongoClient(connection_string, 27017)
db_connection = client["PI2_Construcao"]

# conectando a coleção
collection = db_connection.get_collection("clientes")

login_usuario = input('Digite o seu login: ')
senha_usuario = input('Digite a sua senha: ')

data = collection.find({"loginCliente": login_usuario, "senhaCliente": senha_usuario})

resultado = []
for e in data:
    resultado.append(e)

if len(resultado) > 0:
    print('Credencial válida. Acesso permitido')
else:
    print('Credencial inválida. Acesso negado')

