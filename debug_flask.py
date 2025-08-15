#!/usr/bin/env python3
"""
Debug Flask - Identifica problemas específicos
"""

from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
import os
from pathlib import Path
import traceback

# Configurações básicas
INPUT_DIR = Path("data/input")
OUTPUT_DIR = Path("data/output")

# Cria diretórios se não existirem
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'debug_secret_key'

@app.route('/')
def index():
    try:
        print("🔍 Tentando renderizar template...")
        return render_template('index.html')
    except Exception as e:
        print(f"❌ Erro ao renderizar template: {e}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        return f"Erro: {str(e)}", 500

@app.route('/test')
def test():
    return jsonify({
        'status': 'success',
        'message': 'Flask está funcionando!',
        'input_dir': str(INPUT_DIR),
        'output_dir': str(OUTPUT_DIR)
    })

@app.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        print(f"📁 Upload recebido: {request.files}")
        print(f"📋 Form data: {request.form}")
        
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo selecionado'})
        
        file = request.files['file']
        file_type = request.form.get('file_type')
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'})
        
        return jsonify({
            'success': True,
            'message': f'Arquivo {file.filename} recebido',
            'type': file_type
        })
        
    except Exception as e:
        print(f"❌ Erro no upload: {e}")
        return jsonify({'error': str(e)})

@app.route('/process_data', methods=['POST'])
def process_data():
    try:
        print(f"⚙️ Processamento recebido: {request.form}")
        return jsonify({
            'success': True,
            'message': 'Processamento simulado com sucesso!'
        })
    except Exception as e:
        print(f"❌ Erro no processamento: {e}")
        return jsonify({'error': str(e)})

@app.route('/data_status')
def data_status():
    return jsonify({
        'data_loaded': False,
        'message': 'Dados não carregados (modo debug)'
    })

@app.route('/check_files')
def check_files():
    return jsonify([])

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask de debug...")
    print("📱 Acesse: http://localhost:5000")
    print("🔍 Teste: http://localhost:5000/test")
    app.run(host='0.0.0.0', port=5000, debug=True)
