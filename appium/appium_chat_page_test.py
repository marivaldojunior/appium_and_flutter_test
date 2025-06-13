# d:\repos\appium_and_flutter_test\integration_test\chat_page_test.py
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

# LoginPage (assumindo IDs de exemplos anteriores)
LOC_LOGIN_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "usernameField_LoginPage_ACCESSIBILITY_ID")
LOC_USERNAME_FIELD = (AppiumBy.ACCESSIBILITY_ID, "usernameField")
LOC_PASSWORD_FIELD = (AppiumBy.ACCESSIBILITY_ID, "passwordField")
LOC_LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "loginButton")

# HomePage (assumindo IDs de exemplos anteriores)
LOC_HOME_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "homePageElement_HomePage_ACCESSIBILITY_ID")
LOC_CHAT_BUTTON_ON_HOME = (AppiumBy.ACCESSIBILITY_ID, "homePage.chatButtonKey_ACCESSIBILITY_ID") # Do home_page_test

# ChatPage
LOC_CHAT_PAGE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "chatPage.chatListViewKey_ACCESSIBILITY_ID") # Elemento único da ChatPage, ex: a ListView
LOC_CHAT_LISTVIEW = (AppiumBy.ACCESSIBILITY_ID, "chatPage.chatListViewKey_ACCESSIBILITY_ID")
LOC_MESSAGE_TEXT_FIELD = (AppiumBy.ACCESSIBILITY_ID, "chatPage.messageTextFieldKey_ACCESSIBILITY_ID")
LOC_SEND_TEXT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "chatPage.sendTextButtonKey_ACCESSIBILITY_ID")
LOC_SEND_AUDIO_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "chatPage.sendAudioButtonKey_ACCESSIBILITY_ID")

# Localizador genérico para um contêiner de item de mensagem (bolha de chat)
# Este é o equivalente ao 'messageItemContainerFinderPredicate'.
# Pode ser um XPath baseado em uma classe comum, resource-id parcial, ou accessibility_id parcial se aplicável.
# Exemplo: (AppiumBy.XPATH, "//*[@resource-id='com.seuapp.pacote:id/message_bubble_container']")
# Ou se as keys do Flutter forem expostas: (AppiumBy.XPATH, "//*[starts-with(@content-desc, 'message_item_')]")
LOC_MESSAGE_ITEM_CONTAINER = (AppiumBy.XPATH, "//android.view.View[starts-with(@content-desc, 'message_item_') and not(ends-with(@content-desc, '_content')) and not(ends-with(@content-desc, '_delete_button')) and not(ends-with(@content-desc, '_play_pause_button'))]")


# Localizadores para elementos DENTRO de um item de mensagem (usar com find_element a partir do container)
# O tooltip "Excluir mensagem" provavelmente se torna um content-desc ou accessibility_id
LOC_MESSAGE_DELETE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Excluir mensagem") # Ou XPath como ".//android.widget.ImageView[@content-desc='Excluir mensagem']"
LOC_MESSAGE_PLAY_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "play_button_accessibility_id") # Ou XPath para o ícone de play
LOC_MESSAGE_PAUSE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "pause_button_accessibility_id") # Ou XPath para o ícone de pause

# Textos (para encontrar mensagens específicas ou verificar conteúdo)
TEXT_INITIAL_MSG_1 = "Olá! Como você está?"
TEXT_INITIAL_MSG_2 = "Estou bem, obrigado! E você?"
TEXT_AUDIO_PLACEHOLDER = "Áudio" # Texto exibido para mensagens de áudio
TEXT_SIMULATED_AUDIO_REPLY = "Recebi seu áudio!"

XPATH_TEXT_CONTAINS_TEMPLATE = "//*[contains(@text, \"{text}\") or contains(@content-desc, \"{text}\") or contains(@name, \"{text}\") or contains(@label, \"{text}\")]"
# --- FIM: PLACEHOLDERS DE LOCALIZADORES ---

