#!/usr/bin/env python3
"""
ZapCampanhas - Versão Vercel Simplificada
"""

from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# HTML template simplificado
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍗 ZapCampanhas - Vercel</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .header { background: linear-gradient(135deg, #FF8000 0%, #FF4000 100%); color: white; padding: 2rem; }
        .btn-primary { background-color: #FF8000; border-color: #FF8000; }
        .btn-primary:hover { background-color: #FF4000; border-color: #FF4000; }
    </style>
</head>
<body>
    <div class="header text-center">
        <h1><i class="fas fa-drumstick-bite"></i> ZapCampanhas</h1>
        <h4>Business Intelligence para ZapChicken</h4>
        <p class="mb-0"><small>Versão Vercel - Funcionando!</small></p>
    </div>

    <div class="container mt-4">
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h5><i class="fas fa-upload"></i> Upload de Arquivos</h5>
                    </div>
                    <div class="card-body">
                        <p>Funcionalidade de upload será implementada em breve.</p>
                        <button class="btn btn-primary" onclick="testFunction()">
                            <i class="fas fa-rocket"></i> Testar Funcionalidade
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h5><i class="fas fa-robot"></i> Chat com IA</h5>
                    </div>
                    <div class="card-body">
                        <div id="chat-container" style="height: 200px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; background-color: #f8f9fa;">
                            <div class="text-center text-muted">
                                <i class="fas fa-robot fa-2x mb-2"></i>
                                <p>Olá! Como posso ajudar você hoje?</p>
                            </div>
                        </div>
                        <div class="input-group">
                            <input type="text" id="chat-input" class="form-control" placeholder="Digite sua pergunta..." onkeypress="if(event.keyCode==13) sendMessage()">
                            <button class="btn btn-primary" onclick="sendMessage()">
                                <i class="fas fa-paper-plane"></i> Enviar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-12">
                <div class="alert alert-info">
                    <h6><i class="fas fa-info-circle"></i> Status do Sistema</h6>
                    <p class="mb-0">✅ Sistema funcionando no Vercel!</p>
                    <p class="mb-0">✅ Interface carregada com sucesso</p>
                    <p class="mb-0">✅ Chat com IA disponível</p>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function testFunction() {
            alert('Funcionalidade testada com sucesso!');
        }
        
        function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            addMessage('Você', message, 'user');
            input.value = '';
            
            // Simula resposta da IA
            setTimeout(() => {
                addMessage('IA', 'Esta é uma resposta simulada da IA no Vercel!', 'ai');
            }, 1000);
        }
        
        function addMessage(sender, text, type) {
            const container = document.getElementById('chat-container');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'mb-2';
            
            const time = new Date().toLocaleTimeString();
            
            if (type === 'user') {
                messageDiv.innerHTML = `
                    <div class="d-flex justify-content-end">
                        <div class="bg-primary text-white p-2 rounded" style="max-width: 70%;">
                            <strong>${sender}:</strong> ${text}
                            <br><small class="text-light">${time}</small>
                        </div>
                    </div>
                `;
            } else {
                messageDiv.innerHTML = `
                    <div class="d-flex justify-content-start">
                        <div class="bg-light p-2 rounded" style="max-width: 70%;">
                            <strong>${sender}:</strong> ${text}
                            <br><small class="text-muted">${time}</small>
                        </div>
                    </div>
                `;
            }
            
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Página principal"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def status():
    """Endpoint de status"""
    return jsonify({
        'status': 'online',
        'message': 'ZapCampanhas funcionando no Vercel!',
        'version': '1.0.0'
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat com IA"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        response = f"Você disse: '{message}'. Esta é uma resposta simulada da IA no Vercel!"
        
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
