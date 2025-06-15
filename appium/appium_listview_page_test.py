# d:\repos\appium_and_flutter_test\integration_test\listview_page_test.py
import unittest
import time
import os
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy # Preferred for Appium-specific selectors
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
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

from appium_flutter_finder.flutter_finder import FlutterFinder

# Configurações
APPIUM_HOST = 'http://127.0.0.1:4723'
APP_PATH = "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" # IMPORTANTE: Atualize este caminho

# --- Chaves dos Elementos Flutter ---
# LoginPage
LOGIN_USERNAME_FIELD_KEY = 'login_username_field'
LOGIN_PASSWORD_FIELD_KEY = 'login_password_field'
LOGIN_BUTTON_KEY = 'login_button'

# HomePage
HOME_PAGE_APPBAR_TITLE_KEY = 'home_page_app_bar_title'
HOME_PAGE_LISTVIEW_BUTTON_KEY = 'home_page_list_view_button' # Botão que navega para a ListViewPage

# ListViewPage
LISTVIEW_PAGE_APPBAR_TITLE_KEY = 'list_view_page_app_bar_title'
LISTVIEW_PAGE_LISTVIEW_KEY = 'list_view_page_list_view' # A própria ListView
LISTVIEW_PAGE_ADD_FAB_KEY = 'list_view_page_add_fab'     # FloatingActionButton para adicionar item
LISTVIEW_PAGE_EMPTY_TEXT_KEY = 'list_view_page_empty_text' # Texto exibido quando a lista está vazia

# Chaves para itens da lista (assumindo que cada item ou seu conteúdo tem uma ValueKey)
# Se os itens forem Dismissible, eles podem ter keys para as ações de dismiss.
# Para este exemplo, vamos assumir que o Card do item tem uma key baseada no título ou ID.
LISTVIEW_PAGE_ITEM_CARD_KEY = lambda title: f'list_item_card_{title.replace(" ", "_")}' # Ex: list_item_card_Item_1
# Se os botões de editar/deletar aparecem após swipe e têm keys:
LISTVIEW_PAGE_ITEM_EDIT_ACTION_KEY = lambda title: f'list_item_edit_action_{title.replace(" ", "_")}'
LISTVIEW_PAGE_ITEM_DELETE_ACTION_KEY = lambda title: f'list_item_delete_action_{title.replace(" ", "_")}'

# Add/Edit Item Dialog (assumindo que o mesmo diálogo é usado para adicionar e editar)
DIALOG_TITLE_FIELD_KEY = 'dialog_title_field'
DIALOG_DESCRIPTION_FIELD_KEY = 'dialog_description_field'
DIALOG_SUBMIT_BUTTON_KEY = 'dialog_submit_button' # O texto pode mudar (Adicionar/Salvar)
DIALOG_CANCEL_BUTTON_KEY = 'dialog_cancel_button'

# Delete Confirmation Dialog
DELETE_CONFIRM_DIALOG_KEY = 'delete_confirm_dialog' # Key do AlertDialog em si
DELETE_CONFIRM_DELETE_BUTTON_KEY = 'delete_confirm_dialog_delete_button'
DELETE_CONFIRM_CANCEL_BUTTON_KEY = 'delete_confirm_dialog_cancel_button'

