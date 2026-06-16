#!/bin/bash
# Script de instalación rápida de dependencias para el verificador de citas

echo "================================================"
echo "🚀 INSTALADOR - VERIFICADOR DE CITAS MÁLAGA"
echo "================================================"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar si es Linux o macOS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "✅ Sistema detectado: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo "✅ Sistema detectado: macOS"
else
    echo -e "${RED}❌ Sistema no soportado: $OSTYPE${NC}"
    echo "Este script solo funciona en Linux o macOS"
    exit 1
fi

echo ""
echo "📦 PASO 1: Verificando Python 3..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ $PYTHON_VERSION encontrado${NC}"
else
    echo -e "${RED}❌ Python 3 no está instalado${NC}"
    if [[ "$OS" == "linux" ]]; then
        echo "   Instálalo con: sudo apt-get install python3 python3-pip"
    else
        echo "   Instálalo con: brew install python3"
    fi
    exit 1
fi

echo ""
echo "📦 PASO 2: Instalando librerías Python..."
pip3 install --user selenium requests
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Librerías instaladas correctamente${NC}"
else
    echo -e "${RED}❌ Error instalando librerías${NC}"
    exit 1
fi

echo ""
echo "📦 PASO 3: Verificando ChromeDriver..."
CHROME_AVAILABLE=0

if command -v chromedriver &> /dev/null; then
    CHROMEDRIVER_PATH=$(which chromedriver)
    echo -e "${GREEN}✅ ChromeDriver encontrado en: $CHROMEDRIVER_PATH${NC}"
    CHROME_AVAILABLE=1
elif [ -f "/usr/local/bin/chromedriver" ]; then
    echo -e "${GREEN}✅ ChromeDriver encontrado en: /usr/local/bin/chromedriver${NC}"
    CHROME_AVAILABLE=1
elif [ -f "$(pwd)/chromedriver" ]; then
    echo -e "${GREEN}✅ ChromeDriver encontrado en directorio actual${NC}"
    CHROME_AVAILABLE=1
fi

if [ $CHROME_AVAILABLE -eq 0 ]; then
    echo -e "${YELLOW}⚠️  ChromeDriver NO ENCONTRADO${NC}"
    echo ""
    echo "📥 Para obtener ChromeDriver:"
    echo "1. Averigua tu versión de Chrome:"
    echo "   Chrome → Menú (⋮) → Ayuda → Información de Google Chrome"
    echo ""
    echo "2. Descarga ChromeDriver desde:"
    echo "   https://chromedriver.chromium.org/"
    echo ""
    echo "3. Una vez descargado:"
    echo "   chmod +x chromedriver"
    echo "   sudo mv chromedriver /usr/local/bin/"
    echo ""
fi

echo ""
echo "🔐 PASO 4: Configurando permisos..."
chmod +x /home/claude/check_citas.py
chmod +x /home/claude/check_citas_mejorado.py
echo -e "${GREEN}✅ Permisos configurados${NC}"

echo ""
echo "================================================"
echo -e "${GREEN}✅ INSTALACIÓN COMPLETADA${NC}"
echo "================================================"
echo ""
echo "📝 PRÓXIMOS PASOS:"
echo "1. Lee la guía: cat SETUP_GUIDE.md"
echo "2. Configura Telegram (obtén TOKEN y CHAT_ID)"
echo "3. Edita check_citas.py con tus credenciales de Telegram"
echo "4. Prueba el script: python3 check_citas.py"
echo "5. Configura cron para ejecución automática"
echo ""
echo "💡 Para editar el script:"
echo "   nano check_citas.py"
echo ""
echo "🧪 Para probar:"
echo "   python3 check_citas.py"
echo ""
echo "⏰ Para configurar cron (ejecución automática):"
echo "   crontab -e"
echo "   # Agregar esta línea:"
echo "   0 8,12,16,20 * * * /usr/bin/python3 /home/claude/check_citas.py >> /home/claude/citas_cron.log 2>&1"
echo ""
