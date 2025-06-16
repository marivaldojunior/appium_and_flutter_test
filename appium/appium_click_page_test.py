import unittest
import time
import os
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium_flutter_finder.flutter_finder import FlutterFinder

# --- Configurações ---
APPIUM_HOST = 'http://127.0.0.1:4723'
# ATENÇÃO: Atualize este caminho para o local do seu arquivo APK.
# Usar os.path.abspath garante que o caminho funcione independentemente do diretório de execução.
APP_PATH = os.path.abspath('D:\\repos\\appium_and_flutter_test\\build\\app\\outputs\\flutter-apk\\app-debug.apk')

# Verifique se o caminho acima está correto antes de executar.
if not os.path.exists(APP_PATH):
    APP_PATH = "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI"

# --- Chaves dos Elementos Flutter (ValueKeys) ---
# LoginPage
LOGIN_USERNAME_FIELD_KEY = 'login_username_field'
LOGIN_PASSWORD_FIELD_KEY = 'login_password_field'
LOGIN_BUTTON_KEY = 'login_button'

# HomePage
HOME_PAGE_APPBAR_TITLE_KEY = 'home_page_app_bar_title'
HOME_CLICK_PAGE_BUTTON_KEY = 'home_page_click_and_hold_button'

# ClickPage
CLICK_PAGE_APPBAR_TITLE_KEY = 'click_page_app_bar_title'
CLICK_PAGE_DOUBLE_TAP_CARD_KEY = 'click_page_double_tap_card'
CLICK_PAGE_LONG_PRESS_CARD_KEY = 'click_page_long_press_card'
CLICK_PAGE_ALERT_OK_BUTTON_KEY = 'click_page_alert_dialog_ok_button'

# --- Textos para Validação ---
TEXT_ALERT_DOUBLE_TAP_TITLE = "Duplo Clique!"
TEXT_ALERT_DOUBLE_TAP_CONTENT = "Você clicou duas vezes neste card."
TEXT_ALERT_LONG_PRESS_TITLE = "Clique Longo!"
TEXT_ALERT_LONG_PRESS_CONTENT = "Você pressionou e segurou este card."

