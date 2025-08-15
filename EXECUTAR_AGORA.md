# 🚀 EXECUTAR ZAPCAMPANHAS AGORA

## ⚡ Instalação Rápida (3 minutos)

### Opção 1: Script Automático (Recomendado)
```powershell
# Clique duplo no arquivo:
instalar_local.bat
```

### Opção 2: PowerShell (Mais Robusto)
```powershell
# Execute como Administrador:
.\instalar_local.ps1
```

### Opção 3: Manual (Se os scripts falharem)
```powershell
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar ambiente
python main.py setup

# 3. Copiar arquivos
copy "arquivos upload\*" "data\input\"
```

## 🎯 Executar o Programa

### Processamento Completo da ZapChicken
```powershell
python main.py zapchicken
```

### Chat com IA
```powershell
python main.py chat
```

### Ver Ajuda
```powershell
python main.py --help
```

## 📁 Estrutura de Arquivos

```
zapcampanha-main/
├── data/
│   ├── input/          # ← Suas planilhas aqui
│   └── output/         # ← Resultados aqui
├── instalar_local.bat  # ← Clique duplo para instalar
├── instalar_local.ps1  # ← PowerShell (Administrador)
└── main.py            # ← Programa principal
```

## 🔧 Solução Rápida de Problemas

### Python não encontrado
- Baixe em: https://www.python.org/downloads/
- **IMPORTANTE:** Marque "Add Python to PATH"

### Erro de permissão
```powershell
pip install -r requirements.txt --user
```

### Arquivos não encontrados
```powershell
# Verificar se estão na pasta correta
dir data\input\
```

## 📊 Resultados Esperados

Após executar `python main.py zapchicken`, você terá em `data/output/`:

1. **novos_clientes_google_contacts.csv** - Para importar no Google Contacts
2. **clientes_inativos.xlsx** - Clientes para reativar
3. **clientes_alto_ticket.xlsx** - Clientes premium
4. **analise_geografica.xlsx** - Dados por bairro
5. **produtos_mais_vendidos.xlsx** - Ranking de produtos

## 🎉 Pronto!

Agora você pode:
- ✅ Processar dados da ZapChicken
- ✅ Gerar relatórios automáticos
- ✅ Usar chat com IA
- ✅ Analisar clientes inativos
- ✅ Identificar clientes premium

---

**🚀 Transforme seus dados em insights inteligentes!**
