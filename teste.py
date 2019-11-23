#!/bin/usr/env python3
# -*- coding: utf-8 -*-
#Código para o trabalho da Disciplina de Base de Dados 

#Authors
    #Pedro Natali
    #Samira Mendes
    #Matheus Uema
    #Nelson Neto

#Importa as bibliotecas necessarias
try:
    import psycopg2
    import sys
    import eel
except Exception as e:
    print(e)
    print("Pacotes necessários não encontrados, execute o comando a seguir: ")
    print("pip install -r requirements.txt")

# variaveis de conexão ao banco de dados
connection = None
cursor = None

#Criando a Conexão SQL - só haverá interface com o banco a partir deste código
def connect():
    global connection
    global cursor

    try:
        #define os parâmetros
        print('Conectando no PostgreSQL...')
        connection = psycopg2.connect(host = 'localhost', database = 'postgres',
        user = 'postgres', password = 'matheus123')

        #define o autocomit
        connection.autocommit = True

        #cria o cursor 
        cursor = connection.cursor()

        #Se for bem sucedida, a conexão, mostrar a versão
        cursor.execute('SELECT version()')
        print("Conexão feita com sucesso")
        return connection, cursor

    except (Exception, psycopg2.DatabaseError) as error:
        print(" Conexão do PostgreSQL não foi concluida!")
        print("")
        print(str(error))
        sys.exit()



#Cria funcao que executa os comandos de SQL a partir de um arquivo
#O arquivo deve ter seus comandos separados por ';'
@eel.expose
def executeSQL(filename):
    global connection
    global cursor

    #Abre o arquivo e passa as informacoes dele para a var SQL
    file = open(filename, 'r')
    sql = file.read()
    file.close

    print("Executando..")

    #Separa os comandos por ';'
    comandos = sql.split(';')


    #Passa por todos os comandos da lista
    for comando in comandos[:-1]:
        if (len(comando) > 0):
            comando = comando + ';'
            #Tente executar o comando
            try:
                cursor.execute(comando)
            #Se não for possível, printe o erro
            except(Exception, psycopg2.DatabaseError) as error:
                print('\n' + "ERRO: " + comando)
                print('\n' + str(error))



# SELECT
@eel.expose
def select(tabela, colunas):
    global connection
    global cursor

    #define o tamanho das clunas
    tam_colunas = len(colunas)

    #numero das colunas
    nro_cont_colunas = enumerate(colunas)


    cont_colunas = " "
    for nro, valor in nro_valor_colunas
        #Se não for a última das colunas
        if (nro < tam_colunas - 1):
            #adiciona o valor ao conteudo das colunas separado por virgula
            cont_colunas = cont_colunas + str(valor) + ","
        #Se for a última das colunas
        else:
            cont_colunas = cont_colunas + str(valor)

    # gerar query com dados do site
    query = "SELECT " + cont_colunas + " FROM " + tabela

    #cria a variavel dos resultados
    resultados = []
    try:
        # tentar executar o comando
        cursor.execute(query)
        resultado = cursor.fetchall()

        # exibir resultado
        print("Select : ")

        #Para cada valor em resultado, inserir na variavel de resultados, separando por virgula
        for valor in resultado:
            resultados.append(str(valor))
            print(valor, end=", ")

        print("\n")

        #retorna os resultados
        return resultados

    except Exception as erro:
        # caso SELECT dê erro, exibir erro e retornar lista vazia
        print("ERRO: ")
        print("")
        print(str(erro))

        #retorna os resultados
        return resultados

# INSERT
@eel.expose
def insert(tabela, conteudo):
    global connection
    global cursor

    #define o tamanho do conteudo
    tam_conteudo = len(conteudo)

    #numero e valor dos conteudos
    nro_valor_conteudo = enumerate(conteudo)


    valor_conteudo = " "
    for nro, valor in nro_valor_conteudo
        #Se não for último
        if (nro < tam_conteudo - 1):
            #adiciona o valor separado por virgula
            valor_conteudo = valor_conteudo + "'" + str(valor) + "'" + ", "
        #Se for a última 
        else:
            valor_conteudo = valor_conteudo + "'" + str(valor) + "'"

    # gerar query com dados do site
    query = "INSERT INTO " + tabela + " VALUES (" + valor_conteudo + ");"

    # tentar executar o comando
    try:
        cursor.execute(query)
        resultado = 1

    #Exibe erro
    except Exception as erro:
        # em caso de erro, retornar -1 para alertar no site que deu erro
        print("ERRO: ")
        print("")
        print(str(erro))
        resultado = -1  

    # formatar esse resultado
    return resultado

