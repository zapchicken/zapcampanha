# Teste de Upload - ZapCampanhas

## Problemas Identificados e Corrigidos:

### ✅ **Problemas Corrigidos:**
1. **Rota de upload**: Corrigida de `/upload` para `/upload_file`
2. **Rota de processamento**: Corrigida de `/process` para `/process_data`
3. **Formulário HTML**: Corrigido para chamar a rota correta
4. **Tamanho máximo de upload**: Configurado para 50MB
5. **Logs de debug**: Adicionados para identificar problemas

### 🔧 **Como Testar:**

#### 1. **Iniciar o servidor simplificado:**
```bash
python web_app_flask_simple.py
```

#### 2. **Acessar o site:**
```
http://localhost:5000
```

#### 3. **Testar upload:**
- Faça upload dos 4 arquivos da ZapChicken:
  - **Contacts** (Google Contacts) - arquivo CSV
  - **Lista de Clientes** - arquivo Excel
  - **Histórico de Pedidos** - arquivo Excel
  - **Histórico de Itens** - arquivo Excel

#### 4. **Processar dados:**
- Configure os parâmetros (dias de inatividade, ticket mínimo)
- Clique em "Processar Dados"

#### 5. **Verificar relatórios:**
- Os relatórios devem aparecer na aba "Relatórios"

### 🐛 **Se ainda houver problemas:**

#### **Verificar logs no terminal:**
- O servidor mostra logs detalhados
- Procure por mensagens de erro

#### **Verificar arquivos:**
- Os arquivos são salvos em `data/input/`
- Os relatórios são gerados em `data/output/`

#### **Teste simples:**
```bash
python test_upload.py
```
- Acesse `http://localhost:5001`
- Teste upload de qualquer arquivo

### 📁 **Estrutura de Arquivos Esperada:**
```
data/
├── input/
│   ├── contacts.csv
│   ├── Lista-Clientes.xlsx
│   ├── Todos os pedidos.xlsx
│   └── Historico_Itens_Vendidos.xlsx
└── output/
    ├── novos_clientes_google_contacts.csv
    ├── clientes_inativos.xlsx
    └── clientes_alto_ticket.xlsx
```

### 🔍 **Debug:**
- Verifique o console do navegador (F12)
- Verifique os logs do servidor no terminal
- Verifique se os arquivos estão sendo salvos corretamente

### 📞 **Se precisar de ajuda:**
- Compartilhe os logs de erro
- Descreva exatamente o que acontece quando tenta fazer upload
- Verifique se os arquivos têm as extensões corretas (.csv, .xlsx, .xls)
