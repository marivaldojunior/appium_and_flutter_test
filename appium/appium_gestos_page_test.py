import unittest
import os
import time
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException # Adicionado para _is_element_present_by_value_key
from appium_flutter_finder.flutter_finder import FlutterFinder

# Configurações do Appium e do Aplicativo (ajuste conforme necessário)
APPIUM_HOST = 'http://127.0.0.1:4723' # Ou o endereço do seu servidor Appium
# O caminho para o APK deve ser ajustado para sua máquina local
# Exemplo: 'C:\\Users\\seu_usuario\\path\\to\\your\\app-debug.apk'
# Ou um caminho relativo se o script estiver na estrutura do projeto Flutter:
# APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
#                                         '..', 'build', 'app', 'outputs', 'apk', 'debug', 'app-debug.apk'))
APP_PATH = "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" # IMPORTANTE: Atualize este caminho

# --- Chaves dos Elementos Flutter para Navegação ---
# LoginPage
LOGIN_USERNAME_FIELD_KEY = 'login_username_field'
LOGIN_PASSWORD_FIELD_KEY = 'login_password_field'
LOGIN_BUTTON_KEY = 'login_button'

# HomePage
HOME_PAGE_APPBAR_TITLE_KEY = 'home_page_app_bar_title'
HOME_PAGE_GESTURES_BUTTON_KEY = 'home_page_gestures_button' # Botão que navega para a GestosPage

# Chaves dos elementos Flutter (conforme definido em gestos_page.dart)
GESTOS_PAGE_APPBAR_TITLE_KEY = 'gestos_page_app_bar_title' # Adicionado para verificação
CLEAR_ALL_BUTTON_KEY = 'gestos_clear_all_button'
DRAWING_AREA_KEY = 'gestos_drawing_area'
COLOR_DROPDOWN_KEY = 'gestos_color_dropdown'
STROKE_WIDTH_SLIDER_KEY = 'gestos_stroke_width_slider'

# Indicador da GestosPage (para confirmar navegação)
GESTOS_PAGE_INDICATOR_KEY = GESTOS_PAGE_APPBAR_TITLE_KEY # Ou DRAWING_AREA_KEY

# Chaves para os itens do Dropdown (assumindo que foram adicionadas conforme sugestão)
COLOR_ITEM_RED_KEY = 'color_item_red'
COLOR_ITEM_GREEN_KEY = 'color_item_green'

