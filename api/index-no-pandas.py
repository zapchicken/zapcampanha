#!/usr/bin/env python3
"""
ZapCampanhas API - Versão sem pandas para Vercel
Usa apenas CSV nativo para máxima compatibilidade
"""

from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
import os
from pathlib import Path
import csv
import json
import gc
import time
from functools import wraps
from datetime import datetime
import io

# Configurações
INPUT_DIR = Path("data/input")
OUTPUT_DIR = Path("data/output")
UPLOAD_FOLDER = INPUT_DIR
ALLOWED_EXTENSIONS = {'csv'}

# Limites para Vercel
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_PROCESSING_TIME = 20  # 20 segundos
MAX_MEMORY_USAGE = 256  # 256MB

# Cria diretórios se não existirem
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'zapcampanhas_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Cache global
global_data = None
last_activity = time.time()

def cleanup_memory():
    """Limpa memória"""
    global global_data
    if time.time() - last_activity > 300:  # 5 minutos
        global_data = None
    gc.collect()

def check_limits(func):
    """Decorator para verificar limites"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        if time.time() - start_time > MAX_PROCESSING_TIME:
            return jsonify({'error': 'Tempo limite excedido'}), 408
        cleanup_memory()
        return func(*args, **kwargs)
    return wrapper

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_csv_file(file_path):
    """Lê arquivo CSV sem pandas"""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Erro ao ler CSV: {e}")
    return data

def process_csv_data(data):
    """Processa dados CSV simples"""
    if not data:
        return {"error": "Nenhum dado encontrado"}
    
    # Estatísticas básicas
    total_rows = len(data)
    columns = list(data[0].keys()) if data else []
    
    # Análise simples
    analysis = {
        "total_rows": total_rows,
        "columns": columns,
        "sample_data": data[:5] if data else []
    }
    
    return analysis

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@check_limits
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    file = request.files['file']
    file_type = request.form.get('file_type', 'contacts')
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    # Verifica tamanho
    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': f'Arquivo muito grande. Máximo: {MAX_FILE_SIZE // (1024*1024)}MB'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Tipo de arquivo não permitido. Use CSV.'}), 400
    
    try:
        # Salva arquivo
        filename = secure_filename(file.filename)
        file_path = UPLOAD_FOLDER / filename
        file.save(file_path)
        
        # Processa dados
        data = read_csv_file(file_path)
        analysis = process_csv_data(data)
        
        # Salva relatório
        report_path = OUTPUT_DIR / f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'message': f'Arquivo processado com sucesso! {len(data)} linhas analisadas.',
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro no processamento: {str(e)}'}), 500

@app.route('/check_files')
def check_files():
    """Verifica arquivos disponíveis"""
    try:
        files = []
        if OUTPUT_DIR.exists():
            for file in OUTPUT_DIR.glob('*.json'):
                stat = file.stat()
                mtime = stat.st_mtime
                local_time = datetime.fromtimestamp(mtime)
                modified_str = local_time.strftime('%d/%m/%Y %H:%M')
                
                files.append({
                    'name': file.name,
                    'size': stat.st_size,
                    'modified': modified_str,
                    'url': f'/download/{file.name}'
                })
        
        return jsonify(files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download de arquivo"""
    try:
        file_path = OUTPUT_DIR / filename
        if file_path.exists():
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'Arquivo não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint simples para chat (sem IA por enquanto)"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        # Resposta simples
        response = {
            'response': f'Pergunta recebida: {question}. Funcionalidade de IA será implementada em breve.',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