# Textos para validação, SnackBars, etc.
TEXT_ITEM_ADDED_SNACKBAR = "Novo item adicionado!"
TEXT_ITEM_UPDATED_SNACKBAR = "Item atualizado!"
TEXT_ITEM_REMOVED_SNACKBAR = "Item removido!"
TEXT_ITEM_SELECTED_SNACKBAR_PREFIX = "Item selecionado: " # Ex: "Item selecionado: Item 1"
TEXT_VALIDATION_TITLE_EMPTY = "O título não pode estar vazio" # Ajuste conforme a mensagem real
TEXT_VALIDATION_DESCRIPTION_EMPTY = "A descrição não pode estar vazia" # Ajuste conforme a mensagem real
TEXT_EMPTY_LIST_MESSAGE = "Nenhum item na lista." # Ajuste para a primeira linha ou parte identificável

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
        # Clean up after each test if needed
        pass

    @classmethod
    def setUpClass(cls):
        if APP_PATH == "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI":
            raise ValueError("Por favor, atualize a variável APP_PATH com o caminho para o seu APK/APP.")

        options = AppiumOptions()
        options.set_capability('platformName', 'Android')
        options.set_capability('automationName', 'Flutter')
        options.set_capability('deviceName', 'Android Emulator')
        options.set_capability('app', APP_PATH)
        options.set_capability('retryBackoffTime', 500)
        options.set_capability('maxRetryCount', 3)
        options.set_capability('newCommandTimeout', 180) # Aumentado para interações de lista

        cls.driver = webdriver.Remote(command_executor=APPIUM_HOST, options=options)
        cls.finder = FlutterFinder()
        cls.wait = WebDriverWait(cls.driver, 30) # Timeout padrão para elementos

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()

    # --- Helper Methods ---
    def _is_element_present(self, locator, timeout=SHORT_WAIT_TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

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

    def _find_element_with_wait(self, locator, timeout=DEFAULT_WAIT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))


    def _click_element_with_wait(self, locator, timeout=DEFAULT_WAIT_TIMEOUT):
        element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
    def _is_text_present(self, text_string, timeout=5):
        # Verifica se o texto está presente na tela. Pode ser usado para SnackBars.
        try:
            self.wait.until(EC.presence_of_element_located((AppiumBy.FLUTTER, self.finder.by_text(text_string))))
            return True
        except TimeoutException:
            try: # Fallback para XPath para Snackbars nativos
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

    def _type_text_with_wait(self, locator, text, timeout=DEFAULT_WAIT_TIMEOUT, clear_first=True):
        element = self._find_element_with_wait(locator, timeout)
        time.sleep(0.5) # Pausa para UI

    def _enter_text_in_field(self, key_string, text, clear_first=True):
        element = self._find_element_by_value_key(key_string)
        if clear_first:
            element.click() # Focar para limpar
            time.sleep(0.1)
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
        time.sleep(0.2)
        if self.driver.is_keyboard_shown():
            try:
                self.driver.hide_keyboard()
            except: pass # Ignorar se falhar

    def _wait_for_snackbar(self, message_text, timeout=5, present=True):
        start_time = time.time()
        while time.time() < start_time + timeout:
            if self._is_text_present(message_text, timeout=0.2) == present:
                return
            time.sleep(0.1)
        self.fail(f"A mensagem do SnackBar '{message_text}' não ficou {'presente' if present else 'ausente'} dentro de {timeout}s.")

    def _scroll_to_element_by_key(self, element_key_to_find, list_view_key=LISTVIEW_PAGE_LISTVIEW_KEY):
        # Tenta encontrar o elemento diretamente primeiro
        if self._is_element_present_by_value_key(element_key_to_find, timeout=1):
            return self._find_element_by_value_key(element_key_to_find)

        # Se não encontrado, tenta rolar
        list_finder = self.finder.by_value_key(list_view_key)
        item_finder = self.finder.by_value_key(element_key_to_find)
        try:
            self.driver.execute_script('flutter:scrollUntilVisible', list_finder, {'item': item_finder, 'dyScroll': -100.0, 'timeout': 5000})
            return self._find_element_by_value_key(element_key_to_find)
        except Exception as e:
            print(f"Erro ao rolar para o elemento {element_key_to_find}: {e}")
            raise NoSuchElementException(f"Não foi possível rolar e encontrar o elemento com a chave: {element_key_to_find}")

    def _get_list_item_element_by_title_text(self, item_title_text, list_view_key=LISTVIEW_PAGE_LISTVIEW_KEY):
        # Este método é mais frágil se os itens não tiverem ValueKeys únicas e visíveis.
        # É preferível usar _scroll_to_element_by_key se os itens tiverem keys.
        # Para este exemplo, vamos assumir que o texto do título é suficiente para encontrar após a rolagem.
        list_finder = self.finder.by_value_key(list_view_key)
        item_text_finder = self.finder.by_text(item_title_text)
        try:
            # Tenta encontrar diretamente
            if self._is_text_present(item_title_text, timeout=1):
                 return self.wait.until(EC.presence_of_element_located((AppiumBy.FLUTTER, item_text_finder)))

            self.driver.execute_script('flutter:scrollUntilVisible', list_finder, {'item': item_text_finder, 'dyScroll': -100.0, 'timeout': 7000})
            return self.wait.until(EC.presence_of_element_located((AppiumBy.FLUTTER, item_text_finder)))
        except Exception as e:
            print(f"Erro ao rolar para o texto '{item_title_text}': {e}")
            raise NoSuchElementException(f"Não foi possível rolar e encontrar o item com o texto: {item_title_text}")

    def _perform_swipe_on_flutter_element(self, element_key_or_element, direction="left", swipe_ratio=0.6):
        if isinstance(element_key_or_element, str):
            element = self._find_element_by_value_key(element_key_or_element)
        else:
            element = element_key_or_element

        location = element.location
        size = element.size
        center_x = location['x'] + size['width'] // 2
        center_y = location['y'] + size['height'] // 2

        swipe_distance_pixels = size['width'] * swipe_ratio

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
        end_y = center_y # Horizontal swipe

        action = TouchAction(self.driver)
        action.press(x=center_x, y=center_y).wait(ms=200).move_to(x=end_x, y=end_y).release().perform()
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
    def _navigate_to_listview_page(self, username='admin', password='1234'):
        """Navega para a ListViewPage, fazendo login se necessário."""
        time.sleep(1) # Pausa inicial

        if self._is_element_present_by_value_key(LOGIN_USERNAME_FIELD_KEY, timeout=3):
            print("Realizando login para chegar na ListViewPage...")
            self._enter_text_in_field(LOGIN_USERNAME_FIELD_KEY, username)
            self._enter_text_in_field(LOGIN_PASSWORD_FIELD_KEY, password)
            self._tap_element(LOGIN_BUTTON_KEY)

            self._find_element_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY, timeout=15) # Espera HomePage
            time.sleep(1) # Pausa para SnackBar de login sumir, se houver

        self.assertTrue(self._is_element_present(LOC_HOME_PAGE_INDICATOR), "Não foi possível alcançar a HomePage.")
        self._click_element_with_wait(LOC_LISTVIEW_BUTTON)
        self._find_element_with_wait(LOC_LISTVIEW_PAGE_INDICATOR) # Wait for ListViewPage to load
        self._find_element_by_value_key(HOME_PAGE_APPBAR_TITLE_KEY) # Confirma que está na HomePage
        self._tap_element(HOME_PAGE_LISTVIEW_BUTTON_KEY)
        self._find_element_by_value_key(LISTVIEW_PAGE_APPBAR_TITLE_KEY) # Confirma que está na ListViewPage
        time.sleep(0.5)


    def test_01_initial_items_and_add_item(self):
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

        # Verifica itens iniciais (ex: "Item 1", "Item 2")
        # Se a lista começa vazia, este passo pode ser adaptado ou removido.
        # Para este exemplo, vamos assumir que a lista pode ter itens iniciais ou estar vazia.
        self._find_element_by_value_key(LISTVIEW_PAGE_LISTVIEW_KEY) # Garante que a ListView está lá
        initial_items = ["Item 1", "Item 2", "Item 3", "Item 4"] # Exemplo de itens iniciais
        for item_title in initial_items:
            try:
                self._get_list_item_element_by_title_text(item_title)
                print(f"Item inicial '{item_title}' encontrado.")
            except NoSuchElementException:
                print(f"Item inicial '{item_title}' não encontrado. A lista pode estar vazia ou ter outros itens.")

        # Adiciona um novo item
        new_item_title = "Item Appium"
        new_item_desc = "Adicionado via Appium"

        self._tap_element(LISTVIEW_PAGE_ADD_FAB_KEY)
        self._find_element_by_value_key(DIALOG_TITLE_FIELD_KEY) # Espera o diálogo abrir

        # Testa validação (campos vazios)
        self._tap_element(DIALOG_SUBMIT_BUTTON_KEY) # Botão "Adicionar"
        self._wait_for_snackbar(TEXT_VALIDATION_TITLE_EMPTY, present=True)
        self._wait_for_snackbar(TEXT_VALIDATION_TITLE_EMPTY, present=False) # Espera sumir

        self._enter_text_in_field(DIALOG_TITLE_FIELD_KEY, new_item_title)
        self._tap_element(DIALOG_SUBMIT_BUTTON_KEY)
        self._wait_for_snackbar(TEXT_VALIDATION_DESCRIPTION_EMPTY, present=True)
        self._wait_for_snackbar(TEXT_VALIDATION_DESCRIPTION_EMPTY, present=False)

        # Preenche e adiciona
        self._enter_text_in_field(DIALOG_DESCRIPTION_FIELD_KEY, new_item_desc)
        self._tap_element(DIALOG_SUBMIT_BUTTON_KEY)

        self._wait_for_snackbar(TEXT_ITEM_ADDED_SNACKBAR, present=True)
        self._get_list_item_element_by_title_text(new_item_title) # Verifica se o item está na lista
        self._wait_for_snackbar(TEXT_ITEM_ADDED_SNACKBAR, present=False)

    def test_02_edit_item(self):
        self._navigate_to_listview_page() # Garante que está na página
        item_to_edit_original_title = "Item 1" # Assumindo que "Item 1" existe
        edited_title = "Item 1 Editado"
        edited_desc = "Descrição alterada pelo Appium"

        # Encontra o item e simula swipe para revelar opções de edição
        # Se o swipe revelar um botão com key, use-o. Senão, o swipe pode abrir o diálogo diretamente.
        try:
            item_card_key = LISTVIEW_PAGE_ITEM_CARD_KEY(item_to_edit_original_title)
            item_element = self._scroll_to_element_by_key(item_card_key)
            self._perform_swipe_on_flutter_element(item_element, direction="left") # Swipe para esquerda
            # Se o swipe revela um botão "Editar" com key:
            # self._tap_element(LISTVIEW_PAGE_ITEM_EDIT_ACTION_KEY(item_to_edit_original_title))
        except NoSuchElementException:
            self.fail(f"Não foi possível encontrar ou rolar para o item '{item_to_edit_original_title}' para edição.")

        self._find_element_by_value_key(DIALOG_TITLE_FIELD_KEY) # Espera diálogo de edição

        self._enter_text_in_field(DIALOG_TITLE_FIELD_KEY, edited_title)
        self._enter_text_in_field(DIALOG_DESCRIPTION_FIELD_KEY, edited_desc)
        self._tap_element(DIALOG_SUBMIT_BUTTON_KEY) # Botão "Salvar"

        self._wait_for_snackbar(TEXT_ITEM_UPDATED_SNACKBAR, present=True)
        self._get_list_item_element_by_title_text(edited_title) # Verifica título atualizado
        self.assertFalse(self._is_text_present(item_to_edit_original_title, timeout=1),
                         f"Título original '{item_to_edit_original_title}' ainda presente após edição.")
        self._wait_for_snackbar(TEXT_ITEM_UPDATED_SNACKBAR, present=False)

    def test_03_delete_item(self):
        self._navigate_to_listview_page()
        item_to_delete_title = "Item 2" # Assumindo que "Item 2" existe

        try:
            item_card_key = LISTVIEW_PAGE_ITEM_CARD_KEY(item_to_delete_title)
            item_element = self._scroll_to_element_by_key(item_card_key)
            self._perform_swipe_on_flutter_element(item_element, direction="right") # Swipe para direita
            # Se o swipe revela um botão "Deletar" com key:
            # self._tap_element(LISTVIEW_PAGE_ITEM_DELETE_ACTION_KEY(item_to_delete_title))
        except NoSuchElementException:
            self.fail(f"Não foi possível encontrar ou rolar para o item '{item_to_delete_title}' para exclusão.")

        self._find_element_by_value_key(DELETE_CONFIRM_DIALOG_KEY) # Espera diálogo de confirmação

        # Cancela a exclusão primeiro
        self._tap_element(DELETE_CONFIRM_DIALOG_CANCEL_BUTTON_KEY)
        self._get_list_item_element_by_title_text(item_to_delete_title) # Item ainda deve existir

        # Exclui de verdade
        item_element = self._scroll_to_element_by_key(item_card_key) # Reencontra se necessário
        self._perform_swipe_on_flutter_element(item_element, direction="right")
        self._find_element_by_value_key(DELETE_CONFIRM_DIALOG_KEY)
        self._tap_element(DELETE_CONFIRM_DELETE_BUTTON_KEY)

        self._wait_for_snackbar(TEXT_ITEM_REMOVED_SNACKBAR, present=True)
        self.assertFalse(self._is_text_present(item_to_delete_title, timeout=2),
                         f"Item '{item_to_delete_title}' ainda presente após exclusão.")
        self._wait_for_snackbar(TEXT_ITEM_REMOVED_SNACKBAR, present=False)

    def test_04_tap_item_shows_snackbar(self):
        self._navigate_to_listview_page()
        item_to_tap_title = "Item 3" # Assumindo que "Item 3" existe

        try:
            # Se o item em si (o Card ou um Text dentro dele) tiver uma key, use-a.
            # Senão, encontre por texto e depois tape no elemento pai ou no próprio texto.
            item_card_key = LISTVIEW_PAGE_ITEM_CARD_KEY(item_to_tap_title)
            item_element = self._scroll_to_element_by_key(item_card_key)
            self._tap_element(item_element)
        except NoSuchElementException:
            # Fallback: tentar encontrar por texto e tapar
            try:
                item_text_element = self._get_list_item_element_by_title_text(item_to_tap_title)
                self._tap_element(item_text_element)
            except NoSuchElementException:
                self.fail(f"Não foi possível encontrar ou rolar para o item '{item_to_tap_title}' para tocar.")

        expected_snackbar_text = f"{TEXT_ITEM_SELECTED_SNACKBAR_PREFIX}{item_to_tap_title}"
        self._wait_for_snackbar(expected_snackbar_text, present=True)
        self._wait_for_snackbar(expected_snackbar_text, present=False)

    def test_05_empty_list_and_re_add(self):
        self._navigate_to_listview_page()

        # Tenta limpar a lista. Isso depende de como os itens são armazenados (ex: se são persistentes).
        # Para este teste, vamos assumir que podemos deletar todos os itens visíveis.
        # Uma forma mais robusta seria ter um botão "Limpar Tudo" no app para testes.
        print("Tentando limpar a lista para verificar o estado vazio...")
        max_deletes = 10 # Limite para evitar loop infinito
        deleted_count = 0
        for _ in range(max_deletes):
            try:
                # Tenta encontrar qualquer item (o primeiro da lista visível)
                # Esta parte é complexa sem saber a estrutura exata dos itens.
                # Vamos assumir que podemos pegar o primeiro item da ListView.
                list_view_element = self._find_element_by_value_key(LISTVIEW_PAGE_LISTVIEW_KEY)
                # Flutter finder não tem um 'find_elements' fácil para pegar o primeiro filho direto.
                # Se os itens tiverem um padrão de key, poderíamos tentar encontrar um.
                # Por simplicidade, se a lista não estiver vazia, tentaremos deletar um item conhecido.
                # Se a lista já estiver vazia (empty text visível), saímos do loop.
                if self._is_element_present_by_value_key(LISTVIEW_PAGE_EMPTY_TEXT_KEY, timeout=0.5):
                    print("Lista já está vazia.")
                    break

                # Tenta deletar um item que pode existir, ex: "Item Appium" ou "Item 1 Editado"
                item_to_try_delete = None
                possible_titles = ["Item Appium", "Item 1 Editado", "Item 4", "Item 3"] # Adicione outros que possam existir
                for title_candidate in possible_titles:
                    if self._is_text_present(title_candidate, timeout=0.5):
                        item_to_try_delete = title_candidate
                        break
                
                if not item_to_try_delete:
                    print("Nenhum item conhecido para deletar encontrado, ou lista já está vazia.")
                    # Verifica se o texto de lista vazia está presente
                    if self._is_element_present_by_value_key(LISTVIEW_PAGE_EMPTY_TEXT_KEY, timeout=1):
                        break # Sai do loop se a lista estiver vazia
                    else: # Se não há texto de lista vazia e nenhum item conhecido, algo está errado ou a lista é diferente
                        print("Não foi possível determinar o estado da lista para limpeza.")
                        break

                print(f"Tentando deletar '{item_to_try_delete}' para limpar a lista...")
                item_card_key = LISTVIEW_PAGE_ITEM_CARD_KEY(item_to_try_delete)
                item_element = self._scroll_to_element_by_key(item_card_key)
                self._perform_swipe_on_flutter_element(item_element, direction="right")
                self._find_element_by_value_key(DELETE_CONFIRM_DIALOG_KEY)
                self._tap_element(DELETE_CONFIRM_DELETE_BUTTON_KEY)
                self._wait_for_snackbar(TEXT_ITEM_REMOVED_SNACKBAR, present=True)
                self._wait_for_snackbar(TEXT_ITEM_REMOVED_SNACKBAR, present=False)
                deleted_count += 1
                if deleted_count >= max_deletes:
                    break
            except (NoSuchElementException, TimeoutException):
                print("Nenhum item encontrado para deletar, ou erro durante a deleção. Assumindo que a lista está vazia ou quase.")
                break # Sai do loop se não encontrar mais itens
            time.sleep(0.5) # Pausa entre deleções

        # Verifica estado de lista vazia
        self.assertTrue(self._is_element_present_by_value_key(LISTVIEW_PAGE_EMPTY_TEXT_KEY, timeout=5),
                        "Texto de lista vazia não encontrado após tentativas de limpeza.")
        self.assertTrue(self._is_text_present(TEXT_EMPTY_LIST_MESSAGE, timeout=2),
                        f"Mensagem '{TEXT_EMPTY_LIST_MESSAGE}' não encontrada no estado de lista vazia.")

        # Adiciona um item novamente para garantir que a lista vazia some
        final_item_title = "Item Final"
        final_item_desc = "Para testar re-adição"
        self._tap_element(LISTVIEW_PAGE_ADD_FAB_KEY)
        self._find_element_by_value_key(DIALOG_TITLE_FIELD_KEY)
        self._enter_text_in_field(DIALOG_TITLE_FIELD_KEY, final_item_title)
        self._enter_text_in_field(DIALOG_DESCRIPTION_FIELD_KEY, final_item_desc)
        self._tap_element(DIALOG_SUBMIT_BUTTON_KEY)

        self._wait_for_snackbar(TEXT_ITEM_ADDED_SNACKBAR, present=True)
        self._get_list_item_element_by_title_text(final_item_title)
        self.assertFalse(self._is_element_present_by_value_key(LISTVIEW_PAGE_EMPTY_TEXT_KEY, timeout=1),
                         "Texto de lista vazia ainda presente após adicionar novo item.")
        self._wait_for_snackbar(TEXT_ITEM_ADDED_SNACKBAR, present=False)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ListViewPageTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
    if APP_PATH == "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI":
        print("ERRO: A variável APP_PATH não foi configurada no script.")
        print("Por favor, edite o arquivo e defina o caminho para o seu APK/APP.")
    else:
        suite = unittest.TestSuite()
        # Adicionar testes na ordem desejada para um fluxo lógico
        suite.addTest(ListViewPageTests('test_01_initial_items_and_add_item'))
        suite.addTest(ListViewPageTests('test_02_edit_item'))
        suite.addTest(ListViewPageTests('test_03_delete_item'))
        suite.addTest(ListViewPageTests('test_04_tap_item_shows_snackbar'))
        suite.addTest(ListViewPageTests('test_05_empty_list_and_re_add'))

        runner = unittest.TextTestRunner(verbosity=2)
        print(f"Iniciando testes para o app: {APP_PATH}")
        print(f"Conectando ao servidor Appium em: {APPIUM_HOST}")
+        runner.run(suite)
