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
APP_PATH = "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" # IMPORTANTE: Atualize este caminho

# --- Chaves dos Elementos Flutter (conforme login_page.dart) ---
LOGIN_PAGE_APPBAR_TITLE_KEY = 'login_page_app_bar_title' # Se houver um AppBar com título
LOGIN_USERNAME_FIELD_KEY = 'login_username_field'
LOGIN_PASSWORD_FIELD_KEY = 'login_password_field'
LOGIN_BUTTON_KEY = 'login_button'
LOGIN_FORGOT_PASSWORD_BUTTON_KEY = 'login_forgot_password_button'

# Chaves para feedback (SnackBars, AlertDialogs)
LOGIN_SNACKBAR_SUCCESS_KEY = 'login_snackbar_success' # Key do widget SnackBar em si
LOGIN_ALERT_ERROR_KEY = 'login_alert_error'           # Key do AlertDialog em si
LOGIN_ALERT_ERROR_OK_BUTTON_KEY = 'login_alert_error_ok_button'
LOGIN_SNACKBAR_FORGOT_PASSWORD_INFO_KEY = 'login_snackbar_forgot_password_info'

# Textos para validação e mensagens (ajuste conforme seu app)
TEXT_SNACKBAR_LOGIN_SUCCESS = "Login bem-sucedido!"
TEXT_ALERT_ERROR_TITLE = "Erro de Login" # Título do AlertDialog
TEXT_ALERT_ERROR_CONTENT = "Usuário ou senha incorretos."
TEXT_SNACKBAR_FORGOT_PASSWORD = "Funcionalidade \"Esqueceu a senha?\" não implementada."
TEXT_VALIDATION_USER_EMPTY = "Usuário não pode estar vazio" # Exemplo de mensagem de validação
TEXT_VALIDATION_PASSWORD_EMPTY = "Senha não pode estar vazia" # Exemplo de mensagem de validação

# Indicador da HomePage (para verificar navegação pós-login)
HOME_PAGE_INDICATOR_KEY = 'home_page_app_bar_title' # Ex: ValueKey('home_page_app_bar_title')

