import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima

# Crie um DataFrame de exemplo com datas e valores de faturamento.
data = pd.DataFrame({
    'Data': pd.date_range(start='2023-01-01', periods=30, freq='D'),
    'Faturamento': np.random.randint(1000, 5000, size=30)
})

# Defina 'Data' como o índice.
data.set_index('Data', inplace=True)

# Escolha automaticamente os melhores hiperparâmetros do modelo ARIMA.
model = auto_arima(data['Faturamento'], seasonal=False, stepwise=True, suppress_warnings=True)

# Ajuste o modelo ARIMA com os hiperparâmetros selecionados.
order = model.get_params()['order']
arima_model = ARIMA(data['Faturamento'], order=order)
arima_fit = arima_model.fit()

# Faça previsões para um número específico de períodos no futuro.
num_periods = 7  # Número de períodos para prever no futuro.
forecast = arima_fit.forecast(steps=num_periods)

# Crie um DataFrame com datas futuras.
future_dates = pd.date_range(start=data.index[-1] + pd.DateOffset(1), periods=num_periods, freq='D')

# Crie um DataFrame com as previsões.
forecast_df = pd.DataFrame({
    'Data': future_dates,
    'Faturamento Previsto': forecast
})

# Defina 'Data' como o índice.
forecast_df.set_index('Data', inplace=True)

# Combine os dados de faturamento observados com as previsões.
combined_data = pd.concat([data, forecast_df])

# Plote o gráfico.
plt.figure(figsize=(12, 6))
plt.plot(combined_data.index, combined_data['Faturamento'], label='Faturamento Observado', marker='o')
plt.plot(forecast_df.index, forecast_df['Faturamento Previsto'], label='Faturamento Previsto', linestyle='--', marker='o')
plt.title('Previsão de Faturamento Futuro com ARIMA')
plt.xlabel('Data')
plt.ylabel('Faturamento')
plt.legend()
plt.grid(True)
plt.show()
