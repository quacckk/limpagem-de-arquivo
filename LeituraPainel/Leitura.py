import numpy as np
import pandas as pd
import mysql.connector


def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="db_monitoramento"
        )
        return conexao
    except mysql.connector.Error as erro:
        print(f"Erro: {erro}")
        return None

def tratamento(caminho):
    df = pd.read_excel(caminho ,skiprows=14, skipfooter=3)
    df['Destinatário'] = df['Destinatário'].ffill()
    df_limpar = df.dropna(subset=['Cód. Onda'])
    df_limpar['Data e Hora Geração'] = pd.to_datetime(df_limpar['Data e Hora Geração'], format='%d/%m/%Y %H:%M:%S',
                                                      errors='coerce')
    df_limpar = df_limpar.replace({np.nan: None})
    dados_insert = [tuple(x) for x in df_limpar.to_numpy()]
    return dados_insert
def tratamento_cargas(caminho_cargas):
    df = pd.read_excel(caminho_cargas ,skiprows=4)
def inserir_dados(conexao, dados_insert):
    if not dados_insert:
        print("Nenhum dado encontrado")
        return
    cursor = conexao.cursor()
    query_insert = """
    INSERT INTO onda 
    (DESTINATARIO, Cod_onda, Onda, Data_Hora, Codigo_interno, produto, qtd_sugerida, 
     qtd_gerada_Cx, qtd_gerada_Un, qtd_nao_gerada_Un, lote, onda_bonificada, motivo) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.executemany(query_insert, dados_insert)
        cursor.executemany(query_insert, dados_insert)
        conexao.commit()
        print("Sucesso")
    except mysql.connector.Error as erro:
        print(f"Erro: {erro}")
    finally:
        cursor.close()

if __name__ == '__main__':
    caminho = "C:/Users/redekrill/Documents/Relatorio_Onda.xlsx"
    print("Fazendo tratamento do arquivo")
    dados_para_banco = tratamento(caminho)

    print("Conectando ao banco de dados")
    db_conexao = conectar_banco()
    if db_conexao:
        print("iniciando inserção")
        inserir_dados(db_conexao, dados_para_banco)
        db_conexao.close()
        print("Finalizado")