class LoginPageTests(unittest.TestCase):
    driver: webdriver.Remote
    wait: WebDriverWait
    finder: FlutterFinder

    @classmethod
    def setUpClass(cls):
        if APP_PATH == "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI":
            raise ValueError("Por favor, atualize a variável APP_PATH com o caminho para o seu APK/APP.")

        options = AppiumOptions()
        options.set_capability('platformName', 'Android')
        options.set_capability('automationName', 'Flutter')
        options.set_capability('deviceName', 'Android Emulator') # Substitua pelo seu dispositivo
        options.set_capability('app', APP_PATH)
        # options.set_capability('appPackage', 'com.example.seu_app') # Se app já instalado
        # options.set_capability('appActivity', '.MainActivity')   # Se app já instalado
        options.set_capability('retryBackoffTime', 500)
        options.set_capability('maxRetryCount', 3)
        options.set_capability('newCommandTimeout', 120)
        options.set_capability('noReset', True) # Para não limpar dados entre testes (opcional)

        cls.driver = webdriver.Remote(command_executor=APPIUM_HOST, options=options)
        cls.finder = FlutterFinder()
        cls.wait = WebDriverWait(cls.driver, 30) # Timeout padrão para elementos

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
        except TimeoutException: # Fallback para XPath para Snackbars/Alerts nativos
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

    def _enter_text_in_field(self, key_string, text, clear_first=True):
        element = self._find_element_by_value_key(key_string)
        if clear_first:
            element.click() # Focar para limpar
            time.sleep(0.1)
            element.clear()
        element.send_keys(text)
        time.sleep(0.2)
        if self.driver.is_keyboard_shown():
            try:
                self.driver.hide_keyboard()
            except: pass

    def _wait_for_snackbar_text(self, message_text, present=True, timeout=5):
        start_time = time.time()
        while time.time() < start_time + timeout:
            if self._is_text_present(message_text, timeout=0.2) == present:
                return
            time.sleep(0.1)
        self.fail(f"A mensagem do SnackBar '{message_text}' não ficou {'presente' if present else 'ausente'} dentro de {timeout}s.")

    def _check_flutter_alert_and_dismiss(self, alert_key, expected_title, expected_content, ok_button_key):
        self._find_element_by_value_key(alert_key) # Confirma que o diálogo está visível pela sua key
        self.assertTrue(self._is_text_present(expected_title), f"Título do alerta '{expected_title}' não encontrado.")
        self.assertTrue(self._is_text_present(expected_content), f"Conteúdo do alerta '{expected_content}' não encontrado.")
        self._tap_element(ok_button_key)
        time.sleep(0.5) # Esperar o diálogo fechar
        self.assertFalse(self._is_element_present_by_value_key(alert_key, timeout=2), "Alerta Flutter não desapareceu.")

    def test_01_initial_ui_and_empty_field_validation(self):
        print("Iniciando: test_01_initial_ui_and_empty_field_validation")
        time.sleep(2) # Espera inicial para o app carregar

        # Verifica elementos da UI
        self._find_element_by_value_key(LOGIN_USERNAME_FIELD_KEY)
        self._find_element_by_value_key(LOGIN_PASSWORD_FIELD_KEY)
        self._find_element_by_value_key(LOGIN_BUTTON_KEY)
        self._find_element_by_value_key(LOGIN_FORGOT_PASSWORD_BUTTON_KEY)
        print("Elementos da UI inicial encontrados.")

        # Tenta logar com campos vazios
        self._tap_element(LOGIN_BUTTON_KEY)
        self._wait_for_snackbar_text(TEXT_VALIDATION_USER_EMPTY, present=True)
        self._wait_for_snackbar_text(TEXT_VALIDATION_USER_EMPTY, present=False) # Espera sumir
        print("Validação de usuário vazio OK.")

        # Preenche usuário, deixa senha vazia
        self._enter_text_in_field(LOGIN_USERNAME_FIELD_KEY, "teste")
        self._tap_element(LOGIN_BUTTON_KEY)
        self._wait_for_snackbar_text(TEXT_VALIDATION_PASSWORD_EMPTY, present=True)
        self._wait_for_snackbar_text(TEXT_VALIDATION_PASSWORD_EMPTY, present=False)
        print("Validação de senha vazia OK.")
        self._enter_text_in_field(LOGIN_USERNAME_FIELD_KEY, "", clear_first=True) # Limpa campo

    def test_02_login_with_wrong_credentials(self):
        print("Iniciando: test_02_login_with_wrong_credentials")
        self._enter_text_in_field(LOGIN_USERNAME_FIELD_KEY, "usuarioerrado")
        self._enter_text_in_field(LOGIN_PASSWORD_FIELD_KEY, "senhaerrada")
        self._tap_element(LOGIN_BUTTON_KEY)

        self._check_flutter_alert_and_dismiss(
            alert_key=LOGIN_ALERT_ERROR_KEY,
            expected_title=TEXT_ALERT_ERROR_TITLE,
            expected_content=TEXT_ALERT_ERROR_CONTENT,
            ok_button_key=LOGIN_ALERT_ERROR_OK_BUTTON_KEY
        )
        print("Teste de credenciais erradas OK.")

    def test_03_login_successful(self):
        print("Iniciando: test_03_login_successful")
        self._enter_text_in_field(LOGIN_USERNAME_FIELD_KEY, "admin") # Use credenciais corretas
        self._enter_text_in_field(LOGIN_PASSWORD_FIELD_KEY, "1234")  # Use credenciais corretas
        self._tap_element(LOGIN_BUTTON_KEY)

        self._wait_for_snackbar_text(TEXT_SNACKBAR_LOGIN_SUCCESS, present=True)
        print("SnackBar de sucesso encontrado.")
        # Verifica navegação para HomePage
        self._find_element_by_value_key(HOME_PAGE_INDICATOR_KEY, timeout=15)
        print("Navegou para HomePage com sucesso.")
        self._wait_for_snackbar_text(TEXT_SNACKBAR_LOGIN_SUCCESS, present=False) # Espera sumir

    def test_04_forgot_password_link(self):
        print("Iniciando: test_04_forgot_password_link")
        # Garante que está na LoginPage (pode ter navegado no teste anterior)
        # Se o app não volta automaticamente para Login após sucesso, precisaria de um logout ou reinício.
        # Para este exemplo, vamos assumir que precisamos voltar ou que o teste pode rodar isolado.
        if not self._is_element_present_by_value_key(LOGIN_FORGOT_PASSWORD_BUTTON_KEY, timeout=2):
            self.driver.back() # Tenta voltar para a LoginPage
            time.sleep(1)
            self._find_element_by_value_key(LOGIN_FORGOT_PASSWORD_BUTTON_KEY) # Confirma que voltou

        self._tap_element(LOGIN_FORGOT_PASSWORD_BUTTON_KEY)
        self._wait_for_snackbar_text(TEXT_SNACKBAR_FORGOT_PASSWORD, present=True)
        self._wait_for_snackbar_text(TEXT_SNACKBAR_FORGOT_PASSWORD, present=False)
        print("Teste do link 'Esqueceu a senha?' OK.")

