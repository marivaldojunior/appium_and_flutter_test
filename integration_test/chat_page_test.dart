import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/chat_page.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Testes de Integração da ChatPage', () {
    // Predicado para encontrar o contêiner principal de um item de mensagem
    final messageItemContainerFinderPredicate = (Widget widget) {
      if (widget is! Container ||
          widget.key == null ||
          widget.key is! ValueKey) {
        return false;
      }
      final valueKey = widget.key as ValueKey;
      final keyValueString = valueKey.value.toString();
      return keyValueString.startsWith(ChatPage.messageItemPrefixKey) &&
          !keyValueString.endsWith(ChatPage.messageContentSuffixKey) &&
          !keyValueString.endsWith(ChatPage.messageDeleteButtonSuffixKey) &&
          !keyValueString.endsWith(ChatPage.messagePlayPauseButtonSuffixKey);
    };

    testWidgets('Exibe mensagens iniciais, envia e exclui mensagens, interage com áudio', (
      WidgetTester tester,
    ) async {
      // Inicia o app
      app.main();
      await tester.pumpAndSettle();

      // Verifica se a ChatPage está sendo exibida (ajuste se houver navegação)

      // 1. Verifica mensagens iniciais
      expect(find.byKey(ChatPage.chatListViewKey), findsOneWidget);
      expect(find.text("Olá! Como você está?"), findsOneWidget);
      expect(find.text("Estou bem, obrigado! E você?"), findsOneWidget);
      // A terceira mensagem inicial é um áudio, que exibe o texto "Áudio"
      expect(
        find.descendant(
          of: find.byWidgetPredicate(messageItemContainerFinderPredicate).at(2),
          matching: find.text("Áudio"),
        ),
        findsOneWidget,
      );
      expect(
        find.byWidgetPredicate(messageItemContainerFinderPredicate),
        findsNWidgets(3),
        reason: "Deveria haver 3 mensagens iniciais",
      );

      // 2. Envia uma mensagem de texto
      const String mensagemDeTextoEnviada = 'Olá do teste!';
      await tester.enterText(
        find.byKey(ChatPage.messageTextFieldKey),
        mensagemDeTextoEnviada,
      );
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(ChatPage.sendTextButtonKey));
      await tester.pumpAndSettle(
        const Duration(seconds: 3),
      ); // Aguarda mensagem e resposta simulada

      // Verifica se a mensagem enviada e a resposta são exibidas
      expect(find.text(mensagemDeTextoEnviada), findsOneWidget);
      expect(find.text("Entendido: '$mensagemDeTextoEnviada'"), findsOneWidget);
      expect(
        find.byWidgetPredicate(messageItemContainerFinderPredicate),
        findsNWidgets(3 + 2),
        reason: "Deveria haver 5 mensagens após envio de texto e resposta",
      );

      // 3. Envia uma mensagem de áudio
      await tester.tap(find.byKey(ChatPage.sendAudioButtonKey));
      await tester.pumpAndSettle(
        const Duration(seconds: 3),
      ); // Aguarda mensagem e resposta simulada

      // Verifica se a mensagem de áudio (placeholder "Mensagem de áudio" e depois "Áudio" no bubble) e a resposta são exibidas
      // O texto "Mensagem de áudio" é o `message.text`, mas o widget exibe "Áudio"
      expect(find.text("Áudio"), findsNWidgets(2)); // Uma inicial, uma enviada
      expect(find.text("Recebi seu áudio!"), findsOneWidget);
      expect(
        find.byWidgetPredicate(messageItemContainerFinderPredicate),
        findsNWidgets(5 + 2),
        reason: "Deveria haver 7 mensagens após envio de áudio e resposta",
      );

      // 4. Exclui a mensagem de texto enviada
      final sentTextMessageContentFinder = find.text(mensagemDeTextoEnviada);
      expect(sentTextMessageContentFinder, findsOneWidget);

      final messageItemContainerForSentText = find.ancestor(
        of: sentTextMessageContentFinder,
        matching: find.byWidgetPredicate(messageItemContainerFinderPredicate),
      );
      expect(
        messageItemContainerForSentText,
        findsOneWidget,
        reason:
            "Não foi possível encontrar o contêiner do item da mensagem para '$mensagemDeTextoEnviada'",
      );

      final deleteButtonForSentTextMessage = find.descendant(
        of: messageItemContainerForSentText,
        matching: find.byTooltip("Excluir mensagem"),
      );
      expect(
        deleteButtonForSentTextMessage,
        findsOneWidget,
        reason:
            "Não foi possível encontrar o botão de excluir para '$mensagemDeTextoEnviada'",
      );
      await tester.tap(deleteButtonForSentTextMessage);
      await tester.pumpAndSettle();

      expect(find.text(mensagemDeTextoEnviada), findsNothing);
      expect(
        find.byWidgetPredicate(messageItemContainerFinderPredicate),
        findsNWidgets(7 - 1),
        reason: "Deveria haver 6 mensagens após excluir uma",
      );

      // 5. Reproduz/Pausa a mensagem de áudio enviada
      // A mensagem de áudio enviada exibirá "Áudio". Será a segunda com este texto.
      // Vamos encontrar o item da mensagem de áudio que é do remetente (isSender: true)
      // O item de áudio enviado é o mais recente, provavelmente o último ou penúltimo na lista.
      // Para simplificar, vamos pegar o último item que contém "Áudio" e é do remetente.
      // O botão de play/pause está dentro do item que contém o texto "Áudio".

      // Encontra o item da mensagem de áudio enviada (a segunda que aparece com "Áudio")
      // Esta é uma forma de pegar o segundo widget "Áudio" e seu contêiner.
      final sentAudioMessageTextWidgets = tester.widgetList<Text>(
        find.text("Áudio"),
      );
      expect(
        sentAudioMessageTextWidgets.length,
        greaterThanOrEqualTo(1),
        reason: "Pelo menos uma mensagem de áudio deveria existir",
      );

      // Assumindo que a última mensagem de "Áudio" é a que enviamos e queremos testar.
      // Se a ordem for garantida (novas mensagens no final), isto é razoável.
      final sentAudioMessageContentFinder = find
          .text("Áudio")
          .at(
            sentAudioMessageTextWidgets.length - 1,
          ); // Pega a última mensagem "Áudio"

      final messageItemContainerForSentAudio = find.ancestor(
        of: sentAudioMessageContentFinder,
        matching: find.byWidgetPredicate(messageItemContainerFinderPredicate),
      );
      expect(
        messageItemContainerForSentAudio,
        findsOneWidget,
        reason:
            "Não foi possível encontrar o contêiner do item para a mensagem de áudio enviada",
      );

      // Estado inicial: Botão de Play deve estar visível
      final playButtonForSentAudio = find.descendant(
        of: messageItemContainerForSentAudio,
        matching: find.byIcon(Icons.play_circle_filled),
      );
      expect(
        playButtonForSentAudio,
        findsOneWidget,
        reason: "Botão de Play não encontrado para a mensagem de áudio enviada",
      );
      await tester.tap(playButtonForSentAudio);
      await tester.pumpAndSettle();

      // Após o toque: Botão de Pause deve estar visível
      final pauseButtonForSentAudio = find.descendant(
        of: messageItemContainerForSentAudio,
        matching: find.byIcon(Icons.pause_circle_filled),
      );
      expect(
        pauseButtonForSentAudio,
        findsOneWidget,
        reason: "Botão de Pause não encontrado após tocar em play",
      );

      // Toca no botão de Pause
      await tester.tap(pauseButtonForSentAudio);
      await tester.pumpAndSettle();

      // Após o toque: Botão de Play deve estar visível novamente
      expect(
        playButtonForSentAudio,
        findsOneWidget,
        reason: "Botão de Play não encontrado após tocar em pause",
      );

      // 6. Exclui a mensagem de áudio inicial
      // A mensagem de áudio inicial é a primeira que exibe "Áudio".
      final initialAudioMessageContentFinder = find.text("Áudio").first;
      final initialAudioMessageItemContainer = find.ancestor(
        of: initialAudioMessageContentFinder,
        matching: find.byWidgetPredicate(messageItemContainerFinderPredicate),
      );
      expect(
        initialAudioMessageItemContainer,
        findsOneWidget,
        reason:
            "Não foi possível encontrar o contêiner do item para a mensagem de áudio inicial",
      );

      final deleteButtonForInitialAudio = find.descendant(
        of: initialAudioMessageItemContainer,
        matching: find.byTooltip("Excluir mensagem"),
      );
      expect(
        deleteButtonForInitialAudio,
        findsOneWidget,
        reason: "Botão de excluir para áudio inicial não encontrado",
      );
      await tester.tap(deleteButtonForInitialAudio);
      await tester.pumpAndSettle();

      // Verifica se foi excluída (contagem total de mensagens diminui)
      expect(
        find.byWidgetPredicate(messageItemContainerFinderPredicate),
        findsNWidgets(6 - 1),
        reason: "Deveria haver 5 mensagens após excluir o áudio inicial",
      );
      // Agora deve haver apenas uma mensagem "Áudio" (a que foi enviada)
      expect(find.text("Áudio"), findsOneWidget);
    });
  });
}
