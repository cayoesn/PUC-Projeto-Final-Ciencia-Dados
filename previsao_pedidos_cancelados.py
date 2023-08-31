import pandas as pd
import locale
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def gerar_grafico_previsao_pedidos_cancelados(dados_pedidos):
    dados_pedidos_filtrado = dados_pedidos[[
        'datapedido', 'totalliquido']].loc[dados_pedidos['statuspedido'] == 'CANCELADO']

    dados_pedidos_agrupados = dados_pedidos_filtrado.groupby(pd.Grouper(
        key='datapedido', freq='M')).agg({'totalliquido': 'sum'}).reset_index()

    dados_pedidos_agrupados.set_index('datapedido', inplace=True)

    # Escolha automaticamente os melhores hiperparâmetros do modelo ARIMA.
    model = auto_arima(dados_pedidos_agrupados['totalliquido'],
                       seasonal=False, stepwise=True, suppress_warnings=True)

    # Ajuste o modelo ARIMA com os hiperparâmetros selecionados.
    order = model.get_params()['order']
    arima_model = ARIMA(dados_pedidos_filtrado['totalliquido'], order=order)
    arima_fit = arima_model.fit()

    # Faça previsões para um número específico de períodos no futuro.
    num_periods = 6  # Número de períodos para prever no futuro.
    forecast = arima_fit.forecast(steps=num_periods)

    # Crie um DataFrame com datas futuras.
    future_dates = pd.date_range(
        start=dados_pedidos_agrupados.index[-1] + pd.DateOffset(1), periods=num_periods, freq='M')

    # Crie um DataFrame com as previsões.
    forecast_df = pd.DataFrame({
        'datapedido_futura': future_dates,
        'totalliquido_futuro': forecast
    })

    # Defina 'Data' como o índice.
    forecast_df.set_index('datapedido_futura', inplace=True)

    # Combine os dados de faturamento observados com as previsões.
    combined_data = pd.concat([dados_pedidos_agrupados, forecast_df])

    combined_data_formated = [f'R$ {valor:,.2f}'.replace('.', 'X').replace(
        ',', '.').replace('X', ',') for valor in combined_data['totalliquido']]
    forecast_df_formated = [f'R$ {valor:,.2f}'.replace('.', 'X').replace(
        ',', '.').replace('X', ',') for valor in forecast_df['totalliquido_futuro']]

    fig = go.Figure()
    fig.update_layout(
        title="Total de faturamento - Previsão de pedidos cancelados")

    # Adicione a linha de faturamento atual
    fig.add_trace(go.Scatter(x=combined_data.index, y=combined_data['totalliquido'],
                             text=combined_data_formated,
                             textposition='top center',
                             mode='lines+markers+text',
                             name='Faturamento atual', line=dict(color='red')))

    # Adicione a linha de faturamento futuro
    fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['totalliquido_futuro'],
                             text=forecast_df_formated,
                             textposition='top center',
                             mode='lines+markers+text',
                             name='Faturamento futuro', line=dict(color='orange')))

    fig.update_xaxes(title_text='Meses')
    fig.update_yaxes(title_text='Total de faturamento')
    fig.update_layout(legend_title_text='Faturamento')
    fig.show()
