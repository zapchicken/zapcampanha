# 🚀 Guia de Deploy - ZapCampanhas

## 📋 Resumo: O que você precisa

Para colocar sua ferramenta na web, você precisa apenas de **2 ferramentas**:

1. **GitHub** - Para armazenar o código
2. **Vercel** - Para hospedar a aplicação

**Supabase NÃO é necessário** - sua aplicação usa apenas arquivos locais.

## 🎯 Passo a Passo Completo

### 1. 📁 Preparar o Código

Primeiro, certifique-se de que todos os arquivos estão prontos:

```bash
# Verificar se todos os arquivos estão presentes
ls -la
```

Você deve ter:
- ✅ `web_app_flask.py`
- ✅ `requirements.txt`
- ✅ `vercel.json`
- ✅ `templates/index.html`
- ✅ `src/` (pasta com o código)
- ✅ `config/` (pasta com configurações)

### 2. 🔗 GitHub (Código)

#### 2.1 Criar Repositório
1. Acesse: https://github.com
2. Clique em "New repository"
3. Nome: `zapcampanhas`
4. Público ou Privado (sua escolha)
5. Clique "Create repository"

#### 2.2 Fazer Upload do Código

```bash
# No seu computador, na pasta do projeto
git init
git add .
git commit -m "Primeira versão do ZapCampanhas"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/zapcampanhas.git
git push -u origin main
```

### 3. 🌐 Vercel (Hospedagem)

#### 3.1 Criar Conta
1. Acesse: https://vercel.com
2. Clique "Sign Up"
3. Escolha "Continue with GitHub"
4. Autorize o Vercel a acessar seu GitHub

#### 3.2 Deploy Automático
1. No Vercel, clique "New Project"
2. Importe o repositório `zapcampanhas`
3. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (deixe vazio)
   - **Build Command**: `pip install -r requirements.txt`
   - **Output Directory**: `.`
   - **Install Command**: `pip install -r requirements.txt`

#### 3.3 Configurações Avançadas
No Vercel, vá em "Settings" > "Environment Variables":
```
FLASK_ENV=production
```

### 4. 🚀 Deploy

1. Clique "Deploy"
2. Aguarde 2-3 minutos
3. Sua aplicação estará online!

## 📱 URLs da Aplicação

Após o deploy, você terá:
- **URL Principal**: `https://zapcampanhas.vercel.app`
- **URL Personalizada**: `https://seu-dominio.vercel.app` (se configurar)

## 🔧 Configurações Importantes

### Arquivo `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "web_app_flask.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "web_app_flask.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

### Dependências (`requirements.txt`)
```
flask>=2.0.0
flask-cors>=3.0.0
werkzeug>=2.0.0
gunicorn>=20.0.0
pandas>=2.0.0
openpyxl>=3.1.0
# ... outras dependências
```

## 🎯 Vantagens do Deploy

### ✅ **Acesso de Qualquer Lugar**
- Use no celular, tablet, computador
- Sem instalar nada
- Sempre atualizado

### ✅ **Compartilhamento Fácil**
- Envie o link para sua equipe
- Todos acessam a mesma versão
- Dados centralizados

### ✅ **Backup Automático**
- Código salvo no GitHub
- Versões anteriores disponíveis
- Sem risco de perder dados

### ✅ **Gratuito**
- GitHub: gratuito para repositórios públicos
- Vercel: gratuito para projetos pessoais
- Sem custos mensais

## 🔄 Atualizações

Para atualizar a aplicação:

```bash
# Fazer mudanças no código
git add .
git commit -m "Nova funcionalidade"
git push origin main
```

O Vercel detecta automaticamente e faz o deploy!

## 🚨 Solução de Problemas

### Erro: "Build Failed"
- Verifique se `requirements.txt` está correto
- Confirme se todos os arquivos estão no GitHub
- Verifique os logs no Vercel

### Erro: "Module not found"
- Adicione a dependência em `requirements.txt`
- Faça commit e push
- O Vercel reinstala automaticamente

### Erro: "Port already in use"
- Normal em produção, o Vercel gerencia
- Use a configuração do `vercel.json`

## 📞 Suporte

Se tiver problemas:
1. Verifique os logs no Vercel
2. Confirme se o código está no GitHub
3. Teste localmente primeiro: `python web_app_flask.py`

## 🎉 Resultado Final

Após seguir estes passos, você terá:
- ✅ Aplicação online 24/7
- ✅ Acesso de qualquer dispositivo
- ✅ Atualizações automáticas
- ✅ Backup seguro no GitHub
- ✅ Totalmente gratuito

**Sua ferramenta estará disponível em: `https://zapcampanhas.vercel.app`**

---

**Pronto para começar? Siga os passos acima e sua ferramenta estará na web em menos de 10 minutos!** 🚀
