#!/usr/bin/env python3
"""
Teste específico do template
"""

from flask import Flask, render_template, jsonify
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    try:
        print("🔍 Renderizando template...")
        result = render_template('index.html')
        print("✅ Template renderizado com sucesso!")
        return result
    except Exception as e:
        print(f"❌ Erro ao renderizar template: {e}")
        print(f"📋 Traceback completo:")
        print(traceback.format_exc())
        return f"Erro no template: {str(e)}", 500

@app.route('/test')
def test():
    return jsonify({
        'status': 'success',
        'message': 'Template test funcionando!'
    })

if __name__ == '__main__':
    print("🚀 Iniciando teste de template...")
    print("📱 Acesse: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
