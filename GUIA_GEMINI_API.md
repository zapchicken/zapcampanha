# 🤖 Guia de Configuração da API Gemini - ZapCampanhas

## 🎯 O que é a API Gemini?

A **API Gemini** é a inteligência artificial do Google que permite análises muito mais avançadas e inteligentes dos seus dados da ZapChicken. Com ela, você pode:

- 📊 **Análises preditivas** com machine learning
- 🎯 **Segmentação avançada** de clientes
- 💡 **Sugestões inteligentes** de marketing
- 📈 **Previsões de vendas** baseadas em IA
- 🧠 **Insights estratégicos** personalizados

## 🚀 Como Obter a API Key (GRATUITA)

### **Passo 1: Acessar o Google AI Studio**
1. Abra: https://makersuite.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em **"Create API Key"**

### **Passo 2: Criar a API Key**
1. Clique em **"Create API Key in new project"**
2. Digite um nome para o projeto (ex: "ZapCampanhas")
3. Clique em **"Create API Key"**
4. **Copie a API key** gerada (algo como: `AIzaSyC...`)

### **Passo 3: Configurar no ZapCampanhas**
1. Execute o servidor web: `python main.py web`
2. Acesse: http://localhost:5000
3. Vá na aba **"IA Chat"**
4. Cole sua API key no campo de configuração
5. Clique em **"Configurar Gemini"**

## 🔧 Configuração Passo a Passo

### **1. Iniciar o Servidor Web**
```powershell
# Opção 1 - Script automático
iniciar_web.bat

# Opção 2 - Comando direto
python main.py web
```

### **2. Acessar a Interface**
```
http://localhost:5000
```

### **3. Fazer Upload dos Dados**
- Faça upload dos 4 arquivos da ZapChicken
- Clique em **"Processar Dados"**
- Aguarde o processamento

### **4. Configurar API Gemini**
- Vá na aba **"IA Chat"**
- Cole sua API key do Gemini
- Clique em **"Configurar Gemini"**
- Aguarde a confirmação

### **5. Usar a IA Avançada**
Agora você pode fazer perguntas como:
- "Preveja as vendas dos próximos 3 meses"
- "Faça segmentação RFM dos clientes"
- "Analise tendências com machine learning"
- "Gere estratégias de marketing personalizadas"

## 🎯 Exemplos de Perguntas Avançadas

### **Análise Preditiva:**
```
"Preveja as vendas dos próximos 3 meses com base nos dados históricos"
```

### **Segmentação de Clientes:**
```
"Faça uma análise RFM completa e sugira estratégias para cada segmento"
```

### **Análise de Tendências:**
```
"Identifique padrões sazonais e sugira campanhas otimizadas"
```

### **Estratégias de Marketing:**
```
"Gere uma estratégia de reativação para clientes inativos há mais de 60 dias"
```

### **Otimização de Operações:**
```
"Analise os horários de pico e sugira otimizações de equipe"
```

## 🔧 Solução de Problemas

### **Erro: "API key não fornecida"**
- Verifique se copiou a API key completa
- Certifique-se de que não há espaços extras
- Tente colar novamente

### **Erro: "API key inválida"**
- Verifique se a API key está correta
- Certifique-se de que criou a key no Google AI Studio
- Tente criar uma nova API key

### **Erro: "Erro na API"**
- Verifique sua conexão com a internet
- A API pode estar temporariamente indisponível
- Tente novamente em alguns minutos

### **Erro: "Dados não processados"**
- Faça upload dos arquivos da ZapChicken primeiro
- Clique em "Processar Dados"
- Configure a API Gemini depois

## 💡 Dicas Importantes

### **Segurança:**
- ✅ A API key é gratuita e segura
- ✅ Não compartilhe sua API key publicamente
- ✅ Você pode revogar a key a qualquer momento

### **Limites Gratuitos:**
- 📊 **60 requisições por minuto** (mais que suficiente)
- 💰 **Totalmente gratuito** para uso pessoal
- 🔄 **Sem limite mensal** para análises

### **Performance:**
- ⚡ Respostas em segundos
- 🧠 Análises muito mais inteligentes
- 📈 Insights estratégicos avançados

## 🎉 Benefícios da API Gemini

### **Antes (Análise Básica):**
- 📊 Métricas simples
- 📈 Gráficos básicos
- 📋 Relatórios estáticos

### **Depois (IA Avançada):**
- 🤖 Análises preditivas
- 🎯 Segmentação inteligente
- 💡 Sugestões estratégicas
- 📊 Insights personalizados
- 🚀 Recomendações de ação

## 🔄 Comandos Úteis

```powershell
# Iniciar servidor web
python main.py web

# Verificar status da API
# (na interface web, aba IA Chat)

# Limpar cache se necessário
# (na interface web, botão "Limpar Cache")
```

## 📞 Suporte

Se ainda tiver problemas:

1. **Verifique a conexão** com a internet
2. **Confirme a API key** está correta
3. **Processe os dados** primeiro
4. **Tente recarregar** a página
5. **Verifique os logs** no terminal

---

**🎯 Agora você tem acesso à IA mais avançada do Google para analisar seus dados da ZapChicken!**

**🚀 Configure a API Gemini e transforme seus dados em insights estratégicos inteligentes!**