if __name__ == '__main__':
    if APP_PATH == "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI":
        print("ERRO: A variável APP_PATH não foi configurada no script.")
        print("Por favor, edite o arquivo e defina o caminho para o seu APK/APP.")
    else:
        suite = unittest.TestSuite()
        # Adicionar testes na ordem desejada para um fluxo lógico
        suite.addTest(LoginPageTests('test_01_initial_ui_and_empty_field_validation'))
        suite.addTest(LoginPageTests('test_02_login_with_wrong_credentials'))
        suite.addTest(LoginPageTests('test_03_login_successful'))
        suite.addTest(LoginPageTests('test_04_forgot_password_link'))

        runner = unittest.TextTestRunner(verbosity=2)
        print(f"Iniciando testes de Login para o app: {APP_PATH}")
        print(f"Conectando ao servidor Appium em: {APPIUM_HOST}")
        runner.run(suite)
        try:
            username_field = self.find_element_with_retry(AppiumBy.ACCESSIBILITY_ID, "Usuário")
        except: # Tentar XPath se ACCESSIBILITY_ID não funcionar
            print("ACCESSIBILITY_ID 'Usuário' não encontrado, tentando XPath...")
            # Este XPath é um exemplo e pode precisar de ajuste:
            username_field = self.find_element_with_retry(AppiumBy.XPATH, "//*[@text='Usuário']")


        print("Localizando campo de senha...")
        try:
            password_field = self.find_element_with_retry(AppiumBy.ACCESSIBILITY_ID, "Senha")
        except:
            print("ACCESSIBILITY_ID 'Senha' não encontrado, tentando XPath...")
            password_field = self.find_element_with_retry(AppiumBy.XPATH, "//*[@text='Senha']")

        print("Localizando botão de login...")
        # O ElevatedButton com child: Text('Entrar') deve ter 'Entrar' como 'name' ou 'text'
        login_button = self.find_element_with_retry(AppiumBy.XPATH, "//*[@text='Entrar']")
        # Ou, se o Semantics(label=...) no ElevatedButton estivesse ativo:
        # login_button = self.find_element_with_retry(AppiumBy.ACCESSIBILITY_ID, "Botão para efetuar login")


        # 2. Digitar nos campos
        print("Digitando usuário...")
        username_field.send_keys("admin")
        print("Digitando senha...")
        password_field.send_keys("1234")

        # 3. Clicar no botão de login
        print("Clicando no botão de login...")
        login_button.click()

        # 4. Verificar o SnackBar de sucesso
        # O SnackBar tem a key 'login_snackbar_success'
        # Com Appium Flutter Driver: self.find_element_with_retry(AppiumBy.FLUTTER, 'login_snackbar_success')
        # Sem ele, o texto do SnackBar é a melhor aposta.
        print("Verificando SnackBar de sucesso...")
        success_message = self.find_element_with_retry(AppiumBy.XPATH, "//*[@text='Login bem-sucedido!']")
        self.assertTrue(success_message.is_displayed(), "Mensagem de sucesso do login não encontrada.")
        print("Teste de login bem-sucedido CONCLUÍDO.")

        # Opcional: Verificar navegação para HomePage (se houver um elemento único lá)
        # home_page_element = self.find_element_with_retry(AppiumBy.XPATH, "//*[@text='Bem-vindo à HomePage!']") # Exemplo
        # self.assertTrue(home_page_element.is_displayed(), "Não navegou para a HomePage.")


    def test_failed_login_wrong_credentials(self):
        print("\nIniciando teste: test_failed_login_wrong_credentials")

        # 1. Encontrar campos e botão de login (similar ao teste anterior)
        print("Localizando campo de usuário...")
        try:
            username_field = self.find_element_with_retry(AppiumBy.ACCESSIBILITY_ID, "Usuário")
        except:
            username_field = self.find_element_with_retry(AppiumBy.XPATH, "//*[@text='Usuário']")

        print("Localizando campo de senha...")
        try:
            password_field = self.find_element_with_retry(AppiumBy.ACCESSIBILITY_ID, "Senha")
        except:
            password_field = self.find_element_with_retry(AppiumBy.XPATH, "//*[@text='Senha']")

        print("Localizando botão de login...")
        login_button = self.find_element_with_retry(AppiumBy.XPATH, "//*[@text='Entrar']")

        # 2. Digitar credenciais erradas
        print("Digitando usuário errado...")
        username_field.send_keys("usuarioerrado")
        print("Digitando senha errada...")
        password_field.send_keys("senhaerrada")

        # 3. Clicar no botão de login
        print("Clicando no botão de login...")
        login_button.click()

        # 4. Verificar o AlertDialog de erro
        # O AlertDialog tem a key 'login_alert_error'
        # O título é 'Erro de Login', conteúdo 'Usuário ou senha incorretos.'
        print("Verificando AlertDialog de erro...")
        error_dialog_message = self.find_element_with_retry(AppiumBy.XPATH, "//*[@text='Usuário ou senha incorretos.']")
        self.assertTrue(error_dialog_message.is_displayed(), "Mensagem de erro do AlertDialog não encontrada.")

        # 5. Clicar no botão OK do AlertDialog
        # O botão OK tem o tooltip 'Confirmar erro de login'
        # E a key 'login_alert_error_ok_button'
        print("Localizando botão OK do AlertDialog...")
        # Priorizar ACCESSIBILITY_ID se o tooltip for exposto assim
        try:
            ok_button = self.find_element_with_retry(AppiumBy.ACCESSIBILITY_ID, "Confirmar erro de login")
        except: # Fallback para o texto do botão
            print("ACCESSIBILITY_ID 'Confirmar erro de login' não encontrado, tentando por texto 'OK'...")
            ok_button = self.find_element_with_retry(AppiumBy.XPATH, "//*[@text='OK']")

        print("Clicando no botão OK...")
        ok_button.click()

        # 6. Verificar se o AlertDialog desapareceu (opcional, mas bom)
        # Tentar encontrar o elemento de erro novamente deve falhar ou não ser visível
        time.sleep(1) # Pequena espera para o dialog fechar
        try:
            self.driver.find_element(AppiumBy.XPATH, "//*[@text='Usuário ou senha incorretos.']")
            dialog_still_present = True
        except:
            dialog_still_present = False
        self.assertFalse(dialog_still_present, "AlertDialog de erro não fechou.")
        print("Teste de login com falha CONCLUÍDO.")


    def test_forgot_password_link(self):
        print("\nIniciando teste: test_forgot_password_link")

        # 1. Encontrar o link "Esqueceu a senha?"
        # Tem o tooltip 'Recuperar senha esquecida'
        # E a key 'login_forgot_password_button'
        print("Localizando link 'Esqueceu a senha?'...")
        try:
            forgot_password_button = self.find_element_with_retry(AppiumBy.ACCESSIBILITY_ID, "Recuperar senha esquecida")
        except:
            print("ACCESSIBILITY_ID 'Recuperar senha esquecida' não encontrado, tentando por texto...")
            forgot_password_button = self.find_element_with_retry(AppiumBy.XPATH, "//*[@text='Esqueceu a senha?']")


        # 2. Clicar no link
        print("Clicando no link 'Esqueceu a senha?'...")
        forgot_password_button.click()

        # 3. Verificar o SnackBar informativo
        # O SnackBar tem a key 'login_snackbar_forgot_password_info'
        print("Verificando SnackBar de 'Esqueceu a senha?'...")
        info_snackbar = self.find_element_with_retry(AppiumBy.XPATH, "//*[@text='Funcionalidade \"Esqueceu a senha?\" não implementada.']")
        self.assertTrue(info_snackbar.is_displayed(), "SnackBar de 'Esqueceu a senha?' não encontrado.")
        print("Teste do link 'Esqueceu a senha?' CONCLUÍDO.")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(LoginPageTests("test_successful_login"))
    suite.addTest(LoginPageTests("test_failed_login_wrong_credentials"))
    suite.addTest(LoginPageTests("test_forgot_password_link"))

    runner = unittest.TextTestRunner()
    runner.run(suite)


#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

# ...
#wait = WebDriverWait(self.driver, 20)
#success_message = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[@text='Login bem-sucedido!']")))

#from appium_flutter_finder.flutter_finder import FlutterElement, FlutterFinder # Importar

# ... dentro da classe de teste ...
#finder = FlutterFinder()

# Exemplo de localização por Key do Flutter:
#username_field_by_key = FlutterElement(self.driver, finder.by_value_key('login_username_field'))
#username_field_by_key.send_keys("admin_com_flutter_key")

# Por Tooltip:
#forgot_password_by_tooltip = FlutterElement(self.driver, finder.by_tooltip('Recuperar senha esquecida'))
#forgot_password_by_tooltip.click()