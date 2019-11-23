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
except Exception as e:
    print(e)
    print("Pacotes não instalados.")
    print("Instale os pacotes necessários com o seguinte comando:")
    print("pip install -r requirements.txt")

# variaveis de conexão ao banco de dados
connection = None
cursor = None


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



def main():
    global connection
    global cursor

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

    # fechar conexão com o banco ao terminar
    cursor.close()


if __name__ == '__main__':
    main()