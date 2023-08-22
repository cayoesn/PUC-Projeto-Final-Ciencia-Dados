import pandas as pd
import matplotlib.pyplot as plt

# Crie um DataFrame de exemplo com informações de faturamento e estados.
data = {
    'Estado': ['SP', 'RJ', 'MG', 'SP', 'RJ', 'MG', 'SP', 'RJ', 'MG'],
    'Faturamento': [5000, 3500, 4200, 6000, 4100, 4800, 5500, 3800, 4400]
}

df = pd.DataFrame(data)

faturamento_por_estado = df.groupby('Estado')['Faturamento'].sum().reset_index()

plt.figure(figsize=(10, 6))
plt.bar(faturamento_por_estado['Estado'], faturamento_por_estado['Faturamento'])
plt.xlabel('Estado')
plt.ylabel('Faturamento')
plt.title('Faturamento por Estado')
plt.show()
