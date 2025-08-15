# 🔧 Solução de Problemas - ZapCampanhas

## Problema: "Funcionou mas agora não funciona mais"

### 1. Verificação Básica

#### ✅ Status Atual (Confirmado Funcionando):
- ✅ Python 3.11.9
- ✅ Flask 2.3.3
- ✅ Pandas 2.0.3
- ✅ Todos os diretórios existem
- ✅ Template HTML válido
- ✅ Servidor Flask inicia corretamente

### 2. Possíveis Causas e Soluções

#### 🔍 Problema 1: Porta em Uso
```bash
# Verificar se a porta 5000 está em uso
netstat -ano | findstr :5000

# Se estiver em uso, mate o processo
taskkill /PID [PID_NUMBER] /F
```

#### 🔍 Problema 2: Cache do Navegador
- Pressione `Ctrl + F5` para forçar recarregamento
- Ou abra em aba anônima/privada
- Ou limpe o cache do navegador

#### 🔍 Problema 3: Dependências Desatualizadas
```bash
# Reinstalar dependências
pip install -r requirements.txt --upgrade
```

#### 🔍 Problema 4: Arquivos Corrompidos
```bash
# Executar diagnóstico
python diagnostico.py
```

### 3. Comandos de Teste

#### 🚀 Teste Básico do Flask:
```bash
python test_flask_simple.py
```

#### 🚀 Teste do Template:
```bash
python teste_template.py
```

#### 🚀 Teste Completo:
```bash
python web_app_flask.py
```

### 4. Verificação de Funcionalidades

#### 📁 Upload de Arquivos:
- Verificar se os diretórios `data/input` e `data/output` existem
- Verificar permissões de escrita

#### 🔄 Processamento de Dados:
- Verificar se todos os arquivos necessários estão presentes
- Verificar se há erros no console

#### 🤖 Chat com IA:
- Verificar se a API key do Gemini está configurada
- Verificar conexão com internet

### 5. Logs e Debug

#### 📋 Verificar Logs:
```bash
# Executar com debug ativado
python web_app_flask.py
```

#### 📋 Verificar Console do Navegador:
- Pressione `F12` no navegador
- Vá para a aba "Console"
- Verifique se há erros JavaScript

### 6. Soluções Específicas

#### 🔧 Se o upload não funciona:
1. Verificar se os arquivos são do tipo correto (.csv, .xlsx, .xls)
2. Verificar se os nomes dos arquivos estão corretos
3. Verificar se há espaço suficiente no disco

#### 🔧 Se o processamento falha:
1. Verificar se todos os 4 arquivos foram carregados
2. Verificar se os arquivos não estão corrompidos
3. Verificar se há memória suficiente

#### 🔧 Se o chat não funciona:
1. Verificar se a API key do Gemini está correta
2. Verificar se há conexão com internet
3. Verificar se a API não atingiu o limite de uso

### 7. Contato e Suporte

Se nenhuma das soluções acima funcionar:

1. Execute o diagnóstico completo:
   ```bash
   python diagnostico.py
   ```

2. Verifique os logs de erro no console

3. Teste com arquivos de exemplo

4. Se necessário, reinstale as dependências:
   ```bash
   pip uninstall -r requirements.txt
   pip install -r requirements.txt
   ```

### 8. Status Atual do Sistema

✅ **Funcionando:**
- Servidor Flask
- Template HTML
- Estrutura de diretórios
- Dependências básicas

❓ **Verificar:**
- Funcionalidades específicas que não estão funcionando
- Logs de erro específicos
- Problemas de rede/conexão

---

**💡 Dica:** Se você puder me dizer exatamente qual funcionalidade não está funcionando, posso ajudar de forma mais específica!
