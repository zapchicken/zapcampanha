@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    🚀 INSTALADOR ZAPCAMPANHAS 🚀
echo ========================================
echo.

echo 📋 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo.
    echo 🔧 Por favor, instale o Python 3.8+ em:
    echo    https://www.python.org/downloads/
    echo.
    echo ⚠️  IMPORTANTE: Marque "Add Python to PATH" durante a instalação
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado!
python --version

echo.
echo 📦 Instalando dependências...
pip install -r requirements.txt
if errorlevel 1 (
    echo ⚠️  Tentando instalar com --user...
    pip install -r requirements.txt --user
)

echo.
echo 🔧 Configurando ambiente...
python main.py setup

echo.
echo 📁 Criando estrutura de pastas...
if not exist "data\input" mkdir "data\input"
if not exist "data\output" mkdir "data\output"

echo.
echo 📋 Copiando arquivos de exemplo...
if exist "arquivos upload\contacts (3).csv" (
    copy "arquivos upload\contacts (3).csv" "data\input\contacts.csv" >nul
    echo ✅ contacts.csv copiado
)

if exist "arquivos upload\Lista-Clientes 13-08-25 1615.xlsx" (
    copy "arquivos upload\Lista-Clientes 13-08-25 1615.xlsx" "data\input\Lista-Clientes.xlsx" >nul
    echo ✅ Lista-Clientes.xlsx copiado
)

if exist "arquivos upload\Todos os pedidos  Data de Abertura [01-02-2025 0000 - 01-08-2025 2359].xlsx" (
    copy "arquivos upload\Todos os pedidos  Data de Abertura [01-02-2025 0000 - 01-08-2025 2359].xlsx" "data\input\Todos os pedidos.xlsx" >nul
    echo ✅ Todos os pedidos.xlsx copiado
)

if exist "arquivos upload\Historico_Itens_Vendidos de 01-02-25 à 01-08-25.xlsx" (
    copy "arquivos upload\Historico_Itens_Vendidos de 01-02-25 à 01-08-25.xlsx" "data\input\Historico_Itens_Vendidos.xlsx" >nul
    echo ✅ Historico_Itens_Vendidos.xlsx copiado
)

echo.
echo ✅ Instalação concluída!
echo.
echo 🚀 Para executar o programa:
echo.
echo   1. Processar dados da ZapChicken:
echo      python main.py zapchicken
echo.
echo   2. Chat com IA:
echo      python main.py chat
echo.
echo   3. Ver ajuda:
echo      python main.py --help
echo.
echo 📁 Arquivos de entrada: data\input\
echo 📁 Resultados: data\output\
echo.
pause
