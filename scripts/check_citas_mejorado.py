#!/usr/bin/env python3
"""
Script MEJORADO para verificar disponibilidad de citas de Nacionalidad 
en REGISTRO CIVIL EXCLUSIVO DE MÁLAGA
Notifica por Telegram cuando encuentra slots disponibles
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import logging
from datetime import datetime
import json

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/claude/citas_check.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ===== CONFIGURAR ESTOS VALORES =====
TELEGRAM_BOT_TOKEN = "TU_BOT_TOKEN_AQUI"  # Obtén esto de @BotFather en Telegram
TELEGRAM_CHAT_ID = "TU_CHAT_ID_AQUI"      # Tu ID de Telegram (número)
URL_CITAS = "https://www.juntadeandalucia.es/justicia/citaprevia/?idCliente=4"
# ===================================

def send_telegram_notification(message, available_count=None):
    """Envía una notificación por Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            logger.info(f"✅ Notificación enviada por Telegram ({available_count} slots disponibles)")
            return True
        else:
            logger.error(f"❌ Error enviando Telegram: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Error en Telegram: {str(e)}")
        return False

def extract_available_dates(driver):
    """Extrae información detallada de fechas y horas disponibles"""
    try:
        available_info = []
        
        # Buscar la tabla de disponibilidad
        # Intenta diferentes selectores CSS/XPath
        
        # Opción 1: Buscar todas las celdas con clase "disponible"
        try:
            available_cells = driver.find_elements(By.XPATH, "//*[@class='disponible' or contains(@class, 'disponible')]")
            if available_cells:
                logger.info(f"✅ Encontrados {len(available_cells)} elementos con clase 'disponible'")
                for cell in available_cells[:5]:  # Limitar a 5 primeros
                    try:
                        time_text = cell.text
                        parent = cell.find_element(By.XPATH, "./ancestor::tr")
                        date_text = parent.find_elements(By.TAG_NAME, "th")[0].text if parent.find_elements(By.TAG_NAME, "th") else "Fecha desconocida"
                        available_info.append(f"{date_text} - {time_text}")
                    except:
                        available_info.append(cell.text)
        except Exception as e:
            logger.warning(f"Opción 1 fallida: {e}")
        
        # Opción 2: Buscar por texto "Disponible"
        if not available_info:
            try:
                available_text = driver.find_elements(By.XPATH, "//*[contains(text(), 'Disponible')]")
                if available_text:
                    logger.info(f"✅ Encontrados {len(available_text)} elementos con texto 'Disponible'")
                    for elem in available_text[:5]:
                        available_info.append(elem.text)
            except Exception as e:
                logger.warning(f"Opción 2 fallida: {e}")
        
        # Opción 3: Buscar por color RGB verde (aproximadamente)
        if not available_info:
            try:
                all_cells = driver.find_elements(By.XPATH, "//table//td | //table//th")
                for cell in all_cells:
                    style = cell.get_attribute("style") or ""
                    class_attr = cell.get_attribute("class") or ""
                    
                    # Buscar indicios de verde
                    if "rgb(76, 175, 80)" in style or "rgb(40, 167, 69)" in style or "green" in class_attr.lower():
                        available_info.append(cell.text)
            except Exception as e:
                logger.warning(f"Opción 3 fallida: {e}")
        
        return available_info
        
    except Exception as e:
        logger.warning(f"Error extrayendo información: {e}")
        return []

