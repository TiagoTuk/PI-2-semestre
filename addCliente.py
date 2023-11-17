from pymongo import MongoClient
import datetime
import re

# conectando ao banco de dados
connection_string = "mongodb+srv://tiago:tiago123@projetointegrador.hstyqui.mongodb.net/"
client = MongoClient(connection_string, 27017)
db_connection = client["PI2_Construcao"]

# conectando a coleção
collection = db_connection.get_collection("clientes")

qt_doc = collection.count_documents({})

#Nome
while True:
    nome = input('Nome Completo: ')
    if bool(re.match("^[a-zA-ZÀ-ÖØ-öø-ÿ\s'-]+$", nome)):
        break
    else:
        print('NOME INVÁLIDO: Digite novamente:')

#CPF
while True:
    cpf = input('CPF: ').strip()
    if cpf.isnumeric() and len(cpf) ==11:
        break
    else:
        print('CPF INVÁLIDO: Digite novamente!')

#E-mail
while True:
    email = input('E-mail: ').strip()
    if email.count('@') == 1:
        break
    else:
        print('EMAIL INVÁLIDO: Digite novamente!')

#Data de Nascimento
while True:
    dia_nasc = input('Dia de nascimento: ')
    if dia_nasc.isdigit() and 1 <= int(dia_nasc) <= 31:
        break
    else:
        print('DIA INVÁLIDO: Digite novamente!')

while True:
    mes_nasc = input('Mês de nascimento: ')
    if mes_nasc.isdigit() and 1 <= int(mes_nasc) <= 12:
        break
    else:
        print('MÊS INVÁLIDO: Digite novamente: ')

while True:
    ano_nasc = input('Ano nascimento: ')
    if ano_nasc.isdigit() and 1900 <= int(ano_nasc) <= datetime.datetime.now().year:
        break
    else:
        print('ANO INVÁLIDO : Digite novamente: ')


data_nasc = '-'.join([ano_nasc, mes_nasc, dia_nasc])

# Telefone
while True:
    ddd = input('DDD: ')
    if ddd.isdigit() and len(ddd) == 2:
        break
    else:
        print('DDD INVÁLIDO: Digite novamente:')

while True:
    tel = input('Telefone: ')
    if tel.isdigit() and 8 <=len(tel) <= 9:
        break
    else:
        print('TELEFONE INVÁLIDO: Digite novamente: ')

telefone = "-".join([ddd, tel])

# Endereço
# CEP
while True:
    cep = input('Cep: ')
    if cep.isdigit() and len(cep) == 8:
        break
    else:
        print('CEP INVALIDO: Digite novamente: ')

#Logradouro
while True:
    logra = input('Logradouro: ')
    if all(char.isalpha() or char.isspace() for char in logra):
        break
    else:
        print('LOGRADOURO INVÁLIDO: Digite novamente: ')

#Numero endereço
while True:
    num_end = input('Número endereço: ')
    if num_end.isdigit():
        break
    else:
        print('NÚMERO INVÁLIDO: Digite novamente: ')

#Complemento endereço
comp_end = input('Complemento: ')

#Bairro
while True:
    bairro = input('Bairro: ')
    if all(char.isalpha() or char.isspace() for char in bairro):
        break
    else:
        print('BAIRRO INVÁLIDO: Digite novamente: ')

#UF
while True:
    uf = input('Uf: ')
    if uf.isalpha() and len(uf) == 2:
        break
    else:
        print('UF INVÁLIDO: Digite novamente: ')

#Cidade
while True:
    cidade = input('Cidade: ')
    if all(char.isalpha() or char.isspace() for char in cidade):
        break
    else:
        print('CIDADE INVÁLIDA: Digite novamente: ')

#Senha
while True:
    senha = input('Senha: ')
    if senha:
        break
    else:
        print('FAVOR DIGITAR UMA SENHA!')


collection.insert_one({
    "idCliente" : qt_doc + 1,
    "nomeCliente" : nome,
    "cpfCliente" : cpf,
    "emailCliente" : email,
    "dtNascCliente" : data_nasc,
    "telCliente" : telefone,
    "endCliente":{
        "cepCliente" : cep,
        "logradCliente" : logra,
        "numCliente" : num_end,
        "compCliente": comp_end,
        "bairroCliente" : bairro,
        "ufCliente" : uf,
        "cidadeCliente" : cidade},
    "loginCliente" : email,
    "senhaCliente" : senha
})

