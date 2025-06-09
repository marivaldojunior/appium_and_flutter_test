import 'package:appium_and_flutter_test/pages/home_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/login_page.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Testes de Integração da LoginPage', () {
    setUp(() async {
      // Garante que o app seja reiniciado para cada teste, começando na LoginPage
      app.main();
      await tester.pumpAndSettle();
    });

    testWidgets('Verifica UI inicial e validações de campos vazios', (
      WidgetTester tester,
    ) async {
      // Verifica se a LoginPage está sendo exibida
      expect(find.byType(LoginPage), findsOneWidget);

      // Verifica elementos da UI
      expect(find.byKey(LoginPage.usernameFieldKey), findsOneWidget);
      expect(find.byKey(LoginPage.passwordFieldKey), findsOneWidget);
      expect(find.byKey(LoginPage.loginButtonKey), findsOneWidget);
      expect(find.byKey(LoginPage.forgotPasswordButtonKey), findsOneWidget);
      expect(find.text('Login'), findsOneWidget); // Título do AppBar

      // Tenta logar com campos vazios
      await tester.tap(find.byKey(LoginPage.loginButtonKey));
      await tester
          .pumpAndSettle(); // Aguarda a reconstrução da UI com as mensagens de erro

      // Verifica mensagens de validação
      expect(find.text('Por favor, insira o usuário'), findsOneWidget);
      expect(find.text('Por favor, insira a senha'), findsOneWidget);
    });

    testWidgets('Login com credenciais incorretas exibe diálogo de erro', (
      WidgetTester tester,
    ) async {
      await tester.enterText(
        find.byKey(LoginPage.usernameFieldKey),
        'usuarioerrado',
      );
      await tester.enterText(
        find.byKey(LoginPage.passwordFieldKey),
        'senhaerrada',
      );
      await tester.tap(find.byKey(LoginPage.loginButtonKey));
      await tester.pumpAndSettle(); // Aguarda o diálogo aparecer

      // Verifica o diálogo de erro
      expect(find.byKey(const ValueKey('login_alert_error')), findsOneWidget);
      expect(find.text('Erro de Login'), findsOneWidget);
      expect(find.text('Usuário ou senha incorretos.'), findsOneWidget);

      // Fecha o diálogo
      await tester.tap(find.byKey(LoginPage.alertDialogErrorOkButtonKey));
      await tester.pumpAndSettle(); // Aguarda o diálogo desaparecer

      expect(find.byKey(const ValueKey('login_alert_error')), findsNothing);
      // Garante que ainda está na LoginPage
      expect(find.byType(LoginPage), findsOneWidget);
    });

    testWidgets(
      'Login com credenciais corretas navega para HomePage e exibe SnackBar',
      (WidgetTester tester) async {
        // Usa as credenciais padrão definidas na LoginPageState
        // Se forem diferentes, ajuste aqui.
        const String defaultUsername = 'admin';
        const String defaultPassword = '1234';

        await tester.enterText(
          find.byKey(LoginPage.usernameFieldKey),
          defaultUsername,
        );
        await tester.enterText(
          find.byKey(LoginPage.passwordFieldKey),
          defaultPassword,
        );
        await tester.tap(find.byKey(LoginPage.loginButtonKey));
        await tester.pumpAndSettle(); // Aguarda SnackBar e possível navegação

        // Verifica SnackBar de sucesso
        expect(
          find.byKey(const ValueKey('login_snackbar_success')),
          findsOneWidget,
        );
        expect(find.text('Login bem-sucedido!'), findsOneWidget);

        // Aguarda um pouco mais para a navegação e o SnackBar desaparecer (se configurado para tal)
        await tester.pumpAndSettle(const Duration(seconds: 2));

        // Verifica se navegou para HomePage
        expect(find.byType(HomePage), findsOneWidget);
        expect(find.byType(LoginPage), findsNothing);
      },
    );

    testWidgets('Botão "Esqueceu a senha?" exibe SnackBar informativo', (
      WidgetTester tester,
    ) async {
      await tester.tap(find.byKey(LoginPage.forgotPasswordButtonKey));
      await tester.pumpAndSettle(); // Aguarda o SnackBar aparecer

      // Verifica o SnackBar
      expect(
        find.byKey(const ValueKey('login_snackbar_forgot_password_info')),
        findsOneWidget,
      );
      expect(
        find.text('Funcionalidade "Esqueceu a senha?" não implementada.'),
        findsOneWidget,
      );

      // Aguarda o SnackBar desaparecer (se configurado para tal)
      await tester.pumpAndSettle(const Duration(seconds: 2));
      expect(
        find.byKey(const ValueKey('login_snackbar_forgot_password_info')),
        findsNothing,
      );
    });
  });
}
