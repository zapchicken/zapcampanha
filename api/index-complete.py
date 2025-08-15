#!/usr/bin/env python3
"""
ZapCampanhas API - Versão completa com sistema de arquivos
Suporte a CSV, Excel e processamento de dados
"""

from flask import Flask, request, jsonify, send_file
import json
import csv
import os
import tempfile
from datetime import datetime
from pathlib import Path
import io
import base64
import chardet

app = Flask(__name__)
app.secret_key = 'zapcampanhas_secret_key'

# Configurações
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Armazenamento temporário (em memória para Vercel)
file_storage = {}
reports_storage = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_encoding(content):
    """Detecta a codificação do arquivo"""
    try:
        # Tenta detectar a codificação
        result = chardet.detect(content)
        encoding = result['encoding']
        confidence = result['confidence']
        
        # Se a confiança for baixa, tenta codificações comuns
        if confidence < 0.7:
            for enc in ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']:
                try:
                    content.decode(enc)
                    return enc
                except:
                    continue
        
        return encoding or 'utf-8'
    except:
        return 'utf-8'

def process_csv_data(content_bytes):
    """Processa dados CSV com detecção automática de codificação"""
    try:
        # Detecta a codificação
        encoding = detect_encoding(content_bytes)
        
        # Decodifica o conteúdo
        try:
            content = content_bytes.decode(encoding)
        except UnicodeDecodeError:
            # Se falhar, tenta outras codificações
            for enc in ['latin1', 'cp1252', 'iso-8859-1']:
                try:
                    content = content_bytes.decode(enc)
                    break
                except:
                    continue
            else:
                return {"error": "Não foi possível decodificar o arquivo. Verifique a codificação."}
        
        lines = content.split('\n')
        if not lines or not lines[0].strip():
            return {"error": "Arquivo CSV vazio ou inválido"}
        
        # Lê o CSV
        reader = csv.DictReader(io.StringIO(content))
        data = list(reader)
        
        if not data:
            return {"error": "Nenhum dado encontrado no CSV"}
        
        # Análise dos dados
        total_rows = len(data)
        columns = list(data[0].keys())
        
        # Estatísticas básicas
        analysis = {
            "total_rows": total_rows,
            "columns": columns,
            "column_count": len(columns),
            "sample_data": data[:5],
            "file_type": "CSV",
            "encoding": encoding
        }
        
        # Análise por coluna
        column_analysis = {}
        for col in columns:
            values = [row.get(col, '') for row in data if row.get(col, '')]
            unique_values = len(set(values))
            column_analysis[col] = {
                "total_values": len(values),
                "unique_values": unique_values,
                "empty_values": total_rows - len(values),
                "sample_values": list(set(values))[:5]
            }
        
        analysis["column_analysis"] = column_analysis
        
        return analysis
        
    except Exception as e:
        return {"error": f"Erro ao processar CSV: {str(e)}"}