class ClickPageTests(unittest.TestCase):
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
            'app': APP_PATH,  # Caminho para o APK/APP (padrão correto)
            'newCommandTimeout': 120,
            'retryBackoffTime': 500,
            'maxRetryCount': 3,
        }
        options = AppiumOptions().load_capabilities(capabilities)

        cls.driver = webdriver.Remote(APPIUM_HOST, options=options)
        cls.wait = WebDriverWait(cls.driver, 20) # Reduzido para 20s, ajuste se necessário
        cls.finder = FlutterFinder()

    @classmethod
    def tearDownClass(cls):
        """Encerra a sessão do driver após todos os testes."""
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()

    def setUp(self):
        """Executado antes de cada método de teste para garantir isolamento."""
        print("\nNavegando para a ClickPage...")
        self._navigate_to_click_page()

    # --- Métodos Auxiliares ---

    def _find_element_by_value_key(self, key, timeout=10):
        element_finder = self.finder.by_value_key(key)
        return self.wait.until(
            EC.presence_of_element_located((AppiumBy.FLUTTER, element_finder)),
            message=f"Elemento com a chave '{key}' não foi encontrado no tempo de {timeout}s."
        )

    def _is_text_present(self, text, timeout=5):
        try:
            text_finder = self.finder.by_text(text)
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.FLUTTER, text_finder))
            )
            return True
        except TimeoutException:
            return False
            
    def _is_element_present(self, key, timeout=3):
        try:
            self._find_element_by_value_key(key, timeout)
            return True
        except TimeoutException:
            return False

    def _tap_element(self, element_or_key):
        """Toca em um elemento, seja o próprio elemento ou sua chave (key)."""
        if isinstance(element_or_key, str):
            element = self._find_element_by_value_key(element_or_key)
        else:
            element = element_or_key
        element.click()
        time.sleep(0.5)

    def _fill_text_field(self, key, text):
        element = self._find_element_by_value_key(key)
        element.send_keys(text)

    def _perform_double_tap_on_element(self, element):
        """Executa um duplo clique usando W3C Actions (padrão moderno)."""
        self.driver.execute_script('flutter:doubleTap', element)
        time.sleep(0.5)

    def _perform_long_press_on_element(self, element):
        """Executa um clique longo usando W3C Actions (padrão moderno)."""
        self.driver.execute_script('flutter:longPress', element)
        time.sleep(0.5)

    def _check_flutter_alert_and_dismiss(self, expected_title, expected_content, ok_button_key):
        """Verifica o conteúdo de um AlertDialog e o fecha."""
        self.assertTrue(self._is_text_present(expected_title, timeout=5), f"Título do alerta '{expected_title}' não encontrado.")
        self.assertTrue(self._is_text_present(expected_content, timeout=5), f"Conteúdo do alerta '{expected_content}' não encontrado.")
        
        self._tap_element(ok_button_key)
        
        # Espera explícita para o alerta desaparecer
        self.assertTrue(
            WebDriverWait(self.driver, 5).until_not(
                EC.presence_of_element_located((AppiumBy.FLUTTER, self.finder.by_text(expected_title)))
            ), "Alerta Flutter não desapareceu após clicar em OK."
        )

    def _navigate_to_click_page(self):
        """Faz login (se necessário) e navega para a ClickPage."""
        time.sleep(1) # Pausa inicial para o app estabilizar
        if self._is_element_present(LOGIN_USERNAME_FIELD_KEY, timeout=3):
            print("Tela de login detectada. Realizando login...")
            self._fill_text_field(LOGIN_USERNAME_FIELD_KEY, "admin")
            self._fill_text_field(LOGIN_PASSWORD_FIELD_KEY, "1234")
            self._tap_element(LOGIN_BUTTON_KEY)

        self.assertTrue(self._is_element_present(HOME_PAGE_APPBAR_TITLE_KEY, timeout=10), "Não foi possível chegar à HomePage.")
        self._tap_element(HOME_CLICK_PAGE_BUTTON_KEY)
        
        self.assertTrue(self._is_element_present(CLICK_PAGE_APPBAR_TITLE_KEY), "Não foi possível navegar para a ClickPage.")

    # --- Testes ---

    def test_double_tap_interaction(self):
        """Verifica se o duplo clique em um card aciona o alerta correto."""
        double_tap_card = self._find_element_by_value_key(CLICK_PAGE_DOUBLE_TAP_CARD_KEY)
        self.assertIsNotNone(double_tap_card, "Card de duplo clique não encontrado.")

        print("Realizando duplo clique...")
        self._perform_double_tap_on_element(double_tap_card)
        
        print("Verificando alerta de duplo clique...")
        self._check_flutter_alert_and_dismiss(
            expected_title=TEXT_ALERT_DOUBLE_TAP_TITLE,
            expected_content=TEXT_ALERT_DOUBLE_TAP_CONTENT,
            ok_button_key=CLICK_PAGE_ALERT_OK_BUTTON_KEY
        )
        print("Teste de duplo clique concluído com sucesso.")

    def test_long_press_interaction(self):
        """Verifica se o clique longo em um card aciona o alerta correto."""
        long_press_card = self._find_element_by_value_key(CLICK_PAGE_LONG_PRESS_CARD_KEY)
        self.assertIsNotNone(long_press_card, "Card de clique longo não encontrado.")

        print("Realizando clique longo...")
        self._perform_long_press_on_element(long_press_card)

        print("Verificando alerta de clique longo...")
        self._check_flutter_alert_and_dismiss(
            expected_title=TEXT_ALERT_LONG_PRESS_TITLE,
            expected_content=TEXT_ALERT_LONG_PRESS_CONTENT,
            ok_button_key=CLICK_PAGE_ALERT_OK_BUTTON_KEY
        )
        print("Teste de clique longo concluído com sucesso.")

if __name__ == '__main__':
    if "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" in APP_PATH:
        print("="*60)
        print("ERRO: A variável APP_PATH não foi configurada no script.")
        print(f"Por favor, edite o arquivo '{__file__}' e defina o caminho correto para o seu APK.")
        print("="*60)
    else:
        suite = unittest.TestSuite()
        # Adiciona os testes em uma ordem específica se houver dependência,
        # ou usa makeSuite para adicionar todos os testes da classe.
        suite.addTest(unittest.makeSuite(ClickPageTests))
        
        runner = unittest.TextTestRunner(verbosity=2)
        print(f"\nIniciando testes da ClickPage para o app: {APP_PATH}")
        print(f"Conectando ao servidor Appium em: {APPIUM_HOST}...")
        runner.run(suite)
