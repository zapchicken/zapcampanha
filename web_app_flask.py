#!/usr/bin/env python3
"""
ZapCampanhas Web App - Versão Flask Simples
"""

from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
import os
from pathlib import Path
import pandas as pd
import base64
from werkzeug.utils import secure_filename
import json

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
global_processor = None
global_data_loaded = False
global_ai_gemini = None

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
        return redirect(request.url)
    
    file = request.files['file']
    file_type = request.form.get('file_type')
    
    if file.filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(request.url)
    
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
    else:
        flash('Tipo de arquivo não permitido')
    
    return redirect(url_for('index'))

@app.route('/process_data', methods=['POST'])
def process_data():
    global global_processor, global_data_loaded
    
    print(f"Processamento recebido: {request.form}")
    
    try:
        dias_inatividade = int(request.form.get('dias_inatividade', 30))
        ticket_minimo = float(request.form.get('ticket_minimo', 50))
        
        # Importa e executa o processador real
        from src.zapchicken_processor import ZapChickenProcessor
        
        # Inicializa processador global se não existir
        if global_processor is None:
            global_processor = ZapChickenProcessor(INPUT_DIR, OUTPUT_DIR)
        
        global_processor.config['dias_inatividade'] = dias_inatividade
        global_processor.config['ticket_medio_minimo'] = ticket_minimo
        
        # Carrega e processa os arquivos
        global_processor.load_zapchicken_files()
        global_processor.save_reports()
        
        global_data_loaded = True
        
        flash('Dados processados com sucesso! Relatórios gerados.')
    except Exception as e:
        flash(f'Erro ao processar dados: {str(e)}')
    
    return redirect(url_for('index'))

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
        'clientes_alto_ticket.xlsx': 'Alto Ticket',
        'analise_geografica.xlsx': 'Análise Geográfica',
        'produtos_mais_vendidos.xlsx': 'Produtos Mais Vendidos'
    }
    
    available = []
    for filename, name in files.items():
        file_path = OUTPUT_DIR / filename
        if file_path.exists():
            # Obtém informações do arquivo
            stat = file_path.stat()
            size_kb = round(stat.st_size / 1024, 1)
            
            # Corrige fuso horário - converte para horário local
            from datetime import datetime
            import time
            
            # Obtém timestamp de modificação
            mtime = stat.st_mtime
            
            # Converte para datetime local
            local_time = datetime.fromtimestamp(mtime)
            
            # Formata com fuso horário correto
            modified_str = local_time.strftime('%d/%m/%Y %H:%M')
            
            available.append({
                'filename': filename, 
                'name': name,
                'size': f"{size_kb} KB",
                'modified': modified_str
            })
    
    return jsonify(available)

@app.route('/view_file/<filename>')
def view_file(filename):
    """Visualiza conteúdo do arquivo"""
    try:
        file_path = OUTPUT_DIR / filename
        
        if not file_path.exists():
            return jsonify({'error': 'Arquivo não encontrado'})
        
        # Lê o arquivo baseado na extensão
        if filename.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            return jsonify({'error': 'Tipo de arquivo não suportado'})
        
        # Converte para HTML com formatação
        html_table = df.head(50).to_html(
            classes=['table', 'table-striped', 'table-sm'],
            index=False,
            border=0,
            table_id='data-table'
        )
        
        # Informações do arquivo
        file_info = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': df.columns.tolist(),
            'preview_rows': min(50, len(df))
        }
        
        return jsonify({
            'html': html_table,
            'info': file_info,
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao ler arquivo: {str(e)}'})

@app.route('/chat')
def chat():
    """Página do chat com IA"""
    return render_template('chat.html')

@app.route('/chat_message', methods=['POST'])
def chat_message():
    """Processa mensagem do chat"""
    global global_processor, global_data_loaded
    
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Mensagem vazia'})
        
        # Importa e usa o chat com IA
        try:
            from src.zapchicken_ai_advanced import ZapChickenAI
            from src.zapchicken_ai_gemini import ZapChickenAIGemini
            from src.zapchicken_processor import ZapChickenProcessor
        except ImportError as e:
            return jsonify({'error': f'Erro de importação: {str(e)}'})
        
        # Usa processador global se disponível
        if global_processor is not None and global_data_loaded:
            processor = global_processor
        else:
            # Se não há dados carregados, tenta carregar
            if global_processor is None:
                global_processor = ZapChickenProcessor(INPUT_DIR, OUTPUT_DIR)
            
            # Carrega os dados primeiro
            dataframes = global_processor.load_zapchicken_files()
            if not dataframes:
                return jsonify({'error': 'Nenhum arquivo da ZapChicken encontrado. Faça upload dos arquivos primeiro.'})
            
            global_data_loaded = True
            processor = global_processor
        
        # Tenta usar Gemini primeiro, depois fallback para IA avançada
        global global_ai_gemini
        
        if global_ai_gemini is not None:
            response = global_ai_gemini.process_question(message)
        else:
            ai = ZapChickenAI(processor)
            response = ai.process_question(message)
        
        return jsonify({'response': response})
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Erro detalhado no chat: {error_details}")
        return jsonify({'error': f'Erro no chat: {str(e)}'})

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
    global global_processor, global_data_loaded, global_ai_gemini
    global_processor = None
    global_data_loaded = False
    global_ai_gemini = None
    return jsonify({'message': 'Cache limpo com sucesso!'})

@app.route('/config_gemini', methods=['POST'])
def config_gemini():
    global global_processor, global_ai_gemini
    
    try:
        api_key = request.json.get('api_key', '').strip()
        
        if not api_key:
            return jsonify({'success': False, 'message': '❌ API key não fornecida'})
        
        if global_processor is None:
            return jsonify({'success': False, 'message': '❌ Processe os dados primeiro'})
        
        # Importa a classe Gemini
        try:
            from src.zapchicken_ai_gemini import ZapChickenAIGemini
        except ImportError as e:
            return jsonify({'success': False, 'message': f'❌ Erro ao importar Gemini: {str(e)}'})
        
        # Inicializa IA Gemini
        global_ai_gemini = ZapChickenAIGemini(global_processor, api_key)
        
        # Testa a API
        status = global_ai_gemini.get_api_status()
        
        if "✅" in status:
            return jsonify({'success': True, 'message': '✅ API Gemini configurada e funcionando!'})
        else:
            return jsonify({'success': False, 'message': f'⚠️ API configurada mas com problema: {status}'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'❌ Erro ao configurar Gemini: {str(e)}'})

@app.route('/gemini_status')
def gemini_status():
    global global_ai_gemini
    
    if global_ai_gemini is None:
        return jsonify({'status': 'not_configured', 'message': '❌ API Gemini não configurada'})
    
    try:
        api_status = global_ai_gemini.get_api_status()
        data_status = global_ai_gemini.get_data_status()
        
        if "✅" in api_status:
            return jsonify({
                'status': 'working', 
                'api_message': api_status,
                'data_message': data_status
            })
        else:
            return jsonify({
                'status': 'error', 
                'api_message': api_status,
                'data_message': data_status
            })
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'❌ Erro: {str(e)}'})

# Configuração para deploy no Vercel
if __name__ == '__main__':
    # Verifica se está rodando localmente ou em produção
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
