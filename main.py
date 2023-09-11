import pandas as pd
from datetime import datetime, timedelta
import locale
import warnings
import dashboards

warnings.filterwarnings("ignore")
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

data_atual = datetime.now().date()
um_ano = timedelta(days=365)
data_anterior = data_atual - um_ano

dados_pedidos = pd.read_csv("base_dados_pedidos_esp.csv",
                           encoding='utf-8', low_memory=False)

filtro_data = "'{}' <= datapedido <= '{}'".format(data_anterior, data_atual)

dados_pedidos_filtrado = dados_pedidos.query(filtro_data)

# Substituindo valores nulos no estado por valores que mais aparecem no dataset
dados_pedidos_filtrado['estado'].fillna(
    dados_pedidos_filtrado['estado'].mode()[0], inplace=True)

# Substituindo valores nulos no totalliquido pelo médio dos valores da coluna
dados_pedidos_filtrado['totalliquido'].fillna(
    dados_pedidos_filtrado['totalliquido'].mean())

# Substituindo valores 0 no totalliquido pelo médio dos valores da coluna
dados_pedidos_filtrado.loc[dados_pedidos_filtrado['totalliquido'] == 0,
                          'totalliquido'] = dados_pedidos_filtrado['totalliquido'].mean()

# Transformando coluna datapedido em datetime para calculo de datas
dados_pedidos_filtrado['datapedido'] = pd.to_datetime(
    dados_pedidos_filtrado['datapedido'])

dados_pedidos_agrupado = dados_pedidos_filtrado.groupby(pd.Grouper(
    key='datapedido', freq='M')).agg({'totalliquido': 'sum'}).reset_index()

dashboards = dashboards.DashboardPedidos(data_anterior, data_atual, dados_pedidos_filtrado)
dashboards.run()
