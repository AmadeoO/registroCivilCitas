# 📋 CLAUDE.md - CONTEXTO COMPLETO DEL PROYECTO

**Última actualización:** 2024-06-16
**Versión:** 2.0 (Sistema Completo)

---

## 🎯 RESUMEN EJECUTIVO

Se ha desarrollado un **sistema automatizado completo** que verifica diariamente la disponibilidad de citas de **Nacionalidad en el Registro Civil Exclusivo de Málaga** de la Junta de Andalucía.

**El sistema:**
- ✅ Se ejecuta automáticamente **4 veces al día** (08:00, 12:00, 16:00, 20:00)
- ✅ Envía **notificaciones por Telegram** cuando hay disponibilidad
- ✅ Totalmente **sin intervención manual**
- ✅ Fácil de instalar y configurar

---

## 📊 DETALLES DEL PROYECTO

### Objetivo Principal
Automatizar la búsqueda de citas de Nacionalidad en la Junta de Andalucía porque:
- Las citas suelen estar ocupadas
- Liberan slots ocasionalmente e irregularmente
- Es tedioso verificar manualmente
- El usuario necesita detectar disponibilidad rápidamente

### Fuente de Datos
- **URL:** https://www.juntadeandalucia.es/justicia/citaprevia/?idCliente=4
- **Oficina:** REGISTRO CIVIL EXCLUSIVO DE MÁLAGA
- **Trámite:** NACIONALIDAD

### Método de Notificación
- **Plataforma:** Telegram
- **Ventajas:** Instantáneo, gratuito, confiable
- **Contenido:** Enlace directo a la página de reserva

---

## 📦 ESTRUCTURA DEL PROYECTO

```
Proyecto: Verificador-Citas-Málaga
├── 📚 DOCUMENTACIÓN
│   ├── README.md              (Guía rápida - EMPIEZA AQUÍ)
│   ├── SETUP_GUIDE.md         (Guía completa con detalles)
│   ├── ESTRUCTURA.md          (Descripción del proyecto)
│   └── CLAUDE.md              (Este archivo - contexto para IA)
│
├── 🐍 SCRIPTS PYTHON (Lógica Principal)
│   ├── check_citas.py         (✅ RECOMENDADO - versión estándar)
│   ├── check_citas_mejorado.py (Alternativa más robusta)
│   └── test_config.py         (Verificar configuración)
│
├── 🔧 SCRIPTS BASH (Instalación)
│   ├── install.sh             (Instala dependencias)
│   └── setup_cron.sh          (Configura automatización)
│
└── 📝 ARCHIVOS DE DATOS (Generados)
    └── citas_check.log        (Registro de ejecuciones)
```

---

## 🔧 CÓMO FUNCIONA TÉCNICAMENTE

### Stack Tecnológico
```
Cron (Linux/macOS) 
  ↓ [cada 6 horas]
Python 3.x
  ├─ Selenium WebDriver
  │  └─ Google Chrome (headless)
  │     └─ Navega página de citas
  ├─ Requests Library
  │  └─ API de Telegram
  │     └─ Envía notificación
  └─ Logging
     └─ Registra ejecuciones
```

### Flujo de Ejecución

```
1. INICIO (cron ejecuta a hora programada)
   ↓
2. SELENIUM ABRE CHROME (modo headless)
   ↓
3. NAVEGA A PÁGINA DE CITAS
   ├─ Espera carga
   └─ Timeout: 40 segundos
   ↓
4. SELECCIONA OPCIONES
   ├─ "REGISTRO CIVIL EXCLUSIVO DE MÁLAGA"
   └─ "NACIONALIDAD"
   ↓
5. ESPERA TABLA DE DISPONIBILIDAD
   └─ Analiza HTML/CSS
   ↓
6. BUSCA SLOTS DISPONIBLES (color verde)
   ├─ Método 1: Por clase CSS
   ├─ Método 2: Por texto
   └─ Método 3: Por color RGB
   ↓
7. ANÁLISIS DE RESULTADO
   ├─ SI HAY DISPONIBILIDAD:
   │  ├─ Extrae detalles (fecha/hora)
   │  ├─ Construye mensaje
   │  └─ ENVÍA TELEGRAM
   │
   └─ SI NO HAY:
      └─ Solo registra en log
   ↓
8. CIERRA NAVEGADOR
   ↓
9. REGISTRA EN LOG
   ↓
10. FIN (espera próxima ejecución)
```

