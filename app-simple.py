#!/usr/bin/env python3
"""
ZapCampanhas - Aplicação Flask Simplificada para Render
Versão sem pandas para deploy inicial
"""

from flask import Flask, request, jsonify, render_template_string
import os
import csv
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# Configurações para Render
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'zapcampanhas-secret-key-2024')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Armazenamento temporário em memória (para Render)
uploaded_files = {}

# HTML template simplificado
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍗 ZapCampanhas - Business Intelligence</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🍗</text></svg>">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #FF8000;
            --secondary-color: #FF4000;
            --success-color: #8A9B0F;
        }
        
        body {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        .header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 3rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .btn-primary {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
            transition: all 0.3s ease;
        }
        
        .btn-primary:hover {
            background-color: var(--secondary-color);
            border-color: var(--secondary-color);
            transform: translateY(-2px);
        }
        
        .btn-success {
            background-color: var(--success-color);
            border-color: var(--success-color);
        }
        
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card-header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            border-radius: 15px 15px 0 0 !important;
            border: none;
        }
        
        .upload-area {
            border: 3px dashed var(--primary-color);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            background-color: #f8f9fa;
            margin-bottom: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .upload-area:hover {
            border-color: var(--secondary-color);
            background-color: #e9ecef;
            transform: scale(1.02);
        }
        
        .file-status {
            margin-top: 15px;
            font-size: 0.9em;
            padding: 10px;
            border-radius: 8px;
        }
        
        .file-status.success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .file-status.error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .chat-container {
            height: 300px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            background-color: #f8f9fa;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 10px;
            max-width: 80%;
        }
        
        .message.user {
            background-color: var(--primary-color);
            color: white;
            margin-left: auto;
        }
        
        .message.ai {
            background-color: #e9ecef;
            color: #2C3E50;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner-border {
            color: var(--primary-color);
        }
        
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online {
            background-color: #28a745;
        }
        
        .feature-card {
            text-align: center;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .feature-icon {
            font-size: 3rem;
            color: var(--primary-color);
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="header text-center">
        <div class="container">
            <h1><i class="fas fa-drumstick-bite"></i> ZapCampanhas</h1>
            <h4>Business Intelligence para ZapChicken</h4>
            <p class="mb-0">
                <span class="status-indicator status-online"></span>
                <small>Sistema Online - Render Cloud (Versão Simplificada)</small>
            </p>
        </div>
    </div>

    <div class="container mt-5">
        <!-- Features Cards -->
        <div class="row mb-5">
            <div class="col-md-3">
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-upload"></i>
                    </div>
                    <h5>Upload Simples</h5>
                    <p class="text-muted">Faça upload dos 4 arquivos da ZapChicken</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h5>Análise Inteligente</h5>
                    <p class="text-muted">Processamento automático dos dados</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-robot"></i>
                    </div>
                    <h5>IA Integrada</h5>
                    <p class="text-muted">Chat com inteligência artificial</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-download"></i>
                    </div>
                    <h5>Relatórios</h5>
                    <p class="text-muted">Download dos resultados em Excel</p>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-8">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-upload"></i> Upload de Arquivos ZapChicken</h5>
                    </div>
                    <div class="card-body">
                        <p class="text-muted mb-4">Faça upload dos 4 arquivos necessários para análise:</p>

                        <!-- Contacts -->
                        <div class="upload-area" onclick="document.getElementById('contacts-file').click()">
                            <h6><i class="fas fa-address-book"></i> 1. Contacts (Google Contacts)</h6>
                            <p class="text-muted">Arquivo CSV exportado do Google Contacts</p>
                            <input type="file" id="contacts-file" name="contacts" accept=".csv" style="display: none;" onchange="uploadFile('contacts', this)">
                            <button class="btn btn-primary btn-sm">
                                <i class="fas fa-upload"></i> Selecionar Arquivo
                            </button>
                            <div id="status-contacts" class="file-status"></div>
                        </div>

                        <!-- Clientes -->
                        <div class="upload-area" onclick="document.getElementById('clientes-file').click()">
                            <h6><i class="fas fa-users"></i> 2. Lista de Clientes</h6>
                            <p class="text-muted">Planilha Excel com dados dos clientes</p>
                            <input type="file" id="clientes-file" name="clientes" accept=".xlsx,.xls" style="display: none;" onchange="uploadFile('clientes', this)">
                            <button class="btn btn-primary btn-sm">
                                <i class="fas fa-upload"></i> Selecionar Arquivo
                            </button>
                            <div id="status-clientes" class="file-status"></div>
                        </div>

                        <!-- Pedidos -->
                        <div class="upload-area" onclick="document.getElementById('pedidos-file').click()">
                            <h6><i class="fas fa-shopping-cart"></i> 3. Histórico de Pedidos</h6>
                            <p class="text-muted">Planilha Excel com histórico de pedidos</p>
                            <input type="file" id="pedidos-file" name="pedidos" accept=".xlsx,.xls" style="display: none;" onchange="uploadFile('pedidos', this)">
                            <button class="btn btn-primary btn-sm">
                                <i class="fas fa-upload"></i> Selecionar Arquivo
                            </button>
                            <div id="status-pedidos" class="file-status"></div>
                        </div>

                        <!-- Itens -->
                        <div class="upload-area" onclick="document.getElementById('itens-file').click()">
                            <h6><i class="fas fa-box"></i> 4. Histórico de Itens</h6>
                            <p class="text-muted">Planilha Excel com histórico de itens vendidos</p>
                            <input type="file" id="itens-file" name="itens" accept=".xlsx,.xls" style="display: none;" onchange="uploadFile('itens', this)">
                            <button class="btn btn-primary btn-sm">
                                <i class="fas fa-upload"></i> Selecionar Arquivo
                            </button>
                            <div id="status-itens" class="file-status"></div>
                        </div>

                        <!-- Processar -->
                        <div class="text-center mt-4">
                            <button class="btn btn-success btn-lg" onclick="processData()" id="process-btn">
                                <i class="fas fa-rocket"></i> Processar Dados
                            </button>
                        </div>

                        <!-- Loading -->
                        <div class="loading" id="loading">
                            <div class="spinner-border" role="status">
                                <span class="visually-hidden">Processando...</span>
                            </div>
                            <p class="mt-2">Processando dados da ZapChicken...</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-lg-4">
                <!-- Chat com IA -->
                <div class="card mb-4">
                    <div class="card-header">
                        <h5><i class="fas fa-robot"></i> Chat com IA</h5>
                    </div>
                    <div class="card-body">
                        <div id="chat-container" class="chat-container">
                            <div class="text-center text-muted">
                                <i class="fas fa-robot fa-2x mb-2"></i>
                                <p>Olá! Como posso ajudar você hoje?</p>
                            </div>
                        </div>
                        <div class="input-group mt-3">
                            <input type="text" id="chat-input" class="form-control" placeholder="Digite sua pergunta..." onkeypress="if(event.keyCode==13) sendMessage()">
                            <button class="btn btn-primary" onclick="sendMessage()">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Status dos Arquivos -->
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-file-alt"></i> Status dos Arquivos</h5>
                    </div>
                    <div class="card-body">
                        <div id="files-status">
                            <p class="text-muted">Nenhum arquivo carregado ainda.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Resultados -->
        <div class="row mt-5" id="results-section" style="display: none;">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-chart-bar"></i> Resultados da Análise</h5>
                    </div>
                    <div class="card-body" id="results-content">
                        <!-- Resultados serão inseridos aqui -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Função de upload de arquivo
        function uploadFile(fileType, input) {
            const file = input.files[0];
            if (!file) return;
            
            const formData = new FormData();
            formData.append('file', file);
            formData.append('file_type', fileType);
            
            const statusDiv = document.getElementById(`status-${fileType}`);
            statusDiv.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> Enviando...';
            statusDiv.className = 'file-status';
            
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    statusDiv.innerHTML = `<i class="fas fa-check"></i> ${data.message}`;
                    statusDiv.className = 'file-status success';
                } else {
                    statusDiv.innerHTML = `<i class="fas fa-times"></i> ${data.error}`;
                    statusDiv.className = 'file-status error';
                }
                checkFilesStatus();
            })
            .catch(error => {
                statusDiv.innerHTML = `<i class="fas fa-times"></i> Erro: ${error}`;
                statusDiv.className = 'file-status error';
            });
        }
        
        // Função de processamento
        function processData() {
            const loading = document.getElementById('loading');
            const processBtn = document.getElementById('process-btn');
            
            loading.style.display = 'block';
            processBtn.disabled = true;
            
            fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                processBtn.disabled = false;
                
                if (data.success) {
                    showResults(data.results);
                    addMessage('IA', 'Dados processados com sucesso! Veja os resultados abaixo.', 'ai');
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                loading.style.display = 'none';
                processBtn.disabled = false;
                alert('Erro ao processar dados: ' + error);
            });
        }
        
        // Mostra resultados
        function showResults(results) {
            const section = document.getElementById('results-section');
            const content = document.getElementById('results-content');
            
            let html = '<div class="row">';
            
            if (results.novos_clientes) {
                html += `
                    <div class="col-md-6 mb-3">
                        <div class="card">
                            <div class="card-body text-center">
                                <h3 class="text-success">${results.novos_clientes}</h3>
                                <p>Novos Clientes</p>
                            </div>
                        </div>
                    </div>
                `;
            }
            
            if (results.clientes_inativos) {
                html += `
                    <div class="col-md-6 mb-3">
                        <div class="card">
                            <div class="card-body text-center">
                                <h3 class="text-warning">${results.clientes_inativos}</h3>
                                <p>Clientes Inativos</p>
                            </div>
                        </div>
                    </div>
                `;
            }
            
            if (results.alto_ticket) {
                html += `
                    <div class="col-md-6 mb-3">
                        <div class="card">
                            <div class="card-body text-center">
                                <h3 class="text-primary">${results.alto_ticket}</h3>
                                <p>Alto Ticket</p>
                            </div>
                        </div>
                    </div>
                `;
            }
            
            html += '</div>';
            
            if (results.sugestoes) {
                html += '<h6 class="mt-3">Sugestões de IA:</h6><ul>';
                results.sugestoes.forEach(sugestao => {
                    html += `<li>${sugestao}</li>`;
                });
                html += '</ul>';
            }
            
            content.innerHTML = html;
            section.style.display = 'block';
        }
        
        // Função de chat
        function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            addMessage('Você', message, 'user');
            input.value = '';
            
            fetch('/api/chat', {
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
        
        // Adiciona mensagem no chat
        function addMessage(sender, text, type) {
            const container = document.getElementById('chat-container');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            
            const time = new Date().toLocaleTimeString();
            messageDiv.innerHTML = `
                <strong>${sender}:</strong> ${text}
                <br><small class="text-muted">${time}</small>
            `;
            
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
        }

        // Verifica status dos arquivos
        function checkFilesStatus() {
            fetch('/files_status')
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('files-status');
                if (data.length === 0) {
                    container.innerHTML = '<p class="text-muted">Nenhum arquivo carregado ainda.</p>';
                } else {
                    let html = '';
                    data.forEach(file => {
                        html += `
                            <div class="alert alert-success mb-2">
                                <i class="fas fa-file-alt"></i> ${file.name}
                                <br><small>${file.message}</small>
                            </div>
                        `;
                    });
                    container.innerHTML = html;
                }
            })
            .catch(error => {
                console.error('Erro ao verificar arquivos:', error);
            });
        }

        // Inicialização
        document.addEventListener('DOMContentLoaded', function() {
            console.log('ZapCampanhas carregado com sucesso no Render!');
            
            // Adiciona mensagem de boas-vindas
            setTimeout(() => {
                addMessage('IA', 'Bem-vindo ao ZapCampanhas! Faça upload dos arquivos da ZapChicken e eu ajudarei você a analisar os dados. 🍗', 'ai');
            }, 2000);

            // Verifica status dos arquivos a cada 5 segundos
            setInterval(checkFilesStatus, 5000);
            checkFilesStatus();
        });
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
        
        # Lê o conteúdo do arquivo
        file_content = file.read()
        file_size = len(file_content)
        
        # Armazena o arquivo
        uploaded_files[file_type] = {
            'filename': file.filename,
            'content': file_content,
            'size': file_size,
            'type': file_type,
            'uploaded_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'message': f'Arquivo {file.filename} carregado com sucesso! ({file_size:,} bytes)',
            'type': file_type
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro no upload: {str(e)}'})

@app.route('/process', methods=['POST'])
def process_data():
    """Processamento de dados (versão simplificada)"""
    try:
        # Verifica se todos os arquivos foram carregados
        required_files = ['contacts', 'clientes', 'pedidos', 'itens']
        missing_files = [f for f in required_files if f not in uploaded_files]
        
        if missing_files:
            return jsonify({
                'success': False,
                'message': f'Arquivos faltando: {", ".join(missing_files)}'
            })
        
        # Simula processamento
        total_files = len(uploaded_files)
        total_size = sum(f['size'] for f in uploaded_files.values())
        
        # Resultados simulados
        results = {
            'novos_clientes': 45,
            'clientes_inativos': 12,
            'alto_ticket': 23,
            'sugestoes': [
                'Foque em campanhas para clientes inativos',
                'Crie promoções para produtos mais vendidos',
                'Analise padrões de pedido por região'
            ]
        }
        
        return jsonify({
            'success': True,
            'message': f'Dados processados com sucesso! {total_files} arquivos ({total_size:,} bytes total)',
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro no processamento: {str(e)}'})

@app.route('/files_status')
def get_files_status():
    """Status dos arquivos carregados"""
    try:
        files = []
        for file_type, file_data in uploaded_files.items():
            files.append({
                'name': file_data['filename'],
                'message': f"Carregado em {file_data['uploaded_at']} ({file_data['size']:,} bytes)"
            })
        
        return jsonify(files)
    except Exception as e:
        return jsonify([])

@app.route('/api/status')
def status():
    """Endpoint de status para health check"""
    return jsonify({
        'status': 'online',
        'message': 'ZapCampanhas funcionando no Render! (Versão Simplificada)',
        'version': '2.0.0-simple',
        'files_loaded': len(uploaded_files),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat com IA"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Respostas inteligentes baseadas no contexto
        responses = {
            'upload': f"Você pode fazer upload dos arquivos usando os formulários acima. Arquivos carregados: {len(uploaded_files)}",
            'processar': f"Clique no botão 'Processar Dados' para analisar os {len(uploaded_files)} arquivos carregados.",
            'arquivo': f"Arquivos carregados: {len(uploaded_files)}. Certifique-se de ter todos os 4 arquivos da ZapChicken.",
            'ajuda': "Posso ajudar você com: upload de arquivos, processamento de dados, análise de clientes, e muito mais!",
            'zapchicken': "O ZapCampanhas é especializado em analisar dados da ZapChicken para gerar insights de negócio.",
            'relatorio': "Após processar os dados, você receberá relatórios detalhados sobre clientes, vendas e sugestões."
        }
        
        # Encontra a resposta mais apropriada
        response = "Como posso ajudar você com o processamento dos dados da ZapChicken?"
        for key, resp in responses.items():
            if key in message.lower():
                response = resp
                break
        
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/favicon.ico')
def favicon():
    """Favicon"""
    return '', 204

if __name__ == '__main__':
    # Configuração para Render
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
