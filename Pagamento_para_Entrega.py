from pymongo import MongoClient
from datetime import datetime, timedelta

id_logado = 21

# conectando ao banco de dados
connection_string = "mongodb+srv://tiago:tiago123@projetointegrador.hstyqui.mongodb.net/"
client = MongoClient(connection_string, 27017)
db_connection = client["PI2_Construcao"]

# conectando a coleção
collection = db_connection.get_collection("clientes")
collection2 = db_connection.get_collection("carrinho")
collection3 = db_connection.get_collection("produto")
collection4 = db_connection.get_collection("pedido")
collection5 = db_connection.get_collection("pagamento")
collection6 = db_connection.get_collection("entrega")

qt_doc = collection6.count_documents({})

# verificando se consta pagamento em processamento
client = collection.find_one({"idCliente": id_logado})
pay_processing = collection5.find_one({"idCliente": id_logado, "status": "Em processamento"})
active_pedido = collection4.find_one({"idCliente": id_logado, "status": "ativo"})

print("client_document:", client)
print("pay_processing:", pay_processing)

if client and pay_processing:
    pgto_confir = int(input('Pagamento Aprovado? [1 - Aprovado | 2 - Recusado]: '))

    if pgto_confir == 1:
        nova_entrega = {
            "IdEntrega": qt_doc + 1,
            "idCliente": id_logado,
            "idPedido": pay_processing["idPedido"],
            "dataEmissao": datetime.now() + timedelta(days=1),
            "cpfDestinatario": client["cpfCliente"],
            "telefoneDestinatario": client["telCliente"],
            "cepDestinatario": client["cepCliente"],
            "statusEntrega": "Em andamento"
        }

        result = collection6.insert_one(nova_entrega)

        if result.inserted_id:
            print(f'Nova entrega criada com sucesso. ID:{result.inserted_id}')

            collection5.update_one({"idCliente": id_logado, "status": "Em processamento"},
                                   {"$set": {"status": "Aprovado"}})

            print("Status do pagamento atualizado para 'Aprovado'.")

            collection4.update_one({"idCliente": id_logado, "status": "ativo"},
                                   {"$set": {"status": "Concluido"}})

            print("Status do pedido atualizado para 'Concluido'.")

        else:
            print('Erro ao criar a nova Entrega!')
    else:
        for item in active_pedido["itensPedido"]:
            # Buscando item do pedido na classe produto
            product = collection3.find_one({"codProduto": item["codProd"]})

            if product:
                # Atualizando qt na coleção produto
                collection3.update_one({"codProduto": item["codProd"]},
                                       {"$inc": {"qtDisponivel": item["quantidade"]}})
            else:
                print('Erro ao acessar Produto')

        collection5.update_one({"idCliente": id_logado, "status": "Em processamento"},
                               {"$set": {"status": "Recusado"}})

        print("Status do pagamento atualizado para 'Recusado'.")
else:
    print(f'Cliente com ID {id_logado} não encontrado ou não possui pagamento em processamento.')
