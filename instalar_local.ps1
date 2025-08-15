# 🚀 Script de Instalação ZapCampanhas - PowerShell
# Execute como Administrador para melhor compatibilidade

param(
    [switch]$Force,
    [switch]$SkipPythonCheck
)

# Configurar encoding para UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    🚀 INSTALADOR ZAPCAMPANHAS 🚀" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se está executando como administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "⚠️  Recomendado executar como Administrador para melhor compatibilidade" -ForegroundColor Yellow
    Write-Host ""
}

# Verificar Python
if (-not $SkipPythonCheck) {
    Write-Host "📋 Verificando Python..." -ForegroundColor Green
    
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
        } else {
            throw "Python não encontrado"
        }
    }
    catch {
        Write-Host "❌ Python não encontrado!" -ForegroundColor Red
        Write-Host ""
        Write-Host "🔧 Por favor, instale o Python 3.8+ em:" -ForegroundColor Yellow
        Write-Host "   https://www.python.org/downloads/" -ForegroundColor Blue
        Write-Host ""
        Write-Host "⚠️  IMPORTANTE: Marque 'Add Python to PATH' durante a instalação" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Pressione qualquer tecla para sair..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

# Verificar se requirements.txt existe
if (-not (Test-Path "requirements.txt")) {
    Write-Host "❌ Arquivo requirements.txt não encontrado!" -ForegroundColor Red
    Write-Host "Certifique-se de estar na pasta correta do projeto." -ForegroundColor Yellow
    exit 1
}

# Instalar dependências
Write-Host ""
Write-Host "📦 Instalando dependências..." -ForegroundColor Green

try {
    # Tentar instalar normalmente
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Tentando instalar com --user..." -ForegroundColor Yellow
        python -m pip install -r requirements.txt --user
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependências instaladas com sucesso!" -ForegroundColor Green
    } else {
        throw "Falha na instalação das dependências"
    }
}
catch {
    Write-Host "❌ Erro ao instalar dependências: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Tente executar como Administrador ou use: pip install -r requirements.txt --user" -ForegroundColor Yellow
    exit 1
}

# Configurar ambiente
Write-Host ""
Write-Host "🔧 Configurando ambiente..." -ForegroundColor Green

try {
    python main.py setup
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Ambiente configurado!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Configuração do ambiente pode ter falhado, mas continuando..." -ForegroundColor Yellow
    }
}
catch {
    Write-Host "⚠️  Erro na configuração do ambiente: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Criar estrutura de pastas
Write-Host ""
Write-Host "📁 Criando estrutura de pastas..." -ForegroundColor Green

$folders = @("data\input", "data\output")

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Host "✅ Criada pasta: $folder" -ForegroundColor Green
    } else {
        Write-Host "✅ Pasta já existe: $folder" -ForegroundColor Gray
    }
}

# Copiar arquivos de exemplo
Write-Host ""
Write-Host "📋 Copiando arquivos de exemplo..." -ForegroundColor Green

$fileMappings = @{
    "arquivos upload\contacts (3).csv" = "data\input\contacts.csv"
    "arquivos upload\Lista-Clientes 13-08-25 1615.xlsx" = "data\input\Lista-Clientes.xlsx"
    "arquivos upload\Todos os pedidos  Data de Abertura [01-02-2025 0000 - 01-08-2025 2359].xlsx" = "data\input\Todos os pedidos.xlsx"
    "arquivos upload\Historico_Itens_Vendidos de 01-02-25 à 01-08-25.xlsx" = "data\input\Historico_Itens_Vendidos.xlsx"
}

foreach ($source in $fileMappings.Keys) {
    $destination = $fileMappings[$source]
    if (Test-Path $source) {
        Copy-Item $source $destination -Force
        Write-Host "✅ Copiado: $(Split-Path $source -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Arquivo não encontrado: $source" -ForegroundColor Yellow
    }
}

# Verificar instalação
Write-Host ""
Write-Host "🔍 Verificando instalação..." -ForegroundColor Green

try {
    $helpOutput = python main.py --help 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Instalação verificada com sucesso!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Verificação da instalação falhou, mas o programa pode funcionar" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "⚠️  Erro na verificação: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Resumo final
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ INSTALAÇÃO CONCLUÍDA!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Para executar o programa:" -ForegroundColor White
Write-Host ""
Write-Host "   1. Processar dados da ZapChicken:" -ForegroundColor Gray
Write-Host "      python main.py zapchicken" -ForegroundColor Blue
Write-Host ""
Write-Host "   2. Chat com IA:" -ForegroundColor Gray
Write-Host "      python main.py chat" -ForegroundColor Blue
Write-Host ""
Write-Host "   3. Ver ajuda:" -ForegroundColor Gray
Write-Host "      python main.py --help" -ForegroundColor Blue
Write-Host ""
Write-Host "   4. Processamento genérico:" -ForegroundColor Gray
Write-Host "      python main.py process" -ForegroundColor Blue
Write-Host ""
Write-Host "📁 Arquivos de entrada: data\input\" -ForegroundColor Gray
Write-Host "📁 Resultados: data\output\" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 Para mais informações, consulte: GUIA_EXECUCAO_LOCAL.md" -ForegroundColor Gray
Write-Host ""

# Perguntar se quer executar agora
$response = Read-Host "Deseja executar o programa agora? (s/n)"
if ($response -eq "s" -or $response -eq "S" -or $response -eq "sim" -or $response -eq "SIM") {
    Write-Host ""
    Write-Host "🚀 Iniciando ZapCampanhas..." -ForegroundColor Green
    python main.py zapchicken
}

Write-Host ""
Write-Host "Pressione qualquer tecla para sair..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