def process_excel_data(content_bytes, filename):
    """Processa dados Excel"""
    try:
        # Por enquanto, simula processamento de Excel
        # Em uma versão futura, implementaremos com openpyxl ou xlrd
        
        # Detecta a codificação (para arquivos Excel em texto)
        encoding = detect_encoding(content_bytes)
        
        # Tenta decodificar como texto (para alguns formatos Excel)
        try:
            content = content_bytes.decode(encoding)
            lines = content.split('\n')
            
            # Se parece com CSV, processa como CSV
            if len(lines) > 1 and ',' in lines[0]:
                return process_csv_data(content_bytes)
        except:
            pass
        
        # Para arquivos Excel binários, retorna informação básica
        return {
            "total_rows": 0,
            "columns": [],
            "column_count": 0,
            "sample_data": [],
            "file_type": "Excel",
            "encoding": "binary",
            "message": "Arquivo Excel detectado. Processamento completo será implementado em breve."
        }
        
    except Exception as e:
        return {
            "error": f"Erro ao processar Excel: {str(e)}",
            "filename": filename,
            "file_type": "Excel"
        }

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
            .upload-area {
                border: 2px dashed var(--zap-orange);
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                background-color: #f8f9fa;
                transition: all 0.3s ease;
            }
            .upload-area:hover {
                border-color: var(--zap-orange-dark);
                background-color: #e9ecef;
            }
            .file-list {
                max-height: 300px;
                overflow-y: auto;
            }
            .file-item {
                border: 1px solid #dee2e6;
                border-radius: 5px;
                margin-bottom: 10px;
                padding: 10px;
            }
            .file-item:hover {
                background-color: #f8f9fa;
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
                            <div class="upload-area" id="uploadArea">
                                <i class="fas fa-cloud-upload-alt fa-3x text-muted mb-3"></i>
                                <h5>Arraste arquivos aqui ou clique para selecionar</h5>
                                <p class="text-muted">Suporte: CSV, Excel (xlsx, xls) - Múltiplos arquivos</p>
                                <input type="file" id="fileInput" accept=".csv,.xlsx,.xls" multiple style="display: none;">
                                <button class="btn btn-zap-primary" onclick="document.getElementById('fileInput').click()">
                                    Selecionar Arquivos
                                </button>
                            </div>
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
                                <label for="question" class="form-label">Faça uma pergunta sobre seus dados:</label>
                                <textarea class="form-control" id="question" rows="3" placeholder="Ex: Quais são os produtos mais vendidos?"></textarea>
                            </div>
                            <button onclick="sendQuestion()" class="btn btn-zap-primary">Enviar Pergunta</button>
                            <div id="chatResult" class="mt-3"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5><i class="fas fa-folder"></i> Arquivos Carregados</h5>
                            <button class="btn btn-sm btn-outline-danger" onclick="clearAllFiles()">
                                <i class="fas fa-trash"></i> Limpar Todos
                            </button>
                        </div>
                        <div class="card-body">
                            <div id="fileList" class="file-list">
                                <p class="text-muted">Nenhum arquivo carregado ainda.</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="fas fa-chart-bar"></i> Relatórios Gerados</h5>
                        </div>
                        <div class="card-body">
                            <button onclick="generateReport()" class="btn btn-zap-primary mb-3">
                                <i class="fas fa-plus"></i> Gerar Relatório
                            </button>
                            <div id="reportList" class="file-list">
                                <p class="text-muted">Nenhum relatório gerado ainda.</p>
                            </div>
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
            document.getElementById('fileInput').addEventListener('change', function(e) {
                const files = e.target.files;
                if (files.length > 0) {
                    uploadFiles(files);
                }
            });

            // Drag and drop
            const uploadArea = document.getElementById('uploadArea');
            
            uploadArea.addEventListener('dragover', function(e) {
                e.preventDefault();
                uploadArea.style.borderColor = 'var(--zap-orange-dark)';
                uploadArea.style.backgroundColor = '#e9ecef';
            });
            
            uploadArea.addEventListener('dragleave', function(e) {
                e.preventDefault();
                uploadArea.style.borderColor = 'var(--zap-orange)';
                uploadArea.style.backgroundColor = '#f8f9fa';
            });
            
            uploadArea.addEventListener('drop', function(e) {
                e.preventDefault();
                uploadArea.style.borderColor = 'var(--zap-orange)';
                uploadArea.style.backgroundColor = '#f8f9fa';
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    uploadFiles(files);
                }
            });

            function uploadFiles(files) {
                const totalFiles = files.length;
                let uploadedCount = 0;
                let successCount = 0;
                let errorCount = 0;
                
                document.getElementById('uploadResult').innerHTML = 
                    `<div class="alert alert-info">
                        <strong>📤 Enviando ${totalFiles} arquivo(s)...</strong><br>
                        <div id="uploadProgress">0/${totalFiles} concluído</div>
                    </div>`;
                
                Array.from(files).forEach((file, index) => {
                    const formData = new FormData();
                    formData.append('file', file);
                    
                    fetch('/api/upload', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        uploadedCount++;
                        
                        if (data.success) {
                            successCount++;
                        } else {
                            errorCount++;
                        }
                        
                        // Atualiza progresso
                        document.getElementById('uploadProgress').innerHTML = 
                            `${uploadedCount}/${totalFiles} concluído (${successCount} sucesso, ${errorCount} erro)`;
                        
                        // Se todos os arquivos foram processados
                        if (uploadedCount === totalFiles) {
                            if (errorCount === 0) {
                                document.getElementById('uploadResult').innerHTML = 
                                    `<div class="alert alert-success">
                                        <strong>✅ Todos os ${totalFiles} arquivo(s) processados com sucesso!</strong>
                                    </div>`;
                            } else if (successCount === 0) {
                                document.getElementById('uploadResult').innerHTML = 
                                    `<div class="alert alert-danger">
                                        <strong>❌ Erro ao processar todos os arquivos</strong>
                                    </div>`;
                            } else {
                                document.getElementById('uploadResult').innerHTML = 
                                    `<div class="alert alert-warning">
                                        <strong>⚠️ Processamento parcial:</strong><br>
                                        ${successCount} sucesso(s), ${errorCount} erro(s)
                                    </div>`;
                            }
                            
                            // Atualizar lista de arquivos
                            loadFileList();
                        }
                    })
                    .catch(error => {
                        uploadedCount++;
                        errorCount++;
                        
                        document.getElementById('uploadProgress').innerHTML = 
                            `${uploadedCount}/${totalFiles} concluído (${successCount} sucesso, ${errorCount} erro)`;
                        
                        if (uploadedCount === totalFiles) {
                            document.getElementById('uploadResult').innerHTML = 
                                `<div class="alert alert-danger">
                                    <strong>❌ Erro no upload:</strong><br>
                                    ${error.message}
                                </div>`;
                        }
                    });
                });
            }

            // Carregar lista de arquivos
            function loadFileList() {
                fetch('/api/files')
                    .then(response => response.json())
                    .then(data => {
                        if (data.files && data.files.length > 0) {
                            let html = '<div class="list-group">';
                            data.files.forEach(file => {
                                html += `
                                    <div class="list-group-item d-flex justify-content-between align-items-center">
                                        <div>
                                            <strong>${file.name}</strong><br>
                                            <small class="text-muted">
                                                ${file.size} bytes • ${file.uploaded}
                                            </small>
                                        </div>
                                        <div>
                                            <button class="btn btn-sm btn-outline-primary" onclick="viewFile('${file.id}')">
                                                <i class="fas fa-eye"></i>
                                            </button>
                                            <button class="btn btn-sm btn-outline-danger" onclick="deleteFile('${file.id}')">
                                                <i class="fas fa-trash"></i>
                                            </button>
                                        </div>
                                    </div>
                                `;
                            });
                            html += '</div>';
                            document.getElementById('fileList').innerHTML = html;
                        } else {
                            document.getElementById('fileList').innerHTML = 
                                '<p class="text-muted">Nenhum arquivo carregado ainda.</p>';
                        }
                    })
                    .catch(error => {
                        document.getElementById('fileList').innerHTML = 
                            `<div class="alert alert-danger">Erro ao carregar arquivos: ${error.message}</div>`;
                    });
            }

            // Visualizar arquivo
            function viewFile(fileId) {
                fetch(`/api/files/${fileId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.file) {
                            const file = data.file;
                            const analysis = file.analysis;
                            
                            let html = `
                                <div class="modal fade" id="fileModal" tabindex="-1">
                                    <div class="modal-dialog modal-lg">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title">${file.name}</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                            </div>
                                            <div class="modal-body">
                                                <h6>Informações do Arquivo:</h6>
                                                <ul>
                                                    <li><strong>Tamanho:</strong> ${file.size} bytes</li>
                                                    <li><strong>Linhas:</strong> ${analysis.total_rows}</li>
                                                    <li><strong>Colunas:</strong> ${analysis.column_count}</li>
                                                    <li><strong>Tipo:</strong> ${analysis.file_type}</li>
                                                    ${analysis.encoding ? `<li><strong>Codificação:</strong> ${analysis.encoding}</li>` : ''}
                                                </ul>
                                                
                                                <h6>Colunas:</h6>
                                                <ul>
                                                    ${analysis.columns.map(col => `<li>${col}</li>`).join('')}
                                                </ul>
                                                
                                                <h6>Amostra de Dados:</h6>
                                                <div class="table-responsive">
                                                    <table class="table table-sm">
                                                        <thead>
                                                            <tr>
                                                                ${analysis.columns.map(col => `<th>${col}</th>`).join('')}
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            ${analysis.sample_data.map(row => 
                                                                `<tr>${analysis.columns.map(col => `<td>${row[col] || ''}</td>`).join('')}</tr>`
                                                            ).join('')}
                                                        </tbody>
                                                    </table>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `;
                            
                            // Remove modal anterior se existir
                            const existingModal = document.getElementById('fileModal');
                            if (existingModal) {
                                existingModal.remove();
                            }
                            
                            // Adiciona novo modal
                            document.body.insertAdjacentHTML('beforeend', html);
                            
                            // Mostra modal
                            const modal = new bootstrap.Modal(document.getElementById('fileModal'));
                            modal.show();
                        }
                    })
                    .catch(error => {
                        alert(`Erro ao carregar arquivo: ${error.message}`);
                    });
            }

            // Deletar arquivo
            function deleteFile(fileId) {
                if (confirm('Tem certeza que deseja excluir este arquivo?')) {
                    fetch(`/api/files/${fileId}/delete`, {
                        method: 'DELETE'
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            loadFileList();
                        } else {
                            alert(`Erro ao excluir: ${data.error}`);
                        }
                    })
                    .catch(error => {
                        alert(`Erro ao excluir arquivo: ${error.message}`);
                    });
                }
            }

            // Limpar todos os arquivos
            function clearAllFiles() {
                if (confirm('Tem certeza que deseja excluir todos os arquivos?')) {
                    fetch('/api/files/clear', {
                        method: 'DELETE'
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            loadFileList();
                        } else {
                            alert(`Erro ao limpar: ${data.error}`);
                        }
                    })
                    .catch(error => {
                        alert(`Erro ao limpar arquivos: ${error.message}`);
                    });
                }
            }

            // Gerar relatório
            function generateReport() {
                fetch('/api/reports/generate', {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Relatório gerado com sucesso!');
                        loadReportList();
                    } else {
                        alert(`Erro ao gerar relatório: ${data.error}`);
                    }
                })
                .catch(error => {
                    alert(`Erro ao gerar relatório: ${error.message}`);
                });
            }

            // Carregar lista de relatórios
            function loadReportList() {
                fetch('/api/reports')
                    .then(response => response.json())
                    .then(data => {
                        if (data.reports && data.reports.length > 0) {
                            let html = '<div class="list-group">';
                            data.reports.forEach(report => {
                                html += `
                                    <div class="list-group-item">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <div>
                                                <strong>Relatório ${report.id}</strong><br>
                                                <small class="text-muted">
                                                    Gerado em: ${report.generated}<br>
                                                    Arquivos: ${report.summary.total_files} • 
                                                    Linhas: ${report.summary.total_rows}
                                                </small>
                                            </div>
                                            <button class="btn btn-sm btn-outline-primary" onclick="viewReport('${report.id}')">
                                                <i class="fas fa-eye"></i>
                                            </button>
                                        </div>
                                    </div>
                                `;
                            });
                            html += '</div>';
                            document.getElementById('reportList').innerHTML = html;
                        } else {
                            document.getElementById('reportList').innerHTML = 
                                '<p class="text-muted">Nenhum relatório gerado ainda.</p>';
                        }
                    })
                    .catch(error => {
                        document.getElementById('reportList').innerHTML = 
                            `<div class="alert alert-danger">Erro ao carregar relatórios: ${error.message}</div>`;
                    });
            }

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

            // Carregar dados iniciais
            loadFileList();
            loadReportList();
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
        'version': '2.0.0',
        'message': 'ZapCampanhas API com sistema de arquivos completo!',
        'features': [
            'Upload múltiplo de CSV e Excel',
            'Detecção automática de codificação',
            'Processamento de dados',
            'Chat com IA',
            'Geração de relatórios'
        ]
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload de arquivos"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Verifica extensão
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de arquivo não permitido. Use CSV, XLSX ou XLS.'}), 400
        
        # Verifica tamanho
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': f'Arquivo muito grande. Máximo: {MAX_FILE_SIZE // (1024*1024)}MB'}), 400
        
        # Lê o conteúdo como bytes
        content_bytes = file.read()
        
        # Processa baseado no tipo
        if file.filename.lower().endswith('.csv'):
            analysis = process_csv_data(content_bytes)
        else:
            analysis = process_excel_data(content_bytes, file.filename)
        
        # Verifica se há erro no processamento
        if 'error' in analysis:
            return jsonify({'error': analysis['error']}), 400
        
        # Para arquivos Excel que ainda não são totalmente suportados
        if analysis.get('file_type') == 'Excel' and analysis.get('total_rows', 0) == 0:
            return jsonify({
                'success': True,
                'message': 'Arquivo Excel recebido. Processamento completo será implementado em breve.',
                'file_id': f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'analysis': analysis,
                'warning': 'Processamento limitado para arquivos Excel'
            })
        
        # Salva no armazenamento temporário
        file_id = f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Tenta decodificar o conteúdo para armazenamento
        try:
            content_text = content_bytes.decode(analysis.get('encoding', 'utf-8'))
        except:
            content_text = content_bytes.decode('latin1', errors='ignore')
        
        file_storage[file_id] = {
            'id': file_id,
            'name': file.filename,
            'size': file_size,
            'uploaded': datetime.now().isoformat(),
            'content': content_text,
            'analysis': analysis
        }
        
        return jsonify({
            'success': True,
            'message': f'Arquivo processado com sucesso!',
            'file_id': file_id,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro no processamento: {str(e)}'}), 500

@app.route('/api/files')
def list_files():
    """Lista arquivos carregados"""
    files = []
    for file_id, file_data in file_storage.items():
        files.append({
            'id': file_id,
            'name': file_data['name'],
            'size': file_data['size'],
            'uploaded': file_data['uploaded']
        })
    
    return jsonify({
        'files': files,
        'total': len(files)
    })

@app.route('/api/files/<file_id>')
def get_file(file_id):
    """Obtém dados de um arquivo específico"""
    if file_id not in file_storage:
        return jsonify({'error': 'Arquivo não encontrado'}), 404
    
    file_data = file_storage[file_id]
    return jsonify({
        'file': file_data
    })

@app.route('/api/files/<file_id>/delete', methods=['DELETE'])
def delete_file(file_id):
    """Remove um arquivo"""
    if file_id not in file_storage:
        return jsonify({'error': 'Arquivo não encontrado'}), 404
    
    del file_storage[file_id]
    return jsonify({
        'success': True,
        'message': 'Arquivo removido com sucesso'
    })

@app.route('/api/files/clear', methods=['DELETE'])
def clear_all_files():
    """Remove todos os arquivos"""
    global file_storage
    file_storage = {}
    return jsonify({
        'success': True,
        'message': 'Todos os arquivos removidos com sucesso'
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat com IA"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        # Verifica se há dados carregados
        if not file_storage:
            response = {
                'response': 'Nenhum arquivo carregado ainda. Faça upload de um arquivo CSV ou Excel primeiro.',
                'timestamp': datetime.now().isoformat(),
                'status': 'no_data'
            }
        else:
            # Simula análise com IA
            response = {
                'response': f'Pergunta: "{question}". Análise baseada em {len(file_storage)} arquivo(s) carregado(s). Funcionalidade de IA completa será implementada em breve.',
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'files_loaded': len(file_storage)
            }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/generate', methods=['POST'])
def generate_report():
    """Gera relatório"""
    try:
        if not file_storage:
            return jsonify({'error': 'Nenhum arquivo carregado para gerar relatório'}), 400
        
        # Gera relatório simples
        report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        report_data = {
            'id': report_id,
            'generated': datetime.now().isoformat(),
            'files_analyzed': len(file_storage),
            'summary': {
                'total_files': len(file_storage),
                'total_rows': sum(f['analysis'].get('total_rows', 0) for f in file_storage.values()),
                'file_types': list(set(f['analysis'].get('file_type', 'Unknown') for f in file_storage.values()))
            }
        }
        
        reports_storage[report_id] = report_data
        
        return jsonify({
            'success': True,
            'message': 'Relatório gerado com sucesso!',
            'report_id': report_id,
            'report': report_data
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar relatório: {str(e)}'}), 500

@app.route('/api/reports')
def list_reports():
    """Lista relatórios gerados"""
    reports = []
    for report_id, report_data in reports_storage.items():
        reports.append({
            'id': report_id,
            'generated': report_data['generated'],
            'summary': report_data['summary']
        })
    
    return jsonify({
        'reports': reports,
        'total': len(reports)
    })

@app.route('/api/test')
def test():
    """Endpoint de teste"""
    return jsonify({
        'message': 'API com sistema de arquivos funcionando!',
        'timestamp': datetime.now().isoformat(),
        'endpoints': [
            '/api/status',
            '/api/upload',
            '/api/files',
            '/api/chat',
            '/api/reports/generate',
            '/api/reports'
        ],
        'files_loaded': len(file_storage),
        'reports_generated': len(reports_storage)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
