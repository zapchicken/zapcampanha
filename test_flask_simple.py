#!/usr/bin/env python3
"""
Teste simples do Flask
"""

from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Teste Flask</title>
    </head>
    <body>
        <h1>🍗 Teste ZapCampanhas</h1>
        <p>Se você está vendo esta página, o Flask está funcionando!</p>
        <p>Status: ✅ Funcionando</p>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask de teste...")
    print("📱 Acesse: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
