import unittest
import time
import os
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium_flutter_finder.flutter_finder import FlutterFinder

# Configurações do Appium e do Aplicativo
APPIUM_HOST = 'http://127.0.0.1:4723'
# Caminho para o arquivo APK ou APP do aplicativo em teste.
APP_PATH = "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" # Este caminho deve ser atualizado para o local do arquivo do aplicativo.

# Chaves dos elementos Flutter (ajuste conforme seu código Dart)
# LoginPage (Chaves para elementos da página de login)
LOGIN_USERNAME_FIELD_KEY = 'login_username_field' # ValueKey para o campo de usuário.
LOGIN_PASSWORD_FIELD_KEY = 'login_password_field' # ValueKey para o campo de senha.
LOGIN_BUTTON_KEY = 'login_button'                 # ValueKey para o botão de login.

# HomePage (Chaves para elementos da página inicial)
HOME_PAGE_INDICATOR_KEY = 'home_page_app_bar_title' # Ex: ValueKey('home_page_app_bar_title')
HOME_CLICK_PAGE_BUTTON_KEY = 'home_page_click_and_hold_button' # Ex: ValueKey('home_page_click_and_hold_button')

# ClickPage
CLICK_PAGE_APPBAR_TITLE_KEY = 'click_page_app_bar_title' # Ex: ValueKey('clickPage_appBar_title')
CLICK_PAGE_DOUBLE_TAP_CARD_KEY = 'click_page_double_tap_card'
CLICK_PAGE_LONG_PRESS_CARD_KEY = 'click_page_long_press_card'

# AlertDialog (Flutter AlertDialog)
CLICK_PAGE_ALERT_OK_BUTTON_KEY = 'click_page_alert_dialog_ok_button' # ValueKey para o botão OK do AlertDialog