---

## 📋 ARCHIVOS PRINCIPALES

### 1. `check_citas.py` ⭐ PRINCIPAL

**Propósito:** Script principal que ejecuta toda la lógica

**Funciones clave:**
- `send_telegram_notification(message)` - Envía notificaciones
- `check_availability()` - Verifica disponibilidad
- `main()` - Función principal

**Variables críticas a configurar:**
```python
TELEGRAM_BOT_TOKEN = "TU_BOT_TOKEN_AQUI"  # Token de @BotFather
TELEGRAM_CHAT_ID = "TU_CHAT_ID_AQUI"      # Tu ID de Telegram
URL_CITAS = "https://..."                 # URL de la página
```

**Dependencias:**
- selenium
- requests
- logging (built-in)
- time (built-in)

---

### 2. `check_citas_mejorado.py` (Alternativa)

**Mejoras sobre la versión estándar:**
- Múltiples métodos para detectar disponibilidad
- Mejor manejo de errores
- Extrae información más detallada
- Logging más verboso
- Compatible con diferentes estructuras de HTML

**Usar si:**
- La versión estándar no encuentra disponibilidad correctamente
- Quieres información más detallada
- Tienes problemas de compatibilidad

---

### 3. `test_config.py` (Diagnóstico)

**Propósito:** Prueba automática de toda la configuración

**Verificaciones:**
1. Python 3 instalado
2. Selenium disponible
3. Requests disponible
4. ChromeDriver instalado
5. Google Chrome funcionando
6. Acceso a Internet
7. Acceso a página de citas
8. Configuración de Telegram

**Uso:**
```bash
python3 test_config.py
```

**Salida:** Reporte detallado con ✅ / ❌ para cada verificación

---

### 4. `install.sh` (Instalador)

**Propósito:** Instalación automatizada de dependencias

**Pasos:**
1. Detecta sistema operativo (Linux/macOS)
2. Verifica Python 3
3. Instala pip packages (selenium, requests)
4. Verifica ChromeDriver
5. Configura permisos

**Uso:**
```bash
bash install.sh
```

---

### 5. `setup_cron.sh` (Automatización)

**Propósito:** Configurar ejecución automática con cron

**Funcionalidades:**
- Permite personalizar horarios
- Valida configuración
- Crea entrada en crontab
- Muestra instrucciones finales

**Uso:**
```bash
bash setup_cron.sh
```

---

## 🚀 GUÍA PASO A PASO COMPLETA

### FASE 1: PREPARACIÓN (2 minutos)

**Requisitos previos:**
- [ ] Acceso a terminal/línea de comandos
- [ ] Python 3 instalado (o capacidad para instalarlo)
- [ ] Google Chrome instalado
- [ ] Conexión a Internet
- [ ] Cuenta de Telegram activa

### FASE 2: INSTALACIÓN DE DEPENDENCIAS (5 minutos)

**Paso 1: Ejecutar instalador**
```bash
bash install.sh
```

**Qué hace:**
- Verifica Python 3
- Instala selenium y requests con pip
- Verifica ChromeDriver
- Configura permisos

**Si ChromeDriver no está:**
1. Descargar: https://chromedriver.chromium.org/
2. Descomprimir
3. Mover: `sudo mv chromedriver /usr/local/bin/`
4. Hacer ejecutable: `chmod +x /usr/local/bin/chromedriver`

**Verificar instalación:**
```bash
python3 -c "import selenium; print(selenium.__version__)"
python3 -c "import requests; print(requests.__version__)"
```

### FASE 3: CONFIGURAR TELEGRAM (5 minutos)

