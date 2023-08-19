import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Dados de exemplo
x = [1, 2, 3, 4, 5]
y1 = [1000, 1500, 2000, 2500, 3000]
y2 = [500, 800, 1200, 1500, 2000]

# Criação do DataFrame
df = pd.DataFrame({'X': x, 'Linha 1': y1, 'Linha 2': y2})

# Formate os números em Real Brasileiro (BRL)
def format_to_brl(value):
    return f'R$ {value:,.2f}'.replace(',', '.')

df['Linha 1'] = df['Linha 1'].apply(format_to_brl)
df['Linha 2'] = df['Linha 2'].apply(format_to_brl)

# Criação do gráfico de linha com hovertemplate e texttemplate personalizados
fig = go.Figure()

fig.add_trace(go.Scatter(x=df['X'], y=df['Linha 1'], name='Linha 1',
                         hovertemplate='%{y} no ponto %{x}<extra></extra>',
                         text=df['Linha 1'].values,
                         texttemplate='%{text}',
                         textposition='top center'))

fig.add_trace(go.Scatter(x=df['X'], y=df['Linha 2'], name='Linha 2',
                         hovertemplate='%{y} no ponto %{x}<extra></extra>',
                         text=df['Linha 2'].values,
                         texttemplate='%{text}',
                         textposition='top center'))

# Layout do gráfico
fig.update_layout(title='Gráfico de Linhas com Hovertemplate e Texttemplate em Real Brasileiro',
                  xaxis_title='Eixo X',
                  yaxis_title='Eixo Y')

# Exibe o gráfico
fig.show()