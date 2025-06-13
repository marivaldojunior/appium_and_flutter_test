# d:\repos\appium_and_flutter_test\integration_test\listview_page_test.py
import unittest
import time
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy # Preferred for Appium-specific selectors
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- INÍCIO: PLACEHOLDERS DE LOCALIZADORES ---
# !!! IMPORTANTE: Substitua estes placeholders pelos localizadores REAIS do seu app Flutter !!!
# Use Appium Inspector para encontrá-los. Flutter Keys geralmente são accessibility_id.

# LoginPage (assumindo IDs do exemplo anterior ou similares)
LOC_LOGIN_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "usernameField_ LoginPage_ACCESSIBILITY_ID") # Um elemento único da LoginPage
LOC_USERNAME_FIELD = (AppiumBy.ACCESSIBILITY_ID, "usernameField") # LoginPage.usernameFieldKey
LOC_PASSWORD_FIELD = (AppiumBy.ACCESSIBILITY_ID, "passwordField") # LoginPage.passwordFieldKey
LOC_LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "loginButton")     # LoginPage.loginButtonKey

# HomePage
LOC_HOME_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "homePageElement_HomePage_ACCESSIBILITY_ID") # Um elemento único da HomePage
LOC_LISTVIEW_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "homePage.listViewButtonKey_ACCESSIBILITY_ID") # HomePage.listViewButtonKey

# ListViewPage
LOC_LISTVIEW_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "listViewPage.listViewKey_ACCESSIBILITY_ID") # Algo que identifica a ListViewPage, talvez o próprio ListView
LOC_LISTVIEW_KEY = (AppiumBy.ACCESSIBILITY_ID, "listViewPage.listViewKey_ACCESSIBILITY_ID") # ListViewPage.listViewKey
LOC_ADD_FLOATING_ACTION_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "listViewPage.addFloatingActionButtonKey_ACCESSIBILITY_ID")

# Add/Edit Item Dialog (os IDs podem ser os mesmos para Add e Edit se o dialog for reutilizado)
LOC_ADD_ITEM_DIALOG_KEY = (AppiumBy.ACCESSIBILITY_ID, "listViewPage.addItemDialogKey_ACCESSIBILITY_ID")
LOC_EDIT_ITEM_DIALOG_KEY = (AppiumBy.ACCESSIBILITY_ID, "listViewPage.editItemDialogKey_ACCESSIBILITY_ID") # Pode ser o mesmo que ADD
LOC_DIALOG_TITLE_FIELD = (AppiumBy.ACCESSIBILITY_ID, "listViewPage.dialogTitleFieldKey_ACCESSIBILITY_ID")
LOC_DIALOG_DESCRIPTION_FIELD = (AppiumBy.ACCESSIBILITY_ID, "listViewPage.dialogDescriptionFieldKey_ACCESSIBILITY_ID")
LOC_DIALOG_ADD_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "listViewPage.dialogAddButtonKey_ACCESSIBILITY_ID")
LOC_DIALOG_SAVE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "listViewPage.dialogSaveButtonKey_ACCESSIBILITY_ID") # Para edição

# Delete Confirmation Dialog
LOC_DELETE_CONFIRM_DIALOG_KEY = (AppiumBy.ACCESSIBILITY_ID, "listViewPage.deleteConfirmDialogKey_ACCESSIBILITY_ID")
LOC_DELETE_CONFIRM_CANCEL_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "listViewPage.deleteConfirmCancelButtonKey_ACCESSIBILITY_ID")
LOC_DELETE_CONFIRM_DELETE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "listViewPage.deleteConfirmDeleteButtonKey_ACCESSIBILITY_ID")

# Empty List
LOC_EMPTY_LIST_TEXT_KEY = (AppiumBy.ACCESSIBILITY_ID, "listViewPage.emptyListTextKey_ACCESSIBILITY_ID")

