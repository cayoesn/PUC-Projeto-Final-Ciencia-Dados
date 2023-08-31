import pandas as pd
from datetime import datetime, timedelta
import locale

import valor_faturamento
import grafico_pedidos_entregues_cancelados
# import previsao_pedidos_entregues
# import previsao_pedidos_cancelados

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

data_atual = datetime.now().date()
um_ano = timedelta(days=365)
data_anterior = data_atual - um_ano

dados_stocks = pd.read_csv("base_dados_pedidos_esp.csv",
                           encoding='utf-8', low_memory=False)

filtro_data = "'{}' <= datapedido <= '{}'".format(data_anterior, data_atual)

dados_stocks_filtrado = dados_stocks.query(filtro_data)

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

valor_faturamento.gerar_valor_faturamento(data_atual, dados_stocks_filtrado)
grafico_pedidos_entregues_cancelados.gerar_grafico_pedidos_entregues_cancelados(
    dados_stocks_filtrado)
