# 🚀 Guia de Deploy no Render - ZapCampanhas

## Por que o Render?

O **Render** é uma excelente escolha para o ZapCampanhas porque oferece:

- ✅ **Deploy automático** do GitHub
- ✅ **SSL gratuito** e domínio personalizado
- ✅ **Melhor performance** que o Vercel para Python
- ✅ **Escalabilidade** fácil
- ✅ **Interface amigável** e configuração simples
- ✅ **Suporte a WebSockets** (se necessário no futuro)

## 📋 Pré-requisitos

1. **Conta no Render**: [render.com](https://render.com)
2. **Repositório no GitHub** com o código do ZapCampanhas
3. **Arquivos configurados**:
   - `app.py` ✅
   - `render.yaml` ✅
   - `requirements.txt` ✅

## 🚀 Passo a Passo do Deploy

### 1. Preparar o Repositório

Certifique-se de que seu repositório contém:

```
zapcampanhas/
├── app.py              # Aplicação Flask principal
├── render.yaml         # Configuração do Render
├── requirements.txt    # Dependências Python
├── src/               # Código fonte
├── config/            # Configurações
└── templates/         # Templates HTML
```

### 2. Criar Conta no Render

1. Acesse [render.com](https://render.com)
2. Clique em "Get Started"
3. Faça login com GitHub ou crie uma conta

### 3. Conectar Repositório

1. No dashboard do Render, clique em **"New +"**
2. Selecione **"Web Service"**
3. Conecte sua conta GitHub
4. Selecione o repositório `zapcampanhas`

### 4. Configurar o Serviço

O Render detectará automaticamente o `render.yaml`, mas você pode ajustar:

**Configurações Básicas:**
- **Name**: `zapcampanhas`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

**Variáveis de Ambiente:**
- `PYTHON_VERSION`: `3.11.9`
- `FLASK_ENV`: `production`

### 5. Deploy Automático

1. Clique em **"Create Web Service"**
2. O Render começará o build automaticamente
3. Aguarde o deploy (2-5 minutos)

## 🔧 Configurações Avançadas

### Health Check

O Render verificará automaticamente se a aplicação está funcionando através do endpoint `/api/status`.

### Domínio Personalizado

Após o deploy, você pode:
1. Ir em **Settings** > **Custom Domains**
2. Adicionar seu domínio personalizado
3. Configurar DNS conforme instruções

### Variáveis de Ambiente

Para adicionar variáveis sensíveis:
1. **Settings** > **Environment Variables**
2. Adicione:
   - `SECRET_KEY`: sua chave secreta
   - `GEMINI_API_KEY`: chave da API do Gemini (se usar)

## 📊 Monitoramento

### Logs
- Acesse **Logs** no dashboard do Render
- Monitore erros e performance

### Métricas
- **Uptime**: 99.9% garantido
- **Response Time**: < 200ms
- **Requests/min**: ilimitado no plano gratuito

## 🚨 Solução de Problemas

### Erro de Build
```bash
# Verifique se todas as dependências estão no requirements.txt
pip install -r requirements.txt
```

### Erro de Porta
```python
# O app.py já está configurado para usar a porta do Render
port = int(os.environ.get('PORT', 5000))
```

### Erro de Import
```python
# Certifique-se de que o path está correto
sys.path.append(str(Path(__file__).parent / "src"))
```

## 🔄 Deploy Contínuo

O Render faz **deploy automático** sempre que você:
1. Faz push para a branch `main`
2. Cria uma nova tag
3. Faz merge de um pull request

## 💰 Custos

**Plano Gratuito:**
- ✅ 750 horas/mês
- ✅ 512MB RAM
- ✅ 0.1 CPU
- ✅ Domínio `.onrender.com`

**Plano Pago ($7/mês):**
- ✅ Sem limites de horas
- ✅ 1GB RAM
- ✅ 0.5 CPU
- ✅ Domínio personalizado

## 🎯 Próximos Passos

1. **Deploy**: Siga o passo a passo acima
2. **Teste**: Acesse a URL fornecida pelo Render
3. **Configuração**: Adicione variáveis de ambiente se necessário
4. **Monitoramento**: Configure alertas e logs

## 📞 Suporte

- **Documentação Render**: [docs.render.com](https://docs.render.com)
- **Status do Serviço**: [status.render.com](https://status.render.com)
- **Comunidade**: [community.render.com](https://community.render.com)

---

**🎉 Parabéns!** Seu ZapCampanhas estará rodando na nuvem com o Render!

**URL do Deploy**: `https://zapcampanhas.onrender.com` (exemplo)
