# d:\repos\appium_and_flutter_test\integration_test\recursos_page_test.py
import unittest
from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# --- INÍCIO: PLACEHOLDERS DE LOCALIZADORES ---
# Substitua estes placeholders pelos localizadores reais do seu app.
# É comum que Flutter Keys sejam expostas como accessibility_id.

# LoginPage (assumindo IDs do exemplo anterior ou similares)
LOC_LOGIN_PAGE_INDICATOR = (By.ACCESSIBILITY_ID, "usernameField") # Elemento único da LoginPage
LOC_USERNAME_FIELD = (By.ACCESSIBILITY_ID, "usernameField")
LOC_PASSWORD_FIELD = (By.ACCESSIBILITY_ID, "passwordField")
LOC_LOGIN_BUTTON = (By.ACCESSIBILITY_ID, "loginButton")

# HomePage
LOC_HOME_PAGE_INDICATOR = (By.ACCESSIBILITY_ID, "homePageElement") # Elemento único da HomePage
# O ID para 'HomePage.nativeResourcesButtonKey' precisa ser descoberto
LOC_NATIVE_RESOURCES_BUTTON = (By.ACCESSIBILITY_ID, "homePage.nativeResourcesButtonKey_ACCESSIBILITY_ID")

# RecursosPage
# O ID para 'RecursosPage.imageDisplayAreaKey'
LOC_RECURSOS_PAGE_INDICATOR = (By.ACCESSIBILITY_ID, "recursosPage.imageDisplayAreaKey_ACCESSIBILITY_ID")
LOC_IMAGE_DISPLAY_AREA = (By.ACCESSIBILITY_ID, "recursosPage.imageDisplayAreaKey_ACCESSIBILITY_ID")
# O ID para o ícone 'Icons.image_search'
LOC_IMAGE_SEARCH_ICON = (By.ACCESSIBILITY_ID, "recursosPage.imageSearchIcon_ACCESSIBILITY_ID")
LOC_OPEN_CAMERA_BUTTON = (By.ACCESSIBILITY_ID, "recursosPage.openCameraButtonKey_ACCESSIBILITY_ID")
LOC_OPEN_GALLERY_BUTTON = (By.ACCESSIBILITY_ID, "recursosPage.openGalleryButtonKey_ACCESSIBILITY_ID")
LOC_SELECT_IMAGE_BUTTON = (By.ACCESSIBILITY_ID, "recursosPage.selectImageButtonKey_ACCESSIBILITY_ID")
LOC_REMOVE_IMAGE_BUTTON = (By.ACCESSIBILITY_ID, "recursosPage.removeImageButtonKey_ACCESSIBILITY_ID")
LOC_IMAGE_SOURCE_SHEET = (By.ACCESSIBILITY_ID, "recursosPage.imageSourceSheetKey_ACCESSIBILITY_ID")
LOC_IMAGE_SOURCE_SHEET_GALLERY = (By.ACCESSIBILITY_ID, "recursosPage.imageSourceSheetGalleryOptionKey_ACCESSIBILITY_ID")
LOC_IMAGE_SOURCE_SHEET_CAMERA = (By.ACCESSIBILITY_ID, "recursosPage.imageSourceSheetCameraOptionKey_ACCESSIBILITY_ID")

# Textos para SnackBars/mensagens (usados em XPaths)
TEXT_NENHUMA_IMAGEM_SELECIONADA = "Nenhuma imagem selecionada" # Exatamente como no app
TEXT_NENHUMA_IMAGEM_TIRADA = "Nenhuma imagem tirada."     # Exatamente como no app

# Template XPath para encontrar elementos por texto (ajuste se necessário para iOS/Android)
XPATH_TEXT_CONTAINS_TEMPLATE = "//*[contains(@text, '{text}') or contains(@content-desc, '{text}') or contains(@name, '{text}')]"
# --- FIM: PLACEHOLDERS DE LOCALIZADORES ---


