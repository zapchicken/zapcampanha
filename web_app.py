#!/usr/bin/env python3
"""
ZapCampanhas Web App
Frontend moderno para Business Intelligence da ZapChicken
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import base64
import io
import json
from pathlib import Path
from datetime import datetime, timedelta
import os
from flask import send_file

from src.zapchicken_processor import ZapChickenProcessor
from src.utils import setup_logging

# Configuração
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "ZapCampanhas - Business Intelligence"
logger = setup_logging()

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

# Configurações
INPUT_DIR = Path("data/input")
OUTPUT_DIR = Path("data/output")

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
        
        # Tab 2: Dashboard
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    html.H3("📈 Dashboard de Vendas", className="mb-4"),
                    
                    # Métricas principais
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4(id="metric-total-clientes", children="0"),
                                    html.P("Total de Clientes", className="text-muted")
                                ])
                            ], color="primary", outline=True)
                        ], width=3),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4(id="metric-clientes-inativos", children="0"),
                                    html.P("Clientes Inativos", className="text-muted")
                                ])
                            ], color="warning", outline=True)
                        ], width=3),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4(id="metric-alto-ticket", children="0"),
                                    html.P("Alto Ticket", className="text-muted")
                                ])
                            ], color="success", outline=True)
                        ], width=3),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4(id="metric-novos-clientes", children="0"),
                                    html.P("Novos Clientes", className="text-muted")
                                ])
                            ], color="info", outline=True)
                        ], width=3)
                    ], className="mb-4"),
                    
                    # Gráficos
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id="grafico-bairros")
                        ], width=6),
                        dbc.Col([
                            dcc.Graph(id="grafico-produtos")
                        ], width=6)
                    ], className="mb-4"),
                    
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id="grafico-evolucao")
                        ], width=12)
                    ])
                    
                ])
            ])
        ], label="📈 Dashboard"),
        
        # Tab 3: Relatórios
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
                     ], className="mb-4"),
                     
                     dbc.Row([
                         dbc.Col([
                             dbc.Card([
                                 dbc.CardBody([
                                     html.H5("🗺️ Análise Geográfica"),
                                     html.P("Dados por bairro para campanhas Meta"),
                                     dbc.Button("📥 Download Excel", id="btn-download-geo", color="info", className="w-100"),
                                     html.Div(id="status-download-geo", className="mt-2")
                                 ])
                             ])
                         ], width=6),
                         dbc.Col([
                             dbc.Card([
                                 dbc.CardBody([
                                     html.H5("🔥 Produtos Mais Vendidos"),
                                     html.P("Análise de preferências dos clientes"),
                                     dbc.Button("📥 Download Excel", id="btn-download-produtos", color="danger", className="w-100"),
                                     html.Div(id="status-download-produtos", className="mt-2")
                                 ])
                             ])
                         ], width=6)
                     ])
                    
                ])
            ])
        ], label="📄 Relatórios"),
        
        # Tab 4: IA Chat
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    html.H3("🤖 Assistente IA", className="mb-4"),
                    
                    # Chat container
                    html.Div(id="chat-container", style={
                        'height': '400px',
                        'border': '1px solid #ddd',
                        'borderRadius': '5px',
                        'padding': '10px',
                        'overflowY': 'auto',
                        'backgroundColor': '#f8f9fa'
                    }),
                    
                    # Input area
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(id="chat-input", placeholder="Digite sua pergunta...", type="text")
                        ], width=10),
                        dbc.Col([
                            dbc.Button("Enviar", id="btn-chat", color="primary")
                        ], width=2)
                    ], className="mt-3")
                    
                ])
            ])
        ], label="🤖 IA Chat")
    ])
], fluid=True)

# Callbacks combinados para upload e limpeza
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
    [Output("upload-clientes", "contents"),
     Output("status-clientes", "children")],
    [Input("upload-clientes", "contents"),
     Input("btn-clear-clientes", "n_clicks")],
    [State("upload-clientes", "filename")]
)
def handle_clientes(contents, clear_clicks, filename):
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update, ""
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == "btn-clear-clientes":
        return None, ""
    elif trigger_id == "upload-clientes" and contents is not None:
        return contents, dbc.Alert(f"✅ {filename} carregado com sucesso!", color="success", className="mb-0")
    
    return dash.no_update, ""

@app.callback(
    [Output("upload-pedidos", "contents"),
     Output("status-pedidos", "children")],
    [Input("upload-pedidos", "contents"),
     Input("btn-clear-pedidos", "n_clicks")],
    [State("upload-pedidos", "filename")]
)
def handle_pedidos(contents, clear_clicks, filename):
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update, ""
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == "btn-clear-pedidos":
        return None, ""
    elif trigger_id == "upload-pedidos" and contents is not None:
        return contents, dbc.Alert(f"✅ {filename} carregado com sucesso!", color="success", className="mb-0")
    
    return dash.no_update, ""

@app.callback(
    [Output("upload-itens", "contents"),
     Output("status-itens", "children")],
    [Input("upload-itens", "contents"),
     Input("btn-clear-itens", "n_clicks")],
    [State("upload-itens", "filename")]
)
def handle_itens(contents, clear_clicks, filename):
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update, ""
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == "btn-clear-itens":
        return None, ""
    elif trigger_id == "upload-itens" and contents is not None:
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

# Callback principal para processamento
@app.callback(
    [Output("status-processamento", "children"),
     Output("resultados-container", "children"),
     Output("status-processamento-geral", "children")],
    [Input("btn-processar", "n_clicks")],
    [State("upload-contacts", "contents"),
     State("upload-clientes", "contents"),
     State("upload-pedidos", "contents"),
     State("upload-itens", "contents"),
     State("dias-inatividade", "value"),
     State("ticket-minimo", "value")]
)
def processar_dados(n_clicks, contacts_content, clientes_content, pedidos_content, itens_content, dias_inatividade, ticket_minimo):
    if n_clicks is None:
        return "", "", ""
    
    try:
        # Status inicial de processamento
        status_processamento = dbc.Alert("🔄 Iniciando processamento...", color="info")
        
        # Salva arquivos temporários
        if contacts_content:
            save_uploaded_file(contacts_content, INPUT_DIR / "contacts.csv")
        if clientes_content:
            save_uploaded_file(clientes_content, INPUT_DIR / "Lista-Clientes.xlsx")
        if pedidos_content:
            save_uploaded_file(pedidos_content, INPUT_DIR / "Todos os pedidos.xlsx")
        if itens_content:
            save_uploaded_file(itens_content, INPUT_DIR / "Historico_Itens_Vendidos.xlsx")
        
        # Processa dados
        processor = ZapChickenProcessor(INPUT_DIR, OUTPUT_DIR)
        processor.config['dias_inatividade'] = dias_inatividade
        processor.config['ticket_medio_minimo'] = ticket_minimo
        
        # Carrega e processa
        processor.load_zapchicken_files()
        
        # Análises
        novos_clientes = processor.find_new_clients()
        inativos = processor.analyze_inactive_clients()
        alto_ticket = processor.analyze_ticket_medio()
        geo_data = processor.analyze_geographic_data()
        preferences = processor.analyze_preferences()
        
        # Salva relatórios
        saved_files = processor.save_reports()
        
        # Status de processamento final
        status_processamento_final = dbc.Alert([
            html.H4("✅ Processamento Concluído!", className="alert-heading"),
            html.P(f"• {len(novos_clientes)} novos clientes encontrados"),
            html.P(f"• {len(inativos)} clientes inativos"),
            html.P(f"• {len(alto_ticket)} clientes alto ticket"),
            html.P(f"• {len(saved_files)} relatórios gerados")
        ], color="success")
        
        # Status
        status = dbc.Alert([
            html.H4("✅ Processamento Concluído!", className="alert-heading"),
            html.P(f"• {len(novos_clientes)} novos clientes encontrados"),
            html.P(f"• {len(inativos)} clientes inativos"),
            html.P(f"• {len(alto_ticket)} clientes alto ticket"),
            html.P(f"• {len(saved_files)} relatórios gerados")
        ], color="success")
        
        # Resultados
        resultados = dbc.Card([
            dbc.CardBody([
                html.H5("📊 Resumo dos Dados"),
                dbc.Row([
                    dbc.Col([
                        html.H6("Novos Clientes"),
                        html.P(f"{len(novos_clientes)}", className="h3 text-primary")
                    ], width=3),
                    dbc.Col([
                        html.H6("Inativos"),
                        html.P(f"{len(inativos)}", className="h3 text-warning")
                    ], width=3),
                    dbc.Col([
                        html.H6("Alto Ticket"),
                        html.P(f"{len(alto_ticket)}", className="h3 text-success")
                    ], width=3),
                    dbc.Col([
                        html.H6("Bairros"),
                        html.P(f"{len(geo_data.get('bairros_analise', []))}", className="h3 text-info")
                    ], width=3)
                ])
            ])
        ])
        
        return status, resultados, status_processamento_final
        
    except Exception as e:
        return dbc.Alert(f"❌ Erro: {str(e)}", color="danger"), "", dbc.Alert(f"❌ Erro no processamento: {str(e)}", color="danger")

def save_uploaded_file(content, filepath):
    """Salva arquivo enviado"""
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    
    with open(filepath, 'wb') as f:
        f.write(decoded)

# Callbacks para downloads dos relatórios
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
            # Lê o arquivo e cria um link de download
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return html.Div([
                dbc.Alert("✅ Arquivo encontrado!", color="success", className="mb-2"),
                html.A(
                    "📥 Baixar CSV",
                    href=f"data:text/csv;charset=utf-8,{content}",
                    download="novos_clientes_google_contacts.csv",
                    className="btn btn-primary btn-sm"
                )
            ])
        else:
            return dbc.Alert("❌ Arquivo não encontrado. Processe os dados primeiro.", color="warning")
    except Exception as e:
        return dbc.Alert(f"❌ Erro: {str(e)}", color="danger")

@app.callback(
    Output("status-download-inativos", "children"),
    [Input("btn-download-inativos", "n_clicks")]
)
def download_inativos(n_clicks):
    if n_clicks is None:
        return ""
    
    try:
        file_path = OUTPUT_DIR / "clientes_inativos.xlsx"
        if file_path.exists():
            return html.Div([
                dbc.Alert("✅ Arquivo encontrado!", color="success", className="mb-2"),
                html.A(
                    "📥 Baixar Excel",
                    href=f"/download/{file_path.name}",
                    className="btn btn-warning btn-sm"
                )
            ])
        else:
            return dbc.Alert("❌ Arquivo não encontrado. Processe os dados primeiro.", color="warning")
    except Exception as e:
        return dbc.Alert(f"❌ Erro: {str(e)}", color="danger")

@app.callback(
    Output("status-download-alto-ticket", "children"),
    [Input("btn-download-alto-ticket", "n_clicks")]
)
def download_alto_ticket(n_clicks):
    if n_clicks is None:
        return ""
    
    try:
        file_path = OUTPUT_DIR / "clientes_alto_ticket.xlsx"
        if file_path.exists():
            return html.Div([
                dbc.Alert("✅ Arquivo encontrado!", color="success", className="mb-2"),
                html.A(
                    "📥 Baixar Excel",
                    href=f"/download/{file_path.name}",
                    className="btn btn-success btn-sm"
                )
            ])
        else:
            return dbc.Alert("❌ Arquivo não encontrado. Processe os dados primeiro.", color="warning")
    except Exception as e:
        return dbc.Alert(f"❌ Erro: {str(e)}", color="danger")

@app.callback(
    Output("status-download-geo", "children"),
    [Input("btn-download-geo", "n_clicks")]
)
def download_geo(n_clicks):
    if n_clicks is None:
        return ""
    
    try:
        file_path = OUTPUT_DIR / "analise_geografica.xlsx"
        if file_path.exists():
            return html.Div([
                dbc.Alert("✅ Arquivo encontrado!", color="success", className="mb-2"),
                html.A(
                    "📥 Baixar Excel",
                    href=f"/download/{file_path.name}",
                    className="btn btn-info btn-sm"
                )
            ])
        else:
            return dbc.Alert("❌ Arquivo não encontrado. Processe os dados primeiro.", color="warning")
    except Exception as e:
        return dbc.Alert(f"❌ Erro: {str(e)}", color="danger")

@app.callback(
    Output("status-download-produtos", "children"),
    [Input("btn-download-produtos", "n_clicks")]
)
def download_produtos(n_clicks):
    if n_clicks is None:
        return ""
    
    try:
        file_path = OUTPUT_DIR / "produtos_mais_vendidos.xlsx"
        if file_path.exists():
            return html.Div([
                dbc.Alert("✅ Arquivo encontrado!", color="success", className="mb-2"),
                html.A(
                    "📥 Baixar Excel",
                    href=f"/download/{file_path.name}",
                    className="btn btn-danger btn-sm"
                )
            ])
        else:
            return dbc.Alert("❌ Arquivo não encontrado. Processe os dados primeiro.", color="warning")
    except Exception as e:
        return dbc.Alert(f"❌ Erro: {str(e)}", color="danger")

@app.callback(
    Output("status-relatorios-geral", "children"),
    [Input("btn-download-novos", "n_clicks"),
     Input("btn-download-inativos", "n_clicks"),
     Input("btn-download-alto-ticket", "n_clicks"),
     Input("btn-download-geo", "n_clicks"),
     Input("btn-download-produtos", "n_clicks")]
)
def update_relatorios_status(n1, n2, n3, n4, n5):
    """Atualiza status geral dos relatórios"""
    try:
        relatorios = [
            ("novos_clientes_google_contacts.csv", "Novos Clientes"),
            ("clientes_inativos.xlsx", "Clientes Inativos"),
            ("clientes_alto_ticket.xlsx", "Alto Ticket"),
            ("analise_geografica.xlsx", "Análise Geográfica"),
            ("produtos_mais_vendidos.xlsx", "Produtos Mais Vendidos")
        ]
        
        disponiveis = []
        nao_encontrados = []
        
        for filename, nome in relatorios:
            file_path = OUTPUT_DIR / filename
            if file_path.exists():
                disponiveis.append(nome)
            else:
                nao_encontrados.append(nome)
        
        if disponiveis:
            status = dbc.Alert([
                html.H6("✅ Relatórios Disponíveis:", className="alert-heading"),
                html.Ul([html.Li(nome) for nome in disponiveis])
            ], color="success")
        else:
            status = dbc.Alert("❌ Nenhum relatório encontrado. Processe os dados primeiro.", color="warning")
        
        if nao_encontrados:
            status.children.append(html.Hr())
            status.children.append(html.H6("❌ Relatórios Não Encontrados:", className="alert-heading"))
            status.children.append(html.Ul([html.Li(nome) for nome in nao_encontrados]))
        
        return status
        
    except Exception as e:
        return dbc.Alert(f"❌ Erro ao verificar relatórios: {str(e)}", color="danger")

if __name__ == '__main__':
    # Cria diretórios se não existirem
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("🚀 Iniciando ZapCampanhas Web App...")
    print("📱 Acesse: http://localhost:8050")
    
    app.run(debug=True, host='0.0.0.0', port=8050)
