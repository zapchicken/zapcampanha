# 🔧 Guia de Instalação - ZapCampanhas

## 📋 Pré-requisitos

### 1. Instalar Python

**Windows:**
1. Baixe o Python 3.8+ em: https://www.python.org/downloads/
2. Durante a instalação, **marque a opção "Add Python to PATH"**
3. Verifique a instalação abrindo o PowerShell e digitando: `python --version`

**Alternativa - Microsoft Store:**
- Abra a Microsoft Store
- Procure por "Python 3.11" ou versão mais recente
- Clique em "Instalar"

### 2. Verificar Instalação

Abra o PowerShell e execute:
```bash
python --version
pip --version
```

Se aparecer "Python não foi encontrado", você precisa:
1. Reinstalar o Python marcando "Add to PATH"
2. Ou adicionar manualmente o Python ao PATH do sistema

## 🚀 Instalação do Projeto

### 1. Baixar o Projeto

Se você ainda não tem o projeto:
```bash
git clone [URL_DO_REPOSITORIO]
cd zapcampanha
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar Ambiente

```bash
python main.py setup
```

## 🧪 Testar Instalação

### 1. Verificar se tudo está funcionando:

```bash
python main.py --help
```

Você deve ver algo como:
```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  ZapCampanhas - Automação para processamento de planilhas Excel

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  analyze   Analisa as planilhas sem processar
  process   Processa planilhas Excel e gera lista de leads
  setup     Configura o ambiente inicial
```

### 2. Testar com dados de exemplo:

Crie uma planilha de teste em `data/input/teste.xlsx` com:
- Coluna "nome" 
- Coluna "telefone"
- Alguns dados de exemplo

Depois execute:
```bash
python main.py process
```

## 🔧 Solução de Problemas

### Erro: "Python não foi encontrado"

**Solução 1 - Reinstalar Python:**
1. Desinstale o Python atual
2. Baixe novamente de https://www.python.org/downloads/
3. **IMPORTANTE:** Marque "Add Python to PATH" durante a instalação
4. Reinicie o PowerShell

**Solução 2 - Adicionar ao PATH manualmente:**
1. Abra "Configurações do Sistema" > "Variáveis de Ambiente"
2. Em "Variáveis do Sistema", encontre "Path"
3. Clique em "Editar" e adicione:
   - `C:\Users\[SEU_USUARIO]\AppData\Local\Programs\Python\Python311\`
   - `C:\Users\[SEU_USUARIO]\AppData\Local\Programs\Python\Python311\Scripts\`
4. Reinicie o PowerShell

### Erro: "pip não foi encontrado"

Execute:
```bash
python -m pip install --upgrade pip
```

### Erro: "Módulo não encontrado"

Reinstale as dependências:
```bash
pip install -r requirements.txt --force-reinstall
```

### Erro: "Permission denied"

Execute o PowerShell como Administrador e tente novamente.

## 📁 Estrutura do Projeto

Após a instalação, você terá:

```
zapcampanha/
├── data/
│   ├── input/          # Coloque suas planilhas aqui
│   └── output/         # Resultados serão salvos aqui
├── src/                # Código fonte
├── config/             # Configurações
├── main.py             # Arquivo principal
├── requirements.txt    # Dependências
└── README.md           # Documentação
```

## 🎯 Próximos Passos

1. ✅ Instalar Python
2. ✅ Instalar dependências
3. ✅ Configurar ambiente
4. 📋 Colocar suas 4 planilhas em `data/input/`
5. 🚀 Executar: `python main.py process`

## 📞 Suporte

Se ainda tiver problemas:
1. Verifique se o Python está instalado: `python --version`
2. Verifique se pip está funcionando: `pip --version`
3. Tente reinstalar as dependências: `pip install -r requirements.txt --force-reinstall`

