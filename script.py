from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException

def safe_click(driver, by, value, timeout=10):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
    element = driver.find_element(by, value)
    attempts = 0
    while attempts < 3:
        try:
            element.click()
            return
        except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            print(f"Click exception: {e}")
            attempts += 1
            time.sleep(1)
            element = driver.find_element(by, value)
    raise Exception(f"Failed to click the element after {attempts} attempts")

# Configurar el navegador web (en este caso, Chrome)
driver = webdriver.Chrome()

# Abrir la página de matrícula
driver.get("https://matricula.utp.ac.pa/mmatricula/menu/procesos/%202024/fVdgTSf0UhSkneYeiRVOfnndTnP0")

input("Presione Enter para continuar")

controlador = True
while controlador:
    try:
        # Esperar a que el dropdown sea clickeable
        time.sleep(1)
        grupo_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "cphContenido_ddlGrupos"))
        )
        grupo_dropdown.click()
        #time.sleep(1)  # Esperar un momento para que el dropdown cargue opciones

        # Seleccionar el grupo 1LS131
        grupo_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//option[@value='1LS131']"))
        )
        grupo_option.click()

        # Esperar a que la página se recargue y el botón de matricular esté disponible nuevamente
        #time.sleep(3)  # Ajustar según el tiempo que toma la recarga

        # Hacer clic en el botón de matricular nuevamente
        safe_click(driver, By.ID, "cphContenido_lnkbMatricular")

        #time.sleep(3)

        # Asegurarse de que el modal esté completamente visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "cphContenido_lnkbAceptar"))
        )
        
        # Asegúrate de que el modal esté en vista
        driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.ID, "cphContenido_lnkbAceptar"))

        # Intentar hacer clic en el botón con JavaScript si el clic estándar falla
        accept_button = driver.find_element(By.ID, "cphContenido_lnkbAceptar")
        driver.execute_script("arguments[0].click();", accept_button)
        

    except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException) as e:
        print(f"Exception occurred: {e}")
        time.sleep(5)  # Esperar un momento antes de reintentar
