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
        """Configuração do driver do Appium para cada teste."""
        # As capacidades devem ser ajustadas conforme o ambiente de teste.
        capabilities = dict(
            platformName='Android',  # Plataforma (ex: Android, iOS).
            deviceName='NomeDoSeuDispositivoOuEmulador', # Nome do dispositivo ou emulador.
            appPackage='com.seuapp.pacote', # Package name do aplicativo.
            appActivity='com.seuapp.atividade.Principal', # Activity principal do aplicativo.
            automationName='UiAutomator2'  # Driver de automação (UiAutomator2 para Android, XCUITest para iOS).
        )
        options = AppiumOptions().load_capabilities(capabilities)
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', options=options) # URL do servidor Appium.
        self.wait = WebDriverWait(self.driver, 10)  # Espera até 10 segundos

    def tearDown(self):
        """Encerra a sessão do driver após cada teste."""
        if self.driver:
            self.driver.quit()

    def test_ui_inicial_e_validacoes(self):
        """Verifica a UI inicial e as validações de campos vazios."""
        # Localiza os elementos da UI inicial.
        # Os localizadores (By.ID, XPath, etc.) devem corresponder aos elementos no aplicativo.
        self.wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        self.wait.until(EC.presence_of_element_located((By.ID, "passwordField")))
        self.wait.until(EC.presence_of_element_located((By.ID, "loginButton")))
        self.wait.until(EC.presence_of_element_located((By.ID, "forgotPasswordButton")))
        # A verificação do título do AppBar pode requerer um localizador específico.

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
        #  A mesma lógica de verificação de erro deve ser aplicada para o campo de senha.

    def test_login_credenciais_incorretas(self):
        """Login com credenciais incorretas exibe diálogo de erro."""
        username_field = self.driver.find_element(By.ID, "usernameField")
        password_field = self.driver.find_element(By.ID, "passwordField")
        username_field.send_keys("usuarioerrado")
        password_field.send_keys("senhaerrada")
        self.driver.find_element(By.ID, "loginButton").click()

        # Verifica o diálogo de erro
        alert = self.wait.until(EC.alert_is_present()) # Espera o alerta nativo aparecer.
        self.assertEqual(alert.text, "Usuário ou senha incorretos.") # A mensagem de erro deve ser verificada.
        alert.accept() # Clica no botão "OK" (ou equivalente) do alerta.

    def test_login_credenciais_corretas(self):
        """Login com credenciais corretas navega para HomePage e exibe SnackBar."""
        username_field = self.driver.find_element(By.ID, "usernameField")
        password_field = self.driver.find_element(By.ID, "passwordField")
        username_field.send_keys("admin")  # Credenciais corretas para o teste.
        password_field.send_keys("1234")  # Credenciais corretas para o teste.
        self.driver.find_element(By.ID, "loginButton").click()

        # Verifica SnackBar de sucesso. A localização do SnackBar pode variar.
        # Exemplo com espera por um texto específico:
        # try:
        #     snackbar_text = self.wait.until(EC.presence_of_element_located((By.ID, "snackbarText"))).text
        #     self.assertEqual(snackbar_text, "Login bem-sucedido!")
        # except:
        #     self.fail("SnackBar de sucesso não encontrado ou texto incorreto.")
        
        # Verifica se a navegação para a HomePage ocorreu.
        self.wait.until(EC.presence_of_element_located((By.ID, "homePageElement")))
        #  Pode-se também verificar a ausência de elementos da LoginPage para confirmar a navegação.

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

        time.sleep(2)  # Pausa para permitir que o SnackBar desapareça, se aplicável.


if __name__ == '__main__':
    unittest.main()
