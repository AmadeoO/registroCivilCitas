# 🎯 GUÍA DE CONFIGURACIÓN - VERIFICADOR DE CITAS JUNTA DE ANDALUCÍA

## 📋 REQUISITOS PREVIOS

### 1. Instalar Python 3 y dependencias

```bash
# En Ubuntu/Debian:
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# En macOS (con Homebrew):
brew install python3

# En Windows:
# Descargar e instalar desde https://www.python.org/downloads/
```

### 2. Instalar librerías necesarias

```bash
pip3 install selenium requests
```

### 3. Descargar ChromeDriver

El script usa Selenium con Chrome. Necesitas descargar ChromeDriver compatible con tu versión de Chrome:

```bash
# 1. Verifica tu versión de Chrome:
# Chrome → Menú ⋮ → Ayuda → Información de Google Chrome

# 2. Descarga el ChromeDriver correspondiente:
# https://chromedriver.chromium.org/

# 3. En Linux/macOS (ubicar en /usr/local/bin):
sudo chmod +x chromedriver
sudo mv chromedriver /usr/local/bin/

# 4. En Windows:
# Coloca chromedriver.exe en la carpeta del script
```

---

## 🤖 CONFIGURAR TELEGRAM

### Paso 1: Crear el Bot en Telegram

1. Abre Telegram y busca **@BotFather**
2. Envía `/start` y luego `/newbot`
3. Elige un nombre para el bot (ej: "CitasMálagaBot")
4. Elige un username único (ej: "citas_malaga_bot")
5. **BotFather te dará un TOKEN**. Cópialo.

**Ejemplo de TOKEN:**
```
123456789:ABCDefGHIJklmnoPQRStuvwxyz1234567890
```

### Paso 2: Obtener tu Chat ID

1. Abre el bot que creaste en Telegram (búscalo por username)
2. Envía `/start` o cualquier mensaje
3. Ve a: `https://api.telegram.org/botTU_TOKEN/getUpdates`
4. Busca `"chat":{"id":XXXXX}` - ese XXXXX es tu Chat ID

**Ejemplo:**
```
https://api.telegram.org/bot123456789:ABCDefGHIJklmnoPQRStuvwxyz1234567890/getUpdates
```

Verás algo como:
```json
{"ok":true,"result":[{"update_id":123456,"message":{"chat":{"id":987654321,...
```

Tu Chat ID es: `987654321`

---

## 🔧 CONFIGURAR EL SCRIPT

### Editar el archivo check_citas.py

Abre `check_citas.py` y encuentra estas líneas:

```python
TELEGRAM_BOT_TOKEN = "TU_BOT_TOKEN_AQUI"  # ← Cambia esto
TELEGRAM_CHAT_ID = "TU_CHAT_ID_AQUI"      # ← Cambia esto
```

Ejemplo con valores reales:

```python
TELEGRAM_BOT_TOKEN = "123456789:ABCDefGHIJklmnoPQRStuvwxyz1234567890"
TELEGRAM_CHAT_ID = "987654321"
```

---

## ⏰ PROGRAMAR EJECUCIÓN AUTOMÁTICA

### OPCIÓN A: Linux/macOS (usando cron) ✅ RECOMENDADO

**1. Hacer ejecutable el script:**
```bash
chmod +x /home/claude/check_citas.py
```

**2. Abrir el editor de cron:**
```bash
crontab -e
```

**3. Agregar estas líneas para ejecutar 4 veces al día:**

```cron
# Ejecutar a las 08:00, 12:00, 16:00 y 20:00 todos los días
0 8,12,16,20 * * * /usr/bin/python3 /home/claude/check_citas.py >> /home/claude/citas_cron.log 2>&1

# O si prefieres cada 6 horas desde las 06:00:
0 6,12,18,0 * * * /usr/bin/python3 /home/claude/check_citas.py >> /home/claude/citas_cron.log 2>&1
```

**4. Guardar y salir** (si usas nano: Ctrl+O, Enter, Ctrl+X)

**5. Verificar que se creó:**
```bash
crontab -l
```

### OPCIÓN B: Windows (usando Tareas Programadas)

**1. Abrir Tareas Programadas** (Windows + R → `taskschd.msc`)

**2. Crear tarea básica:**
- Nombre: "Verificador Citas Málaga"
- Desencadenador: Diariamente, 4 veces (08:00, 12:00, 16:00, 20:00)
- Acción: Iniciar programa
  - Programa: `C:\Python311\python.exe` (o tu ruta de Python)
  - Argumentos: `C:\ruta\al\check_citas.py`
  - Iniciar en: `C:\ruta\al\` (carpeta del script)

### OPCIÓN C: macOS (usando LaunchAgent)

**1. Crear archivo de configuración:**
```bash
nano ~/Library/LaunchAgents/com.citas.check.plist
```

**2. Copiar este contenido:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.citas.check</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/tuusuario/check_citas.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Hour</key>
            <integer>8</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>12</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>16</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>20</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
    </array>
    <key>StandardOutPath</key>
    <string>/tmp/citas_check.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/citas_check.log</string>
</dict>
</plist>
```

**3. Cargar el script:**
```bash
launchctl load ~/Library/LaunchAgents/com.citas.check.plist
```

---

## 🧪 PROBAR EL SCRIPT

### Prueba manual antes de programar:

```bash
python3 /home/claude/check_citas.py
```

Deberías ver en consola:
```
2024-01-15 10:30:45,123 - INFO - ==================================================
2024-01-15 10:30:45,456 - INFO - VERIFICADOR DE CITAS - JUNTA DE ANDALUCÍA
2024-01-15 10:30:45,789 - INFO - Ejecución: 15/01/2024 10:30:45
2024-01-15 10:30:45,890 - INFO - ==================================================
```

Y en Telegram deberías recibir una notificación (de prueba o de disponibilidad).

---

## 📊 MONITOREAR LOGS

### Ver logs en tiempo real:
```bash
tail -f /home/claude/citas_check.log
```

### Ver últimas 50 líneas:
```bash
tail -50 /home/claude/citas_check.log
```

---

## 🐛 SOLUCIONAR PROBLEMAS

### Error: "chromedriver not found"
- Descarga ChromeDriver correctamente
- Colócalo en `/usr/local/bin/` (Linux/macOS) o en la carpeta del script (Windows)
- En Linux/macOS: `chmod +x chromedriver`

### Error: "Telegram token invalid"
- Verifica que copiaste bien el token de @BotFather
- No debe tener espacios

### El script se ejecuta pero no envía notificaciones
1. Prueba manualmente el bot en Telegram
2. Verifica Chat ID con: `https://api.telegram.org/bot{TOKEN}/getUpdates`
3. Revisa los logs: `tail -f /home/claude/citas_check.log`

### El cron no se ejecuta
```bash
# Verifica que Python está disponible
which python3

# Verifica permisos
ls -l /home/claude/check_citas.py

# Debe tener -rwxr-xr-x (ejecutable)
chmod +x /home/claude/check_citas.py
```

---

## ✅ CHECKLIST DE INSTALACIÓN

- [ ] Python 3 instalado
- [ ] Librerías instaladas: `pip3 install selenium requests`
- [ ] ChromeDriver descargado y configurado
- [ ] Token de Telegram obtenido de @BotFather
- [ ] Chat ID obtenido
- [ ] Script actualizado con TOKEN y CHAT_ID
- [ ] Script probado manualmente
- [ ] Cron/Tareas programadas configurado
- [ ] Logs monitoreados

---

## 📞 SOPORTE

Si tienes problemas:
1. Revisa los logs: `tail -f /home/claude/citas_check.log`
2. Prueba el script manualmente
3. Verifica que Telegram bot está correctamente configurado
4. Comprueba que tienes conexión a Internet