def check_availability():
    """Verifica la disponibilidad de citas"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    try:
        logger.info("🔍 Iniciando verificación de disponibilidad...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(40)
        
        # Paso 1: Acceder a la página
        logger.info(f"📍 Accediendo a la web de citas...")
        driver.get(URL_CITAS)
        time.sleep(4)
        
        wait = WebDriverWait(driver, 15)
        
        # Paso 2: Seleccionar "REGISTRO CIVIL EXCLUSIVO DE MÁLAGA"
        logger.info("📝 Seleccionando 'REGISTRO CIVIL EXCLUSIVO DE MÁLAGA'...")
        try:
            # Intentar con Select (dropdown estándar)
            try:
                sede_select = wait.until(EC.presence_of_element_located((By.ID, "idSede")))
                select_sede = Select(sede_select)
                select_sede.select_by_visible_text("REGISTRO CIVIL EXCLUSIVO DE MÁLAGA")
                logger.info("✅ Sede seleccionada con Select")
                time.sleep(2)
            except:
                # Intentar clickeando
                registro_option = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//*[contains(text(), 'REGISTRO CIVIL EXCLUSIVO DE MÁLAGA')]")
                ))
                registro_option.click()
                logger.info("✅ Sede seleccionada con click")
                time.sleep(2)
        except Exception as e:
            logger.error(f"❌ Error seleccionando sede: {e}")
            return False
        
        # Paso 3: Seleccionar "NACIONALIDAD" en trámites
        logger.info("📝 Seleccionando trámite 'NACIONALIDAD'...")
        try:
            tramite_select = wait.until(EC.presence_of_element_located((By.ID, "idTramite")))
            select_tramite = Select(tramite_select)
            select_tramite.select_by_visible_text("NACIONALIDAD")
            logger.info("✅ Trámite seleccionado")
            time.sleep(2)
        except Exception as e:
            logger.error(f"❌ Error seleccionando trámite: {e}")
            return False
        
        # Paso 4: Esperar a que cargue la tabla de disponibilidad
        logger.info("⏳ Esperando carga de disponibilidad...")
        time.sleep(3)
        
        # Hacer scroll para asegurar visibilidad
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Paso 5: Buscar slots disponibles
        logger.info("🔍 Analizando disponibilidad...")
        
        # Método 1: Buscar elementos con clase "disponible"
        available_slots = driver.find_elements(By.XPATH, "//*[contains(@class, 'disponible')]")
        
        # Método 2: Si no encuentra, buscar por texto "Disponible" (sin espacios de negra)
        if not available_slots:
            available_slots = driver.find_elements(By.XPATH, "//*[contains(text(), 'Disponible')]")
        
        # Método 3: Búsqueda por color de fondo verde
        if not available_slots:
            all_elements = driver.find_elements(By.TAG_NAME, "*")
            for elem in all_elements:
                try:
                    bg_color = elem.value_of_css_property("background-color")
                    # Colores verdes típicos: rgb(76, 175, 80), rgb(40, 167, 69), #4CAF50
                    if "76, 175, 80" in bg_color or "40, 167, 69" in bg_color or "76,175,80" in bg_color:
                        if "Disponible" in elem.text or elem.text.strip():
                            available_slots.append(elem)
                except:
                    pass
        
        if available_slots:
            logger.info(f"✅ ¡DISPONIBILIDAD ENCONTRADA! {len(available_slots)} slots disponibles")
            
            # Extraer más información
            available_details = extract_available_dates(driver)
            
            # Construir mensaje
            message = "🎉 <b>¡CITA DISPONIBLE EN MÁLAGA!</b>\n\n"
            message += f"📅 Hora de verificación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            message += f"🏛️ <b>REGISTRO CIVIL EXCLUSIVO DE MÁLAGA</b>\n"
            message += f"📋 Trámite: <b>NACIONALIDAD</b>\n\n"
            message += f"✅ <b>{len(available_slots)} slots disponibles encontrados</b>\n\n"
            
            if available_details:
                message += "<b>Fechas/Horas disponibles:</b>\n"
                for detail in available_details[:3]:
                    message += f"• {detail}\n"
                if len(available_details) > 3:
                    message += f"... y {len(available_details) - 3} más\n\n"
            
            message += "🔗 <a href=\"" + URL_CITAS + "\">Haz clic para reservar ahora</a>"
            
            send_telegram_notification(message, len(available_slots))
            return True
        else:
            logger.info("❌ No hay disponibilidad en este momento")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error durante la verificación: {str(e)}")
        logger.error(f"Excepción completa:", exc_info=True)
        return False
        
    finally:
        if driver:
            driver.quit()
            logger.info("🔌 Navegador cerrado")

def main():
    """Función principal"""
    logger.info("=" * 60)
    logger.info("VERIFICADOR DE CITAS - JUNTA DE ANDALUCÍA (VERSIÓN MEJORADA)")
    logger.info(f"Ejecución: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info("=" * 60)
    
    # Validar configuración
    if TELEGRAM_BOT_TOKEN == "TU_BOT_TOKEN_AQUI" or TELEGRAM_CHAT_ID == "TU_CHAT_ID_AQUI":
        logger.error("❌ ERROR: Debes configurar TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID")
        logger.error("Ver SETUP_GUIDE.md para instrucciones")
        return
    
    result = check_availability()
    
    logger.info("=" * 60)
    if result:
        logger.info("✅ VERIFICACIÓN COMPLETADA - DISPONIBILIDAD ENCONTRADA")
    else:
        logger.info("✅ VERIFICACIÓN COMPLETADA - Sin disponibilidad")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
