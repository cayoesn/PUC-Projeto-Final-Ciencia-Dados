import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import locale
import plotly.graph_objs as go

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

data_atual = datetime.now().date()
um_ano = timedelta(days=365)
data_anterior = data_atual - um_ano

dados_stocks = pd.read_csv("base_dados_pedidos_esp.csv",
                           encoding='utf-8', low_memory=False)

filtro_data = "'{}' <= datapedido <= '{}'".format(data_anterior, data_atual)

dados_stocks_filtrado = dados_stocks.query(filtro_data)

# Substituindo valores nulos no totalliquido pelo médio dos valores da coluna
dados_stocks_filtrado['totalliquido'].fillna(
    dados_stocks_filtrado['totalliquido'].mean())

# Substituindo valores 0 no totalliquido pelo médio dos valores da coluna
dados_stocks_filtrado.loc[dados_stocks_filtrado['totalliquido'] == 0,
                          'totalliquido'] = dados_stocks_filtrado['totalliquido'].mean()

# Transformando coluna datapedido em datetime para calculo de datas
dados_stocks_filtrado['datapedido'] = pd.to_datetime(
    dados_stocks_filtrado['datapedido'])

# Cálculo de faturamento do mês atual e mês passado
ano_atual = data_atual.year
mes_atual = data_atual.month

primeiro_dia_do_mes_atual = data_atual.replace(day=1)
primeiro_dia_do_mes_passado = primeiro_dia_do_mes_atual - timedelta(days=1)
ano_mes_passado = primeiro_dia_do_mes_passado.year
mes_passado = primeiro_dia_do_mes_passado.month

faturamento_mes_passado = dados_stocks_filtrado.loc[(dados_stocks_filtrado['datapedido'].dt.month == mes_passado) & (
    dados_stocks_filtrado['datapedido'].dt.year == ano_mes_passado)]['totalliquido'].sum()

faturamento_mes_atual = dados_stocks_filtrado.loc[(dados_stocks_filtrado['datapedido'].dt.month == mes_atual) & (
    dados_stocks_filtrado['datapedido'].dt.year == ano_atual)]['totalliquido'].sum()

fig = go.Figure()

fig.add_trace(go.Indicator(
    mode="number+delta",
    value=faturamento_mes_atual,
    number={"prefix": "R$"},
    title={"text": "Faturamento do mês atual<br><span style='font-size:0.8em;color:gray'>comparado ao mês anterior</span><br>"},
    delta={'reference': faturamento_mes_passado, 'relative': True},
))

fig.add_trace(go.Indicator(
    mode="number+delta",
    value=faturamento_mes_atual,
    number={"prefix": "R$"},
    title={"text": "Faturamento do mês atual<br><span style='font-size:0.8em;color:gray'>comparado ao mês anterior</span><br>"},
    delta={'reference': faturamento_mes_passado, "prefix": "R$"},
    domain={'x': [0.6, 1], 'y': [0, 1]}))

fig.show()
