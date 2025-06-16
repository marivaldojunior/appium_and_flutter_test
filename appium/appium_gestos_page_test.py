import unittest
import os
import time
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
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
HOME_PAGE_GESTURES_BUTTON_KEY = 'home_page_gestures_button'

# GestosPage
GESTOS_PAGE_APPBAR_TITLE_KEY = 'gestos_page_app_bar_title'
CLEAR_ALL_BUTTON_KEY = 'gestos_clear_all_button'
DRAWING_AREA_KEY = 'gestos_drawing_area'
COLOR_DROPDOWN_KEY = 'gestos_color_dropdown'
STROKE_WIDTH_SLIDER_KEY = 'gestos_stroke_width_slider'

# Itens do Dropdown de Cores (IMPORTANTE: Adicione estas chaves aos seus DropdownMenuItems)
COLOR_ITEM_KEY = lambda color: f'color_item_{color}'
COLOR_RED = 'red'
COLOR_GREEN = 'green'

class GestosPageTests(unittest.TestCase):
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
        print("\nNavegando para a GestosPage...")
        self._navigate_to_gestos_page()

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

    def _draw_line(self, drawing_area, start_ratio, end_ratio):
        """Desenha uma linha na área de desenho usando W3C Actions."""
        area_loc = drawing_area.location
        area_size = drawing_area.size
        start_x = area_loc['x'] + area_size['width'] * start_ratio[0]
        start_y = area_loc['y'] + area_size['height'] * start_ratio[1]
        end_x = area_loc['x'] + area_size['width'] * end_ratio[0]
        end_y = area_loc['y'] + area_size['height'] * end_ratio[1]

        actions = ActionChains(self.driver)
        pointer = PointerInput("touch", "touch_1")
        
        # Sequência: Pressionar -> Mover -> Soltar
        pointer.create_pointer_move(duration=0, x=int(start_x), y=int(start_y))
        pointer.create_pointer_down(PointerInput.MouseButton.LEFT)
        pointer.create_pointer_move(duration=300, x=int(end_x), y=int(end_y))
        pointer.create_pointer_up(PointerInput.MouseButton.LEFT)
        
        actions.add_actions(pointer)
        actions.perform()
        time.sleep(0.5)

    def _move_slider(self, slider_element, to_ratio=0.9):
        """Move o knob de um slider para uma posição relativa usando W3C Actions."""
        slider_loc = slider_element.location
        slider_size = slider_element.size
        
        start_x = slider_loc['x'] + slider_size['width'] * 0.1 # Ponto de partida
        target_x = slider_loc['x'] + slider_size['width'] * to_ratio # Ponto de destino
        y_coord = slider_loc['y'] + slider_size['height'] / 2

        actions = ActionChains(self.driver)
        pointer = PointerInput("touch", "touch_1")

        pointer.create_pointer_move(duration=0, x=int(start_x), y=int(y_coord))
        pointer.create_pointer_down(PointerInput.MouseButton.LEFT)
        pointer.create_pointer_move(duration=400, x=int(target_x), y=int(y_coord))
        pointer.create_pointer_up(PointerInput.MouseButton.LEFT)

        actions.add_actions(pointer)
        actions.perform()
        time.sleep(0.5)

    def _navigate_to_gestos_page(self, username='admin', password='1234'):
        """Navega para a GestosPage, fazendo login se necessário."""
        time.sleep(1)
        if self._is_element_present(LOGIN_USERNAME_FIELD_KEY, timeout=3):
            print("Tela de login detectada. Realizando login...")
            self._enter_text(LOGIN_USERNAME_FIELD_KEY, username)
            self._enter_text(LOGIN_PASSWORD_FIELD_KEY, password)
            self._tap_element_by_key(LOGIN_BUTTON_KEY)

        self.assertTrue(self._is_element_present(HOME_PAGE_APPBAR_TITLE_KEY, 10), "Falha ao chegar na HomePage.")
        self._tap_element_by_key(HOME_PAGE_GESTURES_BUTTON_KEY)
        self.assertTrue(self._is_element_present(GESTOS_PAGE_APPBAR_TITLE_KEY), "Falha ao navegar para a GestosPage.")
        print("Navegou para GestosPage com sucesso.")

    # --- Testes ---

    def test_drawing_workflow(self):
        """Executa um fluxo completo: desenhar, mudar cor, mudar espessura, desenhar e limpar."""
        drawing_area = self._find_element_by_key(DRAWING_AREA_KEY)
        
        # 1. Desenha uma linha inicial
        print("Desenhando linha inicial (horizontal)...")
        self._draw_line(drawing_area, start_ratio=(0.25, 0.5), end_ratio=(0.75, 0.5))

        # 2. Muda a cor para vermelho
        print("Mudando a cor para vermelho...")
        self._tap_element_by_key(COLOR_DROPDOWN_KEY)
        time.sleep(1)
        self._tap_element_by_key(COLOR_ITEM_KEY(COLOR_RED))
        
        # 3. Aumenta a espessura do traço
        print("Aumentando a espessura do traço...")
        stroke_slider = self._find_element_by_key(STROKE_WIDTH_SLIDER_KEY)
        self._move_slider(stroke_slider, to_ratio=0.9)

        # 4. Desenha outra linha com as novas configurações
        print("Desenhando linha vermelha e grossa (vertical)...")
        self._draw_line(drawing_area, start_ratio=(0.5, 0.25), end_ratio=(0.5, 0.75))
        
        # 5. Limpa a área de desenho
        print("Limpando a área de desenho...")
        self._tap_element_by_key(CLEAR_ALL_BUTTON_KEY)
        time.sleep(1) # Aguarda a UI atualizar

        # Nota: A verificação de que a tela foi limpa visualmente
        # exigiria comparação de screenshots, que está fora do escopo deste teste.
        # O teste valida que a ação de limpar foi executada sem erros.
        print("Fluxo de desenho concluído com sucesso!")

if __name__ == '__main__':
    if "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" in APP_PATH:
        print("="*60)
        print("ERRO: A variável APP_PATH não foi configurada no script.")
        print(f"Por favor, edite o arquivo '{__file__}' e defina o caminho correto para o seu APK.")
        print("="*60)
    else:
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(GestosPageTests))
        runner = unittest.TextTestRunner(verbosity=2)
        print(f"\nIniciando testes da GestosPage para o app: {APP_PATH}")
        print(f"Conectando ao servidor Appium em: {APPIUM_HOST}...")
        runner.run(suite)
