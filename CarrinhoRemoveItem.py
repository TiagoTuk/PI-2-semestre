from pymongo import MongoClient

id_logado = 2

# conectando ao banco de dados
connection_string = "mongodb+srv://tiago:tiago123@projetointegrador.hstyqui.mongodb.net/"
client = MongoClient(connection_string, 27017)
db_connection = client["PI2_Construcao"]

# conectando a coleção
collection = db_connection.get_collection("clientes")
collection2 = db_connection.get_collection("carrinho")
collection3 = db_connection.get_collection("produto")
collection4 = db_connection.get_collection("pedido")


# verificando se consta carrinho ativo
active_cart = collection2.find_one({"idCliente": id_logado, "status": "ativo"})

# excluindo carrinho
if active_cart:
    collection2.delete_one({"idCliente": id_logado, "status": "ativo"})
    print('Carrinho excluído com sucesso.')
else:
    print('Cliente não possui carrinho ativo.')
