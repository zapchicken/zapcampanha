# 🍗 Guia Completo - ZapChicken Business Intelligence

## 📋 Pré-requisitos

### **Arquivos Necessários:**
1. **contacts.csv** - Exportado do Google Contacts
2. **Lista-Clientes*.xls*** - Extraído do sistema da ZapChicken
3. **Todos os pedidos*.xls*** - Histórico de pedidos (6 meses)
4. **Historico_Itens_Vendidos*.xls*** - Itens vendidos (6 meses)

### **Instalação:**
```bash
pip install -r requirements.txt
python main.py setup
```

## 🚀 Passo a Passo

### **1. Preparar Arquivos**
Coloque os 4 arquivos na pasta `data/input/`:
```
data/input/
├── contacts.csv
├── Lista-Clientes 13-08-25 1615.xls
├── Todos os pedidos Data de Abertura [01-02-2025 0000 - 01-08-2025 2359].xls
└── Historico_Itens_Vendidos de 01-02-25 à 01-08-25.xls
```

### **2. Processar Dados**
```bash
# Processamento padrão
python main.py zapchicken

# Com configurações personalizadas
python main.py zapchicken --dias-inatividade 45 --ticket-minimo 75
```

### **3. Chat com IA**
```bash
python main.py chat
```

## 🤖 Comandos do Chat IA

### **📊 Análise de Clientes:**
- `"Quantos clientes inativos temos?"`
- `"Mostre clientes que não compraram nos últimos 30 dias"`
- `"Quem são os clientes com maior ticket médio?"`
- `"Configure dias de inatividade para 60"`

### **💰 Análise de Vendas:**
- `"Qual foi o faturamento dos últimos 6 meses?"`
- `"Quais são os produtos mais vendidos?"`
- `"Mostre a análise de ticket médio"`
- `"Configure ticket médio mínimo para 100"`

### **📍 Análise Geográfica:**
- `"Quais são os bairros que mais pedem?"`
- `"Como estão as vendas por bairro?"`
- `"Mostre a análise geográfica"`

### **🎯 Sugestões de Marketing:**
- `"Dê sugestões para reativar clientes"`
- `"Sugira campanhas para bairros específicos"`
- `"Quais ofertas fazer para clientes premium?"`
- `"Analise tendências de vendas"`

### **⚙️ Configurações:**
- `"Configure dias de inatividade para 60"`
- `"Configure ticket médio mínimo para 100"`
- `"Mostre configurações atuais"`

### **📋 Relatórios:**
- `"Gere relatório completo"`
- `"Salve todos os relatórios"`
- `"Mostre resumo executivo"`

## 📊 Relatórios Gerados

### **1. novos_clientes_google_contacts.csv**
- **Uso**: Importar no Google Contacts
- **Formato**: nome, telefone
- **Exemplo**: "LT_01 Maria", "19999999999"

### **2. clientes_inativos.xlsx**
- **Uso**: Campanhas de reativação
- **Colunas**: telefone, primeiro_nome, bairro, dias_inativo, qtd_pedidos

### **3. clientes_alto_ticket.xlsx**
- **Uso**: Ofertas premium
- **Colunas**: telefone, primeiro_nome, ticket_medio, valor_total, qtd_pedidos

### **4. analise_geografica.xlsx**
- **Uso**: Campanhas Meta por bairro
- **Colunas**: bairro, valor_total, ticket_medio, qtd_pedidos, clientes_unicos

### **5. produtos_mais_vendidos.xlsx**
- **Uso**: Análise de produtos
- **Colunas**: Nome Prod, Qtd, Valor Tot. Item

## 🎯 Casos de Uso

### **Cenário 1: Reativação de Clientes**
```bash
# 1. Processar dados
python main.py zapchicken --dias-inatividade 45

# 2. Chat com IA
python main.py chat

# 3. Perguntar:
"Quantos clientes inativos temos?"
"Dê sugestões para reativar clientes"
```

### **Cenário 2: Campanhas por Bairro**
```bash
# 1. Chat com IA
python main.py chat

# 2. Perguntar:
"Quais são os bairros que mais pedem?"
"Sugira campanhas para bairros específicos"
```

### **Cenário 3: Clientes Premium**
```bash
# 1. Processar com ticket alto
python main.py zapchicken --ticket-minimo 100

# 2. Chat com IA
python main.py chat

# 3. Perguntar:
"Quem são os clientes com maior ticket médio?"
"Quais ofertas fazer para clientes premium?"
```

## ⚙️ Configurações Avançadas

### **Parâmetros Disponíveis:**
- `--dias-inatividade`: Dias para considerar cliente inativo (padrão: 30)
- `--ticket-minimo`: Ticket médio mínimo para análise (padrão: 50.0)

### **Exemplos:**
```bash
# Clientes inativos há 60 dias
python main.py zapchicken --dias-inatividade 60

# Clientes com ticket > R$ 100
python main.py zapchicken --ticket-minimo 100

# Ambos
python main.py zapchicken --dias-inatividade 60 --ticket-minimo 100
```

## 🔧 Solução de Problemas

### **Erro: "Nenhum arquivo da ZapChicken foi carregado"**
- Verifique se os arquivos estão em `data/input/`
- Confirme os nomes dos arquivos
- Execute `python main.py setup`

### **Erro: "Dados insuficientes"**
- Verifique se os arquivos têm dados
- Confirme o período de 6 meses
- Verifique se há telefones válidos

### **Erro: "Telefones inválidos"**
- O sistema filtra automaticamente telefones (00) 0000-0000
- Verifique se há telefones válidos nos arquivos

## 📈 Exemplos de Perguntas Úteis

### **Para Análise de Vendas:**
- `"Qual foi o faturamento dos últimos 6 meses?"`
- `"Quais são os produtos mais vendidos?"`
- `"Como estão as vendas por bairro?"`

### **Para Marketing:**
- `"Dê sugestões para reativar clientes"`
- `"Sugira campanhas para bairros específicos"`
- `"Quais ofertas fazer para clientes premium?"`

### **Para Configuração:**
- `"Configure dias de inatividade para 60"`
- `"Configure ticket médio mínimo para 100"`
- `"Mostre configurações atuais"`

### **Para Relatórios:**
- `"Gere relatório completo"`
- `"Salve todos os relatórios"`
- `"Mostre resumo executivo"`

## 🎉 Resultados Esperados

### **Após o Processamento:**
1. ✅ **5 relatórios** em Excel na pasta `data/output/`
2. ✅ **Lista de novos clientes** pronta para Google Contacts
3. ✅ **Análise completa** de clientes inativos
4. ✅ **Identificação** de clientes premium
5. ✅ **Sugestões de marketing** baseadas em IA

### **Com o Chat IA:**
1. ✅ **Perguntas em linguagem natural**
2. ✅ **Respostas inteligentes** e contextualizadas
3. ✅ **Sugestões automáticas** de campanhas
4. ✅ **Análise preditiva** de tendências

---

**🚀 Transforme seus dados da ZapChicken em insights inteligentes para aumentar as vendas!**
