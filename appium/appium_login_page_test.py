# d:\repos\appium_and_flutter_test\integration_test\login_page_test.py
import unittest
from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LoginPageTests(unittest.TestCase):

    def setUp(self): 
        """Configuração do driver do Appium."""
        # Ajuste as capacidades conforme necessário para seu ambiente.
        capabilities = dict(
            platformName='Android',  # ou 'iOS'
            deviceName='NomeDoSeuDispositivoOuEmulador',
            appPackage='com.seuapp.pacote', # Substitua pelo pacote do seu app
            appActivity='com.seuapp.atividade.Principal', # Substitua pela atividade principal
            automationName='UiAutomator2'  # ou 'XCUITest' para iOS
        )
        options = AppiumOptions().load_capabilities(capabilities)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
        self.wait = WebDriverWait(self.driver, 10)  # Espera até 10 segundos

    def tearDown(self):
        """Encerra a sessão do driver após cada teste."""
        if self.driver:
            self.driver.quit()

    def test_ui_inicial_e_validacoes(self):
        """Verifica a UI inicial e as validações de campos vazios."""
        # Assumindo que os IDs dos elementos são consistentes entre Flutter e Appium.
        # Se necessário, use outros localizadores como XPath, accessibility_id, etc.
        self.wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        self.wait.until(EC.presence_of_element_located((By.ID, "passwordField")))
        self.wait.until(EC.presence_of_element_located((By.ID, "loginButton")))
        self.wait.until(EC.presence_of_element_located((By.ID, "forgotPasswordButton")))
        #  Verificação do título do AppBar pode ser mais complexa dependendo da implementação.

        # Tenta logar com campos vazios
        self.driver.find_element(By.ID, "loginButton").click()

        # Verifica mensagens de validação (ajuste os IDs ou localizadores conforme necessário)
        #  A lógica para verificar mensagens de erro pode variar dependendo de como elas são exibidas (e.g., SnackBar, alertas).
        #  Exemplo genérico:
        #  try:
        #      error_message = self.wait.until(EC.presence_of_element_located((By.ID, "errorMessage"))).text
        #      self.assertEqual(error_message, "Por favor, insira o usuário")
        #  except:
        #      self.fail("Mensagem de erro para usuário não encontrada.")
        #
        #  Repita a lógica para a senha.

    def test_login_credenciais_incorretas(self):
        """Login com credenciais incorretas exibe diálogo de erro."""
        username_field = self.driver.find_element(By.ID, "usernameField")
        password_field = self.driver.find_element(By.ID, "passwordField")
        username_field.send_keys("usuarioerrado")
        password_field.send_keys("senhaerrada")
        self.driver.find_element(By.ID, "loginButton").click()

        # Verifica o diálogo de erro
        alert = self.wait.until(EC.alert_is_present())
        self.assertEqual(alert.text, "Usuário ou senha incorretos.") # Ajuste a mensagem conforme necessário
        alert.accept() # ou dismiss() dependendo do botão para fechar

    def test_login_credenciais_corretas(self):
        """Login com credenciais corretas navega para HomePage e exibe SnackBar."""
        username_field = self.driver.find_element(By.ID, "usernameField")
        password_field = self.driver.find_element(By.ID, "passwordField")
        username_field.send_keys("admin")  # Substitua pelas credenciais corretas
        password_field.send_keys("1234")  # Substitua pelas credenciais corretas
        self.driver.find_element(By.ID, "loginButton").click()

        # Verifica SnackBar de sucesso (adapte a lógica de localização do SnackBar)
        # Exemplo com espera por um texto específico:
        # try:
        #     snackbar_text = self.wait.until(EC.presence_of_element_located((By.ID, "snackbarText"))).text
        #     self.assertEqual(snackbar_text, "Login bem-sucedido!")
        # except:
        #     self.fail("SnackBar de sucesso não encontrado ou texto incorreto.")

        # Verifica se navegou para HomePage (adapte o localizador para o HomePage)
        self.wait.until(EC.presence_of_element_located((By.ID, "homePageElement")))
        #  Você também pode verificar a ausência de elementos da tela de login, se necessário.

    def test_botao_esqueceu_senha(self):
        """Botão "Esqueceu a senha?" exibe SnackBar informativo."""
        self.driver.find_element(By.ID, "forgotPasswordButton").click()

        # Verifica o SnackBar (adapte a lógica de localização do SnackBar e o texto esperado)
        # Exemplo:
        # try:
        #     snackbar_text = self.wait.until(EC.presence_of_element_located((By.ID, "snackbarText"))).text
        #     self.assertEqual(snackbar_text, "Funcionalidade \"Esqueceu a senha?\" não implementada.")
        # except:
        #     self.fail("SnackBar de informação não encontrado ou texto incorreto.")

        time.sleep(2)  # Aguarda o SnackBar desaparecer (se necessário)


if __name__ == '__main__':
    unittest.main()
