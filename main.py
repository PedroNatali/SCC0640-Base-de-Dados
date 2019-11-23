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



#Criando a Conexão SQL
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
    run_sql('esquema-gamexp.sql')

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