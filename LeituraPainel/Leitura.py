import pandas as pd
import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password=1234,
    database="db_monitoramento"
)
cursor = conexao.cursor()
df = pd.read_excel("C:/Users/redekrill/Documents/Relatorio_Onda.xlsx", skiprows = 14, skipfooter=3)
df['Destinatário'] = df['Destinatário'].ffill()
df['report'] = df['Cód. Onda'].isnull().cumsum()
df_limpar = df.dropna(subset=['Cód. Onda'])

dados_insert = [tuple(x) for x in df_limpar.to_numpy()]
query_insert = "INSERT"
print(df.head())
print(df.tail())
print(df_limpar.columns.tolist())