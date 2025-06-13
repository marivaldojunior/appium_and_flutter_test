# d:\repos\appium_and_flutter_test\integration_test\click_page_test.py
import unittest
import time
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

# --- INÍCIO: PLACEHOLDERS DE LOCALIZADORES ---
# !!! IMPORTANTE: Substitua estes placeholders pelos localizadores REAIS do seu app Flutter !!!

# LoginPage (assumindo IDs de exemplos anteriores)
LOC_LOGIN_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "usernameField_LoginPage_ACCESSIBILITY_ID")
LOC_USERNAME_FIELD = (AppiumBy.ACCESSIBILITY_ID, "usernameField")
LOC_PASSWORD_FIELD = (AppiumBy.ACCESSIBILITY_ID, "passwordField")
LOC_LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "loginButton")

# HomePage (assumindo IDs de exemplos anteriores)
LOC_HOME_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "homePageElement_HomePage_ACCESSIBILITY_ID")
LOC_CLICK_AND_HOLD_BUTTON_ON_HOME = (AppiumBy.ACCESSIBILITY_ID, "homePage.clickAndHoldButtonKey_ACCESSIBILITY_ID") # Do home_page_test

# ClickPage
LOC_CLICK_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "clickPage_UniqueElement_ACCESSIBILITY_ID") # Um elemento único da ClickPage
LOC_DOUBLE_TAP_CARD = (AppiumBy.ACCESSIBILITY_ID, "clickPage.doubleTapCardKey_ACCESSIBILITY_ID")
LOC_LONG_PRESS_CARD = (AppiumBy.ACCESSIBILITY_ID, "clickPage.longPressCardKey_ACCESSIBILITY_ID")

# AlertDialog (se os Keys forem expostos ou se for um widget customizado)
# Se for um alerta nativo, a interação é diferente (driver.switch_to.alert)
LOC_ALERT_DIALOG_GENERIC = (AppiumBy.ACCESSIBILITY_ID, "clickPage.alertDialogKey_ACCESSIBILITY_ID") # Key do AlertDialog
LOC_ALERT_DIALOG_OK_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "clickPage.alertDialogOkButtonKey_ACCESSIBILITY_ID") # Key do botão OK

# Textos dentro do AlertDialog (para verificação)
TEXT_ALERT_DOUBLE_TAP_TITLE = "Duplo Clique!"
TEXT_ALERT_DOUBLE_TAP_CONTENT = "Você clicou duas vezes neste card."
TEXT_ALERT_LONG_PRESS_TITLE = "Clique Longo!"
TEXT_ALERT_LONG_PRESS_CONTENT = "Você pressionou e segurou este card."

XPATH_TEXT_CONTAINS_TEMPLATE = "//*[contains(@text, \"{text}\") or contains(@content-desc, \"{text}\") or contains(@name, \"{text}\") or contains(@label, \"{text}\")]"
# --- FIM: PLACEHOLDERS DE LOCALIZADORES ---

