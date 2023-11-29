from pymongo import MongoClient
from datetime import datetime
import random
import string
import re

id_logado = 3

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


    while True:
        f_pgto = int(input('Forma de pagamento? [1 - PIX  | 2 - Cartão de Crédito]: '))
        # PIX, gera o código
        if f_pgto == 1:
            pix_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(25))
            break
        # Cartão de crédito, solicita os dados do cartão
        if f_pgto == 2:
            while True:
                num_cart = input('Número do cartão: ')
                if num_cart.isnumeric() and len(num_cart) == 16:
                    break
                else:
                    print('NÚMERO INVALIDO - Digite Novamente!')
            while True:
                name_cart = input('Nome impresso no cartão: ')
                if bool(re.match("^[a-zA-ZÀ-ÖØ-öø-ÿ\s'-]+$", name_cart)):
                    break
                else:
                    print('NOME INVÁLIDO: Digite novamente:')
            while True:
                bandeira = input('Bandeira do cartão: ')
                if bool(re.match("^[a-zA-ZÀ-ÖØ-öø-ÿ\s'-]+$", bandeira)):
                    break
            while True:
                mes_val = input('Mês validade: ')
                if mes_val.isdigit() and 1 <= int(mes_val) <= 12:
                    break
                else:
                    print('MÊS INVÁLIDO: Digite novamente:')
            while True:
                ano_val = input('Ano validade: ')
                if ano_val.isdigit() and datetime.now().year <= int(ano_val) <= datetime.now().year + 10:
                    break
                else:
                    print('ANO INVÁLIDO: Digite novamente:')

            val_cart ='/'.join([mes_val, ano_val])

            while True:
                ccv = input('Código CVV: ')
                if ccv.isdigit() and len(ccv) == 3:
                    break
                else:
                    print('CÓDIGO INVÁLIDO: Digite novamente:')
            break
        else:
            print('Opção inválida')

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

    if f_pgto == 1:
        novo_pgto = {
            "idCliente": id_logado,
            "idPedido": novo_pedido["idPedido"],
            "dataCriacao": datetime.now(),
            "valorTotal": novo_pedido["valorTotal"],
            "codPIX": pix_code,
            "status": "Em processamento"
            }
    else:
        novo_pgto = {
            "idCliente": id_logado,
            "idPedido": novo_pedido["idPedido"],
            "dataCriacao": datetime.now(),
            "valorTotal": novo_pedido["valorTotal"],
            "NumeroCartão": num_cart,
            "NomeCartão": name_cart,
            "BandeiraCartão": bandeira,
            "ValidadeCartão": val_cart,
            "CodSegurança": ccv,
            "status": "Em processamento"
        }
    result1 = collection5.insert_one(novo_pgto)

    if result1.inserted_id:
        print(f'Novo pagamento criado com sucesso. ID:{result1.inserted_id}.')
    else:
        print('Erro ao criar o novo pagamento!')
