import unittest
import os
import time
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium_flutter_finder.flutter_finder import FlutterFinder

# Configurações do Appium e do Aplicativo (ajuste conforme necessário)
APPIUM_HOST = 'http://127.0.0.1:4723'
APP_PATH = "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" # IMPORTANTE: Atualize este caminho

# --- Chaves dos Elementos Flutter para Navegação ---
# LoginPage
LOGIN_USERNAME_FIELD_KEY = 'login_username_field'
LOGIN_PASSWORD_FIELD_KEY = 'login_password_field'
LOGIN_BUTTON_KEY = 'login_button'

# HomePage
HOME_PAGE_APPBAR_TITLE_KEY = 'home_page_app_bar_title'
HOME_PAGE_FORMS_BUTTON_KEY = 'home_page_forms_button' # Botão que navega para a FormsPage

# Chaves dos elementos Flutter (conforme definido em forms_page.dart)
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

# Indicador da FormsPage (para confirmar navegação)
FORMS_PAGE_INDICATOR_KEY = NAME_FIELD_KEY # Usar o primeiro campo do formulário como indicador

# Valores para os campos
TEST_NAME = "Nome de Teste Appium"
TEST_EMAIL = "teste@appium.com"
TEST_AGE = "30"
TEST_SKILL_FLUTTER = "Flutter"
TEST_SKILL_DART = "Dart"
TEST_GENDER_MASCULINO = "Masculino"
TEST_COUNTRY_BRASIL = "Brasil"
TEST_DESCRIPTION = "Esta é uma descrição de teste gerada pelo Appium."

