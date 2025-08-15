# 🚀 Guia de Execução Local - ZapCampanhas

## 📋 Pré-requisitos

### 1. Python 3.8 ou superior
- **Baixe em:** https://www.python.org/downloads/
- **IMPORTANTE:** Durante a instalação, marque ✅ "Add Python to PATH"
- **Verifique:** Abra o PowerShell e digite `python --version`

### 2. Git (opcional)
- Para clonar o repositório: https://git-scm.com/download/win

## 🔧 Instalação Passo a Passo

### Passo 1: Preparar o Ambiente

Abra o PowerShell como **Administrador** e navegue até a pasta do projeto:

```powershell
# Navegar para a pasta do projeto
cd "C:\Users\joao_\Desktop\zapcampanha-main"

# Verificar se está na pasta correta
dir
```

### Passo 2: Instalar Dependências

```powershell
# Instalar todas as dependências
pip install -r requirements.txt

# Se der erro de permissão, use:
pip install -r requirements.txt --user
```

### Passo 3: Configurar o Ambiente

```powershell
# Configurar diretórios e ambiente
python main.py setup
```

### Passo 4: Verificar Instalação

```powershell
# Testar se tudo está funcionando
python main.py --help
```

## 📁 Preparar Arquivos de Dados

### 1. Criar Estrutura de Pastas

O programa criará automaticamente:
```
zapcampanha-main/
├── data/
│   ├── input/          # ← Coloque suas planilhas aqui
│   └── output/         # ← Resultados serão salvos aqui
```

### 2. Colocar Arquivos da ZapChicken

Mova os 4 arquivos para `data/input/`:

1. **contacts.csv** - Lista do Google Contacts
2. **Lista-Clientes*.xlsx** - Lista de clientes do sistema
3. **Todos os pedidos*.xlsx** - Histórico de pedidos
4. **Historico_Itens_Vendidos*.xlsx** - Itens vendidos

```powershell
# Copiar arquivos para a pasta input
copy "arquivos upload\contacts (3).csv" "data\input\contacts.csv"
copy "arquivos upload\Lista-Clientes 13-08-25 1615.xlsx" "data\input\Lista-Clientes.xlsx"
copy "arquivos upload\Todos os pedidos  Data de Abertura [01-02-2025 0000 - 01-08-2025 2359].xlsx" "data\input\Todos os pedidos.xlsx"
copy "arquivos upload\Historico_Itens_Vendidos de 01-02-25 à 01-08-25.xlsx" "data\input\Historico_Itens_Vendidos.xlsx"
```

## 🚀 Executar o Programa

### Opção 1: Processamento Completo da ZapChicken

```powershell
# Processar todos os dados da ZapChicken
python main.py zapchicken
```

### Opção 2: Com Parâmetros Personalizados

```powershell
# Configurar dias de inatividade e ticket mínimo
python main.py zapchicken --dias-inatividade 60 --ticket-minimo 100
```

### Opção 3: Chat com IA

```powershell
# Iniciar assistente inteligente
python main.py chat
```

### Opção 4: Processamento Genérico

```powershell
# Para qualquer planilha Excel
python main.py process
```

## 🎯 Exemplos de Uso

### 1. Primeira Execução

```powershell
# 1. Configurar ambiente
python main.py setup

# 2. Processar dados da ZapChicken
python main.py zapchicken

# 3. Ver resultados em data/output/
dir data\output\
```

### 2. Chat com IA

```powershell
# Iniciar chat
python main.py chat

# Perguntas que você pode fazer:
# "Quantos clientes inativos temos?"
# "Quem são os clientes com maior ticket médio?"
# "Quais são os bairros que mais pedem?"
# "Dê sugestões para reativar clientes"
# "Gere relatório completo"
```

### 3. Análise Personalizada

```powershell
# Clientes inativos há 45 dias
python main.py zapchicken --dias-inatividade 45

# Clientes com ticket médio acima de R$ 75
python main.py zapchicken --ticket-minimo 75

# Combinação de parâmetros
python main.py zapchicken --dias-inatividade 45 --ticket-minimo 75
```

## 📊 Resultados Esperados

Após a execução, você encontrará em `data/output/`:

1. **novos_clientes_google_contacts.csv** - Lista para importar no Google Contacts
2. **clientes_inativos.xlsx** - Clientes sem pedido em X dias
3. **clientes_alto_ticket.xlsx** - Clientes com ticket médio > X
4. **analise_geografica.xlsx** - Dados por bairro
5. **produtos_mais_vendidos.xlsx** - Ranking de produtos

## 🔧 Solução de Problemas

### Erro: "Python não foi encontrado"

```powershell
# Verificar se Python está instalado
python --version

# Se não funcionar, reinstale o Python marcando "Add to PATH"
```

### Erro: "Módulo não encontrado"

```powershell
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Erro: "Permission denied"

```powershell
# Executar PowerShell como Administrador
# Ou usar --user
pip install -r requirements.txt --user
```

### Erro: "Arquivo não encontrado"

```powershell
# Verificar se os arquivos estão na pasta correta
dir data\input\

# Se não estiverem, copie-os:
copy "arquivos upload\*" "data\input\"
```

### Erro: "Encoding"

```powershell
# Se houver problemas com caracteres especiais
# Verifique se os arquivos estão em UTF-8
```

## 🎉 Próximos Passos

1. ✅ **Instalar Python e dependências**
2. ✅ **Configurar ambiente** (`python main.py setup`)
3. ✅ **Colocar arquivos em data/input/**
4. ✅ **Executar processamento** (`python main.py zapchicken`)
5. ✅ **Verificar resultados em data/output/**
6. ✅ **Usar chat com IA** (`python main.py chat`)

## 📞 Comandos Úteis

```powershell
# Ver ajuda
python main.py --help

# Ver comandos disponíveis
python main.py --help

# Verificar versão
python main.py --version

# Listar arquivos de entrada
dir data\input\

# Listar resultados
dir data\output\
```

## 🚀 Dicas Importantes

1. **Sempre execute o PowerShell como Administrador** na primeira vez
2. **Verifique se os arquivos estão no formato correto** (.xlsx, .csv)
3. **Mantenha backup dos arquivos originais**
4. **Use o chat com IA** para dúvidas sobre os dados
5. **Verifique os logs** se algo der errado

---

**🎯 Agora você está pronto para usar o ZapCampanhas localmente!**
