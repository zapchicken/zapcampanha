# 🌐 Como Ver o ZapCampanhas no Navegador

## 🚀 Executar a Interface Web

### Opção 1: Comando Direto (Recomendado)
```powershell
# Execute este comando na pasta do projeto:
python main.py web
```

### Opção 2: Executar Arquivo Web Direto
```powershell
# Se o comando acima não funcionar, execute:
python web_app_flask.py
```

### Opção 3: Interface Dash (Mais Moderna)
```powershell
# Para interface mais moderna com gráficos:
python web_app.py
```

## 📱 Acessar no Navegador

Após executar um dos comandos acima, abra seu navegador e acesse:

### **URL Principal:**
```
http://localhost:5000
```

### **URLs Alternativas:**
```
http://127.0.0.1:5000
http://localhost:8050  (para interface Dash)
```

## 🎯 O que você verá na Interface Web

### **Página Principal:**
- 🍗 **Header**: Logo e título "ZapCampanhas"
- 📁 **Upload de Arquivos**: 4 áreas para upload
- ⚙️ **Configurações**: Sliders para ajustar parâmetros
- 🚀 **Botão Processar**: Para iniciar a análise
- 📊 **Resultados**: Métricas e relatórios

### **Funcionalidades Disponíveis:**

#### **1. Upload de Arquivos**
- **Drag & Drop**: Arraste os arquivos diretamente
- **Clique para Selecionar**: Escolha os arquivos
- **4 Arquivos Necessários**:
  1. **Contacts** (Google Contacts) - CSV
  2. **Lista de Clientes** - Excel
  3. **Histórico de Pedidos** - Excel
  4. **Histórico de Itens** - Excel

#### **2. Configurações**
- **Dias para Inatividade**: 7 a 90 dias (padrão: 30)
- **Ticket Médio Mínimo**: R$ 20 a R$ 200 (padrão: R$ 50)

#### **3. Processamento**
- **Botão "Processar Dados"**: Inicia a análise
- **Status em Tempo Real**: Mostra progresso
- **Resumo dos Resultados**: Métricas principais

#### **4. Downloads**
- **Relatórios Excel**: Clique para baixar
- **CSV para Google Contacts**: Lista de novos clientes
- **Análises Detalhadas**: Clientes inativos, alto ticket, etc.

## 🔧 Solução de Problemas

### **Erro: "Porta já em uso"**
```powershell
# Pare o servidor atual (Ctrl+C) e tente outra porta:
python web_app_flask.py --port 5001
```

### **Erro: "Módulo não encontrado"**
```powershell
# Instale as dependências web:
pip install flask dash dash-bootstrap-components
```

### **Erro: "Página não carrega"**
```powershell
# Verifique se o servidor está rodando:
# Você deve ver algo como: "Running on http://127.0.0.1:5000"
```

### **Erro: "Arquivos não carregam"**
- Verifique se os arquivos estão no formato correto (.xlsx, .csv)
- Certifique-se de que os nomes dos arquivos estão corretos
- Tente recarregar a página

## 📊 Resultados na Interface Web

Após processar os dados, você verá:

### **Métricas Principais:**
- 📊 **Total de Clientes**
- ⚠️ **Clientes Inativos**
- 💎 **Alto Ticket**
- 📱 **Novos Clientes**

### **Downloads Disponíveis:**
- 📱 **Novos Clientes** (CSV para Google Contacts)
- ⚠️ **Clientes Inativos** (Excel para reativação)
- 💎 **Alto Ticket** (Excel para ofertas premium)
- 🗺️ **Análise Geográfica** (Excel para campanhas Meta)
- 🔥 **Produtos Mais Vendidos** (Excel para análise)

## 🎨 Características da Interface

### **Design Responsivo:**
- ✅ Funciona em desktop, tablet e celular
- ✅ Interface moderna com Bootstrap
- ✅ Cores e ícones intuitivos

### **Usabilidade:**
- ✅ Upload por drag & drop
- ✅ Configurações visuais (sliders)
- ✅ Feedback em tempo real
- ✅ Downloads diretos

## 🚀 Passos para Usar

### **1. Iniciar o Servidor**
```powershell
python main.py web
```

### **2. Abrir o Navegador**
```
http://localhost:5000
```

### **3. Fazer Upload dos Arquivos**
- Arraste os 4 arquivos da ZapChicken
- Ou clique para selecionar

### **4. Configurar Parâmetros**
- Ajuste dias de inatividade
- Configure ticket mínimo

### **5. Processar Dados**
- Clique em "Processar Dados"
- Aguarde o processamento

### **6. Ver Resultados**
- Analise as métricas
- Baixe os relatórios

## 📱 Compatibilidade

### **Navegadores Suportados:**
- ✅ Chrome (recomendado)
- ✅ Firefox
- ✅ Safari
- ✅ Edge

### **Dispositivos:**
- ✅ Desktop (Windows, Mac, Linux)
- ✅ Tablet (iPad, Android)
- ✅ Celular (iPhone, Android)

## 🎯 Dicas Importantes

1. **Mantenha o terminal aberto** enquanto usa a interface web
2. **Use Ctrl+C** para parar o servidor quando terminar
3. **Recarregue a página** se algo não funcionar
4. **Verifique os logs** no terminal se houver problemas
5. **Use Chrome** para melhor compatibilidade

## 🔄 Comandos Úteis

```powershell
# Iniciar interface web
python main.py web

# Parar servidor
Ctrl+C

# Verificar se está rodando
# Deve aparecer: "Running on http://127.0.0.1:5000"

# Acessar de outro dispositivo na rede
# http://SEU_IP:5000
```

---

**🎉 Agora você pode usar o ZapCampanhas com uma interface web moderna e intuitiva!**

**🌐 Acesse http://localhost:5000 e comece a transformar seus dados em insights!**