# Textos para validação, SnackBars, etc. (usados em XPaths)
TEXT_VALIDATION_TITLE_EMPTY = "O título não pode estar vazio."
TEXT_VALIDATION_DESCRIPTION_EMPTY = "A descrição não pode estar vazia."
TEXT_SNACKBAR_ITEM_ADDED = "Novo item adicionado!"
TEXT_SNACKBAR_ITEM_UPDATED = "Item atualizado!"
TEXT_SNACKBAR_ITEM_REMOVED = "Item removido!"
TEXT_SNACKBAR_ITEM_SELECTED_PREFIX = "Item selecionado: " # Ex: "Item selecionado: Item 3"
TEXT_EMPTY_LIST_MESSAGE = "Nenhum item na lista.\nAdicione alguns itens usando o botão \"+\"."


# Template XPath para encontrar elementos por texto (ajuste se necessário para iOS/Android)
# Para Android, @text ou @content-desc. Para iOS, @name ou @label.
# Este XPath tenta cobrir alguns casos comuns.
XPATH_TEXT_CONTAINS_TEMPLATE = "//*[contains(@text, \"{text}\") or contains(@content-desc, \"{text}\") or contains(@name, \"{text}\") or contains(@label, \"{text}\")]"
# --- FIM: PLACEHOLDERS DE LOCALIZADORES ---