# Textos dentro do AlertDialog (para verificação)
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
        """Configuração inicial do driver do Appium para a suíte de testes."""
        # Capacidades desejadas para a sessão do Appium.
        capabilities = dict(
            platformName='Android',  # Plataforma do dispositivo (Android ou iOS).
            deviceName='Android Emulator', # Nome do dispositivo ou emulador.
            appPackage='com.example.appium_and_flutter_test', # Package name do aplicativo.
            appActivity='.MainActivity', # Activity principal do aplicativo.
            automationName='Flutter'  # Nome do driver de automação (Flutter para apps Flutter).
        )
        options = AppiumOptions().load_capabilities(capabilities)
        # Configurações adicionais da sessão.
        options.set_capability('app-debug.apk', "D:\\repos\\appium_and_flutter_test\\build\\app\\outputs\\flutter-apk\\app-debug.apk")
        options.set_capability('retryBackoffTime', 500)
        options.set_capability('maxRetryCount', 3)
        options.set_capability('newCommandTimeout', 120) # Timeout para novos comandos.

        cls.driver = webdriver.Remote(APPIUM_HOST, options=options)
        cls.wait = WebDriverWait(cls.driver, 30)  # Tempo máximo de espera para elementos.
        cls.finder = FlutterFinder() # Instância do FlutterFinder para localizar elementos Flutter.

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()

    # --- Helper Methods ---
    def _find_element_by_value_key(self, key_string, timeout=20):
        return self.wait.until(
            EC.presence_of_element_located((AppiumBy.FLUTTER, self.finder.by_value_key(key_string)))
        )

    def _find_element_by_text(self, text_string, timeout=10):
        # Nota: by_text pode ser menos performático. Use com cautela.
        # É melhor se o texto for único na tela.
        return self.wait.until(
            EC.presence_of_element_located((AppiumBy.FLUTTER, self.finder.by_text(text_string)))
        )

    def _is_element_present_by_value_key(self, key_string, timeout=3):
        try:
            self._find_element_by_value_key(key_string, timeout)
            return True
        except TimeoutException:
            return False

    def _is_text_present(self, text_string, timeout=3):
        try:
            self._find_element_by_text(text_string, timeout)
            return True
        except TimeoutException:
            return False

    def _tap_element(self, element):
        element.click()
        time.sleep(0.5) # Pausa para UI

    def _perform_double_tap_on_element(self, element):
        action = TouchAction(self.driver)
        action.tap(element).wait(ms=100).tap(element).perform()
        time.sleep(0.5) # Pausa para UI reagir

    def _perform_long_press_on_element(self, element, duration_ms=1000):
        action = TouchAction(self.driver)
        action.long_press(element, duration=duration_ms).release().perform()
        time.sleep(0.5) # Pausa para UI reagir

    def _check_flutter_alert_and_dismiss(self, expected_title, expected_content, ok_button_key):
        """Verifica o título e conteúdo de um AlertDialog Flutter e clica no botão OK."""
        self.assertTrue(self._is_text_present(expected_title, timeout=5), f"Título do alerta '{expected_title}' não encontrado.")
        self.assertTrue(self._is_text_present(expected_content, timeout=5), f"Conteúdo do alerta '{expected_content}' não encontrado.")
        
        ok_button = self._find_element_by_value_key(ok_button_key)
        self._tap_element(ok_button)
        time.sleep(0.5) # Esperar o diálogo fechar

        # Verifica se o diálogo desapareceu (o título não deve mais estar presente)
        self.assertFalse(self._is_text_present(expected_title, timeout=2), "Alerta Flutter não desapareceu após clicar em OK.")

    def _navigate_to_click_page(self):
        """Faz login (se necessário) e navega para a ClickPage."""
        # Tenta fazer login se estiver na LoginPage
        # Assume que a LoginPage tem um elemento identificável, como o campo de usuário.
        if self._is_element_present_by_value_key(LOGIN_USERNAME_FIELD_KEY, timeout=5):
            print("Realizando login...")
            username_field = self._find_element_by_value_key(LOGIN_USERNAME_FIELD_KEY)
            password_field = self._find_element_by_value_key(LOGIN_PASSWORD_FIELD_KEY)
            login_button = self._find_element_by_value_key(LOGIN_BUTTON_KEY)

            username_field.send_keys("admin") # Usuário de teste
            password_field.send_keys("1234")  # Senha de teste
            self._tap_element(login_button)
            time.sleep(1)

        # Espera pela HomePage e navega para ClickPage
        print("Navegando para ClickPage...")
        self._find_element_by_value_key(HOME_PAGE_INDICATOR_KEY) # Confirma que está na HomePage
        click_page_nav_button = self._find_element_by_value_key(HOME_CLICK_PAGE_BUTTON_KEY)
        self._tap_element(click_page_nav_button)

        # Confirma que está na ClickPage
        self._find_element_by_value_key(CLICK_PAGE_APPBAR_TITLE_KEY)
        time.sleep(0.5)

    # --- Test Method ---
    def test_01_double_tap_interaction(self):
        self._navigate_to_click_page()

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
        print("Teste de duplo clique concluído.")

    def test_02_long_press_interaction(self):
        # Assume que já está na ClickPage do teste anterior ou navega novamente
        # Para garantir isolamento, poderia chamar _navigate_to_click_page() aqui também,
        # mas se os testes rodam em ordem e o estado é mantido, não é estritamente necessário.
        # Se não navegou, descomente:
        # self._navigate_to_click_page() 
        # Ou garanta que a página ainda é a ClickPage:
        self._find_element_by_value_key(CLICK_PAGE_APPBAR_TITLE_KEY)

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
        print("Teste de clique longo concluído.")

if __name__ == '__main__':
    if "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" in APP_PATH: # Verificação mais genérica
        print("ERRO: A variável APP_PATH não foi configurada no script.")
        print(f"Por favor, edite o arquivo {__file__} e defina o caminho para o seu APK/APP.")
    else:
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(ClickPageTests))
        runner = unittest.TextTestRunner(verbosity=2)
        print(f"Iniciando testes da ClickPage para o app: {APP_PATH}")
        print(f"Conectando ao servidor Appium em: {APPIUM_HOST}...")
        runner.run(suite)
