import pandas as pd

# Suponha que você tenha um DataFrame com uma coluna 'data'.
data = {'data': ['2023-01-15', '2023-02-20', '2023-02-25', '2023-03-10']}
df = pd.DataFrame(data)

# Converta a coluna 'data' para o tipo datetime.
df['data'] = pd.to_datetime(df['data'])

# Agrupe as datas por mês e defina o dia como 1.
df_grouped = df.groupby(pd.Grouper(key='data', freq='M')).min().reset_index()

# Renomeie a coluna de saída para 'data'.
df_grouped = df_grouped.rename(columns={'data': 'data_agrupada'})

# Exiba o DataFrame resultante.
print(df_grouped)