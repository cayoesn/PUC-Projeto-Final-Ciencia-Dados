import pandas as pd
import plotly.express as px

# Exemplo de DataFrame com faturamento mensal de dois anos
data = {
    'Mes': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
    'Faturamento_2022': [1000, 1500, 2000, 1800, 2200, 2400, 2100, 1900, 1700, 2300, 2500, 2800],
    'Faturamento_2023': [1100, 1600, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800]
}

df = pd.DataFrame(data)

# Criar um gráfico interativo usando Plotly
fig = px.line(df, x='Mes', y=['Faturamento_2022', 'Faturamento_2023'],
              labels={'value': 'Faturamento'},
              title='Faturamento Mensal - Comparação 2022 vs. 2023')

# Adicionar tooltips
fig.update_traces(mode='lines+markers+text', hovertemplate='%{y:.2f}',
                  texttemplate='%{y:.2f}', textposition='top center')

# Exibir o gráfico
fig.show()