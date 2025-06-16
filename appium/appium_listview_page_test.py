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
# ATENÇÃO: Atualize este caminho para o local do seu arquivo APK.
APP_PATH = os.path.abspath('D:\\repos\\appium_and_flutter_test\\build\\app\\outputs\\flutter-apk\\app-debug.apk')
# Verifique se o caminho acima está correto antes de executar.
# Exemplo de verificação:
if not os.path.exists(APP_PATH):
    # Se o caminho padrão não existir, use um placeholder para evitar erro na inicialização.
    # O script principal ainda vai impedir a execução se o placeholder for usado.
    APP_PATH = "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI"

# --- Chaves dos Elementos Flutter (ValueKeys) ---
# LoginPage
LOGIN_USERNAME_FIELD_KEY = 'login_username_field'
LOGIN_PASSWORD_FIELD_KEY = 'login_password_field'
LOGIN_BUTTON_KEY = 'login_button'

# HomePage
HOME_PAGE_APPBAR_TITLE_KEY = 'home_page_app_bar_title'
HOME_PAGE_LISTVIEW_BUTTON_KEY = 'home_page_list_view_button'

# ListViewPage
LISTVIEW_PAGE_APPBAR_TITLE_KEY = 'list_view_page_app_bar_title'
LISTVIEW_PAGE_LISTVIEW_KEY = 'list_view_page_list_view'
LISTVIEW_PAGE_ADD_FAB_KEY = 'list_view_page_add_fab'
LISTVIEW_PAGE_EMPTY_TEXT_KEY = 'list_view_page_empty_text'

# Chaves para itens da lista
LISTVIEW_PAGE_ITEM_CARD_KEY = lambda title: f'list_item_card_{title.replace(" ", "_")}'
LISTVIEW_PAGE_ITEM_EDIT_ACTION_KEY = lambda title: f'list_item_edit_action_{title.replace(" ", "_")}'
LISTVIEW_PAGE_ITEM_DELETE_ACTION_KEY = lambda title: f'list_item_delete_action_{title.replace(" ", "_")}'

# Diálogo de Adicionar/Editar Item
DIALOG_TITLE_FIELD_KEY = 'dialog_title_field'
DIALOG_DESCRIPTION_FIELD_KEY = 'dialog_description_field'
DIALOG_SUBMIT_BUTTON_KEY = 'dialog_submit_button'
DIALOG_CANCEL_BUTTON_KEY = 'dialog_cancel_button'

# Diálogo de Confirmação de Exclusão
DELETE_CONFIRM_DIALOG_KEY = 'delete_confirm_dialog'
DELETE_CONFIRM_DELETE_BUTTON_KEY = 'delete_confirm_dialog_delete_button'
DELETE_CONFIRM_DIALOG_CANCEL_BUTTON_KEY = 'delete_confirm_dialog_cancel_button'

# --- Textos para Validação ---
TEXT_ITEM_ADDED_SNACKBAR = "Novo item adicionado!"
TEXT_ITEM_UPDATED_SNACKBAR = "Item atualizado!"
TEXT_ITEM_REMOVED_SNACKBAR = "Item removido!"
TEXT_ITEM_SELECTED_SNACKBAR_PREFIX = "Item selecionado: "
TEXT_VALIDATION_TITLE_EMPTY = "O título não pode estar vazio"
TEXT_VALIDATION_DESCRIPTION_EMPTY = "A descrição não pode estar vazia"
TEXT_EMPTY_LIST_MESSAGE = "Nenhum item na lista."

