from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import traceback

BASE_URL = "http://localhost:5000"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

try:
    # === LOGIN ===
    driver.get(BASE_URL + "/login")
    wait.until(EC.presence_of_element_located((By.NAME, "usuario"))).send_keys("admin")
    driver.find_element(By.NAME, "senha").send_keys("senha123", Keys.RETURN)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("✅ Login realizado com sucesso.")

    # === DASHBOARD ===
    assert "Dashboard" in driver.page_source or "Bem-vindo" in driver.page_source
    print("✅ Dashboard acessado com sucesso.")

    # === FEEDBACK ===
    driver.get(BASE_URL + "/feedback")
    wait.until(EC.presence_of_element_located((By.NAME, "tipo"))).send_keys("sugestao")
    driver.find_element(By.NAME, "mensagem").send_keys("Feedback automático via Selenium.")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    assert "feedback" in driver.page_source.lower()
    print("✅ Feedback enviado com sucesso.")

    # === CADASTRO DE USUÁRIO ===
    driver.get(BASE_URL + "/cadastro")
    wait.until(EC.presence_of_element_located((By.NAME, "nome"))).send_keys("Teste Selenium")
    driver.find_element(By.NAME, "nome_social").send_keys("Social Teste")
    driver.find_element(By.NAME, "data_nascimento").send_keys("2000-01-01")
    driver.find_element(By.NAME, "sexo").send_keys("masculino")
    driver.find_element(By.NAME, "ocupacao").send_keys("Estudante")

    # CPF (opcional)
    try:
        cpf_field = driver.find_element(By.NAME, "cpf")
        if cpf_field.is_displayed() and cpf_field.is_enabled():
            cpf_field.send_keys("12345678900")
        else:
            print("⚠️ Campo de CPF não interagível.")
    except NoSuchElementException:
        print("⚠️ Campo CPF não encontrado.")


    # E-mail (usa domínio mais comum para evitar alerta)
    # Campo de e-mail
    try:
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        driver.execute_script("arguments[0].scrollIntoView(true);", email_field)
        time.sleep(0.3)
        if email_field.is_displayed() and email_field.is_enabled():
            email_field.click()
            email_field.send_keys("teste.selenium@gmail.com")
        else:
            print("⚠️ Campo de e-mail não está interagível.")
    except Exception as e:
        print(f"❌ Erro ao interagir com campo de e-mail: {e}")


    # Telefone residencial
    try:
        tel_field = driver.find_element(By.NAME, "telefone_residencial")
        if tel_field.is_displayed():
            driver.execute_script("arguments[0].scrollIntoView(true);", tel_field)
            time.sleep(0.3)
            tel_field.clear()
            tel_field.send_keys("81999999999")
        else:
            print("⚠️ Telefone não está visível.")
    except (NoSuchElementException, ElementNotInteractableException):
        print("⚠️ Campo de telefone não encontrado ou não interagível.")

    # Submeter
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    time.sleep(0.5)
    submit_btn.click()

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    assert "sucesso" in driver.page_source.lower() or "cadastrado" in driver.page_source.lower()
    print("✅ Usuário cadastrado com sucesso.")

    # === LOGOUT ===
    driver.get(BASE_URL + "/logout")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    assert "login" in driver.page_source.lower()
    print("✅ Logout realizado com sucesso.")

except UnexpectedAlertPresentException:
    try:
        alert = driver.switch_to.alert
        print(f"⚠️ Alerta inesperado: {alert.text}")
        alert.accept()
    except:
        print("⚠️ Um alerta foi disparado, mas já estava fechado.")
except Exception as e:
    print(f"❌ Erro durante os testes: {e}")
    traceback.print_exc()
finally:
    driver.quit()