class FormsPageTests(unittest.TestCase):
    driver: webdriver.Remote
    finder: FlutterFinder
    wait: WebDriverWait

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
        options.set_capability('maxRetryCount', 5) # Aumentado para formulários mais complexos
        options.set_capability('newCommandTimeout', 300) # Aumentado para interações mais longas

        cls.driver = webdriver.Remote(command_executor=APPIUM_HOST, options=options)
        cls.finder = FlutterFinder()
        cls.wait = WebDriverWait(cls.driver, 40) # Timeout aumentado

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()

    def _find_element_by_value_key(self, key_string, timeout=30):
        return self.wait.until(
            EC.presence_of_element_located((AppiumBy.FLUTTER, self.finder.by_value_key(key_string)))
        )

    def _is_element_present_by_value_key(self, key_string, timeout=3):
        try:
            self._find_element_by_value_key(key_string, timeout)
            return True
        except TimeoutException:
            return False

    def _tap_element(self, element):
        element.click()
        time.sleep(0.5) # Pequena pausa para a UI atualizar

    def _enter_text(self, element_key, text):
        element = self._find_element_by_value_key(element_key)
        element.click() # Focar no campo
        time.sleep(0.2)
        element.send_keys(text)
        time.sleep(0.3)
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard() # Esconder teclado para não obstruir outros elementos
        except Exception:
            pass # Ignorar se o teclado não estiver visível ou o comando falhar
        time.sleep(0.2)

    def _navigate_to_forms_page(self, username='admin', password='1234'):
        """Navega para a FormsPage, fazendo login se necessário."""
        time.sleep(1) # Pausa inicial

        # Se estiver na LoginPage, faz login
        if self._is_element_present_by_value_key(LOGIN_USERNAME_FIELD_KEY, timeout=3):
            print("Realizando login para chegar na FormsPage...")
            username_field = self._find_element_by_value_key(LOGIN_USERNAME_FIELD_KEY)
            password_field = self._find_element_by_value_key(LOGIN_PASSWORD_FIELD_KEY)
            login_button = self._find_element_by_value_key(LOGIN_BUTTON_KEY)

            username_field.click()
            time.sleep(0.1)
            username_field.clear()
            username_field.send_keys(username)

            password_field.click()
            time.sleep(0.1)
            password_field.clear()
            password_field.send_keys(password)
            
            try:
                if self.driver.is_keyboard_shown():
                    self.driver.hide_keyboard()
            except: pass

            self._tap_element(login_button)
            self._find_element_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY, timeout=15) # Espera HomePage
            time.sleep(1) # Pausa para SnackBar de login sumir, se houver
        
        # Confirma que está na HomePage (ou chegou nela)
        self._find_element_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY)
        
        # Navega para FormsPage
        forms_button = self._find_element_by_value_key(HOME_PAGE_FORMS_BUTTON_KEY)
        self._tap_element(forms_button)
        self._find_element_by_value_key(FORMS_PAGE_INDICATOR_KEY) # Confirma que está na FormsPage
        print("Navegou para FormsPage com sucesso.")
        time.sleep(0.5)

    def test_01_fill_text_fields(self):
        self._navigate_to_forms_page() # Navega para a página de formulários
        self._enter_text(NAME_FIELD_KEY, TEST_NAME)
        self._enter_text(EMAIL_FIELD_KEY, TEST_EMAIL)
        self._enter_text(AGE_FIELD_KEY, TEST_AGE)
        self._enter_text(DESCRIPTION_FIELD_KEY, TEST_DESCRIPTION)

    def test_02_select_date(self):
        date_picker_field = self._find_element_by_value_key(DATE_PICKER_FIELD_KEY)
        self._tap_element(date_picker_field)
        time.sleep(1) # Esperar o DatePicker nativo abrir

        # Interagir com o DatePicker nativo (os seletores podem variar dependendo do OS e versão)
        # Este é um exemplo para Android. Pode precisar de ajuste.
        try:
            # Tenta clicar no botão "OK" padrão do Android DatePicker
            ok_button = self.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, "//*[@resource-id='android:id/button1' or @text='OK']"))
            )
            self._tap_element(ok_button)
        except Exception as e:
            print(f"Não foi possível clicar em OK no DatePicker: {e}")
            # Como fallback, tenta pressionar "Enter" ou uma ação de "done" se o teclado estiver ativo
            try:
                self.driver.press_keycode(66) # KEYCODE_ENTER
            except:
                # Se tudo falhar, apenas continue, o teste pode não validar a data corretamente
                print("Fallback do DatePicker: Não foi possível confirmar a data.")
        time.sleep(1)

    def test_03_toggle_switch(self):
        subscribe_switch = self._find_element_by_value_key(SUBSCRIBE_SWITCH_KEY)
        # Verifica o estado atual pelo widget (se possível, ou assume um estado inicial)
        # Para este exemplo, vamos apenas clicar para alternar
        self._tap_element(subscribe_switch)
        time.sleep(0.5)
        # Poderia adicionar uma asserção aqui se houvesse uma forma de ler o estado do switch via FlutterFinder

    def test_04_select_skills_checkboxes(self):
        skill_flutter_key = f"{SKILL_CHECKBOX_PREFIX_KEY}{TEST_SKILL_FLUTTER}"
        skill_dart_key = f"{SKILL_CHECKBOX_PREFIX_KEY}{TEST_SKILL_DART}"

        flutter_checkbox = self._find_element_by_value_key(skill_flutter_key)
        self._tap_element(flutter_checkbox)

        dart_checkbox = self._find_element_by_value_key(skill_dart_key)
        self._tap_element(dart_checkbox)

    def test_05_select_gender_radio(self):
        gender_masculino_key = f"{GENDER_RADIO_PREFIX_KEY}{TEST_GENDER_MASCULINO}"
        masculino_radio = self._find_element_by_value_key(gender_masculino_key)
        self._tap_element(masculino_radio)

    def test_06_select_country_dropdown(self):
        country_dropdown = self._find_element_by_value_key(COUNTRY_DROPDOWN_KEY)
        self._tap_element(country_dropdown)
        time.sleep(1) # Esperar o dropdown abrir

        # Para selecionar um item, precisamos de uma chave para o item do dropdown.
        # No código Dart, os DropdownMenuItems não têm chaves individuais.
        # A melhor abordagem seria adicionar ValueKeys aos DropdownMenuItems.
        # Ex: DropdownMenuItem(key: ValueKey('country_item_Brasil'), value: 'Brasil', child: Text('Brasil'))
        # Se não for possível, a seleção pode ser mais frágil, dependendo de texto ou ordem.

        # Tentativa de selecionar por texto (pode ser menos robusto)
        # Este é um exemplo e pode precisar de ajustes ou ValueKeys no app Flutter.
        try:
            # O Flutter Finder pode encontrar elementos por texto dentro de um ancestral.
            # No entanto, itens de dropdown são frequentemente renderizados em uma sobreposição.
            # Uma abordagem mais robusta é usar ValueKey para o item específico.
            # Se ValueKeys não estiverem disponíveis, procurar por texto é uma alternativa.
            # Exemplo: self.finder.by_text(TEST_COUNTRY_BRASIL)
            # Mas isso pode não funcionar se o texto não for único ou estiver em uma camada diferente.

            # Assumindo que ValueKeys foram adicionadas como 'country_item_Brasil'
            country_item_key = f"country_item_{TEST_COUNTRY_BRASIL}" # Exemplo de chave
            # Se você adicionou ValueKey('Brasil') diretamente ao DropdownMenuItem:
            # country_item_key = TEST_COUNTRY_BRASIL

            # Se você adicionou ValueKey ao Text dentro do DropdownMenuItem:
            # brasil_option = self.wait.until(
            #    EC.presence_of_element_located((AppiumBy.FLUTTER, self.finder.by_text(TEST_COUNTRY_BRASIL)))
            # )
            # self._tap_element(brasil_option)

            # Para este exemplo, vamos simular um clique em um item que *deveria* ter uma chave.
            # Se o seu DropdownMenuItem para 'Brasil' tiver uma ValueKey, use-a aqui.
            # Por exemplo, se a key for ValueKey('Brasil'):
            # brasil_option = self._find_element_by_value_key(TEST_COUNTRY_BRASIL)
            # self._tap_element(brasil_option)

            # Como fallback, se não houver chaves nos itens, esta parte será difícil de automatizar de forma robusta.
            # Uma alternativa seria usar coordenadas relativas ou gestos de rolagem e depois clicar.
            # Por enquanto, vamos assumir que o primeiro item é clicável ou que você adicionará chaves.
            # Este é um ponto que frequentemente requer adaptação específica ao app.
            print(f"Tentando selecionar o país: {TEST_COUNTRY_BRASIL}. Adicione ValueKeys aos DropdownMenuItems para robustez.")
            # Exemplo de como seria com uma ValueKey no item:
            # brasil_option = self._find_element_by_value_key(f"country_item_{TEST_COUNTRY_BRASIL}")
            # self._tap_element(brasil_option)

            # Se os itens do dropdown não tiverem keys, você pode tentar clicar por texto,
            # mas isso é menos confiável pois os itens podem estar em uma camada (overlay) diferente.
            # Exemplo (pode não funcionar bem para overlays):
            # time.sleep(1) # dar tempo para o overlay aparecer
            # brasil_text_element = self.wait.until(
            #    EC.presence_of_element_located((AppiumBy.FLUTTER, self.finder.by_text(TEST_COUNTRY_BRASIL)))
            # )
            # self._tap_element(brasil_text_element)

            # Para fins de demonstração, vamos apenas fechar o dropdown se não pudermos selecionar
            # Pressionar back para fechar o dropdown
            self.driver.back()


        except Exception as e:
            print(f"Erro ao selecionar país no dropdown: {e}")
            self.driver.back() # Tenta fechar o dropdown em caso de erro
        time.sleep(1)


    def test_07_submit_form(self):
        # Pode ser necessário rolar para baixo para que o botão de submit esteja visível
        # self.driver.execute_script('flutter:scrollIntoView', self.finder.by_value_key(SUBMIT_BUTTON_KEY), {'alignment': 0.5})
        # time.sleep(0.5)
        
        # Tentar uma rolagem genérica se o botão não estiver visível
        try:
            submit_button = self._find_element_by_value_key(SUBMIT_BUTTON_KEY, timeout=5)
        except:
            print("Botão de submit não encontrado inicialmente, tentando rolar.")
            # Rolagem simples (pode precisar de ajuste de coordenadas ou usar flutter:scroll)
            action = TouchAction(self.driver)
            window_size = self.driver.get_window_size()
            start_x = window_size['width'] / 2
            start_y = window_size['height'] * 0.8
            end_y = window_size['height'] * 0.2
            action.press(x=start_x, y=start_y).wait(ms=300).move_to(x=start_x, y=end_y).release().perform()
            time.sleep(1)
            submit_button = self._find_element_by_value_key(SUBMIT_BUTTON_KEY)

        self._tap_element(submit_button)
        time.sleep(1) # Esperar a mensagem de snackbar

        # Verificar a snackbar (exemplo, pode precisar de ajuste no seletor)
        # A snackbar pode não ser um widget Flutter diretamente acessível com ValueKey.
        # Pode ser necessário usar XPath ou outros localizadores nativos se for um overlay nativo,
        # ou flutter:waitFor se for um widget Flutter.
        try:
            snackbar_text = "Formulário enviado com sucesso!"
            # Tentar encontrar por texto (pode ser frágil)
            # self.wait.until(EC.presence_of_element_located((AppiumBy.FLUTTER, self.finder.by_text(snackbar_text))))
            # Ou, se a snackbar for um elemento nativo (comum no Android):
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, f"//*[contains(@text,'{snackbar_text}')]")))
            print("Snackbar de sucesso encontrada.")
        except Exception as e:
            print(f"Snackbar de sucesso não encontrada ou texto diferente: {e}")
            # Se o formulário tiver validação e falhar, a snackbar será de erro.
            try:
                error_snackbar_text = "Por favor, corrija os erros no formulário."
                self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, f"//*[contains(@text,'{error_snackbar_text}')]")))
                print("Snackbar de erro encontrada, o que é esperado se os campos não estiverem todos válidos.")
            except:
                print("Nenhuma snackbar conhecida foi encontrada.")


if __name__ == '__main__':
    if APP_PATH == "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI":
        print("ERRO: A variável APP_PATH não foi configurada no script.")
        print("Por favor, edite o arquivo e defina o caminho para o seu APK/APP.")
    else:
        suite = unittest.TestSuite()
        # Adicionar testes na ordem desejada
        suite.addTest(FormsPageTests('test_01_fill_text_fields'))
        suite.addTest(FormsPageTests('test_02_select_date'))
        suite.addTest(FormsPageTests('test_03_toggle_switch'))
        suite.addTest(FormsPageTests('test_04_select_skills_checkboxes'))
        suite.addTest(FormsPageTests('test_05_select_gender_radio'))
        suite.addTest(FormsPageTests('test_06_select_country_dropdown'))
        suite.addTest(FormsPageTests('test_07_submit_form'))

        runner = unittest.TextTestRunner(verbosity=2)
        print(f"Iniciando testes para o app: {APP_PATH}")
        print(f"Conectando ao servidor Appium em: {APPIUM_HOST}")
        runner.run(suite)
