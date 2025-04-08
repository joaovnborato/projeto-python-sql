from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

def conectar_banco():
    dados_conexao = (
        "Driver={SQL Server};"
        "Server=DESKTOP-PUV1CSV;"
        "Database=Test_Base_Py;"
    )

    try:
        conexao = pyodbc.connect(dados_conexao)
        print("Conexão efetuada")
        return conexao
    except pyodbc.Error as erro:
        print(f"Erro ao se conectar com o banco de dados: {erro}")
        return None

@app.route('/')

def index():
    conexao = conectar_banco()
    data = request.args.get('data')
    cliente = request.args.get('cliente')
    produto = request.args.get('produto')

    dados = {}

    if conexao:
        cursor = conexao.cursor()
        query = """SELECT * FROM Vendas WHERE 1=1"""
        parametros = []

        if data:
            query += " AND data = ?"
            parametros.append(data)

        if produto:
            query += " AND produto LIKE ?"
            parametros.append(f"%{produto}%")

        if cliente:
            query += "AND cliente LIKE ?"
            parametros.append(f"%{cliente}%")

        try:
            cursor.execute(query, parametros)
            linhas = cursor.fetchall()
            colunas = [col[0] for col in cursor.description]
            dados = {
                linha[colunas.index("id_venda")]: dict(zip(colunas, linha))
                for linha in linhas
            }
            print("Dados filtrados com sucesso.")
        except Exception as erro:
            print(f"Erro ao executar consulta: {erro}")
        finally:
            cursor.close()
            conexao.close()

    return render_template('index.html', dados=dados)

if __name__ == '__main__':
    app.run(debug=True)


'''  ALGORITMO DE INSERÇÃO'
'
id = 7
cliente = "Diabo Junior"
produto = "Carro"
data = "02/04/2025"
preco = 2000
quantidade = 1

comando_insercao = f"""INSERT INTO Vendas(id_venda, cliente, produto, data_venda, preco, quantidade)
VALUES
    ({id}, '{cliente}', '{produto}', '{data}', {preco}, {quantidade})"""

'''