class ClickPageTests(unittest.TestCase):
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
    def _is_element_present(self, locator, timeout=SHORT_WAIT_TIMEOUT, context=None):
        source = context or self.driver
        try:
            WebDriverWait(source, timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def _find_element_with_wait(self, locator, timeout=DEFAULT_WAIT_TIMEOUT, context=None):
        source = context or self.driver
        return WebDriverWait(source, timeout).until(EC.presence_of_element_located(locator))

    def _click_element_with_wait(self, locator, timeout=DEFAULT_WAIT_TIMEOUT, context=None):
        source = context or self.driver
        element = WebDriverWait(source, timeout).until(EC.element_to_be_clickable(locator))
        element.click()

    def _type_text_with_wait(self, locator, text, timeout=DEFAULT_WAIT_TIMEOUT, context=None, clear_first=True):
        source = context or self.driver
        element = self._find_element_with_wait(locator, timeout, context=source)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def _wait_for_text_visibility(self, text_content, visible=True, timeout=DEFAULT_WAIT_TIMEOUT, context=None):
        source = context or self.driver
        locator = (AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=text_content))
        try:
            if visible:
                WebDriverWait(source, timeout).until(EC.visibility_of_element_located(locator))
            else:
                WebDriverWait(source, timeout).until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            action = "aparecer" if visible else "desaparecer"
            self.fail(f"Timeout esperando o texto '{text_content}' {action}.")

    def _perform_double_tap(self, element):
        """Realiza um duplo toque em um elemento."""
        # Opção 1: Usando tap com count (se suportado e funcionar bem com Flutter)
        # self.driver.execute_script('mobile: doubleClickGesture', {'elementId': element.id}) # Exemplo para iOS com XCUITest
        # Para Android com UiAutomator2, pode ser mais complexo ou usar TouchAction

        # Opção 2: TouchAction (mais genérico)
        action = TouchAction(self.driver)
        action.tap(element).wait(100).tap(element).perform() # Toque, pequena espera, toque
        time.sleep(0.5) # Pausa para UI reagir

    def _perform_long_press(self, element, duration_ms=1000):
        """Realiza um clique longo em um elemento."""
        action = TouchAction(self.driver)
        action.long_press(element, duration=duration_ms).release().perform()
        time.sleep(0.5) # Pausa para UI reagir

    def _handle_alert_if_present(self, accept=True, expected_title=None, expected_content=None):
        """Verifica e interage com um alerta nativo, ou um diálogo Flutter com locators."""
        try:
            # Tenta primeiro como alerta nativo
            WebDriverWait(self.driver, self.SHORT_WAIT_TIMEOUT).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            print(f"Alerta nativo encontrado: {alert.text}")
            if expected_title:
                self.assertIn(expected_title, alert.text, "Título do alerta nativo não corresponde.")
            if expected_content: # Conteúdo pode ser parte do texto principal do alerta nativo
                self.assertIn(expected_content, alert.text, "Conteúdo do alerta nativo não corresponde.")
            
            if accept:
                alert.accept()
            else:
                alert.dismiss()
            time.sleep(0.5)
            return True # Alerta nativo tratado
        except (TimeoutException, NoAlertPresentException):
            # Se não for alerta nativo, tenta como diálogo Flutter
            if self._is_element_present(LOC_ALERT_DIALOG_GENERIC, timeout=self.SHORT_WAIT_TIMEOUT):
                print("Diálogo Flutter (baseado em LOC_ALERT_DIALOG_GENERIC) encontrado.")
                if expected_title:
                    self._wait_for_text_visibility(expected_title, context=self._find_element_with_wait(LOC_ALERT_DIALOG_GENERIC))
                if expected_content:
                    self._wait_for_text_visibility(expected_content, context=self._find_element_with_wait(LOC_ALERT_DIALOG_GENERIC))
                
                if accept:
                    self._click_element_with_wait(LOC_ALERT_DIALOG_OK_BUTTON, context=self._find_element_with_wait(LOC_ALERT_DIALOG_GENERIC))
                else:
                    # Implementar lógica para botão de cancelar se houver
                    self.fail("Lógica de 'dismiss' para diálogo Flutter não implementada neste helper.")
                time.sleep(0.5)
                return True # Diálogo Flutter tratado
        return False # Nenhum alerta/diálogo encontrado ou tratado


    def _navigate_to_click_page(self, username='admin', password='1234'):
        """Faz login (se necessário) e navega para a ClickPage."""
        time.sleep(1)

        if self._is_element_present(LOC_LOGIN_PAGE_INDICATOR, timeout=self.SHORT_WAIT_TIMEOUT):
            self._type_text_with_wait(LOC_USERNAME_FIELD, username)
            self._type_text_with_wait(LOC_PASSWORD_FIELD, password)
            self._click_element_with_wait(LOC_LOGIN_BUTTON)
            self._find_element_with_wait(LOC_HOME_PAGE_INDICATOR, timeout=self.LONG_WAIT_TIMEOUT)
            time.sleep(1)

        self.assertTrue(self._is_element_present(LOC_HOME_PAGE_INDICATOR), "Não foi possível alcançar a HomePage.")
        self._click_element_with_wait(LOC_CLICK_AND_HOLD_BUTTON_ON_HOME)
        self._find_element_with_wait(LOC_CLICK_PAGE_INDICATOR, timeout=self.LONG_WAIT_TIMEOUT) # Espera um elemento único da ClickPage
        time.sleep(0.5)

    # --- Test Method ---
    def test_click_interactions(self):
        self._navigate_to_click_page()

        # Garante que está na ClickPage (verificado em _navigate_to_click_page)
        self.assertTrue(self._is_element_present(LOC_CLICK_PAGE_INDICATOR), "ClickPage não foi carregada.")

        # --- Teste do Card de Duplo Clique ---
        double_tap_card = self._find_element_with_wait(LOC_DOUBLE_TAP_CARD)
        self.assertIsNotNone(double_tap_card, "Card de duplo clique não encontrado")

        self._perform_double_tap(double_tap_card)
        
        alert_handled_double_tap = self._handle_alert_if_present(
            accept=True,
            expected_title=TEXT_ALERT_DOUBLE_TAP_TITLE,
            expected_content=TEXT_ALERT_DOUBLE_TAP_CONTENT
        )
        self.assertTrue(alert_handled_double_tap, "Alerta/Diálogo de duplo clique não apareceu ou não foi tratado.")
        
        # Verifica se o AlertDialog (se for Flutter dialog) desapareceu
        if not (isinstance(alert_handled_double_tap, bool) and alert_handled_double_tap and EC.alert_is_present()(self.driver) is False): # Se foi alerta nativo, já sumiu
             self.assertFalse(self._is_element_present(LOC_ALERT_DIALOG_GENERIC, timeout=1),
                             "Diálogo Flutter de duplo clique não desapareceu.")
        print("Teste de duplo clique concluído.")

        # --- Teste do Card de Clique Longo ---
        long_press_card = self._find_element_with_wait(LOC_LONG_PRESS_CARD)
        self.assertIsNotNone(long_press_card, "Card de clique longo não encontrado")

        self._perform_long_press(long_press_card)

        alert_handled_long_press = self._handle_alert_if_present(
            accept=True,
            expected_title=TEXT_ALERT_LONG_PRESS_TITLE,
            expected_content=TEXT_ALERT_LONG_PRESS_CONTENT
        )
        self.assertTrue(alert_handled_long_press, "Alerta/Diálogo de clique longo não apareceu ou não foi tratado.")

        if not (isinstance(alert_handled_long_press, bool) and alert_handled_long_press and EC.alert_is_present()(self.driver) is False):
            self.assertFalse(self._is_element_present(LOC_ALERT_DIALOG_GENERIC, timeout=1),
                             "Diálogo Flutter de clique longo não desapareceu.")
        print("Teste de clique longo concluído.")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ClickPageTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
