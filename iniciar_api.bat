@echo off
echo.
echo ========================================
echo   API de Otimizacao de Escalas v1.0
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nao encontrado! Instale Python 3.8+ primeiro.
    echo    Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verificar se pip está disponível
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip nao encontrado! Reinstale o Python com pip.
    pause
    exit /b 1
)

echo ✅ Python detectado!
echo.

REM Instalar dependências
echo 📦 Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erro ao instalar dependencias!
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas!
echo.

REM Iniciar API
echo 🚀 Iniciando API...
echo.
echo 📖 Documentacao: http://localhost:8000/docs
echo 🔗 API: http://localhost:8000
echo.
echo ⚠️  Para parar a API: Ctrl+C
echo.

python api_escala_trabalho.py

pause
