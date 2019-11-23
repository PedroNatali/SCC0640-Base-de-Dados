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
    import eel
    from configparser import ConfigParser
    import sys
except Exception as e:
    print(e)
    print("Pacotes não instalados.")
    print("Instale os pacotes necessários com o seguinte comando:")
    print("pip install -r requirements.txt")

# variaveis de conexão ao banco de dados
connection = None
cursor = None


#################### VAMOS DEFINIR TODAS AS OPERAÇÕES 
#################### QUE PODEM SER REALIZADAS


#################### SELECT #########################
@eel.expose
def select(table, columns):
    global connection
    global cursor

    print("Executando SELECT...")
    # parsear colunas
    columns_content = ""
    for index, value in enumerate(columns):
        if (index < len(columns) - 1):
            columns_content += str(value) + ", "
        else:
            columns_content += str(value)

    # gerar query com dados do site
    query = "SELECT " + columns_content + " FROM " + table
    print("\n" + 'QUERY: ' + " " + query)

    results = []
    try:
        # tentar executar a query
        cursor.execute(query)
        result = cursor.fetchall()

        # exibir resultado
        print("Resultado: ")
        for value in result:
            results.append(str(value))
            print(value, end=", ")
        print("\n")
        return results
    except Exception as error:
        # caso SELECT dê erro, exibir erro e retornar lista vazia
        print("ERRO: ")
        print("")
        print(str(error))
        return results

#################### INSERT #########################
@eel.expose
def insert(table, values):
    global connection
    global cursor

    print("Executando INSERT...")
    # parsear dados
    values_content = ""
    for index, value in enumerate(values):
        if (index < len(values) - 1):
            values_content += "'" + str(value) + "'" + ", "
        else:
            values_content += "'" + str(value) + "'"

    # gerar query com dados do site
    query = "INSERT INTO " + table + " VALUES (" + values_content + ");"
    print("\n" + 'QUERY: ' + " " + query)

    try:
        # tentar executar a query
        cursor.execute(query)
        result = 1
    except Exception as error:
        # em caso de erro, retornar -1 para alertar no site que deu erro
        # exibir erro no terminal
        print("ERRO: ")
        print("")
        print(str(error))
        result = -1  # deu errado, alertar no site
    # formatar esse resultado
    return result

#################### DELETE #########################
@eel.expose
def delete(table, columns, values):
    global connection
    global cursor

    print("Executando DELETE...")
    # gerar query com dados do site
    query = "DELETE FROM " + table + " WHERE " + str(columns[0]) + "=" + "'" + str(values[0]) + "'"
    # caso haja mais de uma condição, adicioná-las
    if (len(columns) > 1):
        for index, content in enumerate(columns):
            if (index > 0):
                query += " AND " + str(columns[index]) + "=" + "'" + str(values[index]) + "'"
    print("\n" + 'QUERY' + " " + query)

    try:
        # tentar executar a query
        cursor.execute(query)
        result = 1
    except Exception as error:
        # em caso de erro, retornar -1 para alertar no site que deu erro
        # exibir erro no terminal
        print("ERRO: ")
        print("")
        print(str(error))
        result = -1  # deu errado, alertar no site

    # formatar esse resultado
    return result


#################### UPDATE #########################
@eel.expose
def update(table, column, value, condition_columns, condition_values):
    global connection
    global cursor

    print("Executando UPDATE...")
    table = str(table)

    updates = ""
    for index, content in enumerate(column):
        if (index < len(column) - 1):
            updates += str(column[index]) + "=" + "'" + str(value[index]) + "'" + ", "
        else:
            updates += str(column[index]) + "=" + "'" + str(value[index]) + "'"

    # gerar query com dados do site
    query = "UPDATE " + table + " SET " + updates + " WHERE " + condition_columns[0] + "=" + "'" + condition_values[0] + "'"
    # caso haja mais de uma condição, adicioná-las
    if (len(condition_columns) > 1):
        for index, value in enumerate(condition_columns, start=1):
            query += " AND " + str(condition_columns[index]) + "=" + "'" + str(condition_values[index]) + "'"

    print("\n" + 'QUERY' + " " + query)

    try:
        # tentar executar a query
        cursor.execute(query)
        result = 1
    except Exception as error:
        # em caso de erro, retornar -1 para alertar no site que deu erro
        # exibir erro no terminal
        print("ERRO: ")
        print("")
        print(str(error))
        result = -1  # deu errado, alertar no site

    # formatar esse resultado
    return result

#Criando a Conexão SQL
def connection()
	global connection
	global cursor

	try:
		#define os parâmetros
		print('Conectando no PostgreSQL...')
		connection = psycopg2.connect(host = 'localhost', database = 'gamexp',
		user = 'postgres', password = 'matheus123')

		#define o autocomit
		connection.autocommit = True

		#cria o cursor 
		cursor = connection.cursor()

		#Se for bem sucedida, a conexão, mostrar a versão
		cursor.execute('SELECT version()')
		print("Conexão feita com sucesso. Bem-vindo!")
		return connection, cursor

	except (Exception, psycopg2.DatabaseError) as error:
		print(" Conexão do PostgreSQL não foi concluida com sucesso!")
        print("")
        print(str(error))
        sys.exit()


#Funcao que executa comandos de um arquivo SQL
@eel.expose
def run_sql(filename):
    global connection
    global cursor

    # ler arquivo SQL em um único buffer
    file = open(filename, 'r')
    sql = file.read()
    file.close()

    print("Executando")
    # obter os comandos separando o arquivo por ';'
    commands = sql.split(';')

    # executar todos os comandos
    for command in commands[:-1]:
        if (len(command) > 0):
            command = command + ';'
            try:
                cursor.execute(command)
            except(Exception, psycopg2.DatabaseError) as error:
                print('\n' + "ERRO: " + command)
                print('\n' + str(error))

#Consulta da página inicial
@eel.expose
def home_queries(filename):
    global connection
    global cursor

    # ler arquivo SQL em um único buffer
    file = open(filename, 'r')
    sql = file.read()
    file.close()

    print("Executando...")

    # executar consulta
    results = []
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        print("Resultado da consulta " + filename + ": ")
        print(result)
        for value in result:
            results.append(str(value))
        return results
    except(Exception, psycopg2.DatabaseError) as error:
        print('\n' + 'ERRO: ' + sql)
        print('\n' + str(error))
        return -1

def main():
    global connection
    global cursor

    option_web = {
        'mode': "chrome-app",
        'port': 8000,
        # modo incognito evita problemas com cache
        'chromeFlags': ["--incognito"]
    }

    # inicializar servidor web local
    eel.init('interface')

    # conectar ao banco de dados
    connection, cursor = connect()
    
    #dropar todas as tabelas para que não haja problemas 
    run_sql('drop.sql')

    #Inicializando as tabelas
    print("Cria as tabelas do banco...")
    run_sql('initialize.sql')

    #Popula o Banco com tuplas
    print("Populando o banco de dados com tuplas iniciais...")
    run_sql('insert.sql')

    # abrir interface gráfica
    print("Abrindo a interface gráfica...")

    try:
        eel.start('index.html', options=option_web)
    except (Exception) as e:
        print('\n' + 'ERRO: ' + str(e))

    # fechar conexão com o banco ao terminar
    cursor.close()


if __name__ == '__main__':
    main()