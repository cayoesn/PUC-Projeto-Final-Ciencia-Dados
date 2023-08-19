import pandas as pd
from datetime import datetime
import locale
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

dados_stocks = pd.read_csv("base_dados_pedidos.csv",
                           encoding='utf-8', low_memory=False)
# print(dados_stocks.columns)
dados_stocks_filtrado = dados_stocks.query(
    "'2022-08-01' <= datapedido <= '2023-08-01'")

# Substituindo valores nulos no estado por valores que mais aparecem no dataset
dados_stocks_filtrado['estado'].fillna(
    dados_stocks_filtrado['estado'].mode()[0], inplace=True)

# Substituindo valores nulos no totalliquido pelo médio dos valores da coluna
dados_stocks_filtrado['totalliquido'].fillna(
    dados_stocks_filtrado['totalliquido'].mean())

# Substituindo valores 0 no totalliquido pelo médio dos valores da coluna
dados_stocks_filtrado.loc[dados_stocks_filtrado['totalliquido'] == 0,
                          'totalliquido'] = dados_stocks_filtrado['totalliquido'].mean()

# Transformando coluna datapedido em datetime para calculo de datas
dados_stocks_filtrado['datapedido'] = pd.to_datetime(
    dados_stocks_filtrado['datapedido'])

# Cálculo de faturamento do mês atual
mes_atual = datetime.now().month
faturamento_mes_atual = dados_stocks_filtrado[dados_stocks_filtrado['datapedido'].dt.month ==
                                              mes_atual]['totalliquido'].sum()
faturamento_mes_atual = locale.currency(faturamento_mes_atual, grouping=True)

dados_stocks_agrupado = dados_stocks_filtrado
dados_stocks_agrupado['quantidade_pedido'] = 1
dados_stocks_agrupado = dados_stocks_filtrado.groupby([dados_stocks_filtrado['datapedido'].dt.to_period(
    'M'), 'statuspedido']).agg({'totalliquido': 'sum', 'quantidade_pedido': 'count'}).reset_index()

dados_datas_string = dados_stocks_agrupado['datapedido'].astype(str)
dados_pedidos_entregues = np.array([], dtype=np.float64)
dados_pedidos_cancelados = np.array([], dtype=np.float64)

for data in dados_stocks_agrupado['datapedido']:
    dados_data = dados_stocks_agrupado[dados_stocks_agrupado['datapedido'] == data]
    valor_cancelado = dados_data[dados_data['statuspedido']
                                 == 'CANCELADO']['totalliquido'].values
    valor_entregue = dados_data[dados_data['statuspedido']
                                == 'ENTREGUE']['totalliquido'].values
    valor_cancelado = valor_cancelado[0] if len(valor_cancelado) > 0 else 0
    valor_entregue = valor_entregue[0] if len(valor_entregue) > 0 else 0
    dados_pedidos_cancelados = np.append(
        dados_pedidos_cancelados, valor_cancelado)
    dados_pedidos_entregues = np.append(
        dados_pedidos_entregues, valor_entregue)

data = {
    'Mes': dados_datas_string.values,
    'Pedidos_Cancelados': dados_pedidos_cancelados,
    'Pedidos_Entregues': dados_pedidos_entregues,
}

def format_to_brl(value):
    return f'R$ {value:,.2f}'.replace('.', ',')

df_plt = pd.DataFrame(data)
fig = px.line(df_plt, x='Mes', y=['Pedidos_Entregues', 'Pedidos_Cancelados'],
              title='Faturamento Mensal - Comparação entre Pedidos Entregues e Cancelados')

fig.update_xaxes(title_text='Meses')
fig.update_yaxes(title_text='Total de faturamento')

fig.update_layout(legend_title_text='Pedidos')
fig.update_traces(name='Pedidos entregues', selector=dict(name='Pedidos_Entregues'))
fig.update_traces(name='Pedidos cancelados', selector=dict(name='Pedidos_Cancelados'))

def formatar_moeda(valor):
    return locale.currency(valor, grouping=True)

format_brl = 'R$ %{y:,.2f}'

fig.update_traces(mode='lines+markers+text', hovertemplate=format_brl,
                  texttemplate=format_brl, textposition='top center')

fig.show()