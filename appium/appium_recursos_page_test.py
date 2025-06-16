# d:\repos\appium_and_flutter_test\integration_test\recursos_page_test.py
import unittest
import os
import time
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
# Navegação
LOGIN_USERNAME_FIELD_KEY = 'login_username_field'
LOGIN_PASSWORD_FIELD_KEY = 'login_password_field'
LOGIN_BUTTON_KEY = 'login_button'
HOME_PAGE_APPBAR_TITLE_KEY = 'home_page_app_bar_title'
HOME_PAGE_NATIVE_RESOURCES_BUTTON_KEY = 'home_page_native_resources_button'

# RecursosPage
RECURSOS_PAGE_APPBAR_TITLE_KEY = 'recursos_page_app_bar_title'
RECURSOS_PAGE_IMAGE_DISPLAY_AREA_KEY = 'recursos_page_image_display_area'
RECURSOS_PAGE_SELECT_IMAGE_BUTTON_KEY = 'recursos_page_select_image_button'
RECURSOS_PAGE_REMOVE_IMAGE_BUTTON_KEY = 'recursos_page_remove_image_button'

# ActionSheet (ModalBottomSheet) para seleção de imagem
RECURSOS_PAGE_IMAGE_SOURCE_SHEET_GALLERY_OPTION_KEY = 'recursos_page_image_source_sheet_gallery_option'
RECURSOS_PAGE_IMAGE_SOURCE_SHEET_CAMERA_OPTION_KEY = 'recursos_page_image_source_sheet_camera_option'

# Textos para Validação
# É mais robusto verificar a presença de um widget com uma chave do que um texto literal.
# Se possível, adicione uma ValueKey ao Text widget que mostra essa mensagem.
INITIAL_IMAGE_TEXT_KEY = 'initial_image_text_indicator'
TEXT_SNACKBAR_NO_IMAGE_SELECTED = "Nenhuma imagem selecionada."
TEXT_SNACKBAR_NO_IMAGE_TAKEN = "Nenhuma imagem tirada."