#### Paso 1: Crear Bot en Telegram
1. Abre Telegram
2. Busca **@BotFather**
3. Envía `/start`
4. Envía `/newbot`
5. Elige nombre: "CitasMálagaBot" (o similar)
6. Elige username único: "citas_malaga_bot" (o similar)
7. **BotFather te dará un TOKEN**

**Ejemplo de TOKEN:**
```
123456789:ABCDefGHIJklmnoPQRStuvwxyz1234567890
```

#### Paso 2: Obtener tu Chat ID
1. En Telegram, abre el bot que creaste
2. Envía un mensaje cualquiera (ej: "test")
3. Ve a esta URL (reemplaza {TOKEN}):
```
https://api.telegram.org/bot{TOKEN}/getUpdates
```

Verás algo como:
```json
{
  "ok": true,
  "result": [{
    "update_id": 123456,
    "message": {
      "chat": {
        "id": 987654321,
        ...
```

**Tu Chat ID es:** `987654321`

### FASE 4: CONFIGURAR EL SCRIPT (3 minutos)

**Paso 1: Editar check_citas.py**
```bash
nano check_citas.py
```

**Paso 2: Buscar estas líneas (arriba del archivo):**
```python
TELEGRAM_BOT_TOKEN = "TU_BOT_TOKEN_AQUI"
TELEGRAM_CHAT_ID = "TU_CHAT_ID_AQUI"
```

**Paso 3: Reemplazar con tus valores:**
```python
TELEGRAM_BOT_TOKEN = "123456789:ABCDefGHIJklmnoPQRStuvwxyz1234567890"
TELEGRAM_CHAT_ID = "987654321"
```

**Paso 4: Guardar y salir**
- Presiona: **Ctrl+O**
- Presiona: **Enter**
- Presiona: **Ctrl+X**

### FASE 5: PRUEBAS (5 minutos)

**Paso 1: Verificar configuración**
```bash
python3 test_config.py
```

**Salida esperada:**
```
✓ PASO 1: Verificando Python 3
✅ Python encontrado: Python 3.x.x ...

✓ PASO 2: Verificando librerías requeridas
✅ Selenium: x.x.x
✅ Requests: x.x.x

...

🎉 ¡TODAS LAS PRUEBAS PASARON!
```

Si algo falla, sigue las instrucciones del script.

**Paso 2: Ejecutar script de prueba**
```bash
python3 check_citas.py
```

**Qué debería pasar:**
1. El script se abre (puede tardar 10-20 segundos)
2. Ve el navegador abrirse y cerrarse
3. En Telegram recibes una notificación (con o sin disponibilidad)
4. En terminal ves mensaje de éxito

**En Telegram verás:**
- Si hay disponibilidad: "¡CITA DISPONIBLE EN MÁLAGA!"
- Si no hay: Puedes ver en logs con `tail -f citas_check.log`

### FASE 6: AUTOMATIZAR (2 minutos)

**Paso 1: Ejecutar configurador de cron**
```bash
bash setup_cron.sh
```

**Paso 2: Responder preguntas**
- ¿A qué horas deseas verificar?
- Escribir: `8,12,16,20` (u otros horarios)

**El script hará:**
- Crear entrada en crontab
- Mostrar confirmación
- Proporcionar instrucciones de monitoreo

**Verificar que se creó:**
```bash
crontab -l
```

Deberías ver algo como:
```
0 8,12,16,20 * * * /usr/bin/python3 /home/claude/check_citas.py >> /home/claude/citas_cron.log 2>&1
```

---

## 🧪 TESTING Y VALIDACIÓN

### Test 1: Instalación
```bash
python3 test_config.py
```
**Resultado esperado:** ✅ PASÓ en todos los pasos

### Test 2: Script Manual
```bash
python3 check_citas.py
```
**Resultado esperado:**
- Sin errores en terminal
- Notificación en Telegram
- Entrada en log

### Test 3: Logs
```bash
tail -10 citas_check.log
```
**Esperado:** Últimas 10 líneas con marcas de tiempo

### Test 4: Cron
```bash
crontab -l | grep check_citas
```
**Esperado:** Línea con el schedule configurado

