#!/usr/bin/env python3
"""
Script para verificar disponibilidad de citas de Nacionalidad en REGISTRO CIVIL EXCLUSIVO DE MÁLAGA
Notifica por Telegram cuando encuentra slots disponibles
"""

import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging
from datetime import datetime

# Configuración de logging
_log_handlers = [logging.StreamHandler()]
if not os.environ.get("GITHUB_ACTIONS"):
    _log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    os.makedirs(_log_dir, exist_ok=True)
    _log_handlers.append(logging.FileHandler(os.path.join(_log_dir, "citas_check.log")))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=_log_handlers
)
logger = logging.getLogger(__name__)

# ===== CREDENCIALES =====
# Local: lee de scripts/config.py (ignorado por git)
# GitHub Actions: lee de los secrets del repositorio
try:
    from config import TELEGRAM_BOT_TOKEN as _TOKEN, TELEGRAM_CHAT_ID as _CHAT_ID
except ImportError:
    _TOKEN, _CHAT_ID = "", ""

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", _TOKEN)
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", _CHAT_ID)
URL_CITAS = "https://www.juntadeandalucia.es/justicia/citaprevia/?idCliente=4"
# ========================

def send_telegram_notification(message, screenshot_path=None):
    """Envía una notificación por Telegram, con captura de pantalla opcional"""
    try:
        if screenshot_path:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            with open(screenshot_path, "rb") as photo:
                response = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "caption": message, "parse_mode": "HTML"}, files={"photo": photo}, timeout=30)
        else:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            response = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=10)

        if response.status_code == 200:
            logger.info("Notificación enviada por Telegram")
            return True
        else:
            logger.error(f"Error enviando Telegram: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error en Telegram: {str(e)}")
        return False

def check_availability():
    """Verifica la disponibilidad de citas"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    chrome_options.page_load_strategy = "none"

    driver = None
    try:
        logger.info("🔍 Iniciando verificación de disponibilidad...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(90)
        wait = WebDriverWait(driver, 30)

        # Paso 1: Acceder a la página
        logger.info(f"📍 Accediendo a {URL_CITAS}")
        driver.get(URL_CITAS)

        # Paso 2: Seleccionar oficina "REGISTRO CIVIL EXCLUSIVO DE MÁLAGA"
        logger.info("📝 Seleccionando oficina...")
        oficina_select = wait.until(EC.presence_of_element_located((By.ID, "comboOficinas")))
        Select(oficina_select).select_by_visible_text("REGISTRO CIVIL EXCLUSIVO DE MÁLAGA")
        logger.info("✅ Oficina seleccionada")
        time.sleep(2)

        # Paso 3: Clic en Continuar
        logger.info("▶️ Clic en Continuar...")
        btn_continuar = driver.find_element(By.ID, "btnContinuar1")
        btn_continuar.click()
        time.sleep(3)

        # Paso 4: Seleccionar trámite NACIONALIDAD (aparece dinámicamente)
        logger.info("📝 Seleccionando trámite NACIONALIDAD...")
        try:
            tramite_link = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'NACIONALIDAD')]"))
            )
            tramite_link.click()
            logger.info("✅ Trámite NACIONALIDAD seleccionado")
            time.sleep(3)
        except Exception as e:
            logger.warning(f"⚠️ No se encontró el trámite NACIONALIDAD como enlace: {e}")
            # Intentar como dropdown
            try:
                tramite_select = driver.find_element(By.ID, "comboServicios")
                Select(tramite_select).select_by_visible_text("NACIONALIDAD")
                logger.info("✅ Trámite seleccionado via dropdown")
                time.sleep(3)
            except Exception as e2:
                logger.warning(f"⚠️ Tampoco encontrado como dropdown: {e2}")

        # Paso 5: Continuar al calendario si hay botón
        try:
            btn2 = driver.find_element(By.ID, "btnContinuar1")
            if btn2.is_displayed() and btn2.is_enabled():
                btn2.click()
                time.sleep(3)
        except Exception:
            pass

        # Paso 6: Captura de pantalla del estado actual
        import tempfile, os
        screenshot_path = os.path.join(tempfile.gettempdir(), "citas_screenshot.png")
        driver.set_window_size(1280, 900)
        driver.save_screenshot(screenshot_path)

        # Paso 7: Buscar slots disponibles
        logger.info("🔍 Buscando slots disponibles...")
        page_source = driver.page_source

        disponible_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'disponible') or contains(@class, 'libre')]")
        disponible_text = driver.find_elements(By.XPATH, "//*[contains(text(), 'Disponible') or contains(text(), 'disponible') or contains(text(), 'Libre')]")
        no_disponible = any(msg in page_source for msg in [
            "no hay citas disponibles",
            "Agenda aún no disponible",
            "No hay disponibilidad"
        ])

        all_slots = disponible_elements + disponible_text
        now = datetime.now().strftime('%d/%m/%Y %H:%M')

        # Calcular próxima ejecución
        horas_cron = [4, 8, 16, 20]
        ahora = datetime.now()
        proxima = next((h for h in horas_cron if h > ahora.hour), horas_cron[0])
        proxima_str = f"{proxima:02d}:00"

        if all_slots and not no_disponible:
            logger.info(f"DISPONIBILIDAD ENCONTRADA: {len(all_slots)} indicadores")
            message = (
                f"🎉 <b>¡CITA DISPONIBLE EN MÁLAGA!</b>\n\n"
                f"📅 Detectado: {now}\n"
                f"🏛️ <b>REGISTRO CIVIL EXCLUSIVO DE MÁLAGA</b>\n"
                f"📋 Trámite: <b>NACIONALIDAD</b>\n\n"
                f"✅ {len(all_slots)} slots disponibles\n\n"
                f"🔗 <a href=\"{URL_CITAS}\">Ir a reservar ahora</a>\n\n"
                f"🔂 Próxima ejecución programada para las {proxima_str}"
            )
            send_telegram_notification(message, screenshot_path)
            return True
        else:
            logger.info("No hay disponibilidad en este momento")
            message = (
                f"🔍 <b>Verificación de citas — {now}</b>\n\n"
                f"🏛️ REGISTRO CIVIL EXCLUSIVO DE MÁLAGA\n"
                f"📋 Trámite: NACIONALIDAD\n\n"
                f"❌ No hay citas disponibles en este momento.\n\n"
                f"🔂 Próxima ejecución programada para las {proxima_str}"
            )
            send_telegram_notification(message, screenshot_path)
            return False

    except Exception as e:
        logger.error(f"❌ Error durante la verificación: {str(e)}")
        return False

    finally:
        if driver:
            driver.quit()
            logger.info("🔌 Navegador cerrado")

def main():
    """Función principal"""
    logger.info("=" * 50)
    logger.info("VERIFICADOR DE CITAS - JUNTA DE ANDALUCÍA")
    logger.info(f"Ejecución: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info("=" * 50)
    
    # Validar configuración
    if TELEGRAM_BOT_TOKEN == "TU_BOT_TOKEN_AQUI" or TELEGRAM_CHAT_ID == "TU_CHAT_ID_AQUI":
        logger.error("❌ ERROR: Debes configurar TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID")
        return
    
    check_availability()

if __name__ == "__main__":
    main()
