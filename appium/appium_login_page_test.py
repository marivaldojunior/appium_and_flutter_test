# d:\repos\appium_and_flutter_test\integration_test\login_page_test.py
import unittest
import time
import os
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium_flutter_finder.flutter_finder import FlutterFinder

# --- Configurações ---
APPIUM_HOST = 'http://127.0.0.1:4723'
# ATENÇÃO: Atualize este caminho para o local do seu arquivo APK.
APP_PATH = os.path.abspath('D:\\repos\\appium_and_flutter_test\\build\\app\\outputs\\flutter-apk\\app-debug.apk')

if not os.path.exists(APP_PATH):
    APP_PATH = "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI"

# --- Chaves dos Elementos Flutter ---
# LoginPage
LOGIN_USERNAME_FIELD_KEY = 'login_username_field'
LOGIN_PASSWORD_FIELD_KEY = 'login_password_field'
LOGIN_BUTTON_KEY = 'login_button'
LOGIN_FORGOT_PASSWORD_BUTTON_KEY = 'login_forgot_password_button'

# Feedback de Login
LOGIN_ALERT_ERROR_KEY = 'login_alert_error'
LOGIN_ALERT_ERROR_OK_BUTTON_KEY = 'login_alert_error_ok_button'

# Textos para Validação
TEXT_SNACKBAR_LOGIN_SUCCESS = "Login bem-sucedido!"
TEXT_ALERT_ERROR_TITLE = "Erro de Login"
TEXT_ALERT_ERROR_CONTENT = "Usuário ou senha incorretos."
TEXT_SNACKBAR_FORGOT_PASSWORD = "Funcionalidade \"Esqueceu a senha?\" não implementada."
TEXT_VALIDATION_USER_EMPTY = "Usuário não pode estar vazio"
TEXT_VALIDATION_PASSWORD_EMPTY = "Senha não pode estar vazia"

# Indicador da HomePage
HOME_PAGE_INDICATOR_KEY = 'home_page_app_bar_title'

