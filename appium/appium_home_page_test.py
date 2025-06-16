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

# HomePage
HOME_PAGE_APPBAR_TITLE_KEY = 'home_page_app_bar_title'
HOME_PAGE_FORMS_BUTTON_KEY = 'home_page_forms_button'
HOME_PAGE_LISTVIEW_BUTTON_KEY = 'home_page_list_view_button'
HOME_PAGE_NATIVE_RESOURCES_BUTTON_KEY = 'home_page_native_resources_button'
HOME_PAGE_GESTURES_BUTTON_KEY = 'home_page_gestures_button'
HOME_PAGE_CLICK_AND_HOLD_BUTTON_KEY = 'home_page_click_and_hold_button'
HOME_PAGE_CHAT_BUTTON_KEY = 'home_page_chat_button'
HOME_PAGE_LOGOUT_BUTTON_KEY = 'home_page_logout_button'

# Logout Dialog
HOME_PAGE_LOGOUT_DIALOG_KEY = 'home_page_logout_dialog'
HOME_PAGE_LOGOUT_DIALOG_CANCEL_BUTTON_KEY = 'home_page_logout_dialog_cancel_button'
HOME_PAGE_LOGOUT_DIALOG_CONFIRM_BUTTON_KEY = 'home_page_logout_dialog_confirm_button'
TEXT_LOGOUT_DIALOG_TITLE = "Confirmar Logout"

# Indicadores de outras páginas
FORMS_PAGE_INDICATOR_KEY = 'forms_app_bar_title'
LISTVIEW_PAGE_INDICATOR_KEY = 'list_view_page_list_view'
RECURSOS_PAGE_INDICATOR_KEY = 'recursos_page_app_bar_title'
GESTOS_PAGE_INDICATOR_KEY = 'gestos_page_app_bar_title'
CLICK_PAGE_INDICATOR_KEY = 'click_page_app_bar_title'
CHAT_PAGE_INDICATOR_KEY = 'chat_page_app_bar_title'

