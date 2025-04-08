import pyodbc

dados_conexao = (
    "Driver={SQL Server};"
    "Server=NOME_DO_HOST;"
    "Database=NOME_DO_BANCO;"
)

try:
    conexao = pyodbc.connect(dados_conexao)
    print("Conexão efetuada")
except pyodbc.Error as erro:
    print(f"Erro ao se conectar com o banco de dados: {erro}")

cursor = conexao.cursor()
comando_leitura = f"""SELECT * FROM NOME_DA_TABELA"""
dados = []

def capturar_dados():
    cursor.execute(comando_leitura)
    rows = cursor.fetchall()
    colunas = [column[0] for column in cursor.description]
    for row in rows:
        dados.append(dict(zip(colunas, row)))
    print("Leitura de dados concluída")
    print(dados)

capturar_dados()