#!/usr/bin/env python3
"""
ZapCampanhas API - Versão corrigida
"""

from flask import Flask, request, jsonify
import json
import csv
import os
from datetime import datetime
import io

app = Flask(__name__)

# Configurações
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Armazenamento temporário
file_storage = {}
reports_storage = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_csv_data(content):
    """Processa dados CSV"""
    try:
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
        
        analysis = {
            "total_rows": total_rows,
            "columns": columns,
            "column_count": len(columns),
            "sample_data": data[:5],
            "file_type": "CSV"
        }
        
        return analysis
        
    except Exception as e:
        return {"error": f"Erro ao processar CSV: {str(e)}"}

def process_excel_data(content, filename):
    """Processa dados Excel"""
    return {
        "total_rows": 0,
        "columns": [],
        "column_count": 0,
        "sample_data": [],
        "file_type": "Excel",
        "message": "Arquivo Excel recebido. Processamento completo será implementado em breve."
    }

@app.route('/')
def index():
    """Página principal"""
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
                            <div>
                                <button class="btn btn-sm btn-zap-primary me-2" onclick="processData()">
                                    <i class="fas fa-cogs"></i> Processar Dados
                                </button>
                                <button class="btn btn-sm btn-outline-danger" onclick="clearAllFiles()">
                                    <i class="fas fa-trash"></i> Limpar Todos
                                </button>
                            </div>
                        </div>
                        <div class="card-body">
                            <div id="fileList">
                                <p class="text-muted">Nenhum arquivo carregado ainda.</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="fas fa-chart-bar"></i> Relatórios e Análises</h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <button class="btn btn-zap-primary me-2" onclick="generateReport()">
                                    <i class="fas fa-file-chart"></i> Gerar Relatório
                                </button>
                                <button class="btn btn-outline-primary" onclick="showAnalytics()">
                                    <i class="fas fa-chart-line"></i> Ver Analytics
                                </button>
                            </div>
                            <div id="reportArea">
                                <p class="text-muted">Clique em "Gerar Relatório" para criar análises dos seus dados.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
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
                        console.log('DEBUG: Dados recebidos:', data);
                        
                        if (data.files && data.files.length > 0) {
                            let html = `<div class="alert alert-info mb-3">
                                <strong>📁 Total de arquivos: ${data.total}</strong><br>
                                <small>${data.debug_info || ''}</small>
                            </div>
                            <div class="list-group">`;
                            
                            data.files.forEach(file => {
                                html += `
                                    <div class="list-group-item d-flex justify-content-between align-items-center">
                                        <div>
                                            <strong>${file.name}</strong><br>
                                            <small class="text-muted">
                                                ID: ${file.id} • ${file.size} bytes • ${file.uploaded}
                                            </small>
                                        </div>
                                        <div>
                                            <button class="btn btn-sm btn-outline-primary me-2" onclick="viewFile('${file.id}')">
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
                        console.error('Erro ao carregar arquivos:', error);
                        document.getElementById('fileList').innerHTML = 
                            `<div class="alert alert-danger">Erro ao carregar arquivos: ${error.message}</div>`;
                    });
            }

            // Visualizar arquivo
            function viewFile(fileId) {
                // Por enquanto, apenas mostra uma mensagem
                alert(`Visualizando arquivo ${fileId}. Funcionalidade completa será implementada em breve.`);
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

            // Processar dados
            function processData() {
                fetch('/api/process', {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('reportArea').innerHTML = 
                            `<div class="alert alert-success">
                                <strong>✅ Dados processados!</strong><br>
                                ${data.message}<br>
                                <strong>Resumo:</strong><br>
                                • Total de arquivos: ${data.summary.total_files}<br>
                                • Total de linhas: ${data.summary.total_rows}<br>
                                • Tipos de arquivo: ${data.summary.file_types.join(', ')}
                            </div>`;
                    } else {
                        document.getElementById('reportArea').innerHTML = 
                            `<div class="alert alert-danger">
                                <strong>❌ Erro:</strong><br>
                                ${data.error}
                            </div>`;
                    }
                })
                .catch(error => {
                    document.getElementById('reportArea').innerHTML = 
                        `<div class="alert alert-danger">
                            <strong>❌ Erro:</strong><br>
                            ${error.message}
                        </div>`;
                });
            }

            // Gerar relatório
            function generateReport() {
                fetch('/api/reports/generate', {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const report = data.report;
                        let html = `<div class="alert alert-success">
                            <strong>📊 Relatório Avançado Gerado!</strong><br>
                            ${data.message}<br>
                            <strong>ID:</strong> ${data.report_id}<br>
                            <strong>Registros analisados:</strong> ${report.cross_analysis.total_records}<br>
                            <strong>Arquivos:</strong> ${report.cross_analysis.files_analyzed}<br><br>
                            <button class="btn btn-sm btn-outline-primary me-2" onclick="viewReport('${data.report_id}')">
                                <i class="fas fa-eye"></i> Ver Detalhes
                            </button>
                            <button class="btn btn-sm btn-outline-info" onclick="showReportInsights('${data.report_id}')">
                                <i class="fas fa-lightbulb"></i> Ver Insights
                            </button>
                        </div>`;
                        
                        document.getElementById('reportArea').innerHTML = html;
                    } else {
                        document.getElementById('reportArea').innerHTML = 
                            `<div class="alert alert-danger">
                                <strong>❌ Erro:</strong><br>
                                ${data.error}
                            </div>`;
                    }
                })
                .catch(error => {
                    document.getElementById('reportArea').innerHTML = 
                        `<div class="alert alert-danger">
                            <strong>❌ Erro:</strong><br>
                            ${error.message}
                        </div>`;
                });
            }

            // Visualizar relatório detalhado
            function viewReport(reportId) {
                fetch(`/api/reports/${reportId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const report = data.report;
                        const analysis = report.cross_analysis;
                        
                        let html = `<div class="alert alert-info">
                            <h5><i class="fas fa-chart-bar"></i> Relatório Detalhado</h5>
                            <hr>
                            <strong>📊 Resumo Geral:</strong><br>
                            • Total de registros: ${analysis.total_records}<br>
                            • Arquivos analisados: ${analysis.files_analyzed}<br>
                            • Colunas encontradas: ${Object.keys(analysis.column_mapping).length}<br><br>
                            
                            <strong>🔍 Colunas Comuns:</strong><br>`;
                        
                        if (analysis.common_columns && analysis.common_columns.length > 0) {
                            analysis.common_columns.slice(0, 5).forEach(col => {
                                html += `• <strong>${col.column}</strong> (${col.count} arquivos)<br>`;
                            });
                        } else {
                            html += `• Nenhuma coluna comum encontrada<br>`;
                        }
                        
                        html += `<br><strong>📋 Análise por Coluna:</strong><br>`;
                        
                        Object.entries(analysis.column_analysis).slice(0, 8).forEach(([col, info]) => {
                            html += `• <strong>${col}</strong> (${info.type}) - ${info.unique_values} valores únicos<br>`;
                        });
                        
                        html += `</div>`;
                        
                        document.getElementById('reportArea').innerHTML = html;
                    } else {
                        document.getElementById('reportArea').innerHTML = 
                            `<div class="alert alert-danger">Erro ao carregar relatório: ${data.error}</div>`;
                    }
                })
                .catch(error => {
                    document.getElementById('reportArea').innerHTML = 
                        `<div class="alert alert-danger">Erro ao carregar relatório: ${error.message}</div>`;
                });
            }

            // Mostrar insights do relatório
            function showReportInsights(reportId) {
                fetch(`/api/reports/${reportId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const insights = data.report.cross_analysis.insights;
                        
                        let html = `<div class="alert alert-warning">
                            <h5><i class="fas fa-lightbulb"></i> Insights Inteligentes</h5>
                            <hr>`;
                        
                        if (insights && insights.length > 0) {
                            insights.forEach(insight => {
                                html += `<div class="mb-3">
                                    <strong>💡 ${insight.title}</strong><br>
                                    <small>${insight.description}</small><br>`;
                                
                                if (insight.data && insight.data.length > 0) {
                                    html += `<small class="text-muted">Dados: ${insight.data.join(', ')}</small>`;
                                }
                                
                                html += `</div>`;
                            });
                        } else {
                            html += `<p>Nenhum insight específico encontrado nos dados.</p>`;
                        }
                        
                        html += `</div>`;
                        
                        document.getElementById('reportArea').innerHTML = html;
                    } else {
                        document.getElementById('reportArea').innerHTML = 
                            `<div class="alert alert-danger">Erro ao carregar insights: ${data.error}</div>`;
                    }
                })
                .catch(error => {
                    document.getElementById('reportArea').innerHTML = 
                        `<div class="alert alert-danger">Erro ao carregar insights: ${error.message}</div>`;
                });
            }

            // Mostrar analytics
            function showAnalytics() {
                fetch('/api/analytics')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        let html = `<div class="alert alert-info">
                            <strong>📈 Analytics dos Dados</strong><br><br>`;
                        
                        if (data.analytics) {
                            html += `<strong>Estatísticas Gerais:</strong><br>
                            • Total de arquivos: ${data.analytics.total_files}<br>
                            • Total de linhas: ${data.analytics.total_rows}<br>
                            • Tipos de arquivo: ${data.analytics.file_types.join(', ')}<br><br>`;
                            
                            if (data.analytics.columns) {
                                html += `<strong>Colunas encontradas:</strong><br>`;
                                data.analytics.columns.forEach(col => {
                                    html += `• ${col}<br>`;
                                });
                            }
                        }
                        
                        html += `</div>`;
                        document.getElementById('reportArea').innerHTML = html;
                    } else {
                        document.getElementById('reportArea').innerHTML = 
                            `<div class="alert alert-warning">
                                <strong>⚠️ Nenhum dado para analisar</strong><br>
                                Faça upload de arquivos primeiro.
                            </div>`;
                    }
                })
                .catch(error => {
                    document.getElementById('reportArea').innerHTML = 
                        `<div class="alert alert-danger">
                            <strong>❌ Erro:</strong><br>
                            ${error.message}
                        </div>`;
                });
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
                            document.getElementById('reportArea').innerHTML = 
                                '<p class="text-muted">Clique em "Gerar Relatório" para criar análises dos seus dados.</p>';
                        } else {
                            alert(`Erro ao limpar: ${data.error}`);
                        }
                    })
                    .catch(error => {
                        alert(`Erro ao limpar arquivos: ${error.message}`);
                    });
                }
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
        'version': '2.1.0',
        'message': 'ZapCampanhas API corrigida!'
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
        
        # Lê o conteúdo
        try:
            content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            try:
                file.seek(0)
                content = file.read().decode('latin1')
            except:
                return jsonify({'error': 'Não foi possível ler o arquivo. Verifique a codificação.'}), 400
        
        # Processa baseado no tipo
        if file.filename.lower().endswith('.csv'):
            analysis = process_csv_data(content)
        else:
            analysis = process_excel_data(content, file.filename)
        
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
        
        # Salva no armazenamento temporário com timestamp único
        import time
        file_id = f"file_{int(time.time() * 1000)}"
        file_storage[file_id] = {
            'id': file_id,
            'name': file.filename,
            'size': file_size,
            'uploaded': datetime.now().isoformat(),
            'content': content,
            'analysis': analysis
        }
        
        # Debug: mostra quantos arquivos estão armazenados
        print(f"DEBUG: Arquivo {file.filename} salvo com ID {file_id}. Total de arquivos: {len(file_storage)}")
        
        return jsonify({
            'success': True,
            'message': f'Arquivo {file.filename} processado com sucesso!',
            'file_id': file_id,
            'analysis': analysis,
            'total_files': len(file_storage)
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
    
    # Debug: mostra informações sobre os arquivos
    print(f"DEBUG: Listando {len(files)} arquivos:")
    for f in files:
        print(f"  - {f['name']} (ID: {f['id']})")
    
    return jsonify({
        'files': files,
        'total': len(files),
        'debug_info': f"Total de arquivos no storage: {len(file_storage)}"
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

@app.route('/api/process', methods=['POST'])
def process_data():
    """Processa todos os dados carregados"""
    try:
        if not file_storage:
            return jsonify({'error': 'Nenhum arquivo carregado para processar'}), 400
        
        # Análise geral dos dados
        total_files = len(file_storage)
        total_rows = sum(f['analysis'].get('total_rows', 0) for f in file_storage.values())
        file_types = list(set(f['analysis'].get('file_type', 'Unknown') for f in file_storage.values()))
        
        # Coleta todas as colunas únicas
        all_columns = set()
        for file_data in file_storage.values():
            columns = file_data['analysis'].get('columns', [])
            all_columns.update(columns)
        
        summary = {
            'total_files': total_files,
            'total_rows': total_rows,
            'file_types': file_types,
            'unique_columns': list(all_columns)
        }
        
        return jsonify({
            'success': True,
            'message': f'Dados processados com sucesso! {total_files} arquivo(s) analisado(s).',
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao processar dados: {str(e)}'}), 500

@app.route('/api/analytics')
def get_analytics():
    """Retorna analytics dos dados carregados"""
    try:
        if not file_storage:
            return jsonify({
                'success': False,
                'message': 'Nenhum arquivo carregado'
            })
        
        # Análise detalhada
        total_files = len(file_storage)
        total_rows = sum(f['analysis'].get('total_rows', 0) for f in file_storage.values())
        file_types = list(set(f['analysis'].get('file_type', 'Unknown') for f in file_storage.values()))
        
        # Coleta todas as colunas
        all_columns = set()
        for file_data in file_storage.values():
            columns = file_data['analysis'].get('columns', [])
            all_columns.update(columns)
        
        analytics = {
            'total_files': total_files,
            'total_rows': total_rows,
            'file_types': file_types,
            'columns': list(all_columns)
        }
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar analytics: {str(e)}'}), 500

@app.route('/api/reports/generate', methods=['POST'])
def generate_report():
    """Gera relatório avançado com cruzamento de dados"""
    try:
        if not file_storage:
            return jsonify({'error': 'Nenhum arquivo carregado para gerar relatório'}), 400
        
        # Gera relatório avançado
        report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Análise básica
        total_files = len(file_storage)
        total_rows = sum(f['analysis'].get('total_rows', 0) for f in file_storage.values())
        file_types = list(set(f['analysis'].get('file_type', 'Unknown') for f in file_storage.values()))
        
        # Análise cruzada dos dados
        cross_analysis = analyze_cross_data()
        
        report_data = {
            'id': report_id,
            'generated': datetime.now().isoformat(),
            'summary': {
                'total_files': total_files,
                'total_rows': total_rows,
                'file_types': file_types
            },
            'cross_analysis': cross_analysis
        }
        
        reports_storage[report_id] = report_data
        
        return jsonify({
            'success': True,
            'message': 'Relatório avançado gerado com sucesso!',
            'report_id': report_id,
            'report': report_data
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar relatório: {str(e)}'}), 500

@app.route('/api/reports/<report_id>')
def get_report(report_id):
    """Obtém um relatório específico"""
    if report_id not in reports_storage:
        return jsonify({'error': 'Relatório não encontrado'}), 404
    
    return jsonify({
        'success': True,
        'report': reports_storage[report_id]
    })

@app.route('/api/reports')
def list_reports():
    """Lista todos os relatórios gerados"""
    reports = []
    for report_id, report_data in reports_storage.items():
        reports.append({
            'id': report_id,
            'generated': report_data['generated'],
            'summary': report_data['summary']
        })
    
    return jsonify({
        'success': True,
        'reports': reports,
        'total': len(reports)
    })

def analyze_cross_data():
    """Analisa e cruza dados de todos os arquivos"""
    try:
        all_data = []
        column_mapping = {}
        
        # Coleta todos os dados
        for file_id, file_data in file_storage.items():
            if file_data['analysis'].get('file_type') == 'CSV':
                # Parse CSV data
                content = file_data['content']
                reader = csv.DictReader(io.StringIO(content))
                file_rows = list(reader)
                
                # Adiciona metadados do arquivo
                for row in file_rows:
                    row['_source_file'] = file_data['name']
                    row['_file_id'] = file_id
                
                all_data.extend(file_rows)
                
                # Mapeia colunas
                columns = file_data['analysis'].get('columns', [])
                for col in columns:
                    if col not in column_mapping:
                        column_mapping[col] = []
                    column_mapping[col].append(file_data['name'])
        
        if not all_data:
            return {
                'error': 'Nenhum dado válido encontrado para análise cruzada'
            }
        
        # Análises cruzadas
        analysis = {
            'total_records': len(all_data),
            'files_analyzed': len(file_storage),
            'column_mapping': column_mapping,
            'insights': []
        }
        
        # Detecta colunas comuns
        common_columns = []
        for col, files in column_mapping.items():
            if len(files) > 1:
                common_columns.append({
                    'column': col,
                    'files': files,
                    'count': len(files)
                })
        
        analysis['common_columns'] = sorted(common_columns, key=lambda x: x['count'], reverse=True)
        
        # Análise por tipo de coluna
        column_analysis = {}
        for col in column_mapping.keys():
            values = [row.get(col, '') for row in all_data if row.get(col, '')]
            unique_values = len(set(values))
            
            # Detecta tipo de coluna
            col_type = 'text'
            if col.lower() in ['valor', 'preco', 'price', 'amount', 'total']:
                col_type = 'monetary'
            elif col.lower() in ['data', 'date', 'data_compra', 'data_venda']:
                col_type = 'date'
            elif col.lower() in ['quantidade', 'qtd', 'quantity', 'amount']:
                col_type = 'numeric'
            
            column_analysis[col] = {
                'type': col_type,
                'total_values': len(values),
                'unique_values': unique_values,
                'sample_values': list(set(values))[:5]
            }
        
        analysis['column_analysis'] = column_analysis
        
        # Gera insights
        insights = []
        
        # Insight 1: Colunas comuns
        if analysis['common_columns']:
            insights.append({
                'type': 'common_columns',
                'title': 'Colunas Comuns Encontradas',
                'description': f'Encontradas {len(analysis["common_columns"])} colunas que aparecem em múltiplos arquivos',
                'data': analysis['common_columns'][:5]
            })
        
        # Insight 2: Análise de valores únicos
        high_unique_cols = [col for col, info in column_analysis.items() 
                          if info['unique_values'] > 10 and info['total_values'] > 0]
        if high_unique_cols:
            insights.append({
                'type': 'high_diversity',
                'title': 'Colunas com Alta Diversidade',
                'description': f'Colunas com muitos valores únicos: {", ".join(high_unique_cols[:3])}',
                'data': high_unique_cols[:3]
            })
        
        # Insight 3: Análise de tipos de dados
        monetary_cols = [col for col, info in column_analysis.items() if info['type'] == 'monetary']
        date_cols = [col for col, info in column_analysis.items() if info['type'] == 'date']
        
        if monetary_cols:
            insights.append({
                'type': 'monetary_data',
                'title': 'Dados Monetários Detectados',
                'description': f'Colunas com valores monetários: {", ".join(monetary_cols)}',
                'data': monetary_cols
            })
        
        if date_cols:
            insights.append({
                'type': 'date_data',
                'title': 'Dados de Data Detectados',
                'description': f'Colunas com datas: {", ".join(date_cols)}',
                'data': date_cols
            })
        
        analysis['insights'] = insights
        
        return analysis
        
    except Exception as e:
        return {
            'error': f'Erro na análise cruzada: {str(e)}'
        }

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

@app.route('/api/test')
def test():
    """Endpoint de teste"""
    return jsonify({
        'message': 'API corrigida funcionando!',
        'timestamp': datetime.now().isoformat(),
        'files_loaded': len(file_storage)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
