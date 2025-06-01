// Exemplo: test/app_test.dart
import 'package:appium_and_flutter_test/pages/login_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Login bem-sucedido', (WidgetTester tester) async {
    // app.main(); // Se estiver iniciando o app a partir do main
    await tester.pumpWidget(MaterialApp(home: LoginPage())); // Ou inicie a LoginPage diretamente
    await tester.pumpAndSettle();

    // Encontrar campos e botão pelas keys
    final usernameField = find.byKey(LoginPageState.usernameFieldKey);
    final passwordField = find.byKey(LoginPageState.passwordFieldKey);
    final loginButton = find.byKey(LoginPageState.loginButtonKey);

    expect(usernameField, findsOneWidget);
    expect(passwordField, findsOneWidget);
    expect(loginButton, findsOneWidget);

    // Digitar nos campos
    await tester.enterText(usernameField, 'admin');
    await tester.enterText(passwordField, '1234');
    await tester.pumpAndSettle();

    // Tocar no botão de login
    await tester.tap(loginButton);
    await tester.pumpAndSettle(); // Esperar por navegação ou SnackBar

    // Verificar o SnackBar de sucesso (se a navegação não for imediata)
    // ou verificar se navegou para a HomePage.
    expect(find.byKey(const ValueKey('login_snackbar_success')), findsOneWidget);
    expect(find.text('Login bem-sucedido!'), findsOneWidget);

    // Se você navegar para HomePage, verifique um elemento da HomePage
    // expect(find.byType(HomePage), findsOneWidget);
  });

  testWidgets('Erro de login com credenciais incorretas', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(home: LoginPage()));
    await tester.pumpAndSettle();

    await tester.enterText(find.byKey(LoginPageState.usernameFieldKey), 'errado');
    await tester.enterText(find.byKey(LoginPageState.passwordFieldKey), '123');
    await tester.tap(find.byKey(LoginPageState.loginButtonKey));
    await tester.pumpAndSettle(); // Esperar pelo AlertDialog

    // Verificar o AlertDialog de erro
    expect(find.byKey(const ValueKey('login_alert_error')), findsOneWidget);
    expect(find.text('Usuário ou senha incorretos.'), findsOneWidget);

    // Fechar o AlertDialog
    await tester.tap(find.byKey(const ValueKey('login_alert_error_ok_button')));
    await tester.pumpAndSettle();
    expect(find.byKey(const ValueKey('login_alert_error')), findsNothing);
  });
}