class RecursosPageTests(unittest.TestCase):
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
            'newCommandTimeout': 180,  # Aumentado para interações com recursos nativos
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
        """Garante que cada teste comece na RecursosPage."""
        print("\nAssegurando que o teste começa na RecursosPage...")
        self._navigate_to_recursos_page()

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
        if self.driver.is_keyboard_shown():
            try: self.driver.hide_keyboard()
            except: pass
        time.sleep(0.2)

    def _is_snackbar_present(self, text, timeout=5):
        """Verifica se uma snackbar com o texto especificado está visível."""
        try:
            locator = (AppiumBy.XPATH, f"//*[contains(@text,'{text}')]")
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def _navigate_to_recursos_page(self, username='admin', password='1234'):
        """Navega para a RecursosPage, realizando login se necessário."""
        time.sleep(1)
        if self._is_element_present(LOGIN_USERNAME_FIELD_KEY, timeout=2):
            print("Tela de login detectada. Realizando login...")
            self._enter_text(LOGIN_USERNAME_FIELD_KEY, username)
            self._enter_text(LOGIN_PASSWORD_FIELD_KEY, password)
            self._tap_element_by_key(LOGIN_BUTTON_KEY)

        self.assertTrue(self._is_element_present(HOME_PAGE_APPBAR_TITLE_KEY, 10), "Falha ao chegar na HomePage.")
        self._tap_element_by_key(HOME_PAGE_NATIVE_RESOURCES_BUTTON_KEY)
        self.assertTrue(self._is_element_present(RECURSOS_PAGE_APPBAR_TITLE_KEY), "Falha ao navegar para a RecursosPage.")
        print("Navegação para RecursosPage concluída.")

    # --- Testes ---

    def test_initial_ui_is_correct(self):
        """Verifica se a UI inicial da página de recursos está correta."""
        print("Verificando UI inicial...")
        self.assertTrue(self._is_element_present(RECURSOS_PAGE_IMAGE_DISPLAY_AREA_KEY), "Área de imagem não encontrada.")
        # É preferível ter uma chave para o texto inicial para maior robustez.
        self.assertTrue(self._is_element_present(INITIAL_IMAGE_TEXT_KEY), "Texto/Ícone inicial na área de imagem não encontrado.")
        self.assertTrue(self._is_element_present(RECURSOS_PAGE_SELECT_IMAGE_BUTTON_KEY), "Botão 'Selecionar Imagem' não encontrado.")
        self.assertFalse(self._is_element_present(RECURSOS_PAGE_REMOVE_IMAGE_BUTTON_KEY, timeout=1), "Botão 'Remover Imagem' deveria estar invisível.")
        print("UI inicial verificada com sucesso.")

    def test_select_image_from_gallery_and_cancel(self):
        """Testa o fluxo de abrir a seleção de imagem (Galeria) e cancelar."""
        print("Testando fluxo: Selecionar Imagem -> Galeria (e cancelar)...")
        self._tap_element_by_key(RECURSOS_PAGE_SELECT_IMAGE_BUTTON_KEY)

        # Espera o ActionSheet (ModalBottomSheet) e suas opções aparecerem
        self.assertTrue(self._is_element_present(RECURSOS_PAGE_IMAGE_SOURCE_SHEET_GALLERY_OPTION_KEY, 10), "Opção 'Galeria' no sheet não encontrada.")
        self._tap_element_by_key(RECURSOS_PAGE_IMAGE_SOURCE_SHEET_GALLERY_OPTION_KEY)

        # Simula o cancelamento da seleção na galeria.
        # O app deve mostrar um SnackBar informando que nenhuma imagem foi selecionada.
        # Nota: Testar a interação real com a galeria nativa é complexo e geralmente evitado em testes de unidade/widget.
        # Focamos na resposta do app ao callback do seletor de imagens.
        self.assertTrue(self._is_snackbar_present(TEXT_SNACKBAR_NO_IMAGE_SELECTED), "Snackbar de 'nenhuma imagem selecionada' não apareceu.")
        print("Fluxo de cancelamento da galeria verificado com sucesso.")

    def test_select_image_from_camera_and_cancel(self):
        """Testa o fluxo de abrir a seleção de imagem (Câmera) e cancelar."""
        print("Testando fluxo: Selecionar Imagem -> Câmera (e cancelar)...")
        self._tap_element_by_key(RECURSOS_PAGE_SELECT_IMAGE_BUTTON_KEY)

        # Espera o ActionSheet e clica na opção de câmera
        self.assertTrue(self._is_element_present(RECURSOS_PAGE_IMAGE_SOURCE_SHEET_CAMERA_OPTION_KEY, 10), "Opção 'Câmera' no sheet não encontrada.")
        self._tap_element_by_key(RECURSOS_PAGE_IMAGE_SOURCE_SHEET_CAMERA_OPTION_KEY)

        # Simula o cancelamento da captura da câmera.
        # O app deve mostrar um SnackBar informando que nenhuma imagem foi tirada.
        self.assertTrue(self._is_snackbar_present(TEXT_SNACKBAR_NO_IMAGE_TAKEN), "Snackbar de 'nenhuma imagem tirada' não apareceu.")
        print("Fluxo de cancelamento da câmera verificado com sucesso.")
        
    # Testes para o fluxo de sucesso (selecionar e remover imagem) seriam assim:
    # def test_select_and_remove_image(self):
    #     # 1. Empurrar um arquivo de imagem para o emulador
    #     # self.driver.push_file('/sdcard/Download/test_image.png', '/path/to/local/image.png')
    #     # 2. Abrir galeria
    #     # 3. Interagir com a UI nativa da galeria para selecionar a imagem (usando XPath/UIAutomator2)
    #     # 4. Verificar se a imagem apareceu no app
    #     # self.assertFalse(self._is_element_present(INITIAL_IMAGE_TEXT_KEY))
    #     # self.assertTrue(self._is_element_present(RECURSOS_PAGE_REMOVE_IMAGE_BUTTON_KEY))
    #     # 5. Clicar em remover
    #     # self._tap_element_by_key(RECURSOS_PAGE_REMOVE_IMAGE_BUTTON_KEY)
    #     # 6. Verificar se voltou ao estado inicial
    #     # self.assertTrue(self._is_element_present(INITIAL_IMAGE_TEXT_KEY))

if __name__ == '__main__':
    if "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" in APP_PATH:
        print("="*60)
        print("ERRO: A variável APP_PATH não foi configurada no script.")
        print(f"Por favor, edite o arquivo '{__file__}' e defina o caminho correto para o seu APK.")
        print("="*60)
    else:
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(RecursosPageTests))
        runner = unittest.TextTestRunner(verbosity=2)
        print(f"\nIniciando testes da RecursosPage para o app: {APP_PATH}")
        print(f"Conectando ao servidor Appium em: {APPIUM_HOST}...")
        runner.run(suite)
