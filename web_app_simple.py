#!/usr/bin/env python3
"""
ZapCampanhas Web App - Versão Simplificada para Teste
"""

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from pathlib import Path

# Configuração
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "ZapCampanhas - Teste"

# Layout simples
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("🍗 ZapCampanhas", className="text-center text-primary mb-4"),
            html.H4("Teste da Interface", className="text-center text-muted mb-5")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Teste de Upload"),
                    dcc.Upload(
                        id='upload-test',
                        children=html.Div(['Arraste ou clique para selecionar']),
                        style={'borderStyle': 'dashed', 'padding': '20px', 'textAlign': 'center'},
                        multiple=False
                    ),
                    html.Div(id='status-test', className="mt-2")
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Teste de Botão"),
                    dbc.Button("Clique Aqui", id="btn-test", color="primary", className="w-100"),
                    html.Div(id="result-test", className="mt-2")
                ])
            ])
        ], width=6)
    ])
], fluid=True)

@app.callback(
    Output("status-test", "children"),
    [Input("upload-test", "contents")]
)
def handle_upload(contents):
    if contents is not None:
        return dbc.Alert("✅ Arquivo carregado!", color="success")
    return ""

@app.callback(
    Output("result-test", "children"),
    [Input("btn-test", "n_clicks")]
)
def handle_button(n_clicks):
    if n_clicks is not None:
        return dbc.Alert(f"✅ Botão clicado {n_clicks} vezes!", color="success")
    return ""

if __name__ == '__main__':
    print("🚀 Iniciando ZapCampanhas Web App (Teste)...")
    print("📱 Acesse: http://localhost:8050")
    
    app.run(debug=True, host='0.0.0.0', port=8050)
