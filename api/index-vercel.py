#!/usr/bin/env python3
"""
ZapCampanhas - Versão Vercel
API simples e funcional para deploy no Vercel
"""

from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

# HTML template inline para evitar problemas de template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍗 ZapCampanhas - Business Intelligence</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --zap-orange: #FF8000;
            --zap-orange-dark: #FF4000;
            --zap-red: #FF0000;
            --zap-bordeaux: #800000;
            --zap-black: #000000;
            --zap-gray-dark: #333333;
            --zap-gray: #666666;
            --zap-gray-light: #CCCCCC;
            --zap-white: #FFFFFF;
            --zap-yellow: #F8CA00;
            --zap-green: #8A9B0F;
            --zap-purple: #490A3D;
        }
        
        .upload-area {
            border: 2px dashed var(--zap-orange);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #f8f9fa;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        
        .upload-area:hover {
            border-color: var(--zap-orange-dark);
            background-color: #e9ecef;
        }
        
        .btn-zap-primary {
            background-color: var(--zap-orange);
            border-color: var(--zap-orange);
            color: white;
        }
        
        .btn-zap-primary:hover {
            background-color: var(--zap-orange-dark);
            border-color: var(--zap-orange-dark);
            color: white;
        }
        
        .btn-zap-success {
            background-color: var(--zap-green);
            border-color: var(--zap-green);
            color: white;
        }
        
        .card-zap-header {
            background: linear-gradient(135deg, var(--zap-orange) 0%, var(--zap-orange-dark) 100%);
            color: white;
            padding: 15px;
            border-radius: 8px 8px 0 0;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <!-- Header -->
        <div class="row py-4" style="background: linear-gradient(135deg, var(--zap-orange) 0%, var(--zap-orange-dark) 100%); color: white;">
            <div class="col-12 text-center">
                <h1><i class="fas fa-drumstick-bite"></i> ZapCampanhas</h1>
                <h4>Business Intelligence para ZapChicken</h4>
                <p class="mb-0"><small>Versão Vercel - Deploy Online</small></p>
            </div>
        </div>

        <!-- Status -->
        <div id="status" class="alert alert-info alert-dismissible fade show" role="alert">
            <i class="fas fa-info-circle"></i> Sistema funcionando no Vercel!
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>

        <!-- Conteúdo Principal -->
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header card-zap-header">
                        <h5><i class="fas fa-upload"></i> Upload de Arquivos</h5>
                    </div>
                    <div class="card-body">
                        <p class="text-muted">Faça upload dos arquivos da ZapChicken:</p>

                        <!-- Contacts -->
                        <div class="upload-area">
                            <h6><i class="fas fa-address-book"></i> 1. Contacts (Google Contacts)</h6>
                            <form action="/upload" method="post" enctype="multipart/form-data">
                                <input type="hidden" name="file_type" value="contacts">
                                <input type="file" name="file" accept=".csv,.xlsx,.xls" class="form-control mb-2" required>
                                <button type="submit" class="btn btn-zap-primary btn-sm">
                                    <i class="fas fa-upload"></i> Enviar
                                </button>
                            </form>
                        </div>

                        <!-- Clientes -->
                        <div class="upload-area">
                            <h6><i class="fas fa-users"></i> 2. Lista de Clientes</h6>
                            <form action="/upload" method="post" enctype="multipart/form-data">
                                <input type="hidden" name="file_type" value="clientes">
                                <input type="file" name="file" accept=".xlsx,.xls" class="form-control mb-2" required>
                                <button type="submit" class="btn btn-zap-primary btn-sm">
                                    <i class="fas fa-upload"></i> Enviar
                                </button>
                            </form>
                        </div>

                        <!-- Pedidos -->
                        <div class="upload-area">
                            <h6><i class="fas fa-shopping-cart"></i> 3. Histórico de Pedidos</h6>
                            <form action="/upload" method="post" enctype="multipart/form-data">
                                <input type="hidden" name="file_type" value="pedidos">
                                <input type="file" name="file" accept=".xlsx,.xls" class="form-control mb-2" required>
                                <button type="submit" class="btn btn-zap-primary btn-sm">
                                    <i class="fas fa-upload"></i> Enviar
                                </button>
                            </form>
                        </div>

                        <!-- Itens -->
                        <div class="upload-area">
                            <h6><i class="fas fa-box"></i> 4. Histórico de Itens</h6>
                            <form action="/upload" method="post" enctype="multipart/form-data">
                                <input type="hidden" name="file_type" value="itens">
                                <input type="file" name="file" accept=".xlsx,.xls" class="form-control mb-2" required>
                                <button type="submit" class="btn btn-zap-primary btn-sm">
                                    <i class="fas fa-upload"></i> Enviar
                                </button>
                            </form>
                        </div>

                        <!-- Processar -->
                        <div class="text-center mt-4">
                            <button class="btn btn-zap-success btn-lg" onclick="processData()">
                                <i class="fas fa-rocket"></i> Processar Dados
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card">
                    <div class="card-header card-zap-header">
                        <h5><i class="fas fa-file-alt"></i> Status e Relatórios</h5>
                    </div>
                    <div class="card-body">
                        <div id="reports-container">
                            <p class="text-muted">Processe os dados para gerar relatórios...</p>
                        </div>
                    </div>
                </div>

                <!-- Chat IA -->
                <div class="card mt-3">
                    <div class="card-header bg-info text-white">
                        <h5><i class="fas fa-robot"></i> Chat com IA</h5>
                    </div>
                    <div class="card-body">
                        <div id="chat-container" style="height: 200px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; background-color: #f8f9fa;">
                            <div class="text-center text-muted">
                                <i class="fas fa-robot fa-2x mb-2"></i>
                                <p>Olá! Como posso ajudar você hoje?</p>
                            </div>
                        </div>
                        <div class="input-group">
                            <input type="text" id="chat-input" class="form-control" placeholder="Digite sua pergunta..." onkeypress="if(event.keyCode==13) sendMessage()">
                            <button class="btn btn-zap-primary" onclick="sendMessage()">
                                <i class="fas fa-paper-plane"></i> Enviar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function processData() {
            fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.success) {
                    checkReports();
                }
            })
            .catch(error => {
                alert('Erro ao processar dados: ' + error);
            });
        }

        function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            addMessage('Você', message, 'user');
            input.value = '';
            
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                addMessage('IA', data.response, 'ai');
            })
            .catch(error => {
                addMessage('IA', 'Erro de conexão: ' + error, 'ai');
            });
        }
        
        function addMessage(sender, text, type) {
            const container = document.getElementById('chat-container');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'mb-2';
            
            const time = new Date().toLocaleTimeString();
            
            if (type === 'user') {
                messageDiv.innerHTML = `
                    <div class="d-flex justify-content-end">
                        <div class="bg-primary text-white p-2 rounded" style="max-width: 70%;">
                            <strong>${sender}:</strong> ${text}
                            <br><small class="text-light">${time}</small>
                        </div>
                    </div>
                `;
            } else {
                messageDiv.innerHTML = `
                    <div class="d-flex justify-content-start">
                        <div class="bg-light p-2 rounded" style="max-width: 70%;">
                            <strong>${sender}:</strong> ${text}
                            <br><small class="text-muted">${time}</small>
                        </div>
                    </div>
                `;
            }
            
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
        }

        function checkReports() {
            fetch('/reports')
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('reports-container');
                if (data.length === 0) {
                    container.innerHTML = '<p class="text-muted">Nenhum relatório disponível.</p>';
                } else {
                    let html = '<div class="row">';
                    data.forEach(report => {
                        html += `
                            <div class="col-12 mb-2">
                                <div class="alert alert-success">
                                    <i class="fas fa-file-alt"></i> ${report.name}
                                    <br><small>${report.message}</small>
                                </div>
                            </div>
                        `;
                    });
                    html += '</div>';
                    container.innerHTML = html;
                }
            })
            .catch(error => {
                console.error('Erro ao verificar relatórios:', error);
            });
        }

        // Verifica relatórios a cada 10 segundos
        setInterval(checkReports, 10000);
        checkReports(); // Verifica imediatamente
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Página principal"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload de arquivos"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo selecionado'})
        
        file = request.files['file']
        file_type = request.form.get('file_type')
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'})
        
        # Simula processamento do arquivo
        filename = file.filename
        file_size = len(file.read())
        file.seek(0)  # Volta para o início
        
        return jsonify({
            'success': True,
            'message': f'Arquivo {filename} carregado com sucesso! ({file_size} bytes)',
            'type': file_type
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro no upload: {str(e)}'})

@app.route('/process', methods=['POST'])
def process_data():
    """Processamento de dados"""
    try:
        # Simula processamento
        return jsonify({
            'success': True,
            'message': 'Dados processados com sucesso! Relatórios gerados.'
        })
    except Exception as e:
        return jsonify({'error': f'Erro no processamento: {str(e)}'})

@app.route('/chat', methods=['POST'])
def chat_message():
    """Chat com IA"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Resposta simples da IA
        response = f"Olá! Você disse: '{message}'. Esta é uma resposta simulada da IA no Vercel."
        
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': f'Erro no chat: {str(e)}'})

@app.route('/reports')
def get_reports():
    """Lista relatórios disponíveis"""
    try:
        # Simula relatórios
        reports = [
            {
                'name': 'Relatório de Clientes',
                'message': 'Análise completa dos clientes'
            },
            {
                'name': 'Relatório de Vendas',
                'message': 'Dados de vendas e pedidos'
            }
        ]
        
        return jsonify(reports)
    except Exception as e:
        return jsonify([])

@app.route('/status')
def status():
    """Status da API"""
    return jsonify({
        'status': 'online',
        'message': 'ZapCampanhas funcionando no Vercel!',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True)