class HomePageTests(unittest.TestCase):
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
        """Garante que cada teste comece logado e na HomePage."""
        print("\nAssegurando que o teste começa na HomePage...")
        self._ensure_on_home_page()

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
        element.send_keys(text)
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
        except Exception:
            pass
        time.sleep(0.2)

    def _ensure_on_home_page(self, username='admin', password='1234'):
        """Garante que o app esteja na HomePage, fazendo login ou navegando de volta se necessário."""
        time.sleep(1)
        if self._is_element_present(LOGIN_USERNAME_FIELD_KEY, timeout=2):
            print("Tela de login detectada. Realizando login...")
            self._enter_text(LOGIN_USERNAME_FIELD_KEY, username)
            self._enter_text(LOGIN_PASSWORD_FIELD_KEY, password)
            self._tap_element_by_key(LOGIN_BUTTON_KEY)
        
        # Se não estiver na home page, tenta voltar
        while not self._is_element_present(HOME_PAGE_APPBAR_TITLE_KEY, timeout=1):
            print("Não está na HomePage. Tentando navegar para trás...")
            self.driver.back()
            time.sleep(1)
            # F condição de parada se estiver na tela de login (não pode voltar mais)
            if self._is_element_present(LOGIN_USERNAME_FIELD_KEY, timeout=1):
                self.fail("Falha ao retornar para a HomePage. Encontrou a tela de login.")
        
        self.assertTrue(self._is_element_present(HOME_PAGE_APPBAR_TITLE_KEY, 5), "Não foi possível garantir que o teste está na HomePage.")

    def _test_navigation_to(self, button_key, indicator_key, page_name):
        """Template para testar a navegação para uma página e o retorno."""
        print(f"Testando navegação para {page_name}...")
        self._tap_element_by_key(button_key)
        self.assertTrue(self._is_element_present(indicator_key, 10), f"Falha ao navegar para {page_name}.")
        print(f"Navegou para {page_name} com sucesso.")
        self.driver.back()
        self.assertTrue(self._is_element_present(HOME_PAGE_APPBAR_TITLE_KEY, 5), f"Falha ao retornar da {page_name}.")
        print(f"Retornou da {page_name} com sucesso.")

    # --- Testes ---

    def test_navigation_to_forms(self):
        self._test_navigation_to(HOME_PAGE_FORMS_BUTTON_KEY, FORMS_PAGE_INDICATOR_KEY, "Formulários")
        
    def test_navigation_to_listview(self):
        self._test_navigation_to(HOME_PAGE_LISTVIEW_BUTTON_KEY, LISTVIEW_PAGE_INDICATOR_KEY, "ListView")

    def test_navigation_to_native_resources(self):
        self._test_navigation_to(HOME_PAGE_NATIVE_RESOURCES_BUTTON_KEY, RECURSOS_PAGE_INDICATOR_KEY, "Recursos Nativos")

    def test_navigation_to_gestures(self):
        self._test_navigation_to(HOME_PAGE_GESTURES_BUTTON_KEY, GESTOS_PAGE_INDICATOR_KEY, "Gestos")

    def test_navigation_to_click_and_hold(self):
        self._test_navigation_to(HOME_PAGE_CLICK_AND_HOLD_BUTTON_KEY, CLICK_PAGE_INDICATOR_KEY, "Clicar e Segurar")
    
    def test_navigation_to_chat(self):
        self._test_navigation_to(HOME_PAGE_CHAT_BUTTON_KEY, CHAT_PAGE_INDICATOR_KEY, "Chat")

    def test_logout_cancellation(self):
        """Testa a funcionalidade de cancelar o logout."""
        print("Testando cancelamento do logout...")
        self._tap_element_by_key(HOME_PAGE_LOGOUT_BUTTON_KEY)
        self.assertTrue(self._is_element_present(HOME_PAGE_LOGOUT_DIALOG_KEY), "Diálogo de logout não apareceu.")
        
        self._tap_element_by_key(HOME_PAGE_LOGOUT_DIALOG_CANCEL_BUTTON_KEY)
        
        # Verifica se o diálogo desapareceu e se ainda está na home
        self.assertTrue(
            WebDriverWait(self.driver, 5).until_not(
                EC.presence_of_element_located((AppiumBy.FLUTTER, self.finder.by_value_key(HOME_PAGE_LOGOUT_DIALOG_KEY)))
            ), "Diálogo de logout não fechou após o cancelamento."
        )
        self.assertTrue(self._is_element_present(HOME_PAGE_APPBAR_TITLE_KEY), "Não permaneceu na HomePage após cancelar o logout.")
        print("Cancelamento de logout verificado com sucesso.")

    def test_logout_confirmation(self):
        """Testa a confirmação de logout e o retorno para a tela de login."""
        print("Testando confirmação de logout...")
        self._tap_element_by_key(HOME_PAGE_LOGOUT_BUTTON_KEY)
        self.assertTrue(self._is_element_present(HOME_PAGE_LOGOUT_DIALOG_KEY), "Diálogo de logout não apareceu.")
        
        self._tap_element_by_key(HOME_PAGE_LOGOUT_DIALOG_CONFIRM_BUTTON_KEY)
        
        # Verifica se navegou para a tela de login
        self.assertTrue(self._is_element_present(LOGIN_USERNAME_FIELD_KEY, 10), "Não navegou para a LoginPage após confirmar o logout.")
        print("Logout confirmado com sucesso.")

if __name__ == '__main__':
    if "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" in APP_PATH:
        print("="*60)
        print("ERRO: A variável APP_PATH não foi configurada no script.")
        print(f"Por favor, edite o arquivo '{__file__}' e defina o caminho correto para o seu APK.")
        print("="*60)
    else:
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(HomePageTests))
        runner = unittest.TextTestRunner(verbosity=2)
        print(f"\nIniciando testes da HomePage para o app: {APP_PATH}")
        print(f"Conectando ao servidor Appium em: {APPIUM_HOST}...")
        runner.run(suite)
