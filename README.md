# 🍗 ZapCampanhas - Business Intelligence para Food Service

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Sistema completo de Business Intelligence para restaurantes e food service, com IA integrada e análise avançada de dados.**

## 🚀 Funcionalidades Principais

### 📊 **Análise de Dados**
- **Processamento automático** de dados de vendas, clientes e produtos
- **Análise geográfica** por bairros e regiões
- **Segmentação RFM** de clientes
- **Análise de produtos** mais vendidos
- **Identificação de clientes inativos** e oportunidades

### 🤖 **Inteligência Artificial**
- **IA Gemini integrada** para análises preditivas
- **Chat inteligente** para consultas em linguagem natural
- **Machine Learning** para previsões de vendas
- **Insights estratégicos** automatizados

### 🌐 **Interface Web**
- **Dashboard interativo** com gráficos e métricas
- **Upload de arquivos** drag & drop
- **Relatórios automáticos** em Excel e CSV
- **Interface responsiva** para desktop e mobile

### 📱 **Integrações**
- **Google Contacts** - Exportação automática de novos clientes
- **Meta Ads** - Dados para campanhas geográficas
- **WhatsApp Business** - Listas para campanhas
- **Excel/CSV** - Relatórios prontos para uso

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.8+, Flask, Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **IA**: Google Gemini API, Machine Learning
- **Visualização**: Plotly, Dash
- **Dados**: Excel, CSV, JSON

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/zapchicken/zapcampanha.git
cd zapcampanha

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure o ambiente
python main.py setup

# 4. Execute o sistema
python main.py web
```

### Instalação Detalhada

Veja o guia completo em [INSTALACAO.md](INSTALACAO.md)

## 🎯 Como Usar

### 1. **Execução Local**
```bash
# Interface web (recomendado)
python main.py web

# Interface CLI
python main.py zapchicken

# Chat com IA
python main.py chat
```

### 2. **Upload de Dados**
- **Contacts.csv** - Lista de contatos do Google
- **Lista-Clientes.xlsx** - Base de clientes
- **Todos os pedidos.xlsx** - Histórico de vendas
- **Historico_Itens_Vendidos.xlsx** - Produtos vendidos

### 3. **Configuração da IA**
1. Obtenha API key gratuita em: https://makersuite.google.com/app/apikey
2. Configure na interface web
3. Faça perguntas em linguagem natural

## 📊 Relatórios Gerados

### **📱 Novos Clientes**
- CSV para importar no Google Contacts
- Clientes que ainda não estão na base

### **⚠️ Clientes Inativos**
- Excel para campanhas de reativação
- Clientes sem compras recentes

### **💎 Alto Ticket**
- Excel para ofertas premium
- Clientes com maior valor médio

### **🗺️ Análise Geográfica**
- Excel para campanhas Meta Ads
- Dados por bairro e região

### **🔥 Produtos Mais Vendidos**
- Excel para análise de preferências
- Ranking de produtos por vendas

## 🤖 IA Gemini - Perguntas Exemplo

### **Análise de Vendas**
- "Preveja as vendas dos próximos 3 meses"
- "Qual foi o crescimento mês a mês?"
- "Quais são os melhores horários de vendas?"

### **Análise de Clientes**
- "Faça segmentação RFM dos clientes"
- "Quem são os clientes VIP?"
- "Como reativar clientes inativos?"

### **Estratégias de Marketing**
- "Gere estratégias de marketing personalizadas"
- "Quais campanhas fazer por bairro?"
- "Como aumentar o ticket médio?"

## 🏗️ Estrutura do Projeto

```
zapcampanha/
├── 📁 src/                    # Código fonte principal
│   ├── zapchicken_processor.py    # Processamento de dados
│   ├── zapchicken_ai_gemini.py    # IA Gemini
│   ├── zapchicken_ai_advanced.py  # IA avançada
│   └── utils.py                   # Utilitários
├── 📁 data/                   # Dados de entrada/saída
│   ├── input/                     # Arquivos de entrada
│   └── output/                    # Relatórios gerados
├── 📁 templates/              # Templates HTML
├── 📁 config/                 # Configurações
├── 📁 api/                    # API REST
├── 🌐 web_app_flask.py        # Interface web Flask
├── 📊 web_app.py              # Interface web Dash
├── 🚀 main.py                 # CLI principal
└── 📋 requirements.txt        # Dependências
```

## 🔧 Configuração

### **Variáveis de Ambiente**
```bash
# API Gemini (opcional)
GEMINI_API_KEY=sua_api_key_aqui

# Configurações do sistema
DIAS_INATIVIDADE=30
TICKET_MEDIO_MINIMO=50
```

### **Parâmetros de Processamento**
- **Dias de Inatividade**: 7-90 dias (padrão: 30)
- **Ticket Médio Mínimo**: R$ 20-200 (padrão: R$ 50)

## 📈 Métricas Disponíveis

### **Vendas**
- Receita total e por período
- Ticket médio por origem
- Crescimento mês a mês
- Análise sazonal

### **Clientes**
- Total de clientes únicos
- Segmentação por valor
- Análise de frequência
- Mapeamento geográfico

### **Produtos**
- Ranking de vendas
- Análise por categoria
- Produtos estrela
- Oportunidades de crescimento

## 🚀 Deploy

### **Local (Desenvolvimento)**
```bash
python main.py web
# Acesse: http://localhost:5000
```

### **Vercel (Produção)**
```bash
# Configure vercel.json
vercel --prod
```

### **Docker**
```bash
docker build -t zapcampanha .
docker run -p 5000:5000 zapcampanha
```

## 🤝 Contribuição

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. Abra um **Pull Request**

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🆘 Suporte

### **Documentação**
- [Guia de Instalação](INSTALACAO.md)
- [Guia da API Gemini](GUIA_GEMINI_API.md)
- [Guia Web](GUIA_WEB.md)
- [Exemplo de Uso](exemplo_uso.md)

### **Problemas Comuns**
- [Solução de Problemas](TROUBLESHOOTING.md)
- [FAQ](FAQ.md)

### **Contato**
- **Issues**: [GitHub Issues](https://github.com/zapchicken/zapcampanha/issues)
- **Email**: suporte@zapchicken.com

## 🎉 Agradecimentos

- **Google Gemini** pela API de IA
- **Flask** pelo framework web
- **Pandas** pelo processamento de dados
- **Plotly** pela visualização

---

**⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!**

**🍗 Desenvolvido com ❤️ para a comunidade de food service**

