#!/usr/bin/env python3
"""
ZapCampanhas Web App - Versão Corrigida
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import base64
from pathlib import Path
from flask import send_file

# Configuração
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "ZapCampanhas - Business Intelligence"

# Configurações
INPUT_DIR = Path("data/input")
OUTPUT_DIR = Path("data/output")

# Rota para download de arquivos
@app.server.route('/download/<filename>')
def download_file(filename):
    """Rota para download de arquivos"""
    try:
        file_path = OUTPUT_DIR / filename
        if file_path.exists():
            return send_file(file_path, as_attachment=True)
        else:
            return "Arquivo não encontrado", 404
    except Exception as e:
        return f"Erro: {str(e)}", 500

# Layout principal
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🍗 ZapCampanhas", className="text-center text-primary mb-4"),
            html.H4("Business Intelligence para ZapChicken", className="text-center text-muted mb-5")
        ])
    ]),
    
    # Tabs principais
    dbc.Tabs([
        # Tab 1: Upload e Processamento
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    html.H3("📁 Upload de Arquivos", className="mb-4"),
                    html.P("Faça upload dos 4 arquivos da ZapChicken:"),
                    
                    # Upload areas
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("1. Contacts (Google Contacts)"),
                            dcc.Upload(
                                id='upload-contacts',
                                children=html.Div(['Arraste ou clique para selecionar']),
                                style={'borderStyle': 'dashed', 'padding': '20px', 'textAlign': 'center'},
                                multiple=False
                            ),
                            html.Div(id='status-contacts', className="mt-2"),
                            dbc.Button("🗑️ Limpar", id="btn-clear-contacts", color="danger", size="sm", className="mt-2")
                        ])
                    ], className="mb-3"),
                    
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("2. Lista de Clientes"),
                            dcc.Upload(
                                id='upload-clientes',
                                children=html.Div(['Arraste ou clique para selecionar']),
                                style={'borderStyle': 'dashed', 'padding': '20px', 'textAlign': 'center'},
                                multiple=False
                            ),
                            html.Div(id='status-clientes', className="mt-2"),
                            dbc.Button("🗑️ Limpar", id="btn-clear-clientes", color="danger", size="sm", className="mt-2")
                        ])
                    ], className="mb-3"),
                    
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("3. Histórico de Pedidos"),
                            dcc.Upload(
                                id='upload-pedidos',
                                children=html.Div(['Arraste ou clique para selecionar']),
                                style={'borderStyle': 'dashed', 'padding': '20px', 'textAlign': 'center'},
                                multiple=False
                            ),
                            html.Div(id='status-pedidos', className="mt-2"),
                            dbc.Button("🗑️ Limpar", id="btn-clear-pedidos", color="danger", size="sm", className="mt-2")
                        ])
                    ], className="mb-3"),
                    
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("4. Histórico de Itens"),
                            dcc.Upload(
                                id='upload-itens',
                                children=html.Div(['Arraste ou clique para selecionar']),
                                style={'borderStyle': 'dashed', 'padding': '20px', 'textAlign': 'center'},
                                multiple=False
                            ),
                            html.Div(id='status-itens', className="mt-2"),
                            dbc.Button("🗑️ Limpar", id="btn-clear-itens", color="danger", size="sm", className="mt-2")
                        ])
                    ], className="mb-3"),
                    
                    # Configurações
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("⚙️ Configurações"),
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Dias para considerar inativo:"),
                                    dcc.Slider(id='dias-inatividade', min=7, max=90, step=7, value=30, marks={7: '7', 30: '30', 60: '60', 90: '90'})
                                ]),
                                dbc.Col([
                                    html.Label("Ticket médio mínimo (R$):"),
                                    dcc.Slider(id='ticket-minimo', min=20, max=200, step=10, value=50, marks={20: '20', 50: '50', 100: '100', 200: '200'})
                                ])
                            ])
                        ])
                    ], className="mb-4"),
                    
                    # Status geral dos uploads
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("📊 Status dos Uploads", className="mb-3"),
                            html.Div(id="status-geral-uploads", children="Aguardando upload dos arquivos..."),
                            html.Hr(),
                            html.H6("⚙️ Status do Processamento", className="mb-3"),
                            html.Div(id="status-processamento-geral", children="Aguardando processamento...")
                        ])
                    ], className="mb-4"),
                    
                    # Botão processar
                    dbc.Button("🚀 Processar Dados", id="btn-processar", color="primary", size="lg", className="w-100 mb-4"),
                    
                    # Status
                    html.Div(id="status-processamento", className="mt-3")
                    
                ], width=6),
                
                dbc.Col([
                    html.H3("📊 Resultados", className="mb-4"),
                    html.Div(id="resultados-container")
                ], width=6)
            ])
        ], label="📁 Upload e Processamento"),
        
        # Tab 2: Relatórios
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    html.H3("📄 Relatórios", className="mb-4"),
                    
                    # Status geral dos relatórios
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("📊 Status dos Relatórios", className="mb-3"),
                            html.Div(id="status-relatorios-geral", children="Verificando relatórios disponíveis...")
                        ])
                    ], className="mb-4"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("📱 Novos Clientes"),
                                    html.P("Lista para importar no Google Contacts"),
                                    dbc.Button("📥 Download CSV", id="btn-download-novos", color="primary", className="w-100"),
                                    html.Div(id="status-download-novos", className="mt-2")
                                ])
                            ])
                        ], width=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("⚠️ Clientes Inativos"),
                                    html.P("Para campanhas de reativação"),
                                    dbc.Button("📥 Download Excel", id="btn-download-inativos", color="warning", className="w-100"),
                                    html.Div(id="status-download-inativos", className="mt-2")
                                ])
                            ])
                        ], width=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("💎 Alto Ticket"),
                                    html.P("Clientes premium para ofertas especiais"),
                                    dbc.Button("📥 Download Excel", id="btn-download-alto-ticket", color="success", className="w-100"),
                                    html.Div(id="status-download-alto-ticket", className="mt-2")
                                ])
                            ])
                        ], width=4)
                    ], className="mb-4")
                ])
            ])
        ], label="📄 Relatórios")
    ])
], fluid=True)

# Callbacks básicos
@app.callback(
    [Output("upload-contacts", "contents"),
     Output("status-contacts", "children")],
    [Input("upload-contacts", "contents"),
     Input("btn-clear-contacts", "n_clicks")],
    [State("upload-contacts", "filename")]
)
def handle_contacts(contents, clear_clicks, filename):
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update, ""
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == "btn-clear-contacts":
        return None, ""
    elif trigger_id == "upload-contacts" and contents is not None:
        return contents, dbc.Alert(f"✅ {filename} carregado com sucesso!", color="success", className="mb-0")
    
    return dash.no_update, ""

@app.callback(
    Output("status-geral-uploads", "children"),
    [Input("upload-contacts", "contents"),
     Input("upload-clientes", "contents"),
     Input("upload-pedidos", "contents"),
     Input("upload-itens", "contents")]
)
def update_geral_status(contacts, clientes, pedidos, itens):
    arquivos = [contacts, clientes, pedidos, itens]
    arquivos_carregados = sum(1 for a in arquivos if a is not None)
    
    if arquivos_carregados == 0:
        return dbc.Alert("⏳ Aguardando upload dos arquivos...", color="warning")
    elif arquivos_carregados < 4:
        return dbc.Alert(f"📁 {arquivos_carregados}/4 arquivos carregados", color="info")
    else:
        return dbc.Alert("✅ Todos os arquivos carregados! Pode processar.", color="success")

@app.callback(
    Output("status-download-novos", "children"),
    [Input("btn-download-novos", "n_clicks")]
)
def download_novos_clientes(n_clicks):
    if n_clicks is None:
        return ""
    
    try:
        file_path = OUTPUT_DIR / "novos_clientes_google_contacts.csv"
        if file_path.exists():
            return dbc.Alert("✅ Arquivo encontrado! Clique no link para baixar.", color="success")
        else:
            return dbc.Alert("❌ Arquivo não encontrado. Processe os dados primeiro.", color="warning")
    except Exception as e:
        return dbc.Alert(f"❌ Erro: {str(e)}", color="danger")

if __name__ == '__main__':
    # Cria diretórios se não existirem
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("🚀 Iniciando ZapCampanhas Web App (Corrigido)...")
    print("📱 Acesse: http://localhost:8050")
    
    app.run(debug=True, host='0.0.0.0', port=8050)
