import unittest
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy # Para AppiumBy.ACCESSIBILITY_ID, etc.

# --- Configurações ---
# Atualize estas capabilities com as informações do seu ambiente/app
DESIRED_CAPABILITIES = {
    "platformName": "Android",
    "appium:platformVersion": "12.0",  # Versão do seu Android (ex: "11.0", "12.0")
    "appium:deviceName": "emulator-5554",  # Nome do seu dispositivo/emulador (veja 'adb devices')
    "appium:automationName": "UiAutomator2", # Ou "Flutter" se estiver usando appium-flutter-driver
    "appium:appPackage": "com.example.seu_app", # Substitua pelo seu package name
    "appium:appActivity": ".MainActivity",    # Substitua pela sua activity principal
    # "appium:app": "/caminho/para/seu/app.apk", # Opcional: se o app não estiver instalado
    "appium:noReset": True, # Para não reinstalar/limpar dados do app a cada sessão
    "appium:ensureWebviewsHavePages": True,
    "appium:nativeWebScreenshot": True,
    "appium:newCommandTimeout": 3600,
    "appium:connectHardwareKeyboard": True
}

APPIUM_SERVER_URL = "http://localhost:4723" # URL padrão do servidor Appium

class LoginPageTests(unittest.TestCase):

    def setUp(self):
        """Configura o driver antes de cada teste."""
        self.driver = webdriver.Remote(command_executor=APPIUM_SERVER_URL, desired_capabilities=DESIRED_CAPABILITIES)
        self.driver.implicitly_wait(10) # Espera implícita para elementos

    def tearDown(self):
        """Encerra o driver após cada teste."""
        if self.driver:
            self.driver.quit()

    def find_element_with_retry(self, by, value, retries=3, delay=2):
        """Tenta encontrar um elemento com algumas tentativas."""
        for i in range(retries):
            try:
                element = self.driver.find_element(by, value)
                return element
            except Exception as e:
                print(f"Tentativa {i+1} falhou ao encontrar o elemento ({by}: {value}). Erro: {e}")
                if i < retries - 1:
                    time.sleep(delay)
                else:
                    raise # Levanta a exceção na última tentativa
        return None


    def test_successful_login(self):
        print("\nIniciando teste: test_successful_login")

        # 1. Encontrar campos e botão de login
        # Para TextFormFields, o 'labelText' pode ser o accessibility_id
        # Ou se você tiver uma 'key' e usar appium-flutter-driver, seria melhor.
        # Por enquanto, vamos tentar pelo que o Flutter expõe como acessibilidade.
        # No Flutter, o 'labelText' de um TextFormField geralmente se torna o 'content-desc'
        # ou 'text' do elemento pai ou um TextView irmão no Android nativo.
        # O Appium Inspector é seu melhor amigo aqui para confirmar.

        print("Localizando campo de usuário...")
        # username_field = self.find_element_with_retry(AppiumBy.ACCESSIBILITY_ID, "Usuário") # Se 'labelText' for o acc id
        # Se 'labelText' não funcionar como ACCESSIBILITY_ID direto, você pode precisar de XPath
        # ou esperar que o Appium Flutter Driver use a 'key' do Flutter.
        # Vamos assumir que a 'key' que definimos no Flutter para os campos ('login_username_field')
        # é exposta como 'resource-id' ou 'accessibility_id' (pode precisar de ajuste)
        # Se você definiu uma Key no Flutter como `ValueKey('login_username_field')`,
        # o Appium Flutter Driver a encontraria com `driver.find_element(AppiumBy.FLUTTER, 'login_username_field')`.
        # Sem o Flutter Driver, você precisa ver como essa Key é renderizada nativamente.
        # Frequentemente, para TextFields, o `labelText` é a melhor aposta para ACCESSIBILITY_ID.
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