#!/usr/bin/env python3
"""
Teste simples para verificar upload
"""

from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Teste Upload</title>
    </head>
    <body>
        <h1>Teste de Upload</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="hidden" name="file_type" value="contacts">
            <button type="submit">Enviar</button>
        </form>
    </body>
    </html>
    ''')

@app.route('/upload', methods=['POST'])
def upload():
    print(f"Upload recebido: {request.files}")
    print(f"Form data: {request.form}")
    
    if 'file' not in request.files:
        return "Nenhum arquivo selecionado"
    
    file = request.files['file']
    if file.filename == '':
        return "Nenhum arquivo selecionado"
    
    # Salva o arquivo
    file.save(f"test_{file.filename}")
    return f"Arquivo {file.filename} salvo com sucesso!"

if __name__ == '__main__':
    app.run(debug=True, port=5001)
