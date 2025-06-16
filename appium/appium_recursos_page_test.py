# d:\repos\appium_and_flutter_test\integration_test\recursos_page_test.py
import unittest
import os
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from appium_flutter_finder.flutter_finder import FlutterFinder

# Configurações do Appium e do Aplicativo
APPIUM_HOST = 'http://127.0.0.1:4723'
# Caminho para o arquivo APK ou APP do aplicativo em teste.
APP_PATH = "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" # Este caminho deve ser atualizado para o local do arquivo do aplicativo.

# Chaves dos elementos Flutter (ajuste conforme seu código Dart)
# LoginPage
LOGIN_USERNAME_FIELD_KEY = 'login_username_field'
LOGIN_PASSWORD_FIELD_KEY = 'login_password_field'
LOGIN_BUTTON_KEY = 'login_button'

# HomePage
HOME_PAGE_APPBAR_TITLE_KEY = 'home_page_app_bar_title'
HOME_PAGE_NATIVE_RESOURCES_BUTTON_KEY = 'home_page_native_resources_button'

# RecursosPage
RECURSOS_PAGE_APPBAR_TITLE_KEY = 'recursos_page_app_bar_title' # Ex: ValueKey('recursos_page_app_bar_title')
RECURSOS_PAGE_IMAGE_DISPLAY_AREA_KEY = 'recursos_page_image_display_area'
# O ícone de busca de imagem geralmente faz parte do imageDisplayArea e não tem uma key própria interativa.
# Se for um widget separado com uma key, adicione-a.
RECURSOS_PAGE_OPEN_CAMERA_BUTTON_KEY = 'recursos_page_open_camera_button'
RECURSOS_PAGE_OPEN_GALLERY_BUTTON_KEY = 'recursos_page_open_gallery_button'
RECURSOS_PAGE_SELECT_IMAGE_BUTTON_KEY = 'recursos_page_select_image_button'
RECURSOS_PAGE_REMOVE_IMAGE_BUTTON_KEY = 'recursos_page_remove_image_button'

# ActionSheet (ModalBottomSheet) para seleção de imagem
# A sheet em si pode não ter uma key, mas seus itens sim.
RECURSOS_PAGE_IMAGE_SOURCE_SHEET_GALLERY_OPTION_KEY = 'recursos_page_image_source_sheet_gallery_option'
RECURSOS_PAGE_IMAGE_SOURCE_SHEET_CAMERA_OPTION_KEY = 'recursos_page_image_source_sheet_camera_option'

# Textos para SnackBars/mensagens (usados em XPaths)
TEXT_NENHUMA_IMAGEM_SELECIONADA = "Nenhuma imagem selecionada" # Texto exibido quando nenhuma imagem é selecionada da galeria.
TEXT_NENHUMA_IMAGEM_TIRADA = "Nenhuma imagem tirada."     # Texto exibido quando nenhuma imagem é capturada pela câmera.
TEXT_SNACKBAR_PREFIX = "Snackbar: " # Se o seu app prefixar assim

