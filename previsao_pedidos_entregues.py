import pandas as pd
from datetime import datetime, timedelta
import locale
import plotly.graph_objects as go

from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

data_atual = datetime.now().date()
um_ano = timedelta(days=365)
data_anterior = data_atual - um_ano

dados_stocks = pd.read_csv("base_dados_pedidos_esp.csv",
                           encoding='utf-8', low_memory=False)

filtro_data = "'{}' <= datapedido <= '{}'".format(data_anterior, data_atual)

dados_stocks_filtrado = dados_stocks.query(filtro_data)

dados_stocks_filtrado = dados_stocks_filtrado[[
    'datapedido', 'totalliquido']].loc[dados_stocks_filtrado['statuspedido'] == 'ENTREGUE']

# Substituindo valores nulos no totalliquido pelo médio dos valores da coluna
dados_stocks_filtrado['totalliquido'].fillna(
    dados_stocks_filtrado['totalliquido'].mean())

# Substituindo valores 0 no totalliquido pelo médio dos valores da coluna
dados_stocks_filtrado.loc[dados_stocks_filtrado['totalliquido'] == 0,
                          'totalliquido'] = dados_stocks_filtrado['totalliquido'].mean()

# Transformando coluna datapedido em datetime para calculo de datas
dados_stocks_filtrado['datapedido'] = pd.to_datetime(
    dados_stocks_filtrado['datapedido'])

dados_stocks_agrupado = dados_stocks_filtrado.groupby(pd.Grouper(
    key='datapedido', freq='M')).agg({'totalliquido': 'sum'}).reset_index()

dados_stocks_agrupado.set_index('datapedido', inplace=True)

# Escolha automaticamente os melhores hiperparâmetros do modelo ARIMA.
model = auto_arima(dados_stocks_agrupado['totalliquido'],
                   seasonal=False, stepwise=True, suppress_warnings=True)

# Ajuste o modelo ARIMA com os hiperparâmetros selecionados.
order = model.get_params()['order']
arima_model = ARIMA(dados_stocks_agrupado['totalliquido'], order=order)
arima_fit = arima_model.fit()

# Faça previsões para um número específico de períodos no futuro.
num_periods = 6  # Número de períodos para prever no futuro.
forecast = arima_fit.forecast(steps=num_periods)

# Crie um DataFrame com datas futuras.
future_dates = pd.date_range(
    start=dados_stocks_agrupado.index[-1] + pd.DateOffset(1), periods=num_periods, freq='M')

# Crie um DataFrame com as previsões.
forecast_df = pd.DataFrame({
    'datapedido_futura': future_dates,
    'totalliquido_futuro': forecast
})

# Defina 'Data' como o índice.
forecast_df.set_index('datapedido_futura', inplace=True)

# Combine os dados de faturamento observados com as previsões.
combined_data = pd.concat([dados_stocks_agrupado, forecast_df])

combined_data_formated = [f'R$ {valor:,.2f}'.replace('.', 'X').replace(
    ',', '.').replace('X', ',') for valor in combined_data['totalliquido']]
forecast_df_formated = [f'R$ {valor:,.2f}'.replace('.', 'X').replace(
    ',', '.').replace('X', ',') for valor in forecast_df['totalliquido_futuro']]

fig = go.Figure()
fig.update_layout(title="Total de faturamento - Previsão de pedidos entregues")

# Adicione a linha de faturamento atual
fig.add_trace(go.Scatter(x=combined_data.index, y=combined_data['totalliquido'],
                         text=combined_data_formated,
                         textposition='top center',
                         mode='lines+markers+text',
                         name='Faturamento atual', line=dict(color='green')))

# Adicione a linha de faturamento futuro
fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['totalliquido_futuro'],
                         text=forecast_df_formated,
                         textposition='top center',
                         mode='lines+markers+text',
                         name='Faturamento futuro', line=dict(color='blue')))

fig.update_xaxes(title_text='Meses')
fig.update_yaxes(title_text='Total de faturamento')

fig.update_layout(yaxis_tickformat=",."  # Usa ponto como separador de milhares e vírgula como separador decimal
                  )
fig.update_layout(legend_title_text='Faturamento')

# format_brl = 'R$ %{y:,.2f}'

# fig.update_traces(mode='lines+markers+text', hovertemplate=format_brl,
#                   texttemplate=format_brl, textposition='top center')

fig.show()
