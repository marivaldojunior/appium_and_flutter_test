// test/integration/home_page_test.dart
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/chat_page.dart';
import 'package:appium_and_flutter_test/pages/click_page.dart';
import 'package:appium_and_flutter_test/pages/forms_page.dart';
import 'package:appium_and_flutter_test/pages/gestos_page.dart';
import 'package:appium_and_flutter_test/pages/home_page.dart';
import 'package:appium_and_flutter_test/pages/listview_page.dart';
import 'package:appium_and_flutter_test/pages/login_page.dart';
import 'package:appium_and_flutter_test/pages/recursos_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

// --- Constantes para os Testes ---
const String kCorrectUsername = 'admin';
const String kCorrectPassword = '1234';

// --- Funções Auxiliares de Teste ---

/// Garante um estado limpo, inicializando o app, fazendo login
/// e garantindo que a [HomePage] está visível.
Future<void> _initializeAppAndNavigateToHome(WidgetTester tester) async {
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

  expect(
    find.byType(HomePage),
    findsOneWidget,
    reason: "Deveria estar na HomePage após o login.",
  );
}

/// Testa um fluxo de navegação: toca em um botão, verifica a nova página,
/// e depois volta para a HomePage.
Future<void> _testNavigationPath(
  WidgetTester tester, {
  required Key buttonKey,
  required Type destinationPageType,
  required String pageName,
}) async {
  // Act: Navega para a página de destino.
  await tester.tap(find.byKey(buttonKey));
  await tester.pumpAndSettle();

  // Assert: Verifica se a página de destino foi carregada.
  expect(
    find.byType(destinationPageType),
    findsOneWidget,
    reason: "Deveria ter navegado para a $pageName.",
  );

  // Act: Volta para a página anterior.
  final navigator = tester.state<NavigatorState>(find.byType(Navigator));
  navigator.pop();
  await tester.pumpAndSettle();

  // Assert: Verifica se retornou para a HomePage.
  expect(
    find.byType(HomePage),
    findsOneWidget,
    reason: "Deveria ter retornado para a HomePage após sair da $pageName.",
  );
}

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Testes de Integração da HomePage', () {
    // Garante que cada teste comece em um estado limpo, com o app na HomePage.
    setUp(() async {
      // A inicialização é feita dentro de cada teste para garantir isolamento total.
    });

    testWidgets('Deve exibir os elementos da UI principal corretamente', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigateToHome(tester);

      // Assert
      expect(find.text('Menu Principal'), findsOneWidget);
      expect(find.byKey(HomePage.formsButtonKey), findsOneWidget);
      expect(find.byKey(HomePage.listViewButtonKey), findsOneWidget);
      expect(find.byKey(HomePage.logoutButtonKey), findsOneWidget);
    });

    // --- Testes de Navegação ---
    testWidgets('Deve navegar para a FormsPage e voltar', (
      WidgetTester tester,
    ) async {
      await _initializeAppAndNavigateToHome(tester);
      await _testNavigationPath(
        tester,
        buttonKey: HomePage.formsButtonKey,
        destinationPageType: FormsPage,
        pageName: "FormsPage",
      );
    });

    testWidgets('Deve navegar para a ListViewPage e voltar', (
      WidgetTester tester,
    ) async {
      await _initializeAppAndNavigateToHome(tester);
      await _testNavigationPath(
        tester,
        buttonKey: HomePage.listViewButtonKey,
        destinationPageType: ListViewPage,
        pageName: "ListViewPage",
      );
    });

    testWidgets('Deve navegar para a RecursosPage e voltar', (
      WidgetTester tester,
    ) async {
      await _initializeAppAndNavigateToHome(tester);
      await _testNavigationPath(
        tester,
        buttonKey: HomePage.nativeResourcesButtonKey,
        destinationPageType: RecursosPage,
        pageName: "RecursosPage",
      );
    });

    testWidgets('Deve navegar para a GestosPage e voltar', (
      WidgetTester tester,
    ) async {
      await _initializeAppAndNavigateToHome(tester);
      await _testNavigationPath(
        tester,
        buttonKey: HomePage.gesturesButtonKey,
        destinationPageType: GestosPage,
        pageName: "GestosPage",
      );
    });

    testWidgets('Deve navegar para a ClickPage e voltar', (
      WidgetTester tester,
    ) async {
      await _initializeAppAndNavigateToHome(tester);
      await _testNavigationPath(
        tester,
        buttonKey: HomePage.clickAndHoldButtonKey,
        destinationPageType: ClickPage,
        pageName: "ClickPage",
      );
    });

    testWidgets('Deve navegar para a ChatPage e voltar', (
      WidgetTester tester,
    ) async {
      await _initializeAppAndNavigateToHome(tester);
      await _testNavigationPath(
        tester,
        buttonKey: HomePage.chatButtonKey,
        destinationPageType: ChatPage,
        pageName: "ChatPage",
      );
    });

    // --- Testes de Logout ---
    testWidgets('Deve cancelar o logout e permanecer na HomePage', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigateToHome(tester);

      // Act: Abre e cancela o diálogo de logout.
      await tester.tap(find.byKey(HomePage.logoutButtonKey));
      await tester.pumpAndSettle();
      expect(find.byKey(HomePage.logoutDialogKey), findsOneWidget);
      await tester.tap(find.byKey(HomePage.logoutDialogCancelButtonKey));
      await tester.pumpAndSettle();

      // Assert
      expect(find.byKey(HomePage.logoutDialogKey), findsNothing);
      expect(find.byType(HomePage), findsOneWidget);
    });

    testWidgets('Deve confirmar o logout e navegar para a LoginPage', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigateToHome(tester);

      // Act: Abre e confirma o diálogo de logout.
      await tester.tap(find.byKey(HomePage.logoutButtonKey));
      await tester.pumpAndSettle();
      expect(find.byKey(HomePage.logoutDialogKey), findsOneWidget);
      await tester.tap(find.byKey(HomePage.logoutDialogConfirmButtonKey));
      await tester.pumpAndSettle();

      // Assert
      expect(find.byType(LoginPage), findsOneWidget);
      expect(find.byType(HomePage), findsNothing);
    });
  });
}