---

## 📊 MONITOREO Y MANTENIMIENTO

### Ver Logs en Tiempo Real
```bash
tail -f citas_check.log
```
Presiona Ctrl+C para salir.

### Ver Últimas N Líneas
```bash
tail -50 citas_check.log
```

### Ver Todo el Log
```bash
cat citas_check.log
```

### Limpiar Log (borra contenido anterior)
```bash
echo "" > citas_check.log
```

### Ver Próximas Ejecuciones
```bash
crontab -l
```

---

## ⚙️ PERSONALIZACIÓN

### Cambiar Horarios de Verificación

```bash
crontab -e
```

**Ejemplos de configuración:**

```cron
# Cada 6 horas (8, 14, 20, 2):
0 8,14,20,2 * * * /usr/bin/python3 /home/claude/check_citas.py

# Cada 2 horas:
0 */2 * * * /usr/bin/python3 /home/claude/check_citas.py

# Cada 30 minutos:
*/30 * * * * /usr/bin/python3 /home/claude/check_citas.py

# Solo horas de trabajo (9-17h):
0 9,10,11,12,13,14,15,16,17 * * * /usr/bin/python3 /home/claude/check_citas.py

# Solo fines de semana:
0 8,12,16,20 * * 0,6 /usr/bin/python3 /home/claude/check_citas.py
```

### Cambiar de Versión del Script

Para usar la versión mejorada:

```bash
crontab -e
# Cambiar:
# De: .../check_citas.py
# A:  .../check_citas_mejorado.py
```

### Cambiar Oferta/Trámite

Editar `check_citas.py` y buscar:
```python
select.select_by_visible_text("NACIONALIDAD")
```

Cambiar "NACIONALIDAD" por otro trámite disponible.

---

## 🐛 TROUBLESHOOTING

### Problema 1: "chromedriver not found"

**Causas posibles:**
- ChromeDriver no descargado
- ChromeDriver no está en PATH
- ChromeDriver con permiso incorrecto

**Soluciones:**
```bash
# Opción A: Descargar e instalar
# 1. Ve a: https://chromedriver.chromium.org/
# 2. Descarga la versión correspondiente a tu Chrome
# 3. Descomprime
# 4. Instala:
chmod +x chromedriver
sudo mv chromedriver /usr/local/bin/

# Opción B: Instalar desde repositorio (si disponible)
sudo apt-get install chromium-browser  # Instalará Chrome
```

**Verificar:**
```bash
which chromedriver
chromedriver --version
```

---

### Problema 2: "Selenium not found" o "Requests not found"

**Causas posibles:**
- Pip packages no instalados
- Python incorrecto
- Virtualenv activo

**Soluciones:**
```bash
# Reinstalar
pip3 install --upgrade selenium requests

# O con instalador:
bash install.sh

# Verificar instalación
python3 -c "import selenium; print('✅ Selenium OK')"
python3 -c "import requests; print('✅ Requests OK')"
```

---

### Problema 3: "Telegram token invalid"

**Causas posibles:**
- Token copiado incorrectamente
- Espacios al inicio/final
- Token vencido (muy raro)

**Soluciones:**
```bash
# 1. Verifica el token en @BotFather
# 2. Copia sin espacios
# 3. Edita script:
nano check_citas.py

# 4. Verifica exactamente:
echo "123456789:ABCDefGHIJklmnoPQRStuvwxyz1234567890"

# 5. Si sigue fallando, crea nuevo bot:
# - @BotFather → /newbot
# - Copia nuevo TOKEN
# - Edita script
```

---

### Problema 4: No recibe notificaciones en Telegram

**Causas posibles:**
- Chat ID incorrecto
- Token incorrecto
- Notificaciones desactivadas en Telegram
- No hay disponibilidad (comprueba logs)

**Soluciones:**
```bash
# 1. Ejecutar test
python3 test_config.py

# 2. Ver logs
tail -f citas_check.log

# 3. Ejecutar manualmente
python3 check_citas.py

# 4. Verificar Chat ID
# Ve a: https://api.telegram.org/bot{TOKEN}/getUpdates
# Busca "chat":{"id":XXXXX}

# 5. Verificar notificaciones en Telegram
# Settings → Notifications → Activadas
```

