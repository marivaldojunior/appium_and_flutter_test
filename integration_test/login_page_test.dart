// test/integration/login_page_test.dart
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/home_page.dart';
import 'package:appium_and_flutter_test/pages/login_page.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

// --- Constantes para os Testes ---
// Credenciais
const String kCorrectUsername = 'admin';
const String kCorrectPassword = '1234';
const String kWrongUsername = 'usuarioerrado';
const String kWrongPassword = 'senhaerrada';

// Mensagens de Validação e UI
const String kEmptyUserValidationMsg = 'Por favor, insira o usuário';
const String kEmptyPasswordValidationMsg = 'Por favor, insira a senha';
const String kLoginErrorDialogTitle = 'Erro de Login';
const String kLoginErrorDialogContent = 'Usuário ou senha incorretos.';
const String kLoginSuccessSnackbarMsg = 'Login bem-sucedido!';
const String kForgotPasswordSnackbarMsg =
    'Funcionalidade "Esqueceu a senha?" não implementada.';

// Função auxiliar para inicializar o app de forma limpa para cada teste.
Future<void> _initializeApp(WidgetTester tester) async {
  app.main();
  await tester.pumpAndSettle();
}

// Função auxiliar para encapsular a ação de login.
Future<void> _performLogin(
  WidgetTester tester, {
  String? username,
  String? password,
}) async {
  if (username != null) {
    await tester.enterText(find.byKey(LoginPage.usernameFieldKey), username);
  }
  if (password != null) {
    await tester.enterText(find.byKey(LoginPage.passwordFieldKey), password);
  }
  await tester.tap(find.byKey(LoginPage.loginButtonKey));
  // Aguarda por todas as animações e microtarefas (diálogos, snackbars, navegação).
  await tester.pumpAndSettle();
}

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Testes de Integração da Página de Login', () {
    testWidgets(
      'Deve exibir elementos da UI e mensagens de erro para campos vazios',
      (WidgetTester tester) async {
        // Arrange: Inicia o app.
        await _initializeApp(tester);

        // Assert: Verifica se os elementos iniciais da UI estão presentes.
        expect(find.byKey(LoginPage.usernameFieldKey), findsOneWidget);
        expect(find.byKey(LoginPage.passwordFieldKey), findsOneWidget);
        expect(find.byKey(LoginPage.loginButtonKey), findsOneWidget);
        expect(find.byKey(LoginPage.forgotPasswordButtonKey), findsOneWidget);
        expect(
          find.text('Login'),
          findsOneWidget,
          reason: 'O título do AppBar deve estar visível',
        );

        // Act: Toca no botão de login com os campos vazios.
        await tester.tap(find.byKey(LoginPage.loginButtonKey));
        await tester.pumpAndSettle();

        // Assert: Verifica as mensagens de validação.
        expect(find.text(kEmptyUserValidationMsg), findsOneWidget);
        expect(find.text(kEmptyPasswordValidationMsg), findsOneWidget);
      },
    );

    testWidgets('Deve exibir diálogo de erro ao usar credenciais incorretas', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeApp(tester);

      // Act
      await _performLogin(
        tester,
        username: kWrongUsername,
        password: kWrongPassword,
      );

      // Assert: Verifica se o diálogo de erro é exibido.
      expect(find.byKey(LoginPage.loginAlertError), findsOneWidget);
      expect(find.text(kLoginErrorDialogTitle), findsOneWidget);
      expect(find.text(kLoginErrorDialogContent), findsOneWidget);

      // Act: Fecha o diálogo.
      await tester.tap(find.byKey(LoginPage.alertDialogErrorOkButtonKey));
      await tester.pumpAndSettle();

      // Assert: Verifica se o diálogo desapareceu e se o app continua na página de login.
      expect(find.byKey(LoginPage.loginAlertError), findsNothing);
      expect(find.byType(LoginPage), findsOneWidget);
    });

    testWidgets(
      'Deve exibir SnackBar e navegar para a HomePage com credenciais corretas',
      (WidgetTester tester) async {
        // Arrange
        await _initializeApp(tester);

        // Act
        await _performLogin(
          tester,
          username: kCorrectUsername,
          password: kCorrectPassword,
        );

        // Assert: Verifica se a SnackBar de sucesso é exibida.
        expect(find.byKey(LoginPage.loginSnackbarSuccess), findsOneWidget);
        expect(find.text(kLoginSuccessSnackbarMsg), findsOneWidget);

        // Assert: Verifica a navegação para a HomePage.
        expect(
          find.byType(HomePage),
          findsOneWidget,
          reason: "Deveria navegar para a HomePage",
        );
        expect(
          find.byType(LoginPage),
          findsNothing,
          reason: "A LoginPage não deveria mais estar visível",
        );
      },
    );

    testWidgets(
      'Deve exibir SnackBar informativo ao clicar em "Esqueceu a senha?"',
      (WidgetTester tester) async {
        // Arrange
        await _initializeApp(tester);

        // Act
        await tester.tap(find.byKey(LoginPage.forgotPasswordButtonKey));
        await tester.pumpAndSettle();

        // Assert: Verifica a SnackBar informativa.
        expect(
          find.byKey(LoginPage.snackbarForgotPasswordButtonKey),
          findsOneWidget,
        );
        expect(find.text(kForgotPasswordSnackbarMsg), findsOneWidget);

        // Act: Aguarda a SnackBar desaparecer automaticamente (duração padrão de 4s).
        await tester.pumpAndSettle(const Duration(seconds: 4));

        // Assert: Verifica se a SnackBar desapareceu.
        expect(
          find.byKey(LoginPage.snackbarForgotPasswordButtonKey),
          findsNothing,
        );
      },
    );
  });
}
