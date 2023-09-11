import dash
from dash import html
from dash.dependencies import Input, Output
from dash import dcc
import warnings

import valor_faturamento
import grafico_pedidos_entregues_cancelados
import previsao_pedidos_entregues
import previsao_pedidos_cancelados

warnings.filterwarnings("ignore")


class DashboardPedidos:
    def __init__(self, data_inicial, data_final, dados_pedidos_filtrado):
        self.app = dash.Dash(__name__)
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.dados_pedidos_filtrado = dados_pedidos_filtrado

        self.app.layout = html.Div([
            html.H1("Empresa XPTO - Dashboard de pedidos entregues/cancelados - " + data_final.strftime("%d/%m/%Y"), style={
                "margin": "auto",
                "text-align": "center",
                "width": "50%",
                "padding": "20px",
            },),

            html.Div(dcc.Graph(id='graph-1', style={'height': '250px'})),
            html.Div(dcc.Graph(id='graph-2', style={'height': '650px'})),
            html.Div(dcc.Graph(id='graph-3', style={'height': '650px'})),
            html.Div(dcc.Graph(id='graph-4', style={'height': '650px'})),
        ])

        @self.app.callback(
            [Output('graph-1', 'figure'), Output('graph-2', 'figure'),
             Output('graph-3', 'figure'), Output('graph-4', 'figure')],
            Input('graph-1', 'relayoutData')
        )
        def update_charts(_):
            fig1 = valor_faturamento.gerar_valor_faturamento_comparacao_porcentagem(
                self.data_final, self.dados_pedidos_filtrado)
            fig2 = grafico_pedidos_entregues_cancelados.gerar_grafico_pedidos_entregues_cancelados(
                data_inicial, data_final, dados_pedidos_filtrado)
            fig3 = previsao_pedidos_entregues.gerar_grafico_previsao_pedidos_entregues(
                data_inicial, data_final, dados_pedidos_filtrado)
            fig4 = previsao_pedidos_cancelados.gerar_grafico_previsao_pedidos_cancelados(
                data_inicial, data_final, dados_pedidos_filtrado)
            return fig1, fig2, fig3, fig4

    def run(self):
        self.app.run_server(debug=True)
