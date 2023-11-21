from pymongo import MongoClient
from datetime import datetime, timedelta

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

qt_doc = collection2.count_documents({})

prdSelect = int(input('Produto: '))
qtSelect = int(input('Quantidade: '))

# Verificando quantidade disponivel do produto
data = collection3.find_one({"codProduto": prdSelect})

resultado = {}
for key, value in data.items():
    resultado[key] = value

print(resultado)

# verificando se consta carrinho ativo e adicionando itens ou criando novo carrinho.
active_cart = collection2.find_one({"idCliente": id_logado, "status": "ativo"})


if active_cart:
    novo_item = {
        'codProd': resultado['codProduto'],
        'nomeProd': resultado['nomeProd'],
        'precoProdUnit': resultado['precoProd'],
        'quantidade': qtSelect,
        'precoTotal': resultado['precoProd'] * qtSelect
    }

    collection2.update_one({"idCliente": id_logado, "status": "ativo"},
                           {"$push": {"itensCarrinho": novo_item}})
else:
    collection2.insert_one({
        'dataCriacao': datetime.now(),
        'idCliente': id_logado,
        'numeroCarrinho': qt_doc + 1,
        'itensCarrinho': [{
            'codProd': resultado['codProduto'],
            'nomeProd': resultado['nomeProd'],
            'precoProdUnit': resultado['precoProd'],
            'quantidade': qtSelect,
            'precoTotal': resultado['precoProd'] * qtSelect
        }],
        'status': 'ativo'})

