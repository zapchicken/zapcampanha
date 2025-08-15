#!/usr/bin/env python3
"""
ZapCampanhas API - Versão ultra-simples para Vercel
Sem sistema de arquivos, apenas funcionalidade básica
"""

from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'zapcampanhas_secret_key'

@app.route('/')
def index():
    """Página principal"""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Erro ao carregar página: {str(e)}", 500

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

@app.route('/check_files')
def check_files():
    """Verifica arquivos disponíveis (simulado)"""
    return jsonify([
        {
            'name': 'relatorio_exemplo.json',
            'size': 1024,
            'modified': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'url': '/download/relatorio_exemplo.json'
        }
    ])

@app.route('/download/<filename>')
def download_file(filename):
    """Download de arquivo (simulado)"""
    return jsonify({
        'message': f'Download do arquivo {filename} será implementado em breve.',
        'filename': filename
    })

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
            '/api/test',
            '/check_files'
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
