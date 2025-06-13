# d:\repos\appium_and_flutter_test\integration_test\home_page_test.py
import unittest
import time
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- INÍCIO: PLACEHOLDERS DE LOCALIZADORES ---
# !!! IMPORTANTE: Substitua estes placeholders pelos localizadores REAIS do seu app Flutter !!!
# Use Appium Inspector para encontrá-los. Flutter Keys geralmente são accessibility_id.

# LoginPage (assumindo IDs do exemplo anterior ou similares)
LOC_LOGIN_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "usernameField_LoginPage_ACCESSIBILITY_ID") # Elemento único da LoginPage
LOC_USERNAME_FIELD = (AppiumBy.ACCESSIBILITY_ID, "usernameField") # LoginPage.usernameFieldKey
LOC_PASSWORD_FIELD = (AppiumBy.ACCESSIBILITY_ID, "passwordField") # LoginPage.passwordFieldKey
LOC_LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "loginButton")     # LoginPage.loginButtonKey

# HomePage
LOC_HOME_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "homePageElement_HomePage_ACCESSIBILITY_ID") # Um elemento único da HomePage
LOC_HOME_PAGE_APPBAR_TITLE = (AppiumBy.XPATH, "//*[contains(@text, 'Menu Principal')]") # Ou um ID específico se houver
LOC_FORMS_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "homePage.formsButtonKey_ACCESSIBILITY_ID")
LOC_LISTVIEW_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "homePage.listViewButtonKey_ACCESSIBILITY_ID")
LOC_NATIVE_RESOURCES_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "homePage.nativeResourcesButtonKey_ACCESSIBILITY_ID")
LOC_GESTURES_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "homePage.gesturesButtonKey_ACCESSIBILITY_ID")
LOC_CLICK_AND_HOLD_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "homePage.clickAndHoldButtonKey_ACCESSIBILITY_ID")
LOC_CHAT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "homePage.chatButtonKey_ACCESSIBILITY_ID")
LOC_LOGOUT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "homePage.logoutButtonKey_ACCESSIBILITY_ID")

# Logout Dialog
LOC_LOGOUT_DIALOG_KEY = (AppiumBy.ACCESSIBILITY_ID, "homePage.logoutDialogKey_ACCESSIBILITY_ID")
LOC_LOGOUT_DIALOG_TITLE = (AppiumBy.XPATH, "//*[contains(@text, 'Confirmar Logout')]") # Ou ID
LOC_LOGOUT_DIALOG_CANCEL_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "homePage.logoutDialogCancelButtonKey_ACCESSIBILITY_ID")
LOC_LOGOUT_DIALOG_CONFIRM_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "homePage.logoutDialogConfirmButtonKey_ACCESSIBILITY_ID")

# Indicadores de Página (um elemento único para cada página de destino)
LOC_FORMS_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "formsPage_UniqueElement_ACCESSIBILITY_ID")
LOC_LISTVIEW_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "listViewPage.listViewKey_ACCESSIBILITY_ID") # Reutilizando do teste anterior
LOC_RECURSOS_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "recursosPage.imageDisplayAreaKey_ACCESSIBILITY_ID") # Reutilizando
LOC_GESTOS_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "gestosPage_UniqueElement_ACCESSIBILITY_ID")
LOC_CLICK_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "clickPage_UniqueElement_ACCESSIBILITY_ID")
LOC_CHAT_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "chatPage_UniqueElement_ACCESSIBILITY_ID")

# Template XPath para encontrar elementos por texto
XPATH_TEXT_CONTAINS_TEMPLATE = "//*[contains(@text, \"{text}\") or contains(@content-desc, \"{text}\") or contains(@name, \"{text}\") or contains(@label, \"{text}\")]"
# --- FIM: PLACEHOLDERS DE LOCALIZADORES ---

