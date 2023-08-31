import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import locale
import plotly.graph_objs as go

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def gerar_valor_faturamento(data_atual, dados_pedidos):
    ano_atual = data_atual.year
    mes_atual = data_atual.month

    primeiro_dia_do_mes_atual = data_atual.replace(day=1)
    primeiro_dia_do_mes_passado = primeiro_dia_do_mes_atual - timedelta(days=1)
    ano_mes_passado = primeiro_dia_do_mes_passado.year
    mes_passado = primeiro_dia_do_mes_passado.month

    faturamento_mes_passado = dados_pedidos.loc[(dados_pedidos['datapedido'].dt.month == mes_passado) & (
        dados_pedidos['datapedido'].dt.year == ano_mes_passado)]['totalliquido'].sum()

    faturamento_mes_atual = dados_pedidos.loc[(dados_pedidos['datapedido'].dt.month == mes_atual) & (
        dados_pedidos['datapedido'].dt.year == ano_atual)]['totalliquido'].sum()

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
