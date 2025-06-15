# d:\repos\appium_and_flutter_test\integration_test\home_page_test.py
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

# Configurações do Appium e do Aplicativo
APPIUM_HOST = 'http://127.0.0.1:4723'
APP_PATH = "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" # IMPORTANTE: Atualize este caminho

# Chaves dos elementos Flutter (ajuste conforme seu código Dart)
# LoginPage
LOGIN_USERNAME_FIELD_KEY = 'login_username_field' # Ex: ValueKey('login_username_field')
LOGIN_PASSWORD_FIELD_KEY = 'login_password_field' # Ex: ValueKey('login_password_field')
LOGIN_BUTTON_KEY = 'login_button'                 # Ex: ValueKey('login_button')

# HomePage
HOME_PAGE_APPBAR_TITLE_KEY = 'home_page_app_bar_title' # Ex: ValueKey('home_page_app_bar_title')
HOME_PAGE_FORMS_BUTTON_KEY = 'home_page_forms_button'
HOME_PAGE_LISTVIEW_BUTTON_KEY = 'home_page_list_view_button'
HOME_PAGE_NATIVE_RESOURCES_BUTTON_KEY = 'home_page_native_resources_button'
HOME_PAGE_GESTURES_BUTTON_KEY = 'home_page_gestures_button'
HOME_PAGE_CLICK_AND_HOLD_BUTTON_KEY = 'home_page_click_and_hold_button'
HOME_PAGE_CHAT_BUTTON_KEY = 'home_page_chat_button'
HOME_PAGE_LOGOUT_BUTTON_KEY = 'home_page_logout_button'

# Logout Dialog
HOME_PAGE_LOGOUT_DIALOG_KEY = 'home_page_logout_dialog' # Key para o AlertDialog em si
HOME_PAGE_LOGOUT_DIALOG_CANCEL_BUTTON_KEY = 'home_page_logout_dialog_cancel_button'
HOME_PAGE_LOGOUT_DIALOG_CONFIRM_BUTTON_KEY = 'home_page_logout_dialog_confirm_button'
TEXT_LOGOUT_DIALOG_TITLE = "Confirmar Logout" # Texto para verificação

# Chaves indicadoras de outras páginas (para confirmar navegação)
# Use a chave do AppBar ou um elemento principal da respectiva página
FORMS_PAGE_INDICATOR_KEY = 'forms_app_bar_title' # Ex: ValueKey('forms_app_bar_title')
LISTVIEW_PAGE_INDICATOR_KEY = 'list_view_page_list_view' # Ex: ValueKey('list_view_page_list_view')
RECURSOS_PAGE_INDICATOR_KEY = 'recursos_page_app_bar_title' # Ex: ValueKey('recursos_page_app_bar_title')
GESTOS_PAGE_INDICATOR_KEY = 'gestos_page_app_bar_title' # Ex: ValueKey('gestos_page_app_bar_title')
CLICK_PAGE_INDICATOR_KEY = 'clickPage_appBar_title' # Ex: ValueKey('clickPage_appBar_title')
CHAT_PAGE_INDICATOR_KEY = 'chat_page_app_bar_title' # Ex: ValueKey('chat_page_app_bar_title')

