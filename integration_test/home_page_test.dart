import 'package:appium_and_flutter_test/pages/chat_page.dart';
import 'package:appium_and_flutter_test/pages/click_page.dart';
import 'package:appium_and_flutter_test/pages/forms_page.dart';
import 'package:appium_and_flutter_test/pages/gestos_page.dart';
import 'package:appium_and_flutter_test/pages/listview_page.dart';
import 'package:appium_and_flutter_test/pages/login_page.dart';
import 'package:appium_and_flutter_test/pages/recursos_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/home_page.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  Future<void> navigateBack(WidgetTester tester) async {
    // Encontra o botão de voltar no AppBar (se existir)
    final NavigatorState navigator = tester.state(find.byType(Navigator));
    if (navigator.canPop()) {
      navigator.pop();
      await tester.pumpAndSettle();
    }
  }

  Future<void> ensureLoggedInAndOnHomePage(WidgetTester tester) async {
    app.main(); // Inicia o app
    await tester.pumpAndSettle(
      const Duration(seconds: 1),
    ); // Pequena espera inicial

    // Se o app inicia na LoginPage, faz o login
    if (tester.any(find.byType(LoginPage))) {
      await tester.enterText(
        find.byKey(LoginPage.usernameFieldKey),
        'admin', // Padronizando com outros testes
      );
      await tester.enterText(
        find.byKey(LoginPage.passwordFieldKey),
        '1234', // Padronizando com outros testes
      );
      await tester.tap(find.byKey(LoginPage.loginButtonKey));
      await tester.pumpAndSettle(
        const Duration(seconds: 3), // Aguarda navegação e SnackBar
      );
    }
    // Garante que a HomePage está carregada
    expect(
      find.byType(HomePage),
      findsOneWidget,
      reason: "HomePage não foi carregada após o login.",
    );
  }

  group('Testes de Integração da HomePage', () {
    testWidgets('Verifica elementos da UI e navegação para todas as seções', (
      WidgetTester tester,
    ) async {
      await ensureLoggedInAndOnHomePage(tester);

      // Garante que estamos na HomePage (caso algum teste anterior tenha navegado)
      // Se o setUpAll já garante isso, esta verificação pode ser redundante,
      // mas é bom para testes individuais.
      if (find.byType(HomePage).evaluate().isEmpty) {
        // Tenta voltar para a HomePage se não estiver nela
        final NavigatorState navigator = tester.state(find.byType(Navigator));
        while (navigator.canPop()) {
          navigator.pop();
          await tester.pumpAndSettle();
          if (find.byType(HomePage).evaluate().isNotEmpty) break;
        }
      }
      expect(
        find.byType(HomePage),
        findsOneWidget,
        reason: "Não está na HomePage no início do teste de navegação.",
      );

      // Verifica título do AppBar
      expect(find.text('Menu Principal'), findsOneWidget);

      // Navegação para Formulários
      await tester.tap(find.byKey(HomePage.formsButtonKey));
      await tester.pumpAndSettle();
      expect(find.byType(FormsPage), findsOneWidget);
      await navigateBack(tester);

      // Navegação para ListView
      await tester.tap(find.byKey(HomePage.listViewButtonKey));
      await tester.pumpAndSettle();
      expect(find.byType(ListViewPage), findsOneWidget);
      await navigateBack(tester);

      // Navegação para Recursos Nativos
      await tester.tap(find.byKey(HomePage.nativeResourcesButtonKey));
      await tester.pumpAndSettle();
      expect(find.byType(RecursosPage), findsOneWidget);
      await navigateBack(tester);

      // Navegação para Gestos na Tela
      await tester.tap(find.byKey(HomePage.gesturesButtonKey));
      await tester.pumpAndSettle();
      expect(find.byType(GestosPage), findsOneWidget);
      await navigateBack(tester);

      // Navegação para Clicar e Segurar
      await tester.tap(find.byKey(HomePage.clickAndHoldButtonKey));
      await tester.pumpAndSettle();
      expect(find.byType(ClickPage), findsOneWidget);
      await navigateBack(tester);

      // Navegação para Chat Simulado
      await tester.tap(find.byKey(HomePage.chatButtonKey));
      await tester.pumpAndSettle();
      expect(find.byType(ChatPage), findsOneWidget);
      await navigateBack(tester);

      // Verifica se voltou para a HomePage
      expect(find.byType(HomePage), findsOneWidget);
    });

    testWidgets('Testa funcionalidade de Logout (Cancelar e Confirmar)', (
      WidgetTester tester,
    ) async {
      await ensureLoggedInAndOnHomePage(tester);

      // Garante que estamos na HomePage
      if (find.byType(HomePage).evaluate().isEmpty) {
        final NavigatorState navigator = tester.state(find.byType(Navigator));
        while (navigator.canPop()) {
          navigator.pop();
          await tester.pumpAndSettle();
          if (find.byType(HomePage).evaluate().isNotEmpty) break;
        }
      }
      expect(
        find.byType(HomePage),
        findsOneWidget,
        reason: "Não está na HomePage no início do teste de logout.",
      );

      // 1. Tenta Logout e Cancela
      await tester.tap(find.byKey(HomePage.logoutButtonKey));
      await tester.pumpAndSettle(); // Aguarda o diálogo aparecer

      expect(find.byKey(HomePage.logoutDialogKey), findsOneWidget);
      expect(find.text('Confirmar Logout'), findsOneWidget);

      await tester.tap(find.byKey(HomePage.logoutDialogCancelButtonKey));
      await tester.pumpAndSettle(); // Aguarda o diálogo desaparecer

      expect(find.byKey(HomePage.logoutDialogKey), findsNothing);
      expect(
        find.byType(HomePage),
        findsOneWidget,
        reason: "Deveria permanecer na HomePage após cancelar o logout.",
      );

      // 2. Tenta Logout e Confirma
      await tester.tap(find.byKey(HomePage.logoutButtonKey));
      await tester.pumpAndSettle();

      expect(find.byKey(HomePage.logoutDialogKey), findsOneWidget);
      await tester.tap(find.byKey(HomePage.logoutDialogConfirmButtonKey));
      await tester.pumpAndSettle(
        const Duration(seconds: 1),
      ); // Aguarda navegação

      expect(
        find.byType(LoginPage),
        findsOneWidget,
        reason: "Deveria navegar para LoginPage após confirmar o logout.",
      );
      expect(find.byType(HomePage), findsNothing);
    });
  });
}
