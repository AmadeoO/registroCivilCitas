# 📦 ESTRUCTURA DEL PROYECTO - VERIFICADOR DE CITAS MÁLAGA

## 📂 Archivos Creados

```
/home/claude/
├── 📄 README.md                  ← EMPIEZA POR AQUÍ
├── 📄 SETUP_GUIDE.md             ← Guía completa de configuración
├── 🐍 check_citas.py             ← Script principal (RECOMENDADO)
├── 🐍 check_citas_mejorado.py    ← Script alternativo (más robusto)
├── 🐍 test_config.py             ← Prueba tu configuración
├── 🔧 install.sh                 ← Instala dependencias
├── ⏰ setup_cron.sh              ← Configura ejecución automática
└── 📝 citas_check.log            ← Logs (se crea al ejecutar)
```

---

## 🚀 FLUJO DE USO

### Día 1: Instalación (15 minutos)

```bash
# 1. Instalar dependencias
bash /home/claude/install.sh

# 2. Obtener TOKEN en Telegram (@BotFather)
# 3. Obtener CHAT_ID (getUpdates)
# 4. Editar y configurar
nano /home/claude/check_citas.py
# Reemplaza: TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID

# 5. Probar
python3 /home/claude/test_config.py
python3 /home/claude/check_citas.py
```

### Día 1-2: Configuración Automática (5 minutos)

```bash
# Ejecutar solo UNA VEZ:
bash /home/claude/setup_cron.sh

# Verificar que está configurado:
crontab -l
```

### Día 3+: Uso Normal

- El script se ejecuta automáticamente 4 veces al día
- Recibirás notificación en Telegram si hay disponibilidad
- Ver logs: `tail -f /home/claude/citas_check.log`

---

## 📋 DESCRIPCIÓN DE CADA ARCHIVO

### `README.md` ⭐ EMPIEZA AQUÍ
- Guía rápida de 5 minutos
- Instrucciones paso a paso
- Solución de problemas frecuentes
- Personalizaciones de horarios

### `SETUP_GUIDE.md`
- Guía completa y detallada
- Explicaciones profundas
- Instrucciones para cada SO (Linux, macOS, Windows)
- Monitoreo y logs

### `check_citas.py` ✅ RECOMENDADO
- Script principal
- Automatiza navegación en web
- Detecta disponibilidad de citas
- Envía notificaciones por Telegram
- **Usar este por defecto**

### `check_citas_mejorado.py`
- Versión más robusta
- Mejor detección de slots disponibles
- Más selectores alternativos
- Usar si el estándar no funciona

### `test_config.py`
- Prueba todas las dependencias
- Verifica Selenium + Chrome
- Acceso a página de citas
- Configuración de Telegram
- **Ejecutar si hay problemas**

### `install.sh`
- Instala Python + pip
- Instala librerías (selenium, requests)
- Configura permisos
- Verifica ChromeDriver

### `setup_cron.sh`
- Configura ejecución automática
- Permite personalizar horarios
- Crea entrada en crontab
- Solo ejecutar UNA VEZ

### `citas_check.log`
- Registro de ejecuciones
- Se crea automáticamente
- Ver con: `tail -f citas_check.log`

---

## 🎯 CASOS DE USO

### Caso 1: Principiante (Sistema nuevo)
```bash
1. bash /home/claude/install.sh
2. Obtener TOKEN y CHAT_ID
3. nano /home/claude/check_citas.py (configurar)
4. python3 /home/claude/test_config.py
5. bash /home/claude/setup_cron.sh
```

### Caso 2: Algo no funciona
```bash
# Ejecutar pruebas
python3 /home/claude/test_config.py

# Ver logs
tail -50 /home/claude/citas_check.log

# Si falla Selenium: instalar Chrome
sudo apt-get install google-chrome-stable

# Si falla ChromeDriver: descargarlo
# https://chromedriver.chromium.org/
```

### Caso 3: Cambiar horarios
```bash
crontab -e
# Editar la línea con check_citas.py
# Cambiar números de horas
```

