# 📋 Guia de Uso - ZapCampanhas

## 🚀 Como Usar

### 1. Configuração Inicial

Primeiro, configure o ambiente:

```bash
python main.py setup
```

### 2. Preparar as Planilhas

Coloque suas 4 planilhas Excel na pasta `data/input/`:
- Planilha 1: `clientes.xlsx`
- Planilha 2: `prospectos.xlsx` 
- Planilha 3: `contatos.xlsx`
- Planilha 4: `leads.xlsx`

### 3. Analisar as Planilhas (Opcional)

Para ver a estrutura das suas planilhas antes de processar:

```bash
python main.py analyze
```

### 4. Processar as Planilhas

Para processar todas as planilhas e gerar a lista de leads:

```bash
python main.py process
```

### 5. Opções Avançadas

**Processar com estratégia de interseção:**
```bash
python main.py process --merge-strategy intersection
```

**Especificar diretórios personalizados:**
```bash
python main.py process --input-dir "minhas_planilhas" --output-dir "resultados"
```

## 📊 O que o Sistema Faz

1. **Carrega** todas as planilhas Excel da pasta de entrada
2. **Identifica** automaticamente colunas de telefone
3. **Limpa** e padroniza os números de telefone
4. **Combina** as planilhas em uma única lista
5. **Padroniza** nomes de colunas (nome, telefone, cidade, etc.)
6. **Cria** links diretos para WhatsApp
7. **Segmenta** os leads por cidade (se disponível)
8. **Gera** relatórios detalhados
9. **Salva** os resultados em Excel

## 📁 Arquivos Gerados

Após o processamento, você encontrará na pasta `data/output/`:

- `leads_whatsapp.xlsx` - Lista principal com todos os leads
- `leads_whatsapp_sao_paulo.xlsx` - Segmento por cidade (se houver)
- `leads_whatsapp_rio_de_janeiro.xlsx` - Outro segmento (se houver)
- etc.

## 📱 Colunas Geradas

O sistema cria automaticamente:

- `nome` - Nome do cliente/lead
- `telefone` - Telefone original
- `telefone_whatsapp` - Telefone formatado para WhatsApp
- `link_whatsapp` - Link direto para WhatsApp (ex: https://wa.me/5511999999999)
- `cidade` - Cidade (se disponível)
- `email` - Email (se disponível)
- Outras colunas das planilhas originais

## 🔧 Personalização

### Estrutura Esperada das Planilhas

O sistema é flexível e reconhece automaticamente colunas com nomes como:
- **Nome:** nome, name, cliente, customer
- **Telefone:** telefone, phone, celular, whatsapp, contato
- **Email:** email, e-mail
- **Cidade:** cidade, city
- **Estado:** estado, state, uf

### Exemplo de Planilha

| nome | telefone | cidade | email |
|------|----------|--------|-------|
| João Silva | (11) 99999-9999 | São Paulo | joao@email.com |
| Maria Santos | 11988888888 | Rio de Janeiro | maria@email.com |

## 🚨 Solução de Problemas

**Erro: "Nenhum arquivo Excel encontrado"**
- Verifique se as planilhas estão na pasta `data/input/`
- Certifique-se de que são arquivos `.xlsx` ou `.xls`

**Erro: "Nenhuma coluna de telefone identificada"**
- Verifique se há colunas com nomes como "telefone", "phone", "celular"
- O sistema também detecta automaticamente colunas com números de telefone

**Erro: "Nenhum lead válido encontrado"**
- Verifique se os números de telefone estão em formato válido
- O sistema aceita formatos como: (11) 99999-9999, 11999999999, +55 11 99999-9999

## 📞 Suporte

Se encontrar problemas, verifique:
1. Se todas as dependências estão instaladas: `pip install -r requirements.txt`
2. Se as planilhas estão no formato correto
3. Se há dados válidos nas colunas de telefone

