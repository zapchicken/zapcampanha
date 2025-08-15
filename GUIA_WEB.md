# 🌐 ZapCampanhas - Interface Web

## 🚀 Como Usar a Interface Web

### 1. Iniciar o Servidor Web

```bash
python main.py web
```

### 2. Acessar a Interface

Abra seu navegador e acesse: **http://localhost:8050**

---

## 📱 Funcionalidades da Interface Web

### 🏠 **Página Principal**
- **Header**: Logo e título do sistema
- **Navegação por Abas**: 4 seções principais

---

### 📁 **Aba 1: Upload e Processamento**

#### **Upload de Arquivos**
- **Drag & Drop**: Arraste os arquivos diretamente para as áreas
- **Clique para Selecionar**: Clique nas áreas para escolher arquivos
- **4 Arquivos Necessários**:
  1. **Contacts** (Google Contacts) - CSV
  2. **Lista de Clientes** - Excel
  3. **Histórico de Pedidos** - Excel
  4. **Histórico de Itens** - Excel

#### **Configurações**
- **Dias para Inatividade**: Slider de 7 a 90 dias (padrão: 30)
- **Ticket Médio Mínimo**: Slider de R$ 20 a R$ 200 (padrão: R$ 50)

#### **Processamento**
- **Botão "🚀 Processar Dados"**: Inicia a análise
- **Status em Tempo Real**: Mostra progresso e resultados
- **Resumo dos Dados**: Métricas principais após processamento

---

### 📈 **Aba 2: Dashboard**

#### **Métricas Principais**
- **Total de Clientes**: Número total de clientes
- **Clientes Inativos**: Clientes sem compras recentes
- **Alto Ticket**: Clientes com ticket médio alto
- **Novos Clientes**: Clientes para adicionar ao Google Contacts

#### **Gráficos Interativos**
- **Gráfico de Bairros**: Top bairros por vendas
- **Gráfico de Produtos**: Produtos mais vendidos
- **Gráfico de Evolução**: Evolução das vendas no tempo

---

### 📄 **Aba 3: Relatórios**

#### **Downloads Disponíveis**
- **📱 Novos Clientes**: CSV para Google Contacts
- **⚠️ Clientes Inativos**: Excel para campanhas de reativação
- **💎 Alto Ticket**: Excel para ofertas premium
- **🗺️ Análise Geográfica**: Excel para campanhas Meta
- **🔥 Produtos Mais Vendidos**: Excel para análise de preferências

---

### 🤖 **Aba 4: IA Chat**

#### **Chat Interativo**
- **Interface de Chat**: Conversa com IA sobre seus dados
- **Perguntas Sugeridas**:
  - "Quantos clientes inativos temos?"
  - "Quais são os produtos mais vendidos?"
  - "Dê sugestões para reativar clientes"
  - "Mostre a análise geográfica"
  - "Gere relatório completo"

---

## 🎨 **Características da Interface**

### **Design Responsivo**
- ✅ Funciona em desktop, tablet e celular
- ✅ Interface moderna com Bootstrap
- ✅ Cores e ícones intuitivos

### **Usabilidade**
- ✅ Upload por drag & drop
- ✅ Configurações visuais (sliders)
- ✅ Feedback em tempo real
- ✅ Gráficos interativos
- ✅ Downloads diretos

### **Performance**
- ✅ Processamento assíncrono
- ✅ Cache de dados
- ✅ Otimização de memória

---

## 🔧 **Configurações Avançadas**

### **Porta do Servidor**
Por padrão, o servidor roda na porta **8050**

### **Acesso Remoto**
Para acessar de outros dispositivos na rede:
```bash
# O servidor já está configurado para aceitar conexões externas
# Acesse: http://SEU_IP:8050
```

### **Logs**
- Logs de erro aparecem no terminal
- Logs de processamento na interface web

---

## 🚨 **Solução de Problemas**

### **Erro de Importação**
```bash
pip install flask dash dash-bootstrap-components
```

### **Porta Ocupada**
Se a porta 8050 estiver ocupada, edite o arquivo `web_app.py`:
```python
app.run_server(debug=True, host='0.0.0.0', port=8051)  # Mude para 8051
```

### **Arquivos Não Carregam**
- Verifique se os arquivos estão no formato correto
- Certifique-se de que os nomes dos arquivos estão corretos
- Tente recarregar a página

---

## 📱 **Compatibilidade**

### **Navegadores Suportados**
- ✅ Chrome (recomendado)
- ✅ Firefox
- ✅ Safari
- ✅ Edge

### **Dispositivos**
- ✅ Desktop (Windows, Mac, Linux)
- ✅ Tablet (iPad, Android)
- ✅ Celular (iPhone, Android)

---

## 🎯 **Próximos Passos**

1. **Execute**: `python main.py web`
2. **Acesse**: http://localhost:8050
3. **Faça upload** dos 4 arquivos da ZapChicken
4. **Configure** os parâmetros desejados
5. **Processe** os dados
6. **Analise** os resultados no dashboard
7. **Baixe** os relatórios necessários
8. **Use** o chat com IA para insights

---

## 💡 **Dicas de Uso**

- **Primeira vez**: Use a aba "Upload e Processamento"
- **Análise rápida**: Use o dashboard para visão geral
- **Relatórios**: Baixe os arquivos Excel para análise detalhada
- **Perguntas**: Use o chat IA para insights específicos
- **Configurações**: Ajuste os parâmetros conforme sua necessidade

---

**🎉 Interface Web Pronta! Agora você tem uma ferramenta completa e moderna para gerenciar seus dados da ZapChicken!**
