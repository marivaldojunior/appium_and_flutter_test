import unittest
import os
import time
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
APP_PATH = os.path.abspath('D:\\repos\\appium_and_flutter_test\\build\\app\\outputs\\flutter-apk\\app-debug.apk')

if not os.path.exists(APP_PATH):
    APP_PATH = "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI"

# --- Chaves dos Elementos Flutter ---
# Navegação
LOGIN_USERNAME_FIELD_KEY = 'login_username_field'
LOGIN_PASSWORD_FIELD_KEY = 'login_password_field'
LOGIN_BUTTON_KEY = 'login_button'
HOME_PAGE_APPBAR_TITLE_KEY = 'home_page_app_bar_title'
HOME_PAGE_FORMS_BUTTON_KEY = 'home_page_forms_button'

# FormsPage
FORMS_PAGE_INDICATOR_KEY = 'forms_name_field' # Usa o primeiro campo como indicador da página
NAME_FIELD_KEY = 'forms_name_field'
EMAIL_FIELD_KEY = 'forms_email_field'
AGE_FIELD_KEY = 'forms_age_field'
DATE_PICKER_FIELD_KEY = 'forms_date_picker_field'
SUBSCRIBE_SWITCH_KEY = 'forms_subscribe_switch'
SKILL_CHECKBOX_PREFIX_KEY = 'forms_skill_checkbox_'
GENDER_RADIO_PREFIX_KEY = 'forms_gender_radio_'
COUNTRY_DROPDOWN_KEY = 'forms_country_dropdown'
DESCRIPTION_FIELD_KEY = 'forms_description_field'
SUBMIT_BUTTON_KEY = 'forms_submit_button'
# Chave para o item do Dropdown (IMPORTANTE: Adicione esta chave ao seu widget DropdownMenuItem)
COUNTRY_ITEM_KEY = lambda country: f'country_item_{country}'

# --- Dados de Teste ---
TEST_NAME = "Nome de Teste Appium"
TEST_EMAIL = "teste@appium.com"
TEST_AGE = "30"
TEST_SKILL_FLUTTER = "Flutter"
TEST_GENDER_MASCULINO = "Masculino"
TEST_COUNTRY_BRASIL = "Brasil"
TEST_DESCRIPTION = "Descrição de teste gerada pelo Appium."
SUCCESS_SNACKBAR_TEXT = "Formulário enviado com sucesso!"

