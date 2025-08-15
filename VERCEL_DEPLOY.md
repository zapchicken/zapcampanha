# 🚀 Deploy no Vercel - Guia Otimizado

## ⚠️ **Importante: Otimizações para Evitar Overload**

Este guia contém otimizações específicas para evitar problemas de memória e tempo limite no Vercel.

## 📋 **Pré-requisitos**

### **1. Conta Vercel**
- Crie conta em: https://vercel.com
- Conecte com GitHub

### **2. Limitações do Vercel**
- ⏱️ **Tempo limite**: 30 segundos por função
- 💾 **Memória**: 1024MB por função
- 📁 **Tamanho**: 50MB por deploy
- 🔄 **Cold start**: Primeira execução pode ser lenta

## 🛠️ **Configurações Implementadas**

### **1. vercel.json Otimizado**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb",
        "runtime": "python3.9"
      }
    }
  ],
  "functions": {
    "api/index.py": {
      "maxDuration": 30,
      "memory": 1024
    }
  }
}
```

### **2. Limites de Segurança**
- 📁 **Arquivo máximo**: 10MB
- ⏱️ **Processamento**: 25 segundos
- 💾 **Memória**: 512MB
- 🧹 **Limpeza automática**: 5 minutos

### **3. Dependências Otimizadas**
- ✅ **Pandas 2.0.3** - Versão estável
- ✅ **Flask 2.3.3** - Framework leve
- ✅ **Gunicorn** - Servidor WSGI
- ❌ **Removidas**: Rich, Plotly, Dash (muito pesadas)

## 🚀 **Deploy Step-by-Step**

### **1. Preparar Repositório**
```bash
# Certifique-se de que está no branch main
git checkout main

# Verifique se todos os arquivos estão commitados
git status

# Push para GitHub
git push origin main
```

### **2. Deploy no Vercel**
1. Acesse: https://vercel.com
2. Clique em **"New Project"**
3. Importe o repositório: `zapchicken/zapcampanha`
4. Configure as variáveis de ambiente:

### **3. Variáveis de Ambiente**
```bash
# No painel do Vercel, adicione:
GEMINI_API_KEY=sua_api_key_aqui
VERCEL_ENV=production
DEBUG=false
```

### **4. Configurações de Build**
- **Framework Preset**: Other
- **Build Command**: `pip install -r requirements.txt`
- **Output Directory**: `api`
- **Install Command**: `pip install -r requirements.txt`

## ⚡ **Otimizações Implementadas**

### **1. Processamento em Chunks**
```python
# Processa dados em partes para economizar memória
CHUNK_SIZE = 1000
MAX_ROWS = 50000
```

### **2. Limpeza Automática de Memória**
```python
# Limpa cache a cada 5 minutos
CACHE_TIMEOUT = 300
AUTO_CLEANUP = True
```

### **3. Verificação de Recursos**
```python
# Verifica se há memória suficiente
def check_resources():
    memory = psutil.virtual_memory()
    return memory.available > 100 * 1024 * 1024
```

### **4. Timeout Inteligente**
```python
# Para processamento antes do limite do Vercel
MAX_PROCESSING_TIME = 25  # 25s (deixar margem para 30s)
```

## 🔧 **Solução de Problemas**

### **Erro: "Function Timeout"**
**Causa**: Processamento demorou mais de 30 segundos
**Solução**:
1. Reduza o tamanho dos arquivos
2. Use menos dados para teste
3. Verifique se não há loops infinitos

### **Erro: "Memory Limit Exceeded"**
**Causa**: Uso de memória acima de 1024MB
**Solução**:
1. Processe dados em chunks menores
2. Remova dependências desnecessárias
3. Limpe variáveis globais

### **Erro: "Cold Start"**
**Causa**: Primeira execução lenta
**Solução**:
1. Use funções menores
2. Minimize imports
3. Cache dados quando possível

## 📊 **Monitoramento**

### **1. Logs do Vercel**
```bash
# Ver logs em tempo real
vercel logs --follow
```

### **2. Métricas Importantes**
- ⏱️ **Tempo de resposta**: < 30s
- 💾 **Uso de memória**: < 1024MB
- 🔄 **Taxa de erro**: < 1%

### **3. Alertas Recomendados**
- Tempo de execução > 25s
- Uso de memória > 800MB
- Taxa de erro > 5%

## 🎯 **Boas Práticas**

### **1. Otimização de Código**
```python
# ✅ Bom: Processamento em chunks
for chunk in pd.read_csv(file, chunksize=1000):
    process_chunk(chunk)

# ❌ Ruim: Carregar tudo na memória
df = pd.read_csv(file)  # Pode ser muito grande
```

### **2. Gerenciamento de Memória**
```python
# ✅ Bom: Limpeza automática
import gc
gc.collect()

# ❌ Ruim: Acumular dados
global_data.append(new_data)  # Pode crescer indefinidamente
```

### **3. Tratamento de Erros**
```python
# ✅ Bom: Timeout e fallback
try:
    result = process_data()
except TimeoutError:
    return {"error": "Processamento muito lento"}
```

## 🚀 **URLs de Deploy**

### **Produção**
```
https://zapcampanha.vercel.app
```

### **Preview (desenvolvimento)**
```
https://zapcampanha-git-dev-zapchicken.vercel.app
```

## 📞 **Suporte**

### **Problemas Comuns**
1. **Timeout**: Reduza dados ou otimize código
2. **Memória**: Use chunks e limpeza automática
3. **Cold Start**: Minimize imports e dependências

### **Contato**
- **Vercel Support**: https://vercel.com/support
- **GitHub Issues**: https://github.com/zapchicken/zapcampanha/issues

---

**🎉 Com essas otimizações, o deploy no Vercel deve funcionar sem problemas de overload!**