class GestosPageTests(unittest.TestCase):
    driver: webdriver.Remote
    finder: FlutterFinder
    wait: WebDriverWait

    @classmethod
    def setUpClass(cls):
        """Configuração do driver do Appium."""
        # Ajuste as capacidades conforme necessário para seu ambiente.
        capabilities = dict(
            platformName='Android',  # ou 'iOS'
            deviceName='Android Emulator', # Valor comum nos seus testes
            appPackage='com.example.appium_and_flutter_test', # Pacote do seu app
            appActivity='.MainActivity', # Atividade principal do seu app
            automationName='Flutter'  # Usado para testes Flutter
        )
        options = AppiumOptions().load_capabilities(capabilities)
        # Adicionando outras opções comuns nos seus testes:
        options.set_capability('app-debug.apk', "D:\\repos\\appium_and_flutter_test\\build\\app\\outputs\\flutter-apk\\app-debug.apk")
        options.set_capability('retryBackoffTime', 500)
        options.set_capability('maxRetryCount', 3)
        options.set_capability('newCommandTimeout', 120) # Ou outro valor dependendo da complexidade da página

        cls.driver = webdriver.Remote('http://127.0.0.1:4723', options=options) # URL do servidor Appium
        cls.wait = WebDriverWait(cls.driver, 30)  # Timeout comum nos seus testes
        cls.finder = FlutterFinder() # Adicionado, pois é usado em todos os seus testes Appium/Flutter

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()

    def _find_element_by_value_key(self, key_string, timeout=20):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((AppiumBy.FLUTTER, self.finder.by_value_key(key_string)))
        )

    def _is_element_present_by_value_key(self, key_string, timeout=3):
        try:
            self._find_element_by_value_key(key_string, timeout)
            return True
        except TimeoutException:
            return False

    def _draw_line(self, drawing_area, start_x_ratio, start_y_ratio, end_x_ratio, end_y_ratio):
        area_loc = drawing_area.location
        area_size = drawing_area.size

        start_x = area_loc['x'] + area_size['width'] * start_x_ratio
        start_y = area_loc['y'] + area_size['height'] * start_y_ratio
        end_x = area_loc['x'] + area_size['width'] * end_x_ratio
        end_y = area_loc['y'] + area_size['height'] * end_y_ratio

        touch_action = TouchAction(self.driver)
        touch_action.press(x=start_x, y=start_y).wait(ms=300).move_to(x=end_x, y=end_y).release().perform()
        time.sleep(0.5) # Pequena pausa para a renderização do desenho

    def _tap_element(self, element_or_key): # Helper para clicar em elemento por key ou objeto
        if isinstance(element_or_key, str):
            element = self._find_element_by_value_key(element_or_key)
        else:
            element = element_or_key
        element.click()
        time.sleep(0.5) # Pausa para UI

    def _navigate_to_gestos_page(self, username='admin', password='1234'):
        """Navega para a GestosPage, fazendo login se necessário."""
        time.sleep(1) # Pausa inicial

        # Se estiver na LoginPage, faz login
        if self._is_element_present_by_value_key(LOGIN_USERNAME_FIELD_KEY, timeout=3):
            print("Realizando login para chegar na GestosPage...")
            username_field = self._find_element_by_value_key(LOGIN_USERNAME_FIELD_KEY)
            password_field = self._find_element_by_value_key(LOGIN_PASSWORD_FIELD_KEY)
            login_button = self._find_element_by_value_key(LOGIN_BUTTON_KEY)

            username_field.click(); time.sleep(0.1); username_field.clear(); username_field.send_keys(username)
            password_field.click(); time.sleep(0.1); password_field.clear(); password_field.send_keys(password)
            
            try:
                if self.driver.is_keyboard_shown():
                    self.driver.hide_keyboard()
            except: pass

            self._tap_element(login_button)
            self._find_element_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY, timeout=15) # Espera HomePage
            time.sleep(1) 
        
        # Confirma que está na HomePage (ou chegou nela)
        self._find_element_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY)
        
        # Navega para GestosPage
        gestos_button = self._find_element_by_value_key(HOME_PAGE_GESTURES_BUTTON_KEY)
        self._tap_element(gestos_button)
        self._find_element_by_value_key(GESTOS_PAGE_INDICATOR_KEY) # Confirma que está na GestosPage
        print("Navegou para GestosPage com sucesso.")
        time.sleep(0.5)

    def test_01_initial_draw(self):
        self._navigate_to_gestos_page() # Navega para a página de gestos
        drawing_area = self._find_element_by_value_key(DRAWING_AREA_KEY)
        self.assertIsNotNone(drawing_area, "Área de desenho não encontrada")
        self._draw_line(drawing_area, 0.25, 0.5, 0.75, 0.5) # Linha horizontal

    def test_02_change_color_and_draw(self):
        color_dropdown = self._find_element_by_value_key(COLOR_DROPDOWN_KEY)
        color_dropdown.click()
        time.sleep(1) # Esperar o dropdown abrir e itens renderizarem

        # Selecionar a cor vermelha (assumindo que a ValueKey 'color_item_red' foi adicionada)
        red_color_option = self._find_element_by_value_key(COLOR_ITEM_RED_KEY)
        self._tap_element(red_color_option) # Usar helper _tap_element
        time.sleep(0.5) # Esperar a seleção da cor

        drawing_area = self._find_element_by_value_key(DRAWING_AREA_KEY)
        self._draw_line(drawing_area, 0.5, 0.25, 0.5, 0.75) # Linha vertical

    def test_03_change_stroke_width_and_draw(self):
        stroke_slider = self._find_element_by_value_key(STROKE_WIDTH_SLIDER_KEY)
        self.assertIsNotNone(stroke_slider, "Slider de espessura não encontrado")

        slider_loc = stroke_slider.location
        slider_size = stroke_slider.size
        
        # Mover o slider para a direita para aumentar a espessura
        # Estes são pontos relativos ao elemento slider
        start_x = slider_loc['x'] + slider_size['width'] * 0.1 # Ponto inicial no slider
        y_coord = slider_loc['y'] + slider_size['height'] / 2
        end_x = slider_loc['x'] + slider_size['width'] * 0.9   # Ponto final no slider (aumentar espessura)

        touch_action = TouchAction(self.driver)
        # Pressionar no início do slider, mover para o fim e soltar
        touch_action.long_press(el=stroke_slider, x=slider_size['width'] * 0.1, y=slider_size['height'] / 2)\
                    .move_to(el=stroke_slider, x=slider_size['width'] * 0.9, y=slider_size['height'] / 2)\
                    .release().perform()
        time.sleep(0.5) # Pausa para a UI atualizar

        drawing_area = self._find_element_by_value_key(DRAWING_AREA_KEY)
        self._draw_line(drawing_area, 0.2, 0.2, 0.8, 0.8) # Linha diagonal

    def test_04_clear_drawing(self):
        # Desenhar algo primeiro para garantir que há o que limpar
        drawing_area = self._find_element_by_value_key(DRAWING_AREA_KEY)
        self._draw_line(drawing_area, 0.3, 0.3, 0.7, 0.7)

        clear_button = self._find_element_by_value_key(CLEAR_ALL_BUTTON_KEY)
        self.assertIsNotNone(clear_button, "Botão Limpar Tudo não encontrado")
        self._tap_element(clear_button) # Usar helper _tap_element
        
        time.sleep(1) # Pausa para a limpeza ser processada
        # A verificação de que a área está limpa pode ser complexa.
        # Pode-se tentar desenhar novamente e verificar se apenas o novo desenho existe,
        # ou, se possível, verificar alguma propriedade do estado da lista _drawingLines (requereria extensões de driver).
        # Por agora, confiamos que o clique no botão funciona.
        # Para uma verificação mais robusta, seria necessário comparar screenshots ou ter acesso ao estado interno.

    def test_05_select_another_color_and_stroke(self):
        # Mudar para verde
        color_dropdown = self._find_element_by_value_key(COLOR_DROPDOWN_KEY)
        self._tap_element(color_dropdown) # Usar helper _tap_element
        time.sleep(1) # Esperar o dropdown abrir e itens renderizarem
        green_color_option = self._find_element_by_value_key(COLOR_ITEM_GREEN_KEY)
        self._tap_element(green_color_option) # Usar helper _tap_element
        time.sleep(0.5)

        # Mudar espessura para menor
        stroke_slider = self._find_element_by_value_key(STROKE_WIDTH_SLIDER_KEY)
        slider_loc = stroke_slider.location
        slider_size = stroke_slider.size
        touch_action = TouchAction(self.driver)
        touch_action.long_press(el=stroke_slider, x=slider_size['width'] * 0.8, y=slider_size['height'] / 2)\
                    .move_to(el=stroke_slider, x=slider_size['width'] * 0.2, y=slider_size['height'] / 2)\
                    .release().perform()
        time.sleep(0.5)

        drawing_area = self._find_element_by_value_key(DRAWING_AREA_KEY)
        self._draw_line(drawing_area, 0.8, 0.2, 0.2, 0.8) # Outra linha diagonal

if __name__ == '__main__':
    # Certifique-se de que APP_PATH está configurado antes de rodar.
    if APP_PATH == "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI":
        print("ERRO: A variável APP_PATH não foi configurada no script.")
        print("Por favor, edite o arquivo gestos_page_test.py e defina o caminho para o seu APK/APP.")
    else:
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(GestosPageTests))
        runner = unittest.TextTestRunner()
        print(f"Iniciando testes para o app: {APP_PATH}")
        print(f"Conectando ao servidor Appium em: {APPIUM_HOST}")
        runner.run(suite)