#!/usr/bin/env python3
"""
ZapCampanhas - Versão Super Simples para Render
"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🍗 ZapCampanhas</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .success { color: green; font-size: 24px; }
        </style>
    </head>
    <body>
        <h1>🍗 ZapCampanhas</h1>
        <p class="success">✅ Deploy no Render funcionando!</p>
        <p>Versão: 2.0.1 - Render Cloud</p>
    </body>
    </html>
    '''

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'online',
        'message': 'ZapCampanhas funcionando no Render!',
        'version': '2.0.1-simple'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