### Caso 4: Cambiar de versión (estándar a mejorada)
```bash
crontab -e
# Cambiar:
# De: .../check_citas.py
# A:  .../check_citas_mejorado.py
```

---

## 📊 REQUISITOS MÍNIMOS

- **Python**: 3.7+
- **RAM**: 512 MB
- **Disco**: 100 MB
- **Internet**: Conexión estable
- **Telegram**: Cuenta activa

---

## 🔄 CICLO DE EJECUCIÓN

```
Cron inicia script cada 6 horas (08:00, 12:00, 16:00, 20:00)
    ↓
Script abre navegador Chrome en modo headless
    ↓
Navega a https://www.juntadeandalucia.es/justicia/citaprevia/
    ↓
Selecciona: REGISTRO CIVIL EXCLUSIVO DE MÁLAGA
    ↓
Selecciona: NACIONALIDAD
    ↓
Espera carga de tabla de disponibilidad
    ↓
Busca slots verdes (Disponible)
    ↓
SI hay disponibilidad:
    ├─ Envía notificación Telegram
    └─ Guarda en log
    
SI NO hay disponibilidad:
    └─ Solo guarda en log
    
↓
Script se cierra
↓
Próxima ejecución en X horas...
```

---

## 💾 ALMACENAMIENTO DE DATOS

### Logs
- Ubicación: `/home/claude/citas_check.log`
- Tamaño: ~1 KB por ejecución
- Retención: Indefinida (considera limpiar mensualmente)

### Configuración
- Ubicación: Variables dentro de `check_citas.py`
- Backup: Haz copia de `check_citas.py` antes de modificar

### Cron
- Ubicación: `~/.crontab` (lista con `crontab -l`)
- Backup: `crontab -l > mi_cron_backup.txt`

---

## 🔐 SEGURIDAD

### TOKEN de Telegram
- ✅ Almacenado localmente en el script
- ❌ Nunca compartir públicamente
- ✅ Si se compromete: crear nuevo bot en @BotFather

### Chat ID
- ✅ Solo identifica TU cuenta
- ℹ️ No proporciona acceso completo

### Script
- ✅ No almacena datos personales
- ✅ Solo verifica disponibilidad
- ✅ Acceso solo web de Junta Andalucía

---

## 📞 SOPORTE RÁPIDO

| Problema | Solución |
|----------|----------|
| "chromedriver not found" | `sudo mv chromedriver /usr/local/bin/` |
| "Telegram token invalid" | Copiar sin espacios de @BotFather |
| No recibe notificaciones | Ejecutar `python3 test_config.py` |
| El cron no se ejecuta | `crontab -l` para verificar |
| Script muy lento | Usar versión mejorada |

---

## 📚 REFERENCIAS

- **Telegram Bot API**: https://core.telegram.org/bots
- **Selenium**: https://selenium.dev/
- **Cron**: `man crontab`
- **Web Scraping**: https://www.juntadeandalucia.es/justicia/citaprevia/

---

## ✨ TIPS Y TRUCOS

### Ver ejecuciones en tiempo real
```bash
watch -n 10 'tail -5 /home/claude/citas_check.log'
```

### Ejecutar manualmente en horario específico
```bash
at 14:30 < script.sh  # Ejecutar a las 14:30
```

### Cambiar solo el horario de verificación
```bash
crontab -e
# Cambiar números (0 8,12,16,20 * * * → 0 6,10,14,18 * * *)
```

### Desactivar temporalmente
```bash
crontab -e
# Comentar la línea: #0 8,12,16,20 * * * ...
```

---

## 🎓 APRENDER MÁS

### Sobre Cron
```bash
man crontab
```

### Sobre Selenium
```python
python3 -c "from selenium import webdriver; help(webdriver.Chrome)"
```

### Ver los logs completos
```bash
cat /home/claude/citas_check.log
```

---

**Creado:** 2024
**Versión:** 2.0 (Mejorada)
**Mantenimiento:** Últimas actualizaciones en Sistema Linux/macOS