class RecursosPageTests(unittest.TestCase):
    driver: webdriver.Remote
    wait: WebDriverWait

    def setUp(self):
        """Configuração do driver do Appium."""
        capabilities = dict(
            platformName='Android',  # ou 'iOS'
            deviceName='NomeDoSeuDispositivoOuEmulador', # Ex: emulator-5554
            appPackage='com.seuapp.pacote', # Substitua pelo pacote do seu app
            appActivity='com.seuapp.atividade.Principal', # Substitua pela atividade principal
            automationName='UiAutomator2',  # ou 'XCUITest' para iOS
            # unicodeKeyboard=True, # Descomente se houver problemas com entrada de texto
            # resetKeyboard=True
        )
        options = AppiumOptions().load_capabilities(capabilities)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
        self.wait = WebDriverWait(self.driver, 20) # Tempo de espera padrão aumentado

    def tearDown(self):
        """Encerra a sessão do driver após cada teste."""
        if self.driver:
            self.driver.quit()

    def _is_element_present(self, locator, timeout=1):
        """Verifica se um elemento está presente sem falhar o teste imediatamente."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def _find_element_with_wait(self, locator):
        """Encontra um elemento com espera explícita."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def _click_element_with_wait(self, locator):
        """Encontra e clica em um elemento com espera explícita."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def _wait_for_text_visibility(self, text_content, visible=True, timeout=5):
        """Espera um texto específico ficar visível ou invisível (para SnackBars)."""
        locator = (By.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=text_content))
        try:
            if visible:
                self.wait.until(EC.visibility_of_element_located(locator))
            else:
                # Para invisibilidade, pode ser mais confiável esperar que desapareça
                # ou que não esteja mais presente no DOM após um tempo.
                # EC.invisibility_of_element_located pode ser rápido se o elemento for removido do DOM.
                WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            action = "aparecer" if visible else "desaparecer"
            self.fail(f"Timeout esperando o texto '{text_content}' {action}.")

    def _navigate_to_recursos_page(self):
        """Navega para a RecursosPage, fazendo login se necessário."""
        time.sleep(2) # Tempo inicial para o app estabilizar

        try:
            # Verifica se já estamos na HomePage (ex: após um teste anterior ou se o login não é necessário)
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(LOC_HOME_PAGE_INDICATOR))
            is_on_home_page_initially = True
        except TimeoutException:
            is_on_home_page_initially = False

        if not is_on_home_page_initially:
            # Assume que estamos na LoginPage ou que o app precisa de login
            try:
                self._find_element_with_wait(LOC_USERNAME_FIELD).send_keys('admin')
                self._find_element_with_wait(LOC_PASSWORD_FIELD).send_keys('1234')
                self._click_element_with_wait(LOC_LOGIN_BUTTON)
                self._find_element_with_wait(LOC_HOME_PAGE_INDICATOR) # Espera pela HomePage
            except TimeoutException:
                self.fail("Não foi possível encontrar elementos de login ou navegar para a HomePage após a tentativa de login.")
        
        # Neste ponto, devemos estar na HomePage
        self.assertTrue(self._is_element_present(LOC_HOME_PAGE_INDICATOR, timeout=5),
                        "Não está na HomePage antes de navegar para a RecursosPage.")

        self._click_element_with_wait(LOC_NATIVE_RESOURCES_BUTTON)
        self._find_element_with_wait(LOC_RECURSOS_PAGE_INDICATOR) # Espera pela RecursosPage
        time.sleep(0.5) # Pequena pausa para a página Recursos renderizar completamente

    def test_recursos_page_ui_and_no_image_selection(self):
        """Verifica UI inicial e interage com seletores de imagem (simulando nenhuma seleção)."""
        self._navigate_to_recursos_page()

        # 1. Verifica estado inicial da UI
        self._find_element_with_wait(LOC_IMAGE_DISPLAY_AREA)
        self._wait_for_text_visibility(TEXT_NENHUMA_IMAGEM_SELECIONADA, visible=True)
        self.assertTrue(self._is_element_present(LOC_IMAGE_SEARCH_ICON), "Ícone de busca de imagem não encontrado.")

        self.assertTrue(self._is_element_present(LOC_OPEN_CAMERA_BUTTON), "Botão 'Abrir Câmera' não encontrado.")
        self.assertTrue(self._is_element_present(LOC_OPEN_GALLERY_BUTTON), "Botão 'Abrir Galeria' não encontrado.")
        self.assertTrue(self._is_element_present(LOC_SELECT_IMAGE_BUTTON), "Botão 'Selecionar Imagem' não encontrado.")

        # O botão de remover imagem não deve estar visível inicialmente
        self.assertFalse(self._is_element_present(LOC_REMOVE_IMAGE_BUTTON, timeout=2),
                         "Botão 'Remover Imagem' deveria estar invisível inicialmente.")

        # 2. Tenta abrir a câmera
        self._click_element_with_wait(LOC_OPEN_CAMERA_BUTTON)
        # Se um seletor nativo abrir, pode ser necessário pressionar "Voltar" ou "Cancelar" aqui.
        # Ex: self.driver.back()
        time.sleep(0.5) # Pequena pausa para a ação registrar antes da verificação do SnackBar
        self._wait_for_text_visibility(TEXT_NENHUMA_IMAGEM_TIRADA, visible=True, timeout=5)
        self._wait_for_text_visibility(TEXT_NENHUMA_IMAGEM_TIRADA, visible=False, timeout=5) # Espera SnackBar desaparecer

        # 3. Tenta abrir a galeria
        self._click_element_with_wait(LOC_OPEN_GALLERY_BUTTON)
        time.sleep(0.5)
        self._wait_for_text_visibility(TEXT_NENHUMA_IMAGEM_SELECIONADA, visible=True, timeout=5)
        self._wait_for_text_visibility(TEXT_NENHUMA_IMAGEM_SELECIONADA, visible=False, timeout=5)

        # 4. Tenta selecionar imagem via ActionSheet (Galeria)
        self._click_element_with_wait(LOC_SELECT_IMAGE_BUTTON)
        self._find_element_with_wait(LOC_IMAGE_SOURCE_SHEET) # Espera o ActionSheet aparecer
        self.assertTrue(self._is_element_present(LOC_IMAGE_SOURCE_SHEET_GALLERY), "Opção 'Galeria' no sheet não encontrada.")
        self.assertTrue(self._is_element_present(LOC_IMAGE_SOURCE_SHEET_CAMERA), "Opção 'Câmera' no sheet não encontrada.")

        self._click_element_with_wait(LOC_IMAGE_SOURCE_SHEET_GALLERY)
        time.sleep(0.5) # Espera o sheet fechar e a ação processar
        self._wait_for_text_visibility(TEXT_NENHUMA_IMAGEM_SELECIONADA, visible=True, timeout=5)
        self._wait_for_text_visibility(TEXT_NENHUMA_IMAGEM_SELECIONADA, visible=False, timeout=5)

        # 5. Tenta selecionar imagem via ActionSheet (Câmera)
        self._click_element_with_wait(LOC_SELECT_IMAGE_BUTTON)
        self._find_element_with_wait(LOC_IMAGE_SOURCE_SHEET)

        self._click_element_with_wait(LOC_IMAGE_SOURCE_SHEET_CAMERA)
        time.sleep(0.5)
        self._wait_for_text_visibility(TEXT_NENHUMA_IMAGEM_TIRADA, visible=True, timeout=5)
        self._wait_for_text_visibility(TEXT_NENHUMA_IMAGEM_TIRADA, visible=False, timeout=5)

        # Confirma que a área de imagem ainda mostra "Nenhuma imagem selecionada"
        self._wait_for_text_visibility(TEXT_NENHUMA_IMAGEM_SELECIONADA, visible=True)
        self.assertFalse(self._is_element_present(LOC_REMOVE_IMAGE_BUTTON, timeout=2),
                         "Botão 'Remover Imagem' ainda deveria estar invisível.")

if __name__ == '__main__':
    unittest.main()