class RecursosPageTests(unittest.TestCase):
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

    def _is_element_present_by_value_key(self, key_string, timeout=3):
        try:
            self._find_element_by_value_key(key_string, timeout)
            return True
        except TimeoutException:
            return False

    def _is_text_present(self, text_string, timeout=5):
        # Verifica se um texto está presente na tela. Útil para SnackBars ou alertas.
        # Para elementos interativos, prefira ValueKey.
        # O FlutterFinder by_text pode ser menos performático.
        try:
            # Tenta primeiro com FlutterFinder (se o SnackBar for um widget Flutter)
            self.wait.until(EC.presence_of_element_located((AppiumBy.FLUTTER, self.finder.by_text(text_string))))
            return True
        except TimeoutException:
            # Fallback para XPath (se o SnackBar for um overlay nativo)
            try:
                self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, f"//*[contains(@text,'{text_string}')]")))
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

    def _wait_for_snackbar_message(self, message_text, timeout=5, present=True):
        """Espera por uma mensagem de SnackBar e verifica sua presença/ausência."""
        # Tenta localizar o SnackBar pelo texto. Uma ValueKey no SnackBar seria mais robusta.
        # O FlutterFinder pode não encontrar textos em overlays nativos (SnackBars comuns).
        # Por isso, usamos XPath como fallback.
        start_time = time.time()
        while time.time() < start_time + timeout:
            if self._is_text_present(message_text, timeout=0.5) == present:
                return
            time.sleep(0.2)
        self.fail(f"A mensagem do SnackBar '{message_text}' não ficou {'presente' if present else 'ausente'} dentro de {timeout}s.")

    def _navigate_to_recursos_page(self, username='admin', password='1234'):
        """Navega para a RecursosPage, realizando o login se estiver na LoginPage."""
        time.sleep(1)

        if self._is_element_present_by_value_key(LOGIN_USERNAME_FIELD_KEY, timeout=3):
            print("Realizando login para chegar na RecursosPage...")
            username_field = self._find_element_by_value_key(LOGIN_USERNAME_FIELD_KEY)
            password_field = self._find_element_by_value_key(LOGIN_PASSWORD_FIELD_KEY)
            login_button = self._find_element_by_value_key(LOGIN_BUTTON_KEY)

            username_field.send_keys(username)
            password_field.send_keys(password)
            self._tap_element(login_button)
            self._find_element_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY, timeout=15)
            time.sleep(1)
        
        self._find_element_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY) # Confirma que está na HomePage
        self._tap_element(HOME_PAGE_NATIVE_RESOURCES_BUTTON_KEY)
        self._find_element_by_value_key(RECURSOS_PAGE_APPBAR_TITLE_KEY) # Confirma que está na RecursosPage
        time.sleep(0.5)

    def test_recursos_page_ui_and_no_image_selection(self):
        """Verifica UI inicial e interage com seletores de imagem (simulando nenhuma seleção)."""
        self._navigate_to_recursos_page()

        # 1. Verifica estado inicial da UI
        self._find_element_by_value_key(RECURSOS_PAGE_IMAGE_DISPLAY_AREA_KEY)
        self.assertTrue(self._is_text_present(TEXT_NENHUMA_IMAGEM_SELECIONADA),
                        f"Texto '{TEXT_NENHUMA_IMAGEM_SELECIONADA}' não encontrado na área de imagem inicial.")
        # Se tiver uma key, adicione a verificação:
        # self.assertTrue(self._is_element_present_by_value_key('sua_image_search_icon_key'))

        self.assertTrue(self._is_element_present_by_value_key(RECURSOS_PAGE_OPEN_CAMERA_BUTTON_KEY),
                        "Botão 'Abrir Câmera' não encontrado.")
        self.assertTrue(self._is_element_present_by_value_key(RECURSOS_PAGE_OPEN_GALLERY_BUTTON_KEY),
                        "Botão 'Abrir Galeria' não encontrado.")
        self.assertTrue(self._is_element_present_by_value_key(RECURSOS_PAGE_SELECT_IMAGE_BUTTON_KEY),
                        "Botão 'Selecionar Imagem' não encontrado.")

        self.assertFalse(self._is_element_present_by_value_key(RECURSOS_PAGE_REMOVE_IMAGE_BUTTON_KEY, timeout=2),
                         "Botão 'Remover Imagem' deveria estar invisível inicialmente.")

        # 2. Tenta abrir a câmera (simulando cancelamento ou nenhuma imagem)
        self._tap_element(RECURSOS_PAGE_OPEN_CAMERA_BUTTON_KEY)
        # Se um seletor nativo abrir, o app Flutter pode receber um callback de 'nenhuma imagem'.
        # O teste aqui simula que o app mostrou o SnackBar correspondente.
        self._wait_for_snackbar_message(TEXT_NENHUMA_IMAGEM_TIRADA, present=True)
        self._wait_for_snackbar_message(TEXT_NENHUMA_IMAGEM_TIRADA, present=False) # Espera SnackBar desaparecer

        # 3. Tenta abrir a galeria (simulando cancelamento ou nenhuma imagem)
        self._tap_element(RECURSOS_PAGE_OPEN_GALLERY_BUTTON_KEY)
        self._wait_for_snackbar_message(TEXT_NENHUMA_IMAGEM_SELECIONADA, present=True)
        self._wait_for_snackbar_message(TEXT_NENHUMA_IMAGEM_SELECIONADA, present=False)

        # 4. Tenta selecionar imagem via ActionSheet (Galeria)
        self._tap_element(RECURSOS_PAGE_SELECT_IMAGE_BUTTON_KEY)
        # Espera o ActionSheet (ModalBottomSheet) e suas opções aparecerem
        gallery_option = self._find_element_by_value_key(RECURSOS_PAGE_IMAGE_SOURCE_SHEET_GALLERY_OPTION_KEY, timeout=10)
        self.assertTrue(self._is_element_present_by_value_key(RECURSOS_PAGE_IMAGE_SOURCE_SHEET_CAMERA_OPTION_KEY),
                        "Opção 'Câmera' no sheet não encontrada.")
        self._tap_element(gallery_option)
        self._wait_for_snackbar_message(TEXT_NENHUMA_IMAGEM_SELECIONADA, present=True)
        self._wait_for_snackbar_message(TEXT_NENHUMA_IMAGEM_SELECIONADA, present=False)

        # 5. Tenta selecionar imagem via ActionSheet (Câmera)
        self._tap_element(RECURSOS_PAGE_SELECT_IMAGE_BUTTON_KEY)
        camera_option = self._find_element_by_value_key(RECURSOS_PAGE_IMAGE_SOURCE_SHEET_CAMERA_OPTION_KEY, timeout=10)
        self._tap_element(camera_option)
        self._wait_for_snackbar_message(TEXT_NENHUMA_IMAGEM_TIRADA, present=True)
        self._wait_for_snackbar_message(TEXT_NENHUMA_IMAGEM_TIRADA, present=False)

        # Confirma que a área de imagem ainda mostra "Nenhuma imagem selecionada"
        self.assertTrue(self._is_text_present(TEXT_NENHUMA_IMAGEM_SELECIONADA),
                        f"Texto '{TEXT_NENHUMA_IMAGEM_SELECIONADA}' não encontrado após tentativas.")
        self.assertFalse(self._is_element_present_by_value_key(RECURSOS_PAGE_REMOVE_IMAGE_BUTTON_KEY, timeout=2),
                         "Botão 'Remover Imagem' ainda deveria estar invisível.")

if __name__ == '__main__':
    if "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" in APP_PATH: # Verificação mais genérica
        print("ERRO: A variável APP_PATH não foi configurada no script.")
        print(f"Por favor, edite o arquivo {__file__} e defina o caminho para o seu APK/APP.")
    else:
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(RecursosPageTests))
        runner = unittest.TextTestRunner(verbosity=2)
        print(f"Iniciando testes da RecursosPage para o app: {APP_PATH}")
        print(f"Conectando ao servidor Appium em: {APPIUM_HOST}...")
        runner.run(suite)
