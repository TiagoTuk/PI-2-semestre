from pymongo import MongoClient
from datetime import datetime

id_logado = 1

# conectando ao banco de dados
connection_string = "mongodb+srv://tiago:tiago123@projetointegrador.hstyqui.mongodb.net/"
client = MongoClient(connection_string, 27017)
db_connection = client["PI2_Construcao"]

# conectando a coleção
collection = db_connection.get_collection("clientes")
collection2 = db_connection.get_collection("carrinho")
collection3 = db_connection.get_collection("produto")
collection4 = db_connection.get_collection("pedido")

qt_doc = collection4.count_documents({})

# verificando se consta carrinho ativo
active_cart = collection2.find_one({"idCliente": id_logado, "status": "ativo"})

if active_cart:
    for item in active_cart["itensCarrinho"]:
        # Buscando item do carrinho na classe produto
        product = collection3.find_one({"codProduto": item["codProd"]})

        if product:
            # Verificar qt disponivel
            if item["quantidade"] > product["qtDisponivel"]:
                print(f'Quantidade indisponivel para o produto {item["nomeProd"]}')
            else:
                # Atualizando qt na coleção produto
                collection3.update_one({"codProduto": item["codProd"]},
                                       {"$inc": {"qtDisponivel": -item["quantidade"]}})

    f_pgto = int(input('Forma de pagamento? [1 - PIX  | 2 - Cartão de Crédito]: '))

    novo_pedido = {
        "idCliente": id_logado,
        "idPedido": qt_doc+1,
        "dataCriacao": datetime.now(),
        "numeroCarrinho": active_cart["numeroCarrinho"],
        "itensPedido": active_cart["itensCarrinho"],
        "frete": 15.0,
        "formaPagamento": f_pgto,
        "valorTotal": 0.0,
        "status": "ativo"
    }

    # Calculando o valor total do pedido
    for item in novo_pedido["itensPedido"]:
        novo_pedido["valorTotal"] += item["precoTotal"]

    # Incluindo o valor do frete
    novo_pedido["valorTotal"] += novo_pedido["frete"]

    # Novo pedido na coleção pedidos
    result = collection4.insert_one(novo_pedido)

    if result.inserted_id:
        print(f"Novo pedido criado com sucesso. ID: {result.inserted_id}")

        collection2.update_one({"idCliente": id_logado, "status": "ativo"},
                               {"$set": {"status": "concluido"}})

        print("Status do carrinho atualizado para 'concluído'.")
    else:
        print('Erro ao criar o novo pedido!')
        