class ListViewPageTests(unittest.TestCase):
    driver: webdriver.Remote
    wait: WebDriverWait
    finder: FlutterFinder

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
            'app': APP_PATH,  # Caminho para o APK/APP
            'newCommandTimeout': 180,
            'retryBackoffTime': 500,
            'maxRetryCount': 3,
        }
        options = AppiumOptions().load_capabilities(capabilities)

        cls.driver = webdriver.Remote(APPIUM_HOST, options=options)
        cls.wait = WebDriverWait(cls.driver, 30)
        cls.finder = FlutterFinder()

    @classmethod
    def tearDownClass(cls):
        """Encerra a sessão do driver após todos os testes."""
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()

    def setUp(self):
        """Executado antes de cada método de teste."""
        # Garante que o app está na tela inicial antes de cada teste
        # (Isso pode ser otimizado dependendo do fluxo)
        # self.driver.reset()
        pass

    def tearDown(self):
        """Executado após cada método de teste para limpeza."""
        # Esconde o teclado se estiver visível para não interferir no próximo teste.
        if self.driver.is_keyboard_shown():
            try:
                self.driver.hide_keyboard()
            except:
                pass  # Ignora se o comando falhar

    # --- Métodos Auxiliares ---

    def _find_element_by_value_key(self, key, timeout=10):
        element_finder = self.finder.by_value_key(key)
        return self.wait.until(EC.presence_of_element_located((AppiumBy.FLUTTER, element_finder)),
                               message=f"Elemento com a chave '{key}' não foi encontrado no tempo de {timeout}s.")

    def _tap_element(self, element_or_key):
        """Toca em um elemento, seja o próprio elemento ou sua chave (key)."""
        if isinstance(element_or_key, str):
            element = self._find_element_by_value_key(element_or_key)
        else:
            element = element_or_key
        element.click()
        time.sleep(0.5) # Pausa curta para a UI reagir

    def _fill_text_field(self, key, text):
        element = self._find_element_by_value_key(key)
        element.send_keys(text)

    def _is_element_present_by_value_key(self, key, timeout=3):
        try:
            self._find_element_by_value_key(key, timeout)
            return True
        except TimeoutException:
            return False

    def _is_text_present(self, text, timeout=5):
        try:
            text_finder = self.finder.by_text(text)
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.FLUTTER, text_finder))
            )
            return True
        except TimeoutException:
            return False

    def _wait_for_snackbar(self, message, timeout=5, present=True):
        """Espera um snackbar aparecer ou desaparecer."""
        try:
            if present:
                self.assertTrue(self._is_text_present(message, timeout),
                                f"O snackbar com a mensagem '{message}' não apareceu.")
            else: # Espera desaparecer
                WebDriverWait(self.driver, timeout).until_not(
                    EC.presence_of_element_located((AppiumBy.FLUTTER, self.finder.by_text(message)))
                )
        except TimeoutException:
            status = "aparecer" if present else "desaparecer"
            self.fail(f"Timeout esperando o snackbar '{message}' {status}.")

    def _scroll_to_element_by_key(self, item_key, list_view_key=LISTVIEW_PAGE_LISTVIEW_KEY):
        """Rola a lista até encontrar um elemento com a chave especificada."""
        item_finder = self.finder.by_value_key(item_key)
        list_finder = self.finder.by_value_key(list_view_key)
        self.driver.execute_script('flutter:scrollUntilVisible', list_finder, {'item': item_finder, 'dxScroll': 0, 'dyScroll': -400})
        return self._find_element_by_value_key(item_key)

    def _perform_swipe_on_flutter_element(self, element, direction="left", swipe_distance_ratio=0.5):
        """Executa um swipe horizontal em um elemento Flutter."""
        element_size = element.size
        element_location = element.location
        center_y = element_location['y'] + element_size['height'] / 2
        center_x = element_location['x'] + element_size['width'] / 2
        swipe_distance_pixels = element_size['width'] * swipe_distance_ratio

        start_x = center_x
        if direction == "left":
            end_x = center_x - swipe_distance_pixels
        elif direction == "right":
            end_x = center_x + swipe_distance_pixels
        else:
            self.fail(f"Direção de swipe '{direction}' não suportada.")

        self.driver.swipe(start_x, center_y, end_x, center_y, 400) # Duração de 400ms
        time.sleep(1) # Espera a animação do swipe terminar

    def _navigate_to_listview_page(self, username='admin', password='1234'):
        """Navega para a ListViewPage, realizando login se necessário."""
        time.sleep(1) # Pausa para estabilizar o app no início
        if self._is_element_present_by_value_key(LOGIN_USERNAME_FIELD_KEY, timeout=3):
            print("Tela de login detectada. Realizando login...")
            self._fill_text_field(LOGIN_USERNAME_FIELD_KEY, username)
            self._fill_text_field(LOGIN_PASSWORD_FIELD_KEY, password)
            self._tap_element(LOGIN_BUTTON_KEY)
            # Espera a HomePage carregar
            self.assertTrue(self._is_element_present_by_value_key(HOME_PAGE_LISTVIEW_BUTTON_KEY, timeout=10))
            self._tap_element(HOME_PAGE_LISTVIEW_BUTTON_KEY)
        # Confirma que estamos na página da lista
        self.assertTrue(self._is_element_present_by_value_key(LISTVIEW_PAGE_APPBAR_TITLE_KEY))

    # --- Testes ---

    def test_01_add_new_item(self):
        """Testa a adição de um novo item à lista."""
        self._navigate_to_listview_page()
        
        # Clica no botão de adicionar (FAB)
        self._tap_element(LISTVIEW_PAGE_ADD_FAB_KEY)

        # Preenche o formulário de adição
        new_title = "Novo Item Teste"
        new_desc = "Descrição do item via Appium"
        self._fill_text_field(DIALOG_TITLE_FIELD_KEY, new_title)
        self._fill_text_field(DIALOG_DESCRIPTION_FIELD_KEY, new_desc)
        self._tap_element(DIALOG_SUBMIT_BUTTON_KEY)

        # Verifica se o snackbar de sucesso apareceu
        self._wait_for_snackbar(TEXT_ITEM_ADDED_SNACKBAR, present=True)
        
        # Verifica se o novo item está na lista (rolando até ele)
        item_key = LISTVIEW_PAGE_ITEM_CARD_KEY(new_title)
        item_element = self._scroll_to_element_by_key(item_key)
        self.assertIsNotNone(item_element, "O item adicionado não foi encontrado na lista.")
        self._wait_for_snackbar(TEXT_ITEM_ADDED_SNACKBAR, present=False) # Espera o snackbar sumir

    def test_02_edit_item(self):
        """Testa a edição de um item existente."""
        self._navigate_to_listview_page()

        item_to_edit_original_title = "Novo Item Teste" # Item adicionado no teste anterior
        edited_title = "Item Editado"
        edited_desc = "Descrição alterada pelo Appium"
        
        # Rola até o item e clica para editar (assumindo que o clique abre a edição)
        item_card_key = LISTVIEW_PAGE_ITEM_CARD_KEY(item_to_edit_original_title)
        item_element = self._scroll_to_element_by_key(item_card_key)
        self._tap_element(item_element) # Assumindo que o toque no card abre o diálogo de edição

        # Edita os campos no diálogo
        self._fill_text_field(DIALOG_TITLE_FIELD_KEY, edited_title)
        self._fill_text_field(DIALOG_DESCRIPTION_FIELD_KEY, edited_desc)
        self._tap_element(DIALOG_SUBMIT_BUTTON_KEY)

        # Verifica o snackbar de atualização
        self._wait_for_snackbar(TEXT_ITEM_UPDATED_SNACKBAR, present=True)

        # Verifica se o item com o novo título está presente
        edited_item_key = LISTVIEW_PAGE_ITEM_CARD_KEY(edited_title)
        edited_item_element = self._scroll_to_element_by_key(edited_item_key)
        self.assertIsNotNone(edited_item_element, "O item editado não foi encontrado na lista.")

        # Verifica se o item com o título antigo não existe mais
        self.assertFalse(self._is_element_present_by_value_key(item_card_key, timeout=2),
                         "O item com o título original ainda existe após a edição.")
        self._wait_for_snackbar(TEXT_ITEM_UPDATED_SNACKBAR, present=False)

    def test_03_delete_item_via_swipe(self):
        """Testa a exclusão de um item usando swipe e diálogo de confirmação."""
        self._navigate_to_listview_page()

        item_to_delete_title = "Item Editado" # Item do teste anterior
        
        item_card_key = LISTVIEW_PAGE_ITEM_CARD_KEY(item_to_delete_title)
        item_element = self._scroll_to_element_by_key(item_card_key)

        # Executa swipe para revelar a opção de deletar (ou abrir o diálogo)
        self._perform_swipe_on_flutter_element(item_element, direction="left")

        # Se o swipe revela um botão "Deletar", clique nele.
        # Se abre o diálogo diretamente, pule a próxima linha.
        # Ex: self._tap_element(LISTVIEW_PAGE_ITEM_DELETE_ACTION_KEY(item_to_delete_title))

        # Confirma a exclusão no diálogo
        self.assertTrue(self._is_element_present_by_value_key(DELETE_CONFIRM_DIALOG_KEY),
                        "Diálogo de confirmação de exclusão não apareceu.")
        self._tap_element(DELETE_CONFIRM_DELETE_BUTTON_KEY)

        # Verifica o snackbar de remoção
        self._wait_for_snackbar(TEXT_ITEM_REMOVED_SNACKBAR, present=True)

        # Verifica se o item foi removido da lista
        self.assertFalse(self._is_element_present_by_value_key(item_card_key, timeout=3),
                         "O item deletado ainda foi encontrado na lista.")
        self._wait_for_snackbar(TEXT_ITEM_REMOVED_SNACKBAR, present=False)

    def test_04_empty_list_message(self):
        """Verifica se a mensagem de lista vazia é exibida corretamente."""
        self._navigate_to_listview_page()
        
        # Assume-se que a lista está vazia após o teste de exclusão.
        # Se não, adicione um passo para limpar a lista aqui.
        
        # Verifica se a mensagem de lista vazia está presente
        self.assertTrue(self._is_text_present(TEXT_EMPTY_LIST_MESSAGE),
                        "A mensagem de lista vazia não foi encontrada.")
        
        # Verifica se o widget com a key de lista vazia está presente
        self.assertTrue(self._is_element_present_by_value_key(LISTVIEW_PAGE_EMPTY_TEXT_KEY),
                        "O widget com a chave de texto de lista vazia não foi encontrado.")

if __name__ == '__main__':
    if "COLOQUE_O_CAMINHO_PARA_SEU_APP_AQUI" in APP_PATH:
        print("="*60)
        print("ERRO: A variável APP_PATH não foi configurada no script.")
        print(f"Por favor, edite o arquivo '{__file__}' e defina o caminho correto para o seu APK.")
        print("="*60)
    else:
        print(f"Iniciando testes da ListViewPage para o app: {APP_PATH}")
        print(f"Conectando ao servidor Appium em: {APPIUM_HOST}...")

        # Cria a suíte de testes na ordem de execução desejada
        suite = unittest.TestSuite()
        suite.addTest(ListViewPageTests('test_01_add_new_item'))
        suite.addTest(ListViewPageTests('test_02_edit_item'))
        suite.addTest(ListViewPageTests('test_03_delete_item_via_swipe'))
        suite.addTest(ListViewPageTests('test_04_empty_list_message'))

        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)