class HomePageTests(unittest.TestCase):
    driver: webdriver.Remote
    wait: WebDriverWait
    finder: FlutterFinder

    @classmethod
    def setUpClass(cls):
        if APP_PATH == "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI":
            raise ValueError("Por favor, atualize a variável APP_PATH com o caminho para o seu APK/APP.")

        options = AppiumOptions()
        options.set_capability('platformName', 'Android') # Ou 'iOS'
        options.set_capability('automationName', 'Flutter')
        options.set_capability('deviceName', 'Android Emulator') # Substitua pelo seu dispositivo/emulador
        options.set_capability('app', APP_PATH)
        options.set_capability('retryBackoffTime', 500)
        options.set_capability('maxRetryCount', 3)
        options.set_capability('newCommandTimeout', 120)

        cls.driver = webdriver.Remote(command_executor=APPIUM_HOST, options=options)
        cls.finder = FlutterFinder()
        cls.wait = WebDriverWait(cls.driver, 30)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()

    # --- Helper Methods ---
    def _find_element_by_value_key(self, key_string, timeout=20):
        return self.wait.until(
            EC.presence_of_element_located((AppiumBy.FLUTTER, self.finder.by_value_key(key_string)))
        )

    def _is_element_present_by_value_key(self, key_string, timeout=3):
        try:
            self._find_element_by_value_key(key_string, timeout)
            return True
        except TimeoutException:
            return False

    def _is_text_present(self, text_string, timeout=5):
        try:
            self.wait.until(EC.presence_of_element_located((AppiumBy.FLUTTER, self.finder.by_text(text_string))))
            return True
        except TimeoutException:
            return False

    def _tap_element(self, element_or_key):
        if isinstance(element_or_key, str):
            element = self._find_element_by_value_key(element_or_key)
        else:
            element = element_or_key
        element.click()
        time.sleep(0.5) # Pausa para UI

    def _navigate_back(self):
        """Tenta navegar para trás usando o botão de voltar do sistema."""
        self.driver.back()
        time.sleep(0.5) # Pequena pausa para a navegação completar

    def _ensure_on_home_page(self, username='admin', password='1234'):
        """Garante que o app esteja logado e na HomePage."""
        time.sleep(1) # Pausa inicial

        # Se estiver na LoginPage, faz login
        if self._is_element_present_by_value_key(LOGIN_USERNAME_FIELD_KEY, timeout=3):
            print("Realizando login para chegar na HomePage...")
            username_field = self._find_element_by_value_key(LOGIN_USERNAME_FIELD_KEY)
            password_field = self._find_element_by_value_key(LOGIN_PASSWORD_FIELD_KEY)
            login_button = self._find_element_by_value_key(LOGIN_BUTTON_KEY)

            username_field.send_keys(username)
            password_field.send_keys(password)
            self._tap_element(login_button)
            # Espera pela HomePage após o login
            self._find_element_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY, timeout=15)
            time.sleep(1) # Pausa para SnackBar de login sumir, se houver
        else:
            # Se não estiver na LoginPage, tenta voltar para a HomePage caso esteja em outra tela
            max_pops = 5 # Evita loop infinito
            pops = 0
            while not self._is_element_present_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY, timeout=1) and pops < max_pops:
                print(f"Tentando voltar para a HomePage (tentativa {pops + 1})")
                current_activity = self.driver.current_activity
                self._navigate_back()
                time.sleep(0.5)
                if self.driver.current_activity == current_activity and \
                   not self._is_element_present_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY, timeout=0.5):
                    # Não conseguiu voltar efetivamente ou já está na raiz e não é a home
                    print("Botão voltar não alterou a tela ou já está na raiz (e não é a Home). Interrompendo.")
                    break
                pops += 1

        self.assertTrue(self._is_element_present_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY, timeout=5),
                        "Não foi possível alcançar a HomePage.")
        time.sleep(0.5)

    def _navigate_to_section_and_back(self, button_locator, page_indicator_locator, section_name):
        """Clica em um botão, verifica a navegação e volta."""
        self._tap_element(button_locator)
        self._find_element_by_value_key(page_indicator_locator, timeout=15)
        print(f"Navegou para {section_name} com sucesso.")
        self._navigate_back()
        self._find_element_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY) # Confirma retorno à HomePage
        print(f"Retornou para HomePage de {section_name} com sucesso.")

    # --- Test Methods ---
    def test_ui_elements_and_navigation(self):
        self._ensure_on_home_page()

        # Verifica título do AppBar
        self._find_element_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY)
        print("Título 'Menu Principal' encontrado.")

        # Navegações
        self._navigate_to_section_and_back(HOME_PAGE_FORMS_BUTTON_KEY, FORMS_PAGE_INDICATOR_KEY, "Formulários")
        self._navigate_to_section_and_back(HOME_PAGE_LISTVIEW_BUTTON_KEY, LISTVIEW_PAGE_INDICATOR_KEY, "ListView")
        self._navigate_to_section_and_back(HOME_PAGE_NATIVE_RESOURCES_BUTTON_KEY, RECURSOS_PAGE_INDICATOR_KEY, "Recursos Nativos")
        self._navigate_to_section_and_back(HOME_PAGE_GESTURES_BUTTON_KEY, GESTOS_PAGE_INDICATOR_KEY, "Gestos na Tela")
        self._navigate_to_section_and_back(HOME_PAGE_CLICK_AND_HOLD_BUTTON_KEY, CLICK_PAGE_INDICATOR_KEY, "Clicar e Segurar")
        self._navigate_to_section_and_back(HOME_PAGE_CHAT_BUTTON_KEY, CHAT_PAGE_INDICATOR_KEY, "Chat Simulado")

        # Verifica se voltou para a HomePage no final
        self.assertTrue(self._is_element_present_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY),
                        "Não retornou à HomePage após todas as navegações.")
        print("Teste de navegação concluído.")

    def test_logout_functionality(self):
        self._ensure_on_home_page()

        # 1. Tenta Logout e Cancela
        self._tap_element(HOME_PAGE_LOGOUT_BUTTON_KEY)
        self._find_element_by_value_key(HOME_PAGE_LOGOUT_DIALOG_KEY) # Espera o diálogo
        self.assertTrue(self._is_text_present(TEXT_LOGOUT_DIALOG_TITLE), "Título do diálogo de logout não encontrado.")
        print("Diálogo de logout aberto.")

        self._tap_element(HOME_PAGE_LOGOUT_DIALOG_CANCEL_BUTTON_KEY)
        # Espera o diálogo desaparecer
        self.wait.until(
            EC.invisibility_of_element_located((AppiumBy.FLUTTER, self.finder.by_value_key(HOME_PAGE_LOGOUT_DIALOG_KEY)))
        )
        print("Logout cancelado, diálogo fechado.")

        self.assertTrue(self._is_element_present_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY),
                        "Deveria permanecer na HomePage após cancelar o logout.")

        # 2. Tenta Logout e Confirma
        self._tap_element(HOME_PAGE_LOGOUT_BUTTON_KEY)
        self._find_element_by_value_key(HOME_PAGE_LOGOUT_DIALOG_KEY)
        print("Diálogo de logout reaberto.")

        self._tap_element(HOME_PAGE_LOGOUT_DIALOG_CONFIRM_BUTTON_KEY)
        # Espera a navegação para LoginPage
        self._find_element_by_value_key(LOGIN_USERNAME_FIELD_KEY, timeout=15)
        print("Logout confirmado, navegou para LoginPage.")

        self.assertFalse(self._is_element_present_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY, timeout=1),
                         "HomePage ainda está presente após o logout.")
        print("Teste de logout concluído.")

if __name__ == '__main__':
    if APP_PATH == "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI":
        print("ERRO: A variável APP_PATH não foi configurada no script.")
        print("Por favor, edite o arquivo e defina o caminho para o seu APK/APP.")
    else:
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(HomePageTests))
        runner = unittest.TextTestRunner(verbosity=2)
        print(f"Iniciando testes para o app: {APP_PATH}")
        print(f"Conectando ao servidor Appium em: {APPIUM_HOST}")
        runner.run(suite)
