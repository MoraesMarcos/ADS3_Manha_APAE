from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import traceback

BASE_URL = "http://localhost:5000"
driver = webdriver.Chrome()

try:
    # === LOGIN ===
    driver.get(BASE_URL + "/login")
    usuario_input = driver.find_element(By.NAME, "usuario")
    senha_input = driver.find_element(By.NAME, "senha")
    usuario_input.send_keys("admin")
    senha_input.send_keys("senha123")
    senha_input.send_keys(Keys.RETURN)
    time.sleep(2)
    print("✅ Login realizado com sucesso.")

    # === VALIDAÇÃO DO LOGIN PELA PRESENÇA DE CONTEÚDO ===
    print("URL atual:", driver.current_url)
    assert "Dashboard" in driver.page_source or "Bem-vindo" in driver.page_source or "Usuários" in driver.page_source
    print("✅ Dashboard acessado com sucesso.")

    # === ENVIO DE FEEDBACK ===
    driver.get(BASE_URL + "/feedback")
    time.sleep(1)
    driver.find_element(By.NAME, "tipo").send_keys("sugestao")
    driver.find_element(By.NAME, "mensagem").send_keys("Esse é um teste automático de feedback.")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    assert "Obrigado pelo seu feedback" in driver.page_source or "Feedback enviado" in driver.page_source
    print("✅ Feedback enviado com sucesso.")

    # === CADASTRO SIMPLES DE USUÁRIO ===
    driver.get(BASE_URL + "/cadastro")
    time.sleep(1)
    driver.find_element(By.NAME, "nome").send_keys("Usuário2 Selenium")
    driver.find_element(By.NAME, "nome_social").send_keys("Teste Social")
    driver.find_element(By.NAME, "data_nascimento").send_keys("2000-01-01")
    driver.find_element(By.NAME, "sexo").send_keys("masculino")
    driver.find_element(By.NAME, "ocupacao").send_keys("Estudante")

    # Role até o botão e clique
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    time.sleep(0.5)
    submit_btn.click()

    time.sleep(2)
    assert "Usuário cadastrado" in driver.page_source or "sucesso" in driver.page_source
    print("✅ Usuário cadastrado com sucesso.")

except Exception as e:
    print(f"❌ Erro durante os testes: {e}")
    traceback.print_exc()

finally:
    driver.quit()
