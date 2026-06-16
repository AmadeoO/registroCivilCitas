#!/bin/bash
# Script para configurar automáticamente el cron (ejecución automática)

echo "================================================"
echo "⏰ CONFIGURADOR AUTOMÁTICO DE CRON"
echo "================================================"
echo ""

# Verificar que se está ejecutando en Linux/macOS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "❌ Este script no funciona en Windows"
    echo "Para Windows, usar Tareas Programadas (ver SETUP_GUIDE.md)"
    exit 1
fi

echo "Este script configurará la ejecución automática"
echo "del verificador de citas 4 veces al día"
echo ""

# Preguntar al usuario
echo "¿A qué horas deseas verificar? (Escribe los números separados por comas)"
echo "Ejemplo: 8,12,16,20 (8 AM, 12 PM, 4 PM, 8 PM)"
read -p "Horas (por defecto 8,12,16,20): " HOURS
HOURS=${HOURS:-"8,12,16,20"}

echo ""
echo "Verificando configuración de Python..."

# Encontrar la ruta correcta de Python
if command -v python3 &> /dev/null; then
    PYTHON_PATH=$(which python3)
    echo "✅ Python encontrado en: $PYTHON_PATH"
else
    echo "❌ Python3 no encontrado. Instálalo primero."
    exit 1
fi

echo ""
echo "Verificando script..."

if [ ! -f "/home/claude/check_citas.py" ]; then
    echo "❌ El archivo /home/claude/check_citas.py no existe"
    exit 1
fi

if [ ! -x "/home/claude/check_citas.py" ]; then
    echo "⚠️  Haciendo ejecutable el script..."
    chmod +x /home/claude/check_citas.py
fi

echo "✅ Script encontrado y ejecutable"

echo ""
echo "================================================"
echo "Configurando cron..."
echo "================================================"
echo ""

# Crear la línea de cron
CRON_JOB="0 $HOURS * * * $PYTHON_PATH /home/claude/check_citas.py >> /home/claude/citas_cron.log 2>&1"

# Obtener crontab actual
CURRENT_CRON=$(crontab -l 2>/dev/null || echo "")

# Verificar si ya existe una entrada similar
if echo "$CURRENT_CRON" | grep -q "check_citas.py"; then
    echo "⚠️  Ya existe una entrada en crontab para este script"
    echo ""
    echo "Crontab actual:"
    crontab -l
    echo ""
    read -p "¿Deseas reemplazarla? (s/n): " REPLACE
    if [[ "$REPLACE" != "s" && "$REPLACE" != "S" ]]; then
        echo "Cancelado. No se realizaron cambios."
        exit 0
    fi
    # Eliminar la línea anterior
    CURRENT_CRON=$(echo "$CURRENT_CRON" | grep -v "check_citas.py")
fi

# Agregar la nueva línea
NEW_CRON="$CURRENT_CRON
$CRON_JOB"

# Aplicar el nuevo crontab
echo "$NEW_CRON" | crontab -

echo ""
echo "================================================"
echo "✅ ¡CRON CONFIGURADO CORRECTAMENTE!"
echo "================================================"
echo ""
echo "Tu nueva entrada en crontab:"
echo "$CRON_JOB"
echo ""
echo "El script se ejecutará a las siguientes horas:"
echo "$HOURS"
echo ""
echo "Log de ejecuciones:"
echo "/home/claude/citas_cron.log"
echo ""
echo "Para verificar que se configuró correctamente:"
echo "  crontab -l"
echo ""
echo "Para ver logs:"
echo "  tail -f /home/claude/citas_cron.log"
echo ""
echo "Para editar horarios:"
echo "  crontab -e"
echo ""