class FormsPageTests(unittest.TestCase):
    driver: webdriver.Remote
    finder: FlutterFinder
    wait: WebDriverWait

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
        """Executado antes de cada teste para garantir um estado limpo e navegação."""
        print("\nNavegando para a FormsPage...")
        self._navigate_to_forms_page()

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
        
    def _is_snackbar_present(self, text, timeout=5):
        try:
            # Snackbar no Android geralmente é um elemento nativo, então XPath é mais confiável.
            self.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, f"//*[contains(@text,'{text}')]"))
            )
            return True
        except TimeoutException:
            return False

    def _scroll_to_element(self, key):
        """Rola a tela até que um elemento com a chave dada esteja visível."""
        finder = self.finder.by_value_key(key)
        self.driver.execute_script('flutter:scrollUntilVisible', finder, {'dxScroll': 0, 'dyScroll': -400})
        time.sleep(0.5)

    def _navigate_to_forms_page(self, username='admin', password='1234'):
        """Navega para a FormsPage, realizando login se necessário."""
        time.sleep(1)
        if self._is_element_present(LOGIN_USERNAME_FIELD_KEY, timeout=3):
            print("Tela de login detectada. Realizando login...")
            self._enter_text(LOGIN_USERNAME_FIELD_KEY, username)
            self._enter_text(LOGIN_PASSWORD_FIELD_KEY, password)
            self._tap_element_by_key(LOGIN_BUTTON_KEY)

        self.assertTrue(self._is_element_present(HOME_PAGE_APPBAR_TITLE_KEY, 10), "Falha ao chegar na HomePage.")
        self._tap_element_by_key(HOME_PAGE_FORMS_BUTTON_KEY)
        self.assertTrue(self._is_element_present(FORMS_PAGE_INDICATOR_KEY), "Falha ao navegar para a FormsPage.")
        print("Navegou para FormsPage com sucesso.")

    # --- Testes ---

    def test_fill_and_submit_complete_form(self):
        """Preenche todos os campos do formulário, submete e verifica o sucesso."""
        # Preenche campos de texto
        print("Preenchendo campos de texto...")
        self._enter_text(NAME_FIELD_KEY, TEST_NAME)
        self._enter_text(EMAIL_FIELD_KEY, TEST_EMAIL)
        self._enter_text(AGE_FIELD_KEY, TEST_AGE)

        # Seleciona data no DatePicker
        print("Selecionando data...")
        self._tap_element_by_key(DATE_PICKER_FIELD_KEY)
        time.sleep(1) # Espera o picker nativo abrir
        # Interage com o botão OK do DatePicker nativo do Android
        ok_button = self.wait.until(EC.presence_of_element_located((AppiumBy.ID, "android:id/button1")))
        ok_button.click()
        time.sleep(1)

        # Rola para os próximos campos
        self._scroll_to_element(DESCRIPTION_FIELD_KEY)

        # Ativa o switch de inscrição
        print("Ativando switch...")
        self._tap_element_by_key(SUBSCRIBE_SWITCH_KEY)

        # Seleciona checkboxes de habilidades
        print("Selecionando checkboxes...")
        self._tap_element_by_key(f"{SKILL_CHECKBOX_PREFIX_KEY}{TEST_SKILL_FLUTTER}")
        
        # Seleciona o Radio Button de gênero
        print("Selecionando gênero...")
        self._tap_element_by_key(f"{GENDER_RADIO_PREFIX_KEY}{TEST_GENDER_MASCULINO}")
        
        # Seleciona um país no Dropdown
        print(f"Selecionando país '{TEST_COUNTRY_BRASIL}'...")
        self._tap_element_by_key(COUNTRY_DROPDOWN_KEY)
        time.sleep(1) # Espera o menu do dropdown abrir
        # IMPORTANTE: Garanta que seu DropdownMenuItem tenha uma ValueKey
        # Ex: DropdownMenuItem(key: ValueKey('country_item_Brasil'), ...)
        country_key = COUNTRY_ITEM_KEY(TEST_COUNTRY_BRASIL)
        self._tap_element_by_key(country_key)

        # Preenche a descrição
        print("Preenchendo descrição...")
        self._enter_text(DESCRIPTION_FIELD_KEY, TEST_DESCRIPTION)

        # Rola até o botão de submissão e o clica
        print("Submetendo o formulário...")
        self._scroll_to_element(SUBMIT_BUTTON_KEY)
        self._tap_element_by_key(SUBMIT_BUTTON_KEY)
        
        # Verifica a snackbar de sucesso
        print("Verificando snackbar de sucesso...")
        self.assertTrue(
            self._is_snackbar_present(SUCCESS_SNACKBAR_TEXT),
            "A snackbar de sucesso não foi exibida ou seu texto está incorreto."
        )
        print("Formulário preenchido e submetido com sucesso!")

if __name__ == '__main__':
    if "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" in APP_PATH:
        print("="*60)
        print("ERRO: A variável APP_PATH não foi configurada no script.")
        print(f"Por favor, edite o arquivo '{__file__}' e defina o caminho correto para o seu APK.")
        print("="*60)
    else:
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(FormsPageTests))
        runner = unittest.TextTestRunner(verbosity=2)
        print(f"\nIniciando testes da FormsPage para o app: {APP_PATH}")
        print(f"Conectando ao servidor Appium em: {APPIUM_HOST}...")
        runner.run(suite)
