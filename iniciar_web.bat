@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    🌐 ZAPCAMPANHAS WEB APP 🌐
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
echo 📦 Verificando dependências web...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Instalando dependências web...
    pip install flask dash dash-bootstrap-components
)

echo.
echo 🌐 Iniciando servidor web...
echo.
echo 📱 Abra seu navegador e acesse:
echo    http://localhost:5000
echo.
echo 🔄 Pressione Ctrl+C para parar o servidor
echo.

python main.py web

echo.
echo ✅ Servidor web parado.
pause
