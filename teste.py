try:
    import psycopg2
    import sys
    import eel
except Exception as e:
    print(e)
    print("Pacotes necessarios nao encontrados, execute o comando a seguir: ")
    print("pip install -r requirements.txt")

# variaveis de conexao ao banco de dados
connection = None
cursor = None

#Criando a Conexao SQL - so havera interface com o banco a partir deste codigo
def connect():
    global connection
    global cursor

    try:
        #define os parametros
        print('Conectando no PostgreSQL...')
        connection = psycopg2.connect(host = 'localhost', database = 'postgres',
        user = 'postgres', password = 'matheus123')

        #define o autocommit
        connection.autocommit = True

        #cria o cursor 
        cursor = connection.cursor()

        #Se for bem sucedida, a conexao, mostrar a versao
        cursor.execute('SELECT version()')
        print("Conexao feita com sucesso")
        return connection, cursor

    except (Exception, psycopg2.DatabaseError) as error:
        print(" Conexao do PostgreSQL nao foi concluida!")
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
            #Se nao for possivel, printe o erro
            except(Exception, psycopg2.DatabaseError) as error:
                print('\n' + "ERRO: " + comando)
                print('\n' + str(error))



# SELECT
@eel.expose
def select(tabela):
    global connection
    global cursor

    # gerar query com dados do site
    query = "SELECT *" + " FROM " + tabela
    # print(query)
    #cria a variavel dos resultados
    resultados = []
    try:
        # tentar executar o comando
        cursor.execute(query)
        resultado = cursor.fetchall()
        # print(resultado)
        # exibir resultado
        print("Select : ")

        #Para cada valor em resultado, inserir na variavel de resultados, separando por virgula
        for valor in resultado:
            resultados.append(str(valor))
            # print(resultados)

        print("\n")

        #retorna os resultados
        return resultados

    except Exception as erro:
        # caso SELECT de erro, exibir erro e retornar lista vazia
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
    for nro, valor in nro_valor_conteudo:
        #Se nao for ultimo
        if (nro < tam_conteudo - 1):
            #adiciona o valor separado por virgula
            valor_conteudo = valor_conteudo + "'" + str(valor) + "'" + ", "
        #Se for a ultima 
        else:
            valor_conteudo = valor_conteudo + "'" + str(valor) + "'"

    # gerar query com dados do site
    query = "INSERT INTO " + tabela + " VALUES (" + valor_conteudo + ");"

    # tentar executar o comando
    try:
        cursor.execute(query)
        resultado = 0

    #Exibe erro
    except Exception as erro:
        # em caso de erro, retornar -1 para alertar no site que deu erro
        print("ERRO: ")
        print("")
        print(str(erro))
        resultado = 1  

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

    # caso haja mais de uma condicao, adiciona-las
    if (tam_colunas > 1):
        for nro, valor in nro_valor_colunas:
            if (nro > 0):
                query += " AND " + str(colunas[nro]) + "=" + "'" + str(valores[nro]) + "'"

    #tenta executar o comando
    try:
        cursor.execute(query)
        resultado = 0

    #Exibe erro
    except Exception as erro:
        # em caso de erro, retornar -1 para alertar no site que deu erro
        print("ERRO: ")
        print("")
        print(str(erro))
        resultado = 1 

    # formatar esse resultado
    return resultado

# UPDATE
@eel.expose
def update(tabela, coluna, valores, col_condicao, val_condicao):
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
        #se nao chegou no ultimo
        if (nro < tam_coluna - 1):
            #adiciona o valor a variavel de mudancas
            mudancas = mudancas + str(coluna[nro]) + "=" + "'" + str(valores[nro]) + "'" + ", "
        #se chegou
        else:
            #adiciona o ultimo valor
            mudancas = mudancas + str(coluna[nro]) + "=" + "'" + str(valores[nro]) + "'"

    # gerar query com dados do site
    query = "UPDATE " + tabela + " SET " + mudancas + " WHERE " + col_condicao[0] + "=" + "'" + val_condicao[0] + "'"


    #Quantidade de condicoes
    tam_col_condicao = len(col_condicao)

    nro_valor_colCondicao = enumerate(col_condicao, start=1)

    # caso haja mais de uma condicao
    if (tam_col_condicao > 1):
        for nro, valor in nro_valor_colCondicao:
            query += " AND " + str(col_condicao[nro]) + "=" + "'" + str(val_condicao[nro]) + "'"

    #tenta executar o comando
    try:
        cursor.execute(query)
        resultado = 0

    #exibe erro
    except Exception as error:
        # em caso de erro, retornar -1 para alertar no site que deu erro
        print("ERRO: ")
        print("")
        print(str(error))
        resultado = 1  # deu errado, alertar no site

    # formatar esse resultado
    return resultado

# SELECT SIMPLES (COM APENAS SELECT, FROM E WHERE) DE UMA UNICA TABELA
@eel.expose
def simplesSelect(colunas, tabela, condicoes):
    global connection
    global cursor
    
    col = ""
    nro_valor_coluna = enumerate(colunas)
    tam_coluna = len(colunas)
    for nro,valor in nro_valor_coluna:
        if(nro < tam_coluna - 1):
            col = col + str(valor) +","
        else:
            col = col + str(valor)

    query = "SELECT " + col + " FROM " + tabela + " WHERE " + condicoes + ";"


    try:
        cursor.execute(query)
        resultado = cursor.fetchall()
        print(resultado)

        return resultado
    except Exception as error:
        print("ERRO: ")
        print("")
        print(str(error))

        return error


def main():
    global connection
    global cursor

    # conectar ao banco de dados
    connection, cursor = connect()
    
    #dropar todas as tabelas para que nao haja problemas 
    print("Drop nas tabelas do banco...")
    executeSQL('drop.sql')

    #Inicializando as tabelas
    print("Cria as tabelas do banco...")
    executeSQL('esquema-gamexp.sql')

    #Popula o Banco com tuplas
    print("Populando o banco de dados com tuplas iniciais...")
    executeSQL('insert-gamexp.sql')

    # abrir interface grafica
    print("Abrindo a interface grafica...")

    eel.init('interface')
    #OPEN(INTERFACE)
    try:
        eel.start('home.html', mode = "chrome-app", port = 8000, chromeFlags = ["--incognito"])
    except (Exception) as e:
        print('\n' + "Erro: " + str(e))

    # fechar conexao com o banco ao terminar
    print("Conexao fechada")
    cursor.close()


if __name__ == '__main__':
    main()