class ChatPageTests(unittest.TestCase):
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

    def _find_elements_with_wait(self, locator, timeout=DEFAULT_WAIT_TIMEOUT, context=None):
        source = context or self.driver
        return WebDriverWait(source, timeout).until(EC.presence_of_all_elements_located(locator))
    
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

    def _navigate_to_chat_page(self, username='flutter', password='123456'):
        """Faz login (se necessário) e navega para a ChatPage."""
        time.sleep(1) # Pausa inicial

        if self._is_element_present(LOC_LOGIN_PAGE_INDICATOR, timeout=self.SHORT_WAIT_TIMEOUT):
            self._type_text_with_wait(LOC_USERNAME_FIELD, username)
            self._type_text_with_wait(LOC_PASSWORD_FIELD, password)
            self._click_element_with_wait(LOC_LOGIN_BUTTON)
            self._find_element_with_wait(LOC_HOME_PAGE_INDICATOR, timeout=self.LONG_WAIT_TIMEOUT)
            time.sleep(1)

        self.assertTrue(self._is_element_present(LOC_HOME_PAGE_INDICATOR), "Não foi possível alcançar a HomePage.")
        self._click_element_with_wait(LOC_CHAT_BUTTON_ON_HOME)
        self._find_element_with_wait(LOC_CHAT_PAGE_INDICATOR, timeout=self.LONG_WAIT_TIMEOUT)
        time.sleep(0.5)

    def _get_message_container_by_text(self, text_to_find, occurrence_index=0):
        """Encontra o contêiner de mensagem que contém um texto específico."""
        text_elements = self._find_elements_with_wait((AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=text_to_find)))
        if not text_elements or len(text_elements) <= occurrence_index:
            self.fail(f"Não foi possível encontrar a {occurrence_index+1}ª ocorrência do texto '{text_to_find}'.")
        
        target_text_element = text_elements[occurrence_index]
        
        # Tenta encontrar o ancestral que é um LOC_MESSAGE_ITEM_CONTAINER
        # Esta é uma forma simplificada. O XPath para ancestor pode ser mais específico.
        # Ex: target_text_element.find_element(AppiumBy.XPATH, "ancestor::*[@content-desc='message_item_...']")
        # Para um XPath genérico de ancestral que corresponda ao LOC_MESSAGE_ITEM_CONTAINER:
        # Supondo que LOC_MESSAGE_ITEM_CONTAINER[1] seja o XPath string
        ancestor_xpath_template = LOC_MESSAGE_ITEM_CONTAINER[1]
        # Precisamos de uma forma de dizer "o ancestral que corresponde a este XPath"
        # Uma forma é iterar pelos pais, mas é ineficiente.
        # Outra é usar um XPath mais complexo:
        # xpath_for_container = f"{ancestor_xpath_template}[.//{XPATH_TEXT_CONTAINS_TEMPLATE.format(text=text_to_find)}]"
        # E então pegar o elemento correto se houver múltiplos.

        # Abordagem mais simples: assumir que o LOC_MESSAGE_ITEM_CONTAINER é um ancestral direto ou próximo.
        # E que o `target_text_element` está DENTRO de um `LOC_MESSAGE_ITEM_CONTAINER`.
        # Vamos pegar todos os containers e ver qual contém o `target_text_element`.
        all_containers = self._find_elements_with_wait(LOC_MESSAGE_ITEM_CONTAINER)
        for container in all_containers:
            try:
                # Verifica se o target_text_element é um descendente deste container
                # Isto pode ser feito verificando se o `target_text_element` é encontrado *dentro* do `container`
                # Ou comparando localizações, o que é mais complexo.
                # Uma forma é verificar se o `target_text_element.id` é o mesmo que um elemento encontrado dentro do container.
                if container.find_element(AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=text_to_find)).id == target_text_element.id:
                    return container
            except NoSuchElementException:
                continue
        self.fail(f"Não foi possível encontrar o contêiner para o texto '{text_to_find}'.")


    # --- Test Method ---
    def test_chat_interactions(self):
        self._navigate_to_chat_page()

        # 1. Verifica mensagens iniciais
        self._find_element_with_wait(LOC_CHAT_LISTVIEW)
        self._wait_for_text_visibility(TEXT_INITIAL_MSG_1)
        self._wait_for_text_visibility(TEXT_INITIAL_MSG_2)

        all_message_containers = self._find_elements_with_wait(LOC_MESSAGE_ITEM_CONTAINER)
        self.assertEqual(len(all_message_containers), 3, "Deveria haver 3 mensagens iniciais.")

        # Verifica a terceira mensagem (áudio)
        third_message_container = all_message_containers[2]
        self._find_element_with_wait((AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=TEXT_AUDIO_PLACEHOLDER)), context=third_message_container)
        print("Mensagens iniciais verificadas.")

        # 2. Envia uma mensagem de texto
        mensagem_de_texto_enviada = 'Olá do teste Appium Python!'
        self._type_text_with_wait(LOC_MESSAGE_TEXT_FIELD, mensagem_de_texto_enviada)
        time.sleep(0.5) # Pequena pausa antes de clicar em enviar
        self._click_element_with_wait(LOC_SEND_TEXT_BUTTON)
        time.sleep(3) # Aguarda mensagem e resposta simulada (como no Flutter test)

        self._wait_for_text_visibility(mensagem_de_texto_enviada)
        self._wait_for_text_visibility(f"Entendido: '{mensagem_de_texto_enviada}'")
        
        current_message_count = len(self._find_elements_with_wait(LOC_MESSAGE_ITEM_CONTAINER))
        self.assertEqual(current_message_count, 3 + 2, "Deveria haver 5 mensagens após envio de texto e resposta.")
        print(f"Mensagem de texto '{mensagem_de_texto_enviada}' enviada e resposta recebida.")

        # 3. Envia uma mensagem de áudio
        self._click_element_with_wait(LOC_SEND_AUDIO_BUTTON)
        time.sleep(3) # Aguarda mensagem e resposta simulada

        # Verifica se a mensagem de áudio (placeholder "Áudio") e a resposta são exibidas
        # Deve haver 2x "Áudio" agora (1 inicial, 1 enviada)
        audio_placeholders = self._find_elements_with_wait((AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=TEXT_AUDIO_PLACEHOLDER)))
        self.assertEqual(len(audio_placeholders), 2, "Deveria haver duas mensagens 'Áudio'.")
        self._wait_for_text_visibility(TEXT_SIMULATED_AUDIO_REPLY)

        current_message_count = len(self._find_elements_with_wait(LOC_MESSAGE_ITEM_CONTAINER))
        self.assertEqual(current_message_count, 5 + 2, "Deveria haver 7 mensagens após envio de áudio e resposta.")
        print("Mensagem de áudio enviada e resposta recebida.")

        # 4. Exclui a mensagem de texto enviada
        # Precisamos de uma forma robusta de encontrar o container da mensagem específica
        # Se o LOC_MESSAGE_ITEM_CONTAINER for bem definido, e o texto for único:
        sent_text_message_container = self._get_message_container_by_text(mensagem_de_texto_enviada)
        
        self._click_element_with_wait(LOC_MESSAGE_DELETE_BUTTON, context=sent_text_message_container)
        time.sleep(1) # Aguarda a UI atualizar

        self.assertFalse(self._is_element_present((AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=mensagem_de_texto_enviada)), timeout=1),
                         "Mensagem de texto enviada não foi excluída.")
        current_message_count = len(self._find_elements_with_wait(LOC_MESSAGE_ITEM_CONTAINER))
        self.assertEqual(current_message_count, 7 - 1, "Deveria haver 6 mensagens após excluir uma.")
        print(f"Mensagem de texto '{mensagem_de_texto_enviada}' excluída.")

        # 5. Reproduz/Pausa a mensagem de áudio enviada
        # A mensagem de áudio enviada é a segunda que contém "Áudio".
        # Ou, se as mensagens são adicionadas no final, é a última mensagem de áudio.
        all_audio_containers = []
        all_containers = self._find_elements_with_wait(LOC_MESSAGE_ITEM_CONTAINER)
        for container in all_containers:
            if self._is_element_present((AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=TEXT_AUDIO_PLACEHOLDER)), context=container, timeout=0.5):
                all_audio_containers.append(container)
        
        self.assertGreaterEqual(len(all_audio_containers), 1, "Nenhuma mensagem de áudio encontrada para interagir.")
        sent_audio_message_container = all_audio_containers[-1] # Assume que a última é a enviada

        # Estado inicial: Botão de Play deve estar visível
        self._click_element_with_wait(LOC_MESSAGE_PLAY_BUTTON, context=sent_audio_message_container)
        time.sleep(0.5)

        # Após o toque: Botão de Pause deve estar visível
        self._find_element_with_wait(LOC_MESSAGE_PAUSE_BUTTON, context=sent_audio_message_container)
        self._click_element_with_wait(LOC_MESSAGE_PAUSE_BUTTON, context=sent_audio_message_container)
        time.sleep(0.5)

        # Após o toque: Botão de Play deve estar visível novamente
        self._find_element_with_wait(LOC_MESSAGE_PLAY_BUTTON, context=sent_audio_message_container)
        print("Interação Play/Pause da mensagem de áudio enviada verificada.")

        # 6. Exclui a mensagem de áudio inicial
        # A mensagem de áudio inicial é a primeira que exibe "Áudio".
        initial_audio_message_container = all_audio_containers[0]

        self._click_element_with_wait(LOC_MESSAGE_DELETE_BUTTON, context=initial_audio_message_container)
        time.sleep(1)

        current_message_count = len(self._find_elements_with_wait(LOC_MESSAGE_ITEM_CONTAINER))
        self.assertEqual(current_message_count, 6 - 1, "Deveria haver 5 mensagens após excluir o áudio inicial.")
        
        # Agora deve haver apenas uma mensagem "Áudio" (a que foi enviada e interagida)
        audio_placeholders_after_delete = self._find_elements_with_wait((AppiumBy.XPATH, XPATH_TEXT_CONTAINS_TEMPLATE.format(text=TEXT_AUDIO_PLACEHOLDER)))
        self.assertEqual(len(audio_placeholders_after_delete), 1, "Deveria restar apenas uma mensagem 'Áudio'.")
        print("Mensagem de áudio inicial excluída.")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ChatPageTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