class HomePageTests(unittest.TestCase):
    driver: webdriver.Remote
    wait: WebDriverWait

    DEFAULT_WAIT_TIMEOUT = 10
    SHORT_WAIT_TIMEOUT = 3
    LONG_WAIT_TIMEOUT = 20

    CAPABILITIES = dict(
        platformName='Android',
        deviceName='emulator-5554',
        appPackage='com.example.appium_and_flutter_test',
        appActivity='.MainActivity',
        automationName='UiAutomator2',
        # noReset=True # Para desenvolvimento, evita reinstalar
    )
    APPIUM_SERVER_URL = 'http://localhost:4723'

    def setUp(self):
        options = AppiumOptions().load_capabilities(self.CAPABILITIES)
        self.driver = webdriver.Remote(self.APPIUM_SERVER_URL, options=options)
        self.wait = WebDriverWait(self.driver, self.DEFAULT_WAIT_TIMEOUT)

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    # --- Helper Methods ---
    def _is_element_present(self, locator, timeout=SHORT_WAIT_TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def _find_element_with_wait(self, locator, timeout=DEFAULT_WAIT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def _click_element_with_wait(self, locator, timeout=DEFAULT_WAIT_TIMEOUT):
        element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()

    def _type_text_with_wait(self, locator, text, timeout=DEFAULT_WAIT_TIMEOUT, clear_first=True):
        element = self._find_element_with_wait(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def _navigate_back(self):
        """Tenta navegar para trás usando o botão de voltar do sistema."""
        self.driver.back()
        time.sleep(0.5) # Pequena pausa para a navegação completar

    def _ensure_on_home_page(self, username='flutter', password='123456'):
        """Garante que o app esteja logado e na HomePage."""
        time.sleep(1) # Pausa inicial

        # Se estiver na LoginPage, faz login
        if self._is_element_present(LOC_LOGIN_PAGE_INDICATOR, timeout=self.SHORT_WAIT_TIMEOUT):
            self._type_text_with_wait(LOC_USERNAME_FIELD, username)
            self._type_text_with_wait(LOC_PASSWORD_FIELD, password)
            self._click_element_with_wait(LOC_LOGIN_BUTTON)
            # Espera pela HomePage após o login
            self._find_element_with_wait(LOC_HOME_PAGE_INDICATOR, timeout=self.LONG_WAIT_TIMEOUT)
            time.sleep(1) # Pausa para SnackBar de login sumir, se houver
        else:
            # Se não estiver na LoginPage, tenta voltar para a HomePage caso esteja em outra tela
            max_pops = 5 # Evita loop infinito
            pops = 0
            while not self._is_element_present(LOC_HOME_PAGE_INDICATOR, timeout=1) and pops < max_pops:
                # Verifica se é possível voltar (ex: não estamos na tela raiz absoluta)
                # Esta é uma heurística, pode precisar de ajuste.
                # Se o app fechar ao invés de voltar, esta lógica precisa ser mais robusta.
                current_activity = self.driver.current_activity
                self._navigate_back()
                time.sleep(0.5)
                if self.driver.current_activity == current_activity and not self._is_element_present(LOC_HOME_PAGE_INDICATOR, timeout=0.5):
                    # Não conseguiu voltar efetivamente ou já está na raiz e não é a home
                    break
                pops += 1

        self.assertTrue(self._is_element_present(LOC_HOME_PAGE_INDICATOR, timeout=self.SHORT_WAIT_TIMEOUT),
                        "Não foi possível alcançar a HomePage.")
        time.sleep(0.5)


    def _navigate_to_section_and_back(self, button_locator, page_indicator_locator, section_name):
        """Clica em um botão, verifica a navegação e volta."""
        self._click_element_with_wait(button_locator)
        self._find_element_with_wait(page_indicator_locator, timeout=self.LONG_WAIT_TIMEOUT)
        print(f"Navegou para {section_name} com sucesso.")
        self._navigate_back()
        self._find_element_with_wait(LOC_HOME_PAGE_INDICATOR) # Confirma retorno à HomePage
        print(f"Retornou para HomePage de {section_name} com sucesso.")


    # --- Test Methods ---
    def test_ui_elements_and_navigation(self):
        self._ensure_on_home_page()

        # Verifica título do AppBar
        self._find_element_with_wait(LOC_HOME_PAGE_APPBAR_TITLE)
        print("Título 'Menu Principal' encontrado.")

        # Navegações
        self._navigate_to_section_and_back(LOC_FORMS_BUTTON, LOC_FORMS_PAGE_INDICATOR, "Formulários")
        self._navigate_to_section_and_back(LOC_LISTVIEW_BUTTON, LOC_LISTVIEW_PAGE_INDICATOR, "ListView")
        self._navigate_to_section_and_back(LOC_NATIVE_RESOURCES_BUTTON, LOC_RECURSOS_PAGE_INDICATOR, "Recursos Nativos")
        self._navigate_to_section_and_back(LOC_GESTURES_BUTTON, LOC_GESTOS_PAGE_INDICATOR, "Gestos na Tela")
        self._navigate_to_section_and_back(LOC_CLICK_AND_HOLD_BUTTON, LOC_CLICK_PAGE_INDICATOR, "Clicar e Segurar")
        self._navigate_to_section_and_back(LOC_CHAT_BUTTON, LOC_CHAT_PAGE_INDICATOR, "Chat Simulado")

        # Verifica se voltou para a HomePage no final
        self.assertTrue(self._is_element_present(LOC_HOME_PAGE_INDICATOR),
                        "Não retornou à HomePage após todas as navegações.")
        print("Teste de navegação concluído.")

    def test_logout_functionality(self):
        self._ensure_on_home_page()

        # 1. Tenta Logout e Cancela
        self._click_element_with_wait(LOC_LOGOUT_BUTTON)
        self._find_element_with_wait(LOC_LOGOUT_DIALOG_KEY)
        self._find_element_with_wait(LOC_LOGOUT_DIALOG_TITLE)
        print("Diálogo de logout aberto.")

        self._click_element_with_wait(LOC_LOGOUT_DIALOG_CANCEL_BUTTON)
        # Espera o diálogo desaparecer
        WebDriverWait(self.driver, self.DEFAULT_WAIT_TIMEOUT).until(
            EC.invisibility_of_element_located(LOC_LOGOUT_DIALOG_KEY)
        )
        print("Logout cancelado, diálogo fechado.")

        self.assertTrue(self._is_element_present(LOC_HOME_PAGE_INDICATOR),
                        "Deveria permanecer na HomePage após cancelar o logout.")

        # 2. Tenta Logout e Confirma
        self._click_element_with_wait(LOC_LOGOUT_BUTTON)
        self._find_element_with_wait(LOC_LOGOUT_DIALOG_KEY)
        print("Diálogo de logout reaberto.")

        self._click_element_with_wait(LOC_LOGOUT_DIALOG_CONFIRM_BUTTON)
        # Espera a navegação para LoginPage
        self._find_element_with_wait(LOC_LOGIN_PAGE_INDICATOR, timeout=self.LONG_WAIT_TIMEOUT)
        print("Logout confirmado, navegou para LoginPage.")

        self.assertFalse(self._is_element_present(LOC_HOME_PAGE_INDICATOR, timeout=1),
                         "HomePage ainda está presente após o logout.")
        print("Teste de logout concluído.")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HomePageTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

