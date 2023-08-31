import pandas as pd
import locale
import numpy as np
import plotly.graph_objects as go

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def gerar_grafico_pedidos_entregues_cancelados(dados_pedidos):
    dados_pedidos_agrupado = dados_pedidos.groupby([dados_pedidos['datapedido'].dt.to_period(
        'M'), 'statuspedido']).agg({'totalliquido': 'sum'}).reset_index()

    dados_datas_string = dados_pedidos_agrupado['datapedido'].astype(str)
    dados_pedidos_entregues = np.array([], dtype=np.float64)
    dados_pedidos_cancelados = np.array([], dtype=np.float64)

    for data in dados_pedidos_agrupado['datapedido']:
        dados_data = dados_pedidos_agrupado[dados_pedidos_agrupado['datapedido'] == data]
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

    dados_pedidos_agrupado = pd.DataFrame({
        'Mes': dados_datas_string.values,
        'Pedidos_Cancelados': dados_pedidos_cancelados,
        'Pedidos_Entregues': dados_pedidos_entregues,
        'Pedidos_Cancelados_Formatados': [f'R$ {valor:,.2f}'.replace('.', 'X').replace(
            ',', '.').replace('X', ',') for valor in dados_pedidos_cancelados],
        'Pedidos_Entregues_Formatados': [f'R$ {valor:,.2f}'.replace('.', 'X').replace(
            ',', '.').replace('X', ',') for valor in dados_pedidos_entregues],
    })

    fig = go.Figure()
    fig.update_layout(
        title="Faturamento Mensal - Comparação entre Pedidos Entregues e Cancelados")

    fig.add_trace(go.Scatter(x=dados_pedidos_agrupado['Mes'], y=dados_pedidos_agrupado['Pedidos_Entregues'],
                             text=dados_pedidos_agrupado['Pedidos_Entregues_Formatados'],
                             textposition='top center',
                             mode='lines+markers+text',
                             name='Pedidos entregues', line=dict(color='green')))

    fig.add_trace(go.Scatter(x=dados_pedidos_agrupado['Mes'], y=dados_pedidos_agrupado['Pedidos_Cancelados'],
                             text=dados_pedidos_agrupado['Pedidos_Cancelados_Formatados'],
                             textposition='top center',
                             mode='lines+markers+text',
                             name='Pedidos cancelados', line=dict(color='red')))

    fig.update_xaxes(title_text='Meses')
    fig.update_yaxes(title_text='Total de faturamento')
    fig.update_layout(legend_title_text='Faturamento')
    fig.show()