---

### Problema 5: El cron no se ejecuta

**Causas posibles:**
- Cron no configurado
- Path incorrecto
- Permisos insuficientes
- Servicio cron no activo

**Soluciones:**
```bash
# 1. Verificar si está en crontab
crontab -l | grep check_citas

# 2. Si está vacío, configurar:
bash setup_cron.sh

# 3. Verificar permisos del script
ls -l check_citas.py
# Debe mostrar: -rwxr-xr-x (ejecutable)
chmod +x check_citas.py

# 4. Verificar que cron está activo
sudo systemctl status cron

# 5. Ver logs de cron
grep CRON /var/log/syslog | tail -20
```

---

### Problema 6: Script muy lento

**Causas posibles:**
- Internet lento
- Página de citas lenta
- Chrome usando mucha RAM

**Soluciones:**
```bash
# 1. Usar versión mejorada
crontab -e
# Cambiar a: .../check_citas_mejorado.py

# 2. Aumentar timeouts en script
nano check_citas.py
# Buscar: driver.set_page_load_timeout(40)
# Cambiar 40 a número mayor si es necesario

# 3. Ejecutar en horas de menos carga
crontab -e
# Cambiar a: 0 3,9,15,21 * * *
```

---

## 📝 LOGS Y DIAGNÓSTICO

### Estructura de Log

Cada ejecución genera:
```
2024-01-15 10:30:45,123 - INFO - =================================================
2024-01-15 10:30:45,456 - INFO - VERIFICADOR DE CITAS - JUNTA DE ANDALUCÍA
2024-01-15 10:30:45,789 - INFO - Ejecución: 15/01/2024 10:30:45
2024-01-15 10:30:45,890 - INFO - =================================================
2024-01-15 10:30:46,100 - INFO - 🔍 Iniciando verificación de disponibilidad...
2024-01-15 10:30:46,200 - INFO - 📍 Accediendo a la web de citas...
2024-01-15 10:30:50,300 - INFO - 📝 Seleccionando 'REGISTRO CIVIL EXCLUSIVO DE MÁLAGA'...
2024-01-15 10:30:50,400 - INFO - ✅ Sede seleccionada con Select
...
```

### Interpretar Logs

| Mensaje | Significado | Acción |
|---------|-----------|--------|
| `Iniciando verificación` | Script comenzó | Normal |
| `Accediendo a la web` | Abriendo navegador | Esperar |
| `Sede seleccionada` | Paso 1 completado | Continúa normalmente |
| `Trámite seleccionado` | Paso 2 completado | Continúa normalmente |
| `DISPONIBILIDAD ENCONTRADA` | ¡HAY CITAS! | Debe haber notificación |
| `No hay disponibilidad` | Sin citas ahora | Intentará después |
| `Error durante` | Algo falló | Ver descripción del error |
| `Navegador cerrado` | Ejecución terminada | Normal |

---

## 🔒 SEGURIDAD

### Consideraciones de Seguridad

**TOKEN DE TELEGRAM:**
- ✅ Almacenado localmente en el script
- ❌ NUNCA compartir públicamente
- ❌ NUNCA subir a GitHub/repositorios públicos
- ✅ Si se compromete: crea nuevo bot en @BotFather

**CHAT ID:**
- ✅ Relativamente seguro (solo identifica tu chat)
- ℹ️ No proporciona acceso a otras funciones del bot

**DATOS PERSONALES:**
- ✅ El script no almacena datos personales
- ✅ Solo verifica disponibilidad
- ✅ No extrae información sensible

**SCRIPT EN GENERAL:**
- ✅ Código abierto, revisable
- ✅ No contiene malware
- ✅ Solo accede a web de Junta Andalucía

### Backup de Configuración

```bash
# Guardar tu configuración
cp check_citas.py check_citas_backup.py

# Restaurar si es necesario
cp check_citas_backup.py check_citas.py
```

