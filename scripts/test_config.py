#!/usr/bin/env python3
"""
Script de PRUEBA para verificar que todo está configurado correctamente
NO requiere configuración de Telegram
"""

import sys
import time
import subprocess

def print_step(step_num, title):
    print(f"\n{'='*60}")
    print(f"✓ PASO {step_num}: {title}")
    print(f"{'='*60}\n")

def check_python():
    print_step(1, "Verificando Python 3")
    version = sys.version
    print(f"✅ Python encontrado: {version}")
    return True

def check_imports():
    print_step(2, "Verificando librerías requeridas")
    
    try:
        import selenium
        print(f"✅ Selenium: {selenium.__version__}")
    except ImportError:
        print("❌ Selenium no está instalado")
        print("   Instala con: pip3 install selenium")
        return False
    
    try:
        import requests
        print(f"✅ Requests: {requests.__version__}")
    except ImportError:
        print("❌ Requests no está instalado")
        print("   Instala con: pip3 install requests")
        return False
    
    return True

def check_chromedriver():
    print_step(3, "Verificando ChromeDriver")
    
    try:
        result = subprocess.run(['chromedriver', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✅ ChromeDriver encontrado:")
            print(f"   {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"⚠️  Error verificando: {e}")
    
    print("❌ ChromeDriver NO encontrado")
    print("\n   Pasos para instalarlo:")
    print("   1. Descarga desde: https://chromedriver.chromium.org/")
    print("   2. Descomprime el archivo")
    print("   3. Muévelo a: sudo mv chromedriver /usr/local/bin/")
    print("   4. Hazlo ejecutable: chmod +x /usr/local/bin/chromedriver")
    return False

def check_chrome():
    print_step(4, "Verificando Google Chrome/Chromium")
    
    try:
        # Intentar ejecutar Chrome en modo test
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        version = driver.execute_script("return navigator.userAgent")
        driver.quit()
        
        print(f"✅ Chrome funcional:")
        print(f"   {version[:80]}")
        return True
        
    except Exception as e:
        print(f"❌ Error con Chrome: {str(e)}")
        print("\n   Posibles soluciones:")
        print("   • Instalar Chrome: sudo apt-get install google-chrome-stable")
        print("   • O Chromium: sudo apt-get install chromium-browser")
        return False

def check_selenium_web_access():
    print_step(5, "Verificando acceso web con Selenium")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        
        print("⏳ Abriendo navegador (esto toma unos segundos)...")
        driver = webdriver.Chrome(options=options)
        
        print("⏳ Accediendo a página de prueba...")
        driver.get("https://www.example.com")
        
        # Verificar que cargó
        title = driver.title
        if "example" in title.lower():
            print(f"✅ Acceso web funcionando")
            print(f"   Título de página: {title}")
            driver.quit()
            return True
        else:
            print(f"⚠️  Página cargada pero con título inesperado: {title}")
            driver.quit()
            return True
            
    except Exception as e:
        print(f"❌ Error de acceso web: {str(e)}")
        return False

def check_target_website():
    print_step(6, "Verificando acceso a página de citas de Junta Andalucía")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        
        url = "https://www.juntadeandalucia.es/justicia/citaprevia/?idCliente=4"
        
        print(f"⏳ Accediendo a: {url}")
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)
        driver.get(url)
        
        time.sleep(2)
        
        # Verificar que está en la página correcta
        page_source = driver.page_source
        if "cita" in page_source.lower() or "andalucia" in page_source.lower():
            print("✅ Página de citas cargada correctamente")
            
            # Intentar encontrar elementos
            try:
                from selenium.webdriver.support.ui import Select
                from selenium.webdriver.common.by import By
                
                sede_elem = driver.find_element(By.ID, "idSede")
                print("✅ Campo 'Sede' encontrado en página")
                
                tramite_elem = driver.find_element(By.ID, "idTramite")
                print("✅ Campo 'Trámite' encontrado en página")
                
            except Exception as e:
                print(f"⚠️  No se encontraron todos los campos: {e}")
            
            driver.quit()
            return True
        else:
            print("❌ Página no se cargó correctamente")
            driver.quit()
            return False
            
    except Exception as e:
        print(f"❌ Error accediendo a página de citas: {str(e)}")
        return False

def check_telegram_config():
    print_step(7, "Verificando configuración de Telegram")
    
    try:
        with open('/home/claude/check_citas.py', 'r') as f:
            content = f.read()
            
        if 'TU_BOT_TOKEN_AQUI' in content and 'TU_CHAT_ID_AQUI' in content:
            print("⚠️  Telegram NO está configurado")
            print("\n   Pasos para configurar:")
            print("   1. Busca @BotFather en Telegram")
            print("   2. Envía /newbot")
            print("   3. Copia el TOKEN que recibes")
            print("   4. Edita check_citas.py: nano /home/claude/check_citas.py")
            print("   5. Reemplaza TU_BOT_TOKEN_AQUI con tu token")
            print("   6. Obtén tu Chat ID desde: https://api.telegram.org/bot{TOKEN}/getUpdates")
            print("   7. Reemplaza TU_CHAT_ID_AQUI con tu ID")
            return False
        else:
            print("✅ Telegram aparenta estar configurado")
            return True
            
    except Exception as e:
        print(f"⚠️  Error verificando Telegram: {e}")
        return False

def run_all_checks():
    print("\n" + "="*60)
    print("🧪 PRUEBA DE CONFIGURACIÓN - VERIFICADOR DE CITAS")
    print("="*60)
    
    results = []
    
    # Pruebas esenciales
    results.append(("Python 3", check_python()))
    results.append(("Librerías", check_imports()))
    results.append(("ChromeDriver", check_chromedriver()))
    results.append(("Google Chrome", check_chrome()))
    results.append(("Acceso Web", check_selenium_web_access()))
    results.append(("Página de Citas", check_target_website()))
    results.append(("Telegram", check_telegram_config()))
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60 + "\n")
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {passed} pasadas, {failed} fallidas\n")
    
    if failed == 0:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("\n✅ Tu sistema está listo para usar el verificador de citas")
        print("\nPróximos pasos:")
        print("1. Asegúrate de que Telegram está configurado")
        print("2. Prueba el script: python3 /home/claude/check_citas.py")
        print("3. Configura cron: bash /home/claude/setup_cron.sh")
        return True
    else:
        print("❌ Hay problemas que deben resolverse")
        print("\nRe-ejecuta este script después de corregir los errores:")
        print("  python3 test_config.py")
        return False

if __name__ == "__main__":
    success = run_all_checks()
    sys.exit(0 if success else 1)
