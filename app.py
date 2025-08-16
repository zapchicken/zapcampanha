#!/usr/bin/env python3
"""
ZapCampanhas - Versão Super Simples para Render
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '🍗 ZapCampanhas funcionando no Render!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
