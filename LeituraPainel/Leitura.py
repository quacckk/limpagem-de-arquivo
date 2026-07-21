import numpy as np
import pandas as pd
import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="db_monitoramento"
)
cursor = conexao.cursor()
df = pd.read_excel("C:/Users/redekrill/Documents/Relatorio_Onda.xlsx", skiprows = 14, skipfooter=3)
df['Destinatário'] = df['Destinatário'].ffill()
df_limpar = df.dropna(subset=['Cód. Onda'])
print(df.head())
df_limpar['Data e Hora Geração'] = pd.to_datetime(df_limpar['Data e Hora Geração'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
df_limpar = df_limpar.replace({np.nan: None})
dados_insert = [tuple(x) for x in df_limpar.to_numpy()]
query_insert = """
INSERT INTO onda 
(DESTINATARIO, Cod_onda, Onda, Data_Hora, Codigo_interno, produto, qtd_sugerida, 
 qtd_gerada_Cx, qtd_gerada_Un, qtd_nao_gerada_Un, lote, onda_bonificada, motivo) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
cursor.executemany(query_insert, dados_insert)
conexao.commit()
print("Sucesso")

cursor.close()
conexao.close()

print(df.head())
print(df.tail())
print(df_limpar.columns.tolist())