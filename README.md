# 🎯 VERIFICADOR AUTOMÁTICO DE CITAS - JUNTA DE ANDALUCÍA

## ⚡ INICIO RÁPIDO (5 minutos)

### 1️⃣ Instalar dependencias
```bash
bash install.sh
```

### 2️⃣ Obtener credenciales de Telegram

#### A. Crear bot en Telegram:
1. Abre Telegram → Busca **@BotFather**
2. Envía `/newbot`
3. Sigue las instrucciones
4. **Copia el TOKEN** que te proporciona

#### B. Obtener tu Chat ID:
1. Abre tu bot nuevo en Telegram
2. Envía un mensaje cualquiera
3. Visita: `https://api.telegram.org/bot{TOKEN_AQUI}/getUpdates`
   - Reemplaza `{TOKEN_AQUI}` con tu token
4. **Busca `"id":XXXXX`** - ese es tu Chat ID

### 3️⃣ Configurar el script
```bash
nano check_citas.py
```

Busca y reemplaza:
```python
TELEGRAM_BOT_TOKEN = "TU_BOT_TOKEN_AQUI"  # ← Pega aquí tu token
TELEGRAM_CHAT_ID = "TU_CHAT_ID_AQUI"      # ← Pega aquí tu Chat ID
```

**Ejemplo:**
```python
TELEGRAM_BOT_TOKEN = "123456789:ABCDefGHIJklmnoPQRStuvwxyz1234567890"
TELEGRAM_CHAT_ID = "987654321"
```

Guarda: **Ctrl+O → Enter → Ctrl+X**

### 4️⃣ Probar que funciona
```bash
python3 check_citas.py
```

Deberías recibir una notificación en Telegram (de disponibilidad o sin disponibilidad).

### 5️⃣ Configurar ejecución automática 4 veces al día

#### En Linux/macOS:
```bash
crontab -e
```

Agrega esta línea al final:
```cron
0 8,12,16,20 * * * /usr/bin/python3 /home/claude/check_citas.py >> /home/claude/citas_cron.log 2>&1
```

Esto ejecutará el script a las **8:00, 12:00, 16:00 y 20:00** todos los días.

Guarda: **Ctrl+O → Enter → Ctrl+X** (en nano)

#### En Windows:
Ver `SETUP_GUIDE.md` sección "OPCIÓN B: Windows"

---

## 📊 MONITOREAR

### Ver logs en tiempo real:
```bash
tail -f /home/claude/citas_check.log
```

### Ver logs de cron:
```bash
tail -f /home/claude/citas_cron.log
```

---

## 🔄 SELECCIONAR VERSIÓN

Hay 2 versiones disponibles:

### `check_citas.py` (Versión Estándar)
- Más ligera
- Más rápida
- Recomendada para la mayoría

### `check_citas_mejorado.py` (Versión Mejorada)
- Más robusta
- Mejor detección de disponibilidad
- Recomendada si la estándar no funciona

Para usar la versión mejorada en cron:
```bash
crontab -e
# Cambia:
0 8,12,16,20 * * * /usr/bin/python3 /home/claude/check_citas.py

# Por:
0 8,12,16,20 * * * /usr/bin/python3 /home/claude/check_citas_mejorado.py
```

---

## ✅ CHECKLIST

- [ ] Instaladas dependencias (`bash install.sh`)
- [ ] Obtenido TOKEN de Telegram (@BotFather)
- [ ] Obtenido CHAT_ID (getUpdates)
- [ ] Configurado TOKEN y CHAT_ID en script
- [ ] Prueba manual exitosa (`python3 check_citas.py`)
- [ ] Cron configurado (`crontab -e`)
- [ ] Verificar logs (`tail -f citas_check.log`)

---

## 📞 PROBLEMAS FRECUENTES

### "chromedriver not found"
```bash
# Descargar desde: https://chromedriver.chromium.org/
# Luego:
chmod +x chromedriver
sudo mv chromedriver /usr/local/bin/
```

### "Telegram token invalid"
- Verifica que copiaste bien el token
- Sin espacios al inicio/final
- Debe ser `numero:letrasYnumeros`

### No recibe notificaciones
1. Prueba bot manualmente en Telegram
2. Verifica Chat ID en: `https://api.telegram.org/bot{TOKEN}/getUpdates`
3. Revisa logs: `tail -50 citas_check.log`

### El cron no se ejecuta
```bash
# Verifica que está en crontab:
crontab -l

# Verifica permisos del script:
ls -l check_citas.py
# Debe mostrar: -rwxr-xr-x

# Si no, hacer ejecutable:
chmod +x check_citas.py
```

---

## 📚 DOCUMENTACIÓN COMPLETA

Para más detalles: `cat SETUP_GUIDE.md`

---

## 🎉 ¡LISTO!

El script verificará automáticamente 4 veces al día y te notificará en Telegram si hay disponibilidad.

**Horarios de verificación:**
- ✅ 08:00
- ✅ 12:00  
- ✅ 16:00
- ✅ 20:00

---

## 💡 TIPS

**Personalizacion de horarios en cron:**

Cambiar hora de verificación:
```cron
# Cada 6 horas empezando a las 6 AM:
0 6,12,18,0 * * * /usr/bin/python3 /home/claude/check_citas.py

# Cada hora:
0 * * * * /usr/bin/python3 /home/claude/check_citas.py

# Cada 30 minutos:
*/30 * * * * /usr/bin/python3 /home/claude/check_citas.py

# Solo de lunes a viernes:
0 8,12,16,20 * * 1-5 /usr/bin/python3 /home/claude/check_citas.py
```

**Suspender/Reanudar verificación:**
```bash
# Ver cron actual:
crontab -l

# Editar (comentar la línea con #):
crontab -e
# #0 8,12,16,20 * * * /usr/bin/python3 /home/claude/check_citas.py

# Guardar y salir
```

---

**Última actualización:** 2024
**Versión:** 2.0 (Mejorada)