class LoginPageTests(unittest.TestCase):
    driver: webdriver.Remote
    wait: WebDriverWait
    finder: FlutterFinder

    @classmethod
    def setUpClass(cls):
        """Configura o driver do Appium antes de todos os testes da classe."""
        if "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" in APP_PATH:
            raise Exception("ERRO: A variável APP_PATH não foi configurada. Abortando testes.")

        capabilities = {
            'platformName': 'Android',
            'deviceName': 'Android Emulator',
            'appPackage': 'com.example.appium_and_flutter_test',
            'appActivity': '.MainActivity',
            'automationName': 'Flutter',
            'app': APP_PATH,
            'newCommandTimeout': 120,
        }
        options = AppiumOptions().load_capabilities(capabilities)
        cls.driver = webdriver.Remote(APPIUM_HOST, options=options)
        cls.wait = WebDriverWait(cls.driver, 20)
        cls.finder = FlutterFinder()

    @classmethod
    def tearDownClass(cls):
        """Encerra a sessão do driver após todos os testes."""
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()

    def setUp(self):
        """Garante que cada teste comece na LoginPage."""
        print("\nAssegurando que o teste começa na LoginPage...")
        self._ensure_on_login_page()

    # --- Métodos Auxiliares ---

    def _find_element_by_key(self, key, timeout=10):
        finder = self.finder.by_value_key(key)
        return self.wait.until(
            EC.presence_of_element_located((AppiumBy.FLUTTER, finder)),
            message=f"Elemento com a chave '{key}' não foi encontrado."
        )

    def _is_element_present(self, key, timeout=3):
        try:
            self._find_element_by_key(key, timeout)
            return True
        except TimeoutException:
            return False

    def _tap_element_by_key(self, key):
        element = self._find_element_by_key(key)
        element.click()
        time.sleep(0.5)

    def _enter_text(self, key, text):
        element = self._find_element_by_key(key)
        element.clear()
        element.send_keys(text)
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
        except Exception:
            pass
        time.sleep(0.2)

    def _is_snackbar_present(self, text, timeout=5):
        """Verifica se uma snackbar com o texto especificado está visível."""
        try:
            # Snackbar no Android geralmente é um elemento nativo
            locator = (AppiumBy.XPATH, f"//*[contains(@text,'{text}')]")
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def _ensure_on_login_page(self):
        """Garante que a tela de login esteja visível, fazendo logout se necessário."""
        time.sleep(1)
        if not self._is_element_present(LOGIN_USERNAME_FIELD_KEY, timeout=2):
            print("Não está na LoginPage. Tentando fazer logout...")
            if self._is_element_present('home_page_logout_button'):
                self._tap_element_by_key('home_page_logout_button')
                self.assertTrue(self._is_element_present('home_page_logout_dialog_confirm_button'))
                self._tap_element_by_key('home_page_logout_dialog_confirm_button')
            else: # Se não sabe onde está, tenta voltar
                self.driver.back()

        self.assertTrue(self._is_element_present(LOGIN_USERNAME_FIELD_KEY, 10), "Falha ao retornar para a LoginPage.")

    # --- Testes ---

    def test_initial_ui_elements_are_present(self):
        """Verifica se todos os elementos principais da UI estão na tela."""
        print("Verificando elementos da UI inicial...")
        self.assertTrue(self._is_element_present(LOGIN_USERNAME_FIELD_KEY), "Campo de usuário não encontrado.")
        self.assertTrue(self._is_element_present(LOGIN_PASSWORD_FIELD_KEY), "Campo de senha não encontrado.")
        self.assertTrue(self._is_element_present(LOGIN_BUTTON_KEY), "Botão de login não encontrado.")
        self.assertTrue(self._is_element_present(LOGIN_FORGOT_PASSWORD_BUTTON_KEY), "Botão 'Esqueceu a senha' não encontrado.")
        print("Elementos da UI inicial verificados com sucesso.")

    def test_login_fails_with_empty_credentials(self):
        """Verifica a validação de erro para campos vazios."""
        print("Testando validação de campos vazios...")
        # Tenta logar com tudo vazio
        self._tap_element_by_key(LOGIN_BUTTON_KEY)
        self.assertTrue(self._is_snackbar_present(TEXT_VALIDATION_USER_EMPTY), "Validação de usuário vazio falhou.")

        # Preenche usuário e deixa senha vazia
        self._enter_text(LOGIN_USERNAME_FIELD_KEY, "teste")
        self._tap_element_by_key(LOGIN_BUTTON_KEY)
        self.assertTrue(self._is_snackbar_present(TEXT_VALIDATION_PASSWORD_EMPTY), "Validação de senha vazia falhou.")
        print("Validações de campos vazios verificadas com sucesso.")

    def test_login_fails_with_wrong_credentials(self):
        """Verifica se um alerta de erro é exibido com credenciais inválidas."""
        print("Testando login com credenciais incorretas...")
        self._enter_text(LOGIN_USERNAME_FIELD_KEY, "usuario_errado")
        self._enter_text(LOGIN_PASSWORD_FIELD_KEY, "senha_errada")
        self._tap_element_by_key(LOGIN_BUTTON_KEY)

        # Verifica e fecha o alerta de erro
        self.assertTrue(self._is_element_present(LOGIN_ALERT_ERROR_KEY), "Alerta de erro não foi exibido.")
        self.assertTrue(self._is_snackbar_present(TEXT_ALERT_ERROR_TITLE), "Título do alerta de erro incorreto.")
        self._tap_element_by_key(LOGIN_ALERT_ERROR_OK_BUTTON_KEY)

        # Garante que o alerta desapareceu
        self.assertFalse(self._is_element_present(LOGIN_ALERT_ERROR_KEY, timeout=2), "Alerta de erro não fechou.")
        print("Teste de credenciais incorretas verificado com sucesso.")

    def test_successful_login_and_navigation(self):
        """Verifica o fluxo de login bem-sucedido e a navegação para a HomePage."""
        print("Testando login bem-sucedido...")
        self._enter_text(LOGIN_USERNAME_FIELD_KEY, "admin")
        self._enter_text(LOGIN_PASSWORD_FIELD_KEY, "1234")
        self._tap_element_by_key(LOGIN_BUTTON_KEY)

        # Verifica a navegação para a HomePage
        self.assertTrue(self._is_element_present(HOME_PAGE_INDICATOR_KEY, 15), "Não navegou para a HomePage após o login.")
        print("Login bem-sucedido e navegação para HomePage verificados.")

    def test_forgot_password_link(self):
        """Verifica a funcionalidade do link 'Esqueceu a senha?'."""
        print("Testando link 'Esqueceu a senha?'...")
        self._tap_element_by_key(LOGIN_FORGOT_PASSWORD_BUTTON_KEY)
        self.assertTrue(self._is_snackbar_present(TEXT_SNACKBAR_FORGOT_PASSWORD), "Snackbar de 'Esqueceu a senha' não apareceu.")
        print("Link 'Esqueceu a senha?' verificado com sucesso.")

if __name__ == '__main__':
    if "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" in APP_PATH:
        print("="*60)
        print("ERRO: A variável APP_PATH não foi configurada no script.")
        print(f"Por favor, edite o arquivo '{__file__}' e defina o caminho correto para o seu APK.")
        print("="*60)
    else:
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(LoginPageTests))
        runner = unittest.TextTestRunner(verbosity=2)
        print(f"\nIniciando testes da LoginPage para o app: {APP_PATH}")
        print(f"Conectando ao servidor Appium em: {APPIUM_HOST}...")
        runner.run(suite)
