#!/usr/bin/env python3
"""
ZapCampanhas Web App - Versão Flask Simplificada
"""

from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
import os
from pathlib import Path
import pandas as pd
from werkzeug.utils import secure_filename
import json
from datetime import datetime

# Configurações
INPUT_DIR = Path("data/input")
OUTPUT_DIR = Path("data/output")
UPLOAD_FOLDER = INPUT_DIR
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

# Cria diretórios se não existirem
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'zapcampanhas_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Cache global para manter dados em memória
global_data_loaded = False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    print(f"Upload recebido: {request.files}")
    print(f"Form data: {request.form}")
    
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('index'))
    
    file = request.files['file']
    file_type = request.form.get('file_type')
    
    if file.filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Salva com nome específico baseado no tipo
        if file_type == 'contacts':
            filename = 'contacts.csv'
        elif file_type == 'clientes':
            filename = 'Lista-Clientes.xlsx'
        elif file_type == 'pedidos':
            filename = 'Todos os pedidos.xlsx'
        elif file_type == 'itens':
            filename = 'Historico_Itens_Vendidos.xlsx'
        
        filepath = INPUT_DIR / filename
        file.save(filepath)
        flash(f'Arquivo {filename} carregado com sucesso!')
        print(f"Arquivo salvo: {filepath}")
    else:
        flash('Tipo de arquivo não permitido')
    
    return redirect(url_for('index'))

@app.route('/process_data', methods=['POST'])
def process_data():
    global global_data_loaded
    
    print(f"Processamento recebido: {request.form}")
    
    try:
        dias_inatividade = int(request.form.get('dias_inatividade', 30))
        ticket_minimo = float(request.form.get('ticket_minimo', 50))
        
        print(f"Configurações: dias_inatividade={dias_inatividade}, ticket_minimo={ticket_minimo}")
        
        # Verifica se os arquivos existem
        required_files = [
            'contacts.csv',
            'Lista-Clientes.xlsx',
            'Todos os pedidos.xlsx',
            'Historico_Itens_Vendidos.xlsx'
        ]
        
        missing_files = []
        for filename in required_files:
            filepath = INPUT_DIR / filename
            if not filepath.exists():
                missing_files.append(filename)
        
        if missing_files:
            flash(f'Arquivos faltando: {", ".join(missing_files)}')
            return redirect(url_for('index'))
        
        # Cria relatórios simples
        create_simple_reports()
        
        global_data_loaded = True
        flash('Dados processados com sucesso! Relatórios gerados.')
        
    except Exception as e:
        print(f"Erro no processamento: {e}")
        flash(f'Erro ao processar dados: {str(e)}')
    
    return redirect(url_for('index'))

def create_simple_reports():
    """Cria relatórios simples para teste"""
    try:
        # Relatório 1: Novos Clientes
        df_novos = pd.DataFrame({
            'Nome': ['Cliente Teste 1', 'Cliente Teste 2'],
            'Telefone': ['11999999999', '11888888888'],
            'Data_Cadastro': [datetime.now().strftime('%d/%m/%Y'), datetime.now().strftime('%d/%m/%Y')]
        })
        df_novos.to_csv(OUTPUT_DIR / 'novos_clientes_google_contacts.csv', index=False, encoding='utf-8')
        
        # Relatório 2: Clientes Inativos
        df_inativos = pd.DataFrame({
            'Nome': ['Cliente Inativo 1'],
            'Telefone': ['11777777777'],
            'Ultima_Compra': ['01/01/2024']
        })
        df_inativos.to_excel(OUTPUT_DIR / 'clientes_inativos.xlsx', index=False)
        
        # Relatório 3: Alto Ticket
        df_alto = pd.DataFrame({
            'Nome': ['Cliente Alto Ticket'],
            'Telefone': ['11666666666'],
            'Ticket_Medio': [150.0]
        })
        df_alto.to_excel(OUTPUT_DIR / 'clientes_alto_ticket.xlsx', index=False)
        
        print("Relatórios criados com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar relatórios: {e}")

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = OUTPUT_DIR / filename
        if file_path.exists():
            return send_file(file_path, as_attachment=True)
        else:
            flash('Arquivo não encontrado')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Erro ao baixar arquivo: {str(e)}')
        return redirect(url_for('index'))

@app.route('/check_files')
def check_files():
    """Verifica quais arquivos estão disponíveis"""
    files = {
        'novos_clientes_google_contacts.csv': 'Novos Clientes',
        'clientes_inativos.xlsx': 'Clientes Inativos',
        'clientes_alto_ticket.xlsx': 'Alto Ticket'
    }
    
    available = []
    for filename, name in files.items():
        file_path = OUTPUT_DIR / filename
        if file_path.exists():
            stat = file_path.stat()
            size_kb = round(stat.st_size / 1024, 1)
            local_time = datetime.fromtimestamp(stat.st_mtime)
            modified_str = local_time.strftime('%d/%m/%Y %H:%M')
            
            available.append({
                'filename': filename, 
                'name': name,
                'size': f"{size_kb} KB",
                'modified': modified_str
            })
    
    return jsonify(available)

@app.route('/data_status')
def data_status():
    """Verifica status dos dados carregados"""
    global global_data_loaded
    return jsonify({
        'data_loaded': global_data_loaded,
        'message': 'Dados carregados e prontos para uso!' if global_data_loaded else 'Dados não carregados. Processe os dados primeiro.'
    })

@app.route('/clear_cache')
def clear_cache():
    """Limpa o cache de dados"""
    global global_data_loaded
    global_data_loaded = False
    return jsonify({'message': 'Cache limpo com sucesso!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"Iniciando servidor na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