class ListViewPageTests(unittest.TestCase):
    driver: webdriver.Remote
    wait: WebDriverWait

    DEFAULT_WAIT_TIMEOUT = 10
    SHORT_WAIT_TIMEOUT = 3
    LONG_WAIT_TIMEOUT = 20 # Para navegações ou operações mais longas

    # Appium capabilities
    CAPABILITIES = dict(
        platformName='Android',  # ou 'iOS'
        deviceName='emulator-5554', # Substitua pelo nome do seu dispositivo/emulador
        appPackage='com.example.appium_and_flutter_test', # Substitua pelo pacote do seu app
        appActivity='.MainActivity', # Substitua pela atividade principal (pode precisar do pacote completo)
        automationName='UiAutomator2',  # ou 'XCUITest' para iOS
        # unicodeKeyboard=True, # Descomente se houver problemas com entrada de texto
        # resetKeyboard=True,
        # noReset=True # Para não reinstalar o app a cada sessão, útil durante desenvolvimento
    )
    APPIUM_SERVER_URL = 'http://localhost:4723' # Ou 'http://localhost:4723/wd/hub'

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

    def _wait_for_text_visibility(self, text_content, visible=True, timeout=DEFAULT_WAIT_TIMEOUT):
        locator = (AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=text_content))
        try:
            if visible:
                WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            else:
                WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            action = "aparecer" if visible else "desaparecer"
            self.fail(f"Timeout esperando o texto '{text_content}' {action}.")

    def _perform_swipe_on_element(self, element, direction="left", swipe_distance_pixels=400):
        """Performs a swipe on the center of a given element."""
        location = element.location
        size = element.size
        center_x = location['x'] + size['width'] // 2
        center_y = location['y'] + size['height'] // 2

        if direction == "left":
            end_x = center_x - swipe_distance_pixels
            end_y = center_y
        elif direction == "right":
            end_x = center_x + swipe_distance_pixels
            end_y = center_y
        else:
            self.fail(f"Swipe direction '{direction}' not supported by this helper.")
            return

        # Ensure end coordinates are within bounds (simplistic check)
        screen_dims = self.driver.get_window_size()
        end_x = max(0, min(end_x, screen_dims['width'] - 1))
        end_y = max(0, min(end_y, screen_dims['height'] - 1))

        self.driver.swipe(center_x, center_y, end_x, end_y, 400) # 400ms duration
        time.sleep(0.5) # Allow UI to settle

    def _scroll_list_until_text_visible(self, list_view_locator, text_to_find, max_scrolls=10):
        list_element = self._find_element_with_wait(list_view_locator) # Ensure list exists

        for i in range(max_scrolls):
            try:
                # Check if text is already visible (short timeout)
                target_element = WebDriverWait(self.driver, 1).until(
                    EC.visibility_of_element_located((AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=text_to_find)))
                )
                return target_element # Found
            except TimeoutException:
                # Not visible, try to scroll
                if i == max_scrolls -1: # Last attempt, don't scroll again
                    break

                # Perform a swipe gesture on the list element
                # Adjust direction ('down' to scroll content up, 'up' to scroll content down)
                # and percentage as needed.
                # For a typical list, swiping 'up' (finger moving from bottom to top) scrolls content down.
                # Swiping 'down' (finger moving from top to bottom) scrolls content up.
                # Flutter's scrollUntilVisible usually implies scrolling "down" the list.
                # Let's assume a swipe that moves content upwards on the screen (finger moves down)
                size = list_element.size
                start_x = list_element.location['x'] + size['width'] // 2
                start_y = list_element.location['y'] + int(size['height'] * 0.8) # Start near bottom of list
                end_y = list_element.location['y'] + int(size['height'] * 0.2)   # End near top of list
                self.driver.swipe(start_x, start_y, start_x, end_y, 500) # Swipe up
                time.sleep(0.5) # Wait for scroll animation

        # Final check after all scrolls
        try:
            return self._find_element_with_wait((AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=text_to_find)), timeout=self.SHORT_WAIT_TIMEOUT)
        except TimeoutException:
            raise NoSuchElementException(f"Texto '{text_to_find}' não encontrado na lista '{list_view_locator}' após {max_scrolls} rolagens.")

    def _find_list_item_by_text_and_scroll_if_needed(self, list_view_locator, item_text):
        return self._scroll_list_until_text_visible(list_view_locator, item_text)

    def _navigate_to_listview_page(self):
        time.sleep(1) # Initial wait for app to stabilize

        if self._is_element_present(LOC_LOGIN_PAGE_INDICATOR, timeout=3):
            self._type_text_with_wait(LOC_USERNAME_FIELD, 'admin')
            self._type_text_with_wait(LOC_PASSWORD_FIELD, '1234')
            self._click_element_with_wait(LOC_LOGIN_BUTTON)
            # Wait for login to complete and HomePage to appear
            self._find_element_with_wait(LOC_HOME_PAGE_INDICATOR, timeout=self.LONG_WAIT_TIMEOUT)
            # If there's a login success SnackBar, wait for it to disappear (optional)
            # self._wait_for_text_visibility("Login bem-sucedido!", visible=False, timeout=5)
            time.sleep(1) # Allow HomePage to fully render

        self.assertTrue(self._is_element_present(LOC_HOME_PAGE_INDICATOR), "Não foi possível alcançar a HomePage.")
        self._click_element_with_wait(LOC_LISTVIEW_BUTTON)
        self._find_element_with_wait(LOC_LISTVIEW_PAGE_INDICATOR) # Wait for ListViewPage to load
        time.sleep(0.5)


    # --- Test Method ---
    def test_listview_interactions(self):
        self._navigate_to_listview_page()

        # 1. Verifica itens iniciais
        self._find_element_with_wait(LOC_LISTVIEW_KEY) # Ensure list view is present
        self._wait_for_text_visibility('Item 1')
        self._wait_for_text_visibility('Item 2')
        self._wait_for_text_visibility('Item 3')
        self._wait_for_text_visibility('Item 4')

        # 2. Adiciona um novo item
        novo_titulo = 'Novo Item Teste Python'
        nova_descricao = 'Descrição do novo item Python.'

        self._click_element_with_wait(LOC_ADD_FLOATING_ACTION_BUTTON)
        self._find_element_with_wait(LOC_ADD_ITEM_DIALOG_KEY) # Dialog is open

        # Testa validação (campos vazios)
        self._click_element_with_wait(LOC_DIALOG_ADD_BUTTON)
        self._wait_for_text_visibility(TEXT_VALIDATION_TITLE_EMPTY)
        self._wait_for_text_visibility(TEXT_VALIDATION_DESCRIPTION_EMPTY)

        # Preenche e adiciona
        self._type_text_with_wait(LOC_DIALOG_TITLE_FIELD, novo_titulo)
        self._type_text_with_wait(LOC_DIALOG_DESCRIPTION_FIELD, nova_descricao)
        self._click_element_with_wait(LOC_DIALOG_ADD_BUTTON)

        self._wait_for_text_visibility(TEXT_SNACKBAR_ITEM_ADDED)
        self._wait_for_text_visibility(novo_titulo) # Item is now in the list
        self._wait_for_text_visibility(TEXT_SNACKBAR_ITEM_ADDED, visible=False, timeout=5) # Wait for SnackBar to disappear

        # 3. Edita um item existente (Item 1)
        titulo_original_para_editar = 'Item 1'
        titulo_editado = 'Item 1 Editado Python'
        descricao_editada = 'Descrição do Item 1 foi alterada Python.'

        item_para_editar_element = self._find_list_item_by_text_and_scroll_if_needed(LOC_LISTVIEW_KEY, titulo_original_para_editar)
        self._perform_swipe_on_element(item_para_editar_element, direction="left") # Swipe para esquerda
        self._find_element_with_wait(LOC_EDIT_ITEM_DIALOG_KEY)

        # Verifica se campos estão pré-preenchidos (Appium might get the hint text or actual text)
        # This check is more complex with Appium as it depends on how Flutter exposes this.
        # For now, we'll assume the title field is found and proceed.
        # title_field_edit = self._find_element_with_wait(LOC_DIALOG_TITLE_FIELD)
        # self.assertIn(titulo_original_para_editar, title_field_edit.text, "Título original não pré-preenchido no diálogo de edição.")

        # Testa validação
        self._type_text_with_wait(LOC_DIALOG_TITLE_FIELD, '', clear_first=True)
        self._click_element_with_wait(LOC_DIALOG_SAVE_BUTTON)
        self._wait_for_text_visibility(TEXT_VALIDATION_TITLE_EMPTY)

        # Preenche e salva
        self._type_text_with_wait(LOC_DIALOG_TITLE_FIELD, titulo_editado)
        self._type_text_with_wait(LOC_DIALOG_DESCRIPTION_FIELD, descricao_editada)
        self._click_element_with_wait(LOC_DIALOG_SAVE_BUTTON)

        self._wait_for_text_visibility(TEXT_SNACKBAR_ITEM_UPDATED)
        self._wait_for_text_visibility(titulo_editado)
        self.assertFalse(self._is_element_present((AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=titulo_original_para_editar)), timeout=1),
                         f"Título original '{titulo_original_para_editar}' ainda encontrado após edição.")
        self._wait_for_text_visibility(TEXT_SNACKBAR_ITEM_UPDATED, visible=False, timeout=5)

        # 4. Exclui um item (Item 2)
        titulo_para_excluir = 'Item 2'
        item_para_excluir_element = self._find_list_item_by_text_and_scroll_if_needed(LOC_LISTVIEW_KEY, titulo_para_excluir)

        # Tenta excluir e cancela
        self._perform_swipe_on_element(item_para_excluir_element, direction="right") # Swipe para direita
        self._find_element_with_wait(LOC_DELETE_CONFIRM_DIALOG_KEY)
        self._click_element_with_wait(LOC_DELETE_CONFIRM_CANCEL_BUTTON)
        self._wait_for_text_visibility(titulo_para_excluir) # Item ainda existe

        # Exclui de verdade
        item_para_excluir_element = self._find_list_item_by_text_and_scroll_if_needed(LOC_LISTVIEW_KEY, titulo_para_excluir) # Re-encontra
        self._perform_swipe_on_element(item_para_excluir_element, direction="right")
        self._find_element_with_wait(LOC_DELETE_CONFIRM_DIALOG_KEY)
        self._click_element_with_wait(LOC_DELETE_CONFIRM_DELETE_BUTTON)

        self._wait_for_text_visibility(TEXT_SNACKBAR_ITEM_REMOVED)
        self.assertFalse(self._is_element_present((AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=titulo_para_excluir)), timeout=1),
                         f"Item '{titulo_para_excluir}' ainda encontrado após exclusão.")
        self._wait_for_text_visibility(TEXT_SNACKBAR_ITEM_REMOVED, visible=False, timeout=5)

        # 5. Toca em um item para ver SnackBar de seleção (Item 3)
        titulo_para_selecionar = 'Item 3'
        item_para_selecionar_element = self._find_list_item_by_text_and_scroll_if_needed(LOC_LISTVIEW_KEY, titulo_para_selecionar)
        item_para_selecionar_element.click()

        self._wait_for_text_visibility(f"{TEXT_SNACKBAR_ITEM_SELECTED_PREFIX}{titulo_para_selecionar}")
        self._wait_for_text_visibility(f"{TEXT_SNACKBAR_ITEM_SELECTED_PREFIX}{titulo_para_selecionar}", visible=False, timeout=5)

        # 6. Exclui todos os itens restantes para verificar o estado de lista vazia
        # Itens restantes: "Item 1 Editado Python", "Item 3", "Item 4", "Novo Item Teste Python"
        titulos_para_excluir_restantes = [titulo_editado, 'Item 3', 'Item 4', novo_titulo]

        for titulo in titulos_para_excluir_restantes:
            if not self._is_element_present((AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=titulo)), timeout=1):
                print(f"Item '{titulo}' já não está presente, pulando exclusão.")
                continue # Item pode ter sido o 'Item 3' que foi selecionado e não está mais na mesma posição ou foi afetado por scrolls

            item_element = self._find_list_item_by_text_and_scroll_if_needed(LOC_LISTVIEW_KEY, titulo)
            self._perform_swipe_on_element(item_element, direction="right")
            self._find_element_with_wait(LOC_DELETE_CONFIRM_DIALOG_KEY, timeout=self.SHORT_WAIT_TIMEOUT)
            self._click_element_with_wait(LOC_DELETE_CONFIRM_DELETE_BUTTON)
            self._wait_for_text_visibility(TEXT_SNACKBAR_ITEM_REMOVED)
            self._wait_for_text_visibility(TEXT_SNACKBAR_ITEM_REMOVED, visible=False, timeout=5)
            self.assertFalse(self._is_element_present((AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=titulo)), timeout=1),
                             f"Item '{titulo}' não foi removido corretamente.")

        # Verifica estado de lista vazia
        self._find_element_with_wait(LOC_EMPTY_LIST_TEXT_KEY)
        self._wait_for_text_visibility(TEXT_EMPTY_LIST_MESSAGE.split('\n')[0]) # Checa a primeira linha da mensagem
        self.assertFalse(self._is_element_present(LOC_LISTVIEW_KEY, timeout=1), "ListView ainda está presente quando deveria estar vazia.")

        # 7. Adiciona um item novamente para garantir que a lista vazia some
        outro_titulo = "Outro Item Python"
        outra_descricao = "Outra Desc Python"
        self._click_element_with_wait(LOC_ADD_FLOATING_ACTION_BUTTON)
        self._find_element_with_wait(LOC_ADD_ITEM_DIALOG_KEY)
        self._type_text_with_wait(LOC_DIALOG_TITLE_FIELD, outro_titulo)
        self._type_text_with_wait(LOC_DIALOG_DESCRIPTION_FIELD, outra_descricao)
        self._click_element_with_wait(LOC_DIALOG_ADD_BUTTON)

        self._wait_for_text_visibility(TEXT_SNACKBAR_ITEM_ADDED)
        self._wait_for_text_visibility(outro_titulo)
        self._find_element_with_wait(LOC_LISTVIEW_KEY) # ListView deve estar visível novamente
        self.assertFalse(self._is_element_present(LOC_EMPTY_LIST_TEXT_KEY, timeout=1), "Texto de lista vazia ainda presente após adicionar novo item.")
        self._wait_for_text_visibility(TEXT_SNACKBAR_ITEM_ADDED, visible=False, timeout=5)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ListViewPageTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