# DELETE
@eel.expose
def delete(tabela, colunas, valores):
    global connection
    global cursor

    # gerar query com dados do site
    query = "DELETE FROM " + tabela + " WHERE " + str(colunas[0]) + "=" + "'" + str(valores[0]) + "'"

    #Tamanho das colunas 
    tam_colunas = len(colunas)

    #atribui a variavel nro_valor um numero da coluna com seu respectivo valor
    nro_valor_colunas = enumerate(colunas)

    # caso haja mais de uma condição, adicioná-las
    if (tam_colunas > 1):
        for nro, valor in nro_valor_colunas:
            if (nro > 0):
                query += " AND " + str(colunas[nro]) + "=" + "'" + str(valores[nro]) + "'"

    #tenta executar o comando
    try:
        cursor.execute(query)
        resultado = 1

    #Exibe erro
    except Exception as erro:
        # em caso de erro, retornar -1 para alertar no site que deu erro
        print("ERRO: ")
        print("")
        print(str(erro))
        resultado = -1 

    # formatar esse resultado
    return resultado

# UPDATE
@eel.expose
def update(tabela, coluna, valor, col_condicao, val_condicao):
    global connection
    global cursor

    tabela = str(tabela)

    #Atribui a variavel nro-valor uma tupla c numero e valor atribuido a cada coluna
    nro_valor_coluna = enumerate(coluna)

    #Tamanho da colunna
    tam_coluna = len(coluna)

    mudancas = ""

    #percorre tudo
    for nro, valor in nro_valor_coluna:
        #se não chegou no último
        if (nro < tam_coluna - 1):
            #adiciona o valor a variável de mudanças
            mudancas = mudancas + str(coluna[nro]) + "=" + "'" + str(valor[nro]) + "'" + ", "
        #se chegou
        else:
            #adiciona o ultimo valor
            mudancas = mudancas + str(coluna[nro]) + "=" + "'" + str(valor[nro]) + "'"

    # gerar query com dados do site
    query = "UPDATE " + tabela + " SET " + mudancas + " WHERE " + col_condicao[0] + "=" + "'" + val_condicao[0] + "'"


    #Quantidade de condicoes
    tam_col_condicao = len(col_condicao)

    nro_valor_colCondicao = enumerate(col_condicao, start=1)

    # caso haja mais de uma condição
    if (tam_col_condicao > 1):
        for nro, valor in nro_valor_colCondicao:
            query += " AND " + str(col_condicao[nro]) + "=" + "'" + str(val_condicao[nro]) + "'"

    #tenta executar o comando
    try:
        cursor.execute(query)
        resultado = 1

    #exibe erro
    except Exception as error:
        # em caso de erro, retornar -1 para alertar no site que deu erro
        print("ERRO: ")
        print("")
        print(str(error))
        resultado = -1  # deu errado, alertar no site

    # formatar esse resultado
    return resultado


def main():
    global connection
    global cursor

    # conectar ao banco de dados
    connection, cursor = connect()
    
    #dropar todas as tabelas para que não haja problemas 
    print("Drop nas tabelas do banco...")
    executeSQL('drop.sql')

    #Inicializando as tabelas
    print("Cria as tabelas do banco...")
    executeSQL('initialize.sql')

    #Popula o Banco com tuplas
    print("Populando o banco de dados com tuplas iniciais...")
    executeSQL('insert.sql')

    # abrir interface gráfica
    print("Abrindo a interface gráfica...")


    #OPEN(INTERFACE)

    # fechar conexão com o banco ao terminar
    cursor.close()


if __name__ == '__main__':
    main()