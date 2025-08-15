# 🚀 ZapCampanhas - Resumo do Projeto

## 📋 O que foi Criado

O **ZapCampanhas** é um sistema completo de automação para processamento de planilhas Excel e geração de listas de leads otimizadas para campanhas de WhatsApp.

## 🎯 Objetivo Principal

Automatizar tarefas manuais que você faz atualmente com 4 planilhas de Excel para:
- ✅ Ganhar velocidade no processamento
- ✅ Aumentar acertividade na geração de leads
- ✅ Padronizar o formato dos dados
- ✅ Criar links diretos para WhatsApp
- ✅ Segmentar leads automaticamente

## 🏗️ Estrutura do Projeto

```
zapcampanha/
├── 📁 data/
│   ├── 📁 input/          # Suas 4 planilhas vão aqui
│   └── 📁 output/         # Resultados processados
├── 📁 src/                # Código fonte
│   ├── excel_processor.py # Processador de planilhas
│   ├── lead_generator.py  # Gerador de leads
│   └── utils.py          # Utilitários
├── 📁 config/             # Configurações
├── 🐍 main.py             # Arquivo principal
├── 📋 requirements.txt    # Dependências Python
├── 📖 README.md           # Documentação
├── 🔧 INSTALACAO.md       # Guia de instalação
├── 📋 exemplo_uso.md      # Guia de uso
└── 🧪 criar_exemplo.py    # Script para criar dados de teste
```

## ⚡ Funcionalidades Principais

### 1. **Processamento Inteligente de Planilhas**
- Carrega automaticamente todas as planilhas Excel da pasta
- Identifica automaticamente colunas de telefone
- Processa múltiplas abas de cada planilha
- Combina dados de diferentes fontes

### 2. **Limpeza e Padronização**
- Limpa e formata números de telefone
- Padroniza nomes de colunas (nome, telefone, cidade, etc.)
- Remove duplicatas automaticamente
- Valida dados de entrada

### 3. **Geração de Leads para WhatsApp**
- Cria telefones formatados para WhatsApp
- Gera links diretos (https://wa.me/5511999999999)
- Filtra apenas leads com telefones válidos
- Segmenta por cidade automaticamente

### 4. **Interface Amigável**
- Interface de linha de comando intuitiva
- Relatórios visuais com Rich
- Progresso em tempo real
- Mensagens de erro claras

### 5. **Relatórios Detalhados**
- Estatísticas de processamento
- Contagem de leads válidos
- Segmentação por cidade
- Resumo dos dados processados

## 🚀 Como Usar

### Passo 1: Instalação
```bash
# Instalar Python (se não tiver)
# Baixar de: https://www.python.org/downloads/

# Instalar dependências
pip install -r requirements.txt

# Configurar ambiente
python main.py setup
```

### Passo 2: Preparar Planilhas
Coloque suas 4 planilhas em `data/input/`:
- `clientes.xlsx`
- `prospectos.xlsx` 
- `contatos.xlsx`
- `leads.xlsx`

### Passo 3: Processar
```bash
# Processar todas as planilhas
python main.py process

# Ou analisar primeiro
python main.py analyze
```

### Passo 4: Resultados
Os arquivos serão salvos em `data/output/`:
- `leads_whatsapp.xlsx` - Lista principal
- `leads_whatsapp_sao_paulo.xlsx` - Segmento por cidade
- etc.

## 📊 O que o Sistema Faz Automaticamente

1. **Carrega** todas as planilhas Excel
2. **Identifica** colunas de telefone automaticamente
3. **Limpa** e padroniza números de telefone
4. **Combina** dados de múltiplas planilhas
5. **Padroniza** nomes de colunas
6. **Cria** links diretos para WhatsApp
7. **Segmenta** por cidade (se disponível)
8. **Gera** relatórios detalhados
9. **Salva** resultados em Excel

## 🔧 Tecnologias Utilizadas

- **Python 3.8+** - Linguagem principal
- **Pandas** - Processamento de dados
- **OpenPyXL** - Leitura/escrita de Excel
- **Click** - Interface de linha de comando
- **Rich** - Interface visual rica
- **Pathlib** - Manipulação de arquivos

## 📱 Formato de Saída

O sistema gera planilhas com colunas como:
- `nome` - Nome do cliente/lead
- `telefone` - Telefone original
- `telefone_whatsapp` - Telefone formatado
- `link_whatsapp` - Link direto para WhatsApp
- `cidade` - Cidade (se disponível)
- `email` - Email (se disponível)
- Outras colunas das planilhas originais

## 🎯 Benefícios

### Antes (Manual):
- ❌ Processamento lento e manual
- ❌ Erros de digitação
- ❌ Formato inconsistente
- ❌ Sem validação de dados
- ❌ Sem segmentação automática

### Depois (Automatizado):
- ✅ Processamento rápido e automático
- ✅ Dados validados e limpos
- ✅ Formato padronizado
- ✅ Links diretos para WhatsApp
- ✅ Segmentação automática
- ✅ Relatórios detalhados

## 🧪 Teste Rápido

Para testar o sistema sem suas planilhas reais:

```bash
# Criar dados de exemplo
python criar_exemplo.py

# Processar dados de exemplo
python main.py process
```

## 📞 Próximos Passos

1. **Instalar Python** (se necessário)
2. **Instalar dependências**: `pip install -r requirements.txt`
3. **Configurar ambiente**: `python main.py setup`
4. **Colocar suas 4 planilhas** em `data/input/`
5. **Processar**: `python main.py process`
6. **Usar os resultados** para suas campanhas de WhatsApp

## 🎉 Resultado Final

Você terá uma lista de leads limpa, validada e pronta para usar em suas campanhas de WhatsApp, com links diretos para cada contato, tudo processado automaticamente em segundos!

---

**Agora você pode me descrever suas 4 planilhas para que eu possa ajustar o sistema especificamente para o seu caso de uso!** 📋

