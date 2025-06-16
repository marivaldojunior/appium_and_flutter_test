// test/integration/click_page_test.dart
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/click_page.dart';
import 'package:appium_and_flutter_test/pages/home_page.dart';
import 'package:appium_and_flutter_test/pages/login_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

// --- Constantes para os Testes ---
const String kCorrectUsername = 'admin';
const String kCorrectPassword = '1234';

// Mensagens de Alerta
const String kDoubleTapAlertTitle = 'Duplo Clique!';
const String kDoubleTapAlertContent = 'Você clicou duas vezes neste card.';
const String kLongPressAlertTitle = 'Clique Longo!';
const String kLongPressAlertContent = 'Você pressionou e segurou este card.';

// --- Funções Auxiliares de Teste ---

/// Garante um estado limpo, inicializando o app e navegando até a [ClickPage].
Future<void> _initializeAppAndNavigateToClick(WidgetTester tester) async {
  app.main();
  await tester.pumpAndSettle();

  if (tester.any(find.byType(LoginPage))) {
    await tester.enterText(
      find.byKey(LoginPage.usernameFieldKey),
      kCorrectUsername,
    );
    await tester.enterText(
      find.byKey(LoginPage.passwordFieldKey),
      kCorrectPassword,
    );
    await tester.tap(find.byKey(LoginPage.loginButtonKey));
    await tester.pumpAndSettle();
  }

  expect(find.byType(HomePage), findsOneWidget);
  await tester.tap(find.byKey(HomePage.clickAndHoldButtonKey));
  await tester.pumpAndSettle();
  expect(find.byType(ClickPage), findsOneWidget);
}

/// Testa um gesto em um card, verifica o alerta resultante e o fecha.
Future<void> _testGestureAndAlert(
  WidgetTester tester, {
  required Future<void> Function(Finder) gesture,
  required Key cardKey,
  required String alertTitle,
  required String alertContent,
}) async {
  // Act: Executa o gesto no card.
  final cardFinder = find.byKey(cardKey);
  expect(cardFinder, findsOneWidget);
  await gesture(cardFinder);
  await tester.pumpAndSettle();

  // Assert: Verifica se o diálogo de alerta é exibido corretamente.
  expect(find.byKey(ClickPage.alertDialogKey), findsOneWidget);
  expect(find.text(alertTitle), findsOneWidget);
  expect(find.text(alertContent), findsOneWidget);

  // Act: Fecha o diálogo.
  await tester.tap(find.byKey(ClickPage.alertDialogOkButtonKey));
  await tester.pumpAndSettle();

  // Assert: Verifica se o diálogo desapareceu.
  expect(find.byKey(ClickPage.alertDialogKey), findsNothing);
}

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Testes de Integração da ClickPage', () {
    // Garante que cada teste comece em um estado limpo.
    setUp(() async {
      // A inicialização será feita dentro de cada teste para garantir isolamento total.
    });

    testWidgets('Deve exibir um alerta ao realizar um duplo clique no card', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigateToClick(tester);

      // Act & Assert
      await _testGestureAndAlert(
        tester,
        // O método `tester.doubleTap(finder)` pode não estar disponível em algumas
        // versões. Esta abordagem manual com dois `tap` e um atraso
        // (`pump`) é uma alternativa mais explícita e robusta.
        gesture: (finder) async {
          await tester.tap(finder);
          // É necessário um pequeno atraso entre os toques para ser
          // reconhecido como um duplo clique.
          await tester.pump(const Duration(milliseconds: 100));
          await tester.tap(finder);
        },
        cardKey: ClickPage.doubleTapCardKey,
        alertTitle: kDoubleTapAlertTitle,
        alertContent: kDoubleTapAlertContent,
      );
    });

    testWidgets('Deve exibir um alerta ao realizar um clique longo no card', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigateToClick(tester);

      // Act & Assert
      await _testGestureAndAlert(
        tester,
        gesture: (finder) => tester.longPress(finder),
        cardKey: ClickPage.longPressCardKey,
        alertTitle: kLongPressAlertTitle,
        alertContent: kLongPressAlertContent,
      );
    });
  });
}
