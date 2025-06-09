import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/click_page.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Testes de Integração da ClickPage', () {
    testWidgets('Interage com double tap e long press cards exibindo alertas', (
      WidgetTester tester,
    ) async {
      // Inicia o app.
      // Certifique-se de que seu app/main.dart esteja configurado para exibir
      // a ClickPage ou que haja navegação para ela.
      app.main();
      await tester.pumpAndSettle();

      // --- Teste do Card de Duplo Clique ---
      final doubleTapCardFinder = find.byKey(ClickPage.doubleTapCardKey);
      expect(
        doubleTapCardFinder,
        findsOneWidget,
        reason: "Card de duplo clique não encontrado",
      );

      // Realiza o duplo clique
      await tester.doubleTap(doubleTapCardFinder);
      await tester.pumpAndSettle(); // Aguarda o diálogo aparecer

      // Verifica se o AlertDialog de duplo clique apareceu
      expect(
        find.byKey(ClickPage.alertDialogKey),
        findsOneWidget,
        reason: "AlertDialog de duplo clique não apareceu",
      );
      expect(
        find.text('Duplo Clique!'),
        findsOneWidget,
        reason: "Título do alerta de duplo clique incorreto",
      );
      expect(
        find.text('Você clicou duas vezes neste card.'),
        findsOneWidget,
        reason: "Conteúdo do alerta de duplo clique incorreto",
      );

      // Fecha o AlertDialog
      await tester.tap(find.byKey(ClickPage.alertDialogOkButtonKey));
      await tester.pumpAndSettle(); // Aguarda o diálogo desaparecer

      // Verifica se o AlertDialog desapareceu
      expect(
        find.byKey(ClickPage.alertDialogKey),
        findsNothing,
        reason: "AlertDialog de duplo clique não desapareceu",
      );

      // --- Teste do Card de Clique Longo ---
      final longPressCardFinder = find.byKey(ClickPage.longPressCardKey);
      expect(
        longPressCardFinder,
        findsOneWidget,
        reason: "Card de clique longo não encontrado",
      );

      // Realiza o clique longo
      await tester.longPress(longPressCardFinder);
      await tester.pumpAndSettle(); // Aguarda o diálogo aparecer

      // Verifica se o AlertDialog de clique longo apareceu
      expect(
        find.byKey(ClickPage.alertDialogKey),
        findsOneWidget,
        reason: "AlertDialog de clique longo não apareceu",
      );
      expect(
        find.text('Clique Longo!'),
        findsOneWidget,
        reason: "Título do alerta de clique longo incorreto",
      );
      expect(
        find.text('Você pressionou e segurou este card.'),
        findsOneWidget,
        reason: "Conteúdo do alerta de clique longo incorreto",
      );

      // Fecha o AlertDialog
      await tester.tap(find.byKey(ClickPage.alertDialogOkButtonKey));
      await tester.pumpAndSettle(); // Aguarda o diálogo desaparecer

      // Verifica se o AlertDialog desapareceu
      expect(
        find.byKey(ClickPage.alertDialogKey),
        findsNothing,
        reason: "AlertDialog de clique longo não desapareceu",
      );
    });
  });
}