---

## 💾 MANTENIMIENTO

### Limpieza de Logs

```bash
# Ver tamaño del log
du -h citas_check.log

# Limpiar log (mantiene estructura)
echo ""> citas_check.log

# Ver últimas líneas antes de limpiar
tail -20 citas_check.log > citas_check_backup.txt
```

### Actualizar Script

Si hay nueva versión:
```bash
# Backup de actual
cp check_citas.py check_citas_old.py

# Descargar nueva versión
# Copiar nueva versión

# Restaurar configuración
nano check_citas.py
# Poner de nuevo tus credenciales de Telegram

# Probar
python3 test_config.py
python3 check_citas.py
```

### Verificación Periódica

Cada mes:
```bash
# 1. Verificar que sigue ejecutándose
crontab -l

# 2. Revisar logs recientes
tail -100 citas_check.log

# 3. Ejecutar test
python3 test_config.py

# 4. Probar manualmente
python3 check_citas.py
```

---

## 📚 REFERENCIAS Y RECURSOS

### Documentación Oficial
- **Telegram Bot API:** https://core.telegram.org/bots/api
- **Selenium:** https://selenium.dev/
- **Cron:** `man crontab`
- **Python:** https://www.python.org/doc/

### Herramientas Útiles
- **Cron Generator:** https://crontab.guru/
- **Telegram Bot Testing:** https://api.telegram.org/bot{TOKEN}/getMe
- **Chrome Downloads:** https://chromedriver.chromium.org/

### Troubleshooting Online
- Stack Overflow tag: `selenium`, `cron`, `python`
- GitHub Issues en proyectos similares
- Documentación oficial de dependencias

---

## 🎓 CÓMO APRENDER MÁS

### Si quieres entender Cron
```bash
man crontab
# O leer: https://crontab.guru/
```

### Si quieres entender Selenium
```python
python3 -c "from selenium import webdriver; help(webdriver.Chrome)"
```

### Si quieres ver el código
```bash
cat check_citas.py
# O editar:
nano check_citas.py
```

---

## 📞 SOPORTE Y AYUDA

### Si tienes problemas:

1. **Ejecutar test automático:**
   ```bash
   python3 test_config.py
   ```

2. **Ver logs detallados:**
   ```bash
   tail -50 citas_check.log
   ```

3. **Verificar instalación:**
   ```bash
   which python3 chromedriver
   ```

4. **Probar manualmente:**
   ```bash
   python3 check_citas.py
   ```

5. **Leer documentación:**
   - README.md (rápido)
   - SETUP_GUIDE.md (detallado)
   - ESTRUCTURA.md (técnico)

---

## 🎯 CHECKLIST FINAL

### ✅ Instalación
- [ ] Python 3 instalado
- [ ] Dependencias instaladas (selenium, requests)
- [ ] ChromeDriver en /usr/local/bin/
- [ ] Permisos configurados

### ✅ Configuración
- [ ] TOKEN de Telegram obtenido
- [ ] CHAT_ID obtenido
- [ ] Script actualizado con credenciales
- [ ] Test ejecutado exitosamente

### ✅ Automatización
- [ ] Cron configurado
- [ ] Horarios correctos
- [ ] Logs accesibles

### ✅ Verificación
- [ ] Script ejecuta sin errores
- [ ] Notificaciones llegan a Telegram
- [ ] Logs se generan correctamente

---

## 🎉 ¡LISTO!

Tu sistema de verificación de citas está **completamente operativo**. 

**Próximos pasos:**
1. Repose y deje ejecutarse automáticamente
2. Espere notificación en Telegram cuando haya disponibilidad
3. Haga clic en el link para reservar inmediatamente

**El sistema continuará verificando 4 veces al día hasta que:**
- Encuentre disponibilidad (notificará)
- Lo deshabilite (comentar en crontab)
- Algo falle (revisar logs)

---

**Documento generado:** 2024-06-16
**Versión:** 2.0 (Completa)
**Mantenimiento:** Sistema probado y funcional
