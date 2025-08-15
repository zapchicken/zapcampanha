#!/usr/bin/env python3
"""
ZapCampanhas API - Versão ultra-simples sem templates
Retorna HTML direto para evitar problemas no Vercel
"""

from flask import Flask, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'zapcampanhas_secret_key'

@app.route('/')
def index():
    """Página principal - HTML direto"""
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🍗 ZapCampanhas - Business Intelligence</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
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
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row py-4" style="background: linear-gradient(135deg, var(--zap-orange) 0%, var(--zap-orange-dark) 100%); color: white;">
                <div class="col-12 text-center">
                    <h1><i class="fas fa-chart-line"></i> ZapCampanhas</h1>
                    <p class="lead">Business Intelligence para Restaurantes</p>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="fas fa-upload"></i> Upload de Arquivos</h5>
                        </div>
                        <div class="card-body">
                            <form id="uploadForm" enctype="multipart/form-data">
                                <div class="mb-3">
                                    <label for="file" class="form-label">Selecione um arquivo CSV:</label>
                                    <input type="file" class="form-control" id="file" name="file" accept=".csv" required>
                                </div>
                                <button type="submit" class="btn btn-zap-primary">Processar Arquivo</button>
                            </form>
                            <div id="uploadResult" class="mt-3"></div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="fas fa-robot"></i> Chat com IA</h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <label for="question" class="form-label">Faça uma pergunta:</label>
                                <textarea class="form-control" id="question" rows="3" placeholder="Ex: Quais são os produtos mais vendidos?"></textarea>
                            </div>
                            <button onclick="sendQuestion()" class="btn btn-zap-primary">Enviar Pergunta</button>
                            <div id="chatResult" class="mt-3"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="fas fa-list"></i> Status da API</h5>
                        </div>
                        <div class="card-body">
                            <div id="apiStatus">Carregando...</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Verificar status da API
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('apiStatus').innerHTML = 
                        `<div class="alert alert-success">
                            <strong>✅ API Online!</strong><br>
                            Status: ${data.status}<br>
                            Versão: ${data.version}<br>
                            Mensagem: ${data.message}
                        </div>`;
                })
                .catch(error => {
                    document.getElementById('apiStatus').innerHTML = 
                        `<div class="alert alert-danger">
                            <strong>❌ Erro na API:</strong><br>
                            ${error.message}
                        </div>`;
                });

            // Upload de arquivo
            document.getElementById('uploadForm').addEventListener('submit', function(e) {
                e.preventDefault();
                
                const formData = new FormData();
                const fileInput = document.getElementById('file');
                formData.append('file', fileInput.files[0]);
                
                fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('uploadResult').innerHTML = 
                            `<div class="alert alert-success">
                                <strong>✅ Sucesso!</strong><br>
                                ${data.message}<br>
                                Arquivo: ${data.analysis.filename}<br>
                                Linhas: ${data.analysis.total_lines}<br>
                                Colunas: ${data.analysis.columns.join(', ')}
                            </div>`;
                    } else {
                        document.getElementById('uploadResult').innerHTML = 
                            `<div class="alert alert-danger">
                                <strong>❌ Erro:</strong><br>
                                ${data.error}
                            </div>`;
                    }
                })
                .catch(error => {
                    document.getElementById('uploadResult').innerHTML = 
                        `<div class="alert alert-danger">
                            <strong>❌ Erro:</strong><br>
                            ${error.message}
                        </div>`;
                });
            });

            // Chat
            function sendQuestion() {
                const question = document.getElementById('question').value;
                if (!question) {
                    alert('Digite uma pergunta!');
                    return;
                }
                
                fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({question: question})
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('chatResult').innerHTML = 
                        `<div class="alert alert-info">
                            <strong>🤖 Resposta:</strong><br>
                            ${data.response}
                        </div>`;
                })
                .catch(error => {
                    document.getElementById('chatResult').innerHTML = 
                        `<div class="alert alert-danger">
                            <strong>❌ Erro:</strong><br>
                            ${error.message}
                        </div>`;
                });
            }
        </script>
    </body>
    </html>
    """
    return html

@app.route('/api/status')
def status():
    """Endpoint de status"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'message': 'ZapCampanhas API funcionando!'
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload simplificado"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Verifica se é CSV
        if not file.filename.lower().endswith('.csv'):
            return jsonify({'error': 'Apenas arquivos CSV são aceitos'}), 400
        
        # Lê o conteúdo do arquivo
        content = file.read().decode('utf-8')
        lines = content.split('\n')
        
        # Análise básica
        total_lines = len(lines)
        if total_lines > 0:
            headers = lines[0].split(',')
            data_rows = total_lines - 1
        else:
            headers = []
            data_rows = 0
        
        return jsonify({
            'success': True,
            'message': f'Arquivo processado com sucesso!',
            'analysis': {
                'filename': file.filename,
                'total_lines': total_lines,
                'data_rows': data_rows,
                'columns': headers,
                'sample_data': lines[:5] if lines else []
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro no processamento: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint de chat simples"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        response = {
            'response': f'Pergunta recebida: "{question}". Funcionalidade de IA será implementada em breve.',
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test')
def test():
    """Endpoint de teste"""
    return jsonify({
        'message': 'API funcionando corretamente!',
        'timestamp': datetime.now().isoformat(),
        'endpoints': [
            '/api/status',
            '/api/upload',
            '/api/chat',
            '/api/test'
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
