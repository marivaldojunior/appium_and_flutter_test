// test/integration/forms_page_test.dart
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/forms_page.dart';
import 'package:appium_and_flutter_test/pages/home_page.dart';
import 'package:appium_and_flutter_test/pages/login_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

// --- Constantes para os Testes ---
const String kCorrectUsername = 'admin';
const String kCorrectPassword = '1234';

// Dados de teste para o formulário
const String kTestName = 'Nome de Teste';
const String kTestEmail = 'teste@exemplo.com';
const String kTestAge = '30';
const String kTestDescription = 'Descrição de teste.';
const String kTestCountry = 'Brasil';
const String kTestSkill = 'Flutter';
const String kTestGender = 'Masculino';

// Mensagens de validação e UI
const String kSuccessSnackbarMsg = 'Formulário enviado com sucesso!';
const String kErrorSnackbarMsg = 'Por favor, corrija os erros no formulário.';
const String kEmptyNameMsg = 'Por favor, insira seu nome.';
const String kInvalidEmailMsg = 'Por favor, insira um email válido.';
const String kInvalidAgeMsg = 'Por favor, insira uma idade válida.';

// --- Funções Auxiliares de Teste ---

/// Garante um estado limpo, inicializando o app e navegando até a [FormsPage].
Future<void> _initializeAppAndNavigateToForms(WidgetTester tester) async {
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
  await tester.tap(find.byKey(HomePage.formsButtonKey));
  await tester.pumpAndSettle();
  expect(find.byType(FormsPage), findsOneWidget);
}

/// Preenche todos os campos do formulário com dados válidos.
Future<void> _fillCompleteForm(WidgetTester tester) async {
  // Rola para garantir a visibilidade dos campos antes de interagir.
  await tester.scrollUntilVisible(find.byKey(FormsPage.submitButtonKey), 200);

  // Preenche os campos de texto.
  await tester.enterText(find.byKey(FormsPage.nameFieldKey), kTestName);
  await tester.enterText(find.byKey(FormsPage.emailFieldKey), kTestEmail);
  await tester.enterText(find.byKey(FormsPage.ageFieldKey), kTestAge);
  await tester.enterText(
    find.byKey(FormsPage.descriptionFieldKey),
    kTestDescription,
  );

  // Interage com outros widgets.
  await tester.tap(find.byKey(FormsPage.datePickerFieldKey));
  await tester.pumpAndSettle();
  await tester.tap(find.text('OK'));
  await tester.pumpAndSettle();

  await tester.tap(find.byKey(FormsPage.subscribeSwitchKey));
  await tester.tap(
    find.byKey(ValueKey('${FormsPage.skillCheckboxPrefixKey}$kTestSkill')),
  );
  await tester.tap(
    find.byKey(ValueKey('${FormsPage.genderRadioPrefixKey}$kTestGender')),
  );

  await tester.tap(find.byKey(FormsPage.countryDropdownKey));
  await tester.pumpAndSettle();
  await tester.tap(find.text(kTestCountry).last);
  await tester.pumpAndSettle();
}

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Testes de Integração da FormsPage', () {
    testWidgets(
      'Deve preencher e submeter o formulário com sucesso e resetar os campos',
      (WidgetTester tester) async {
        // Arrange
        await _initializeAppAndNavigateToForms(tester);

        // Act
        await _fillCompleteForm(tester);
        await tester.tap(find.byKey(FormsPage.submitButtonKey));
        await tester.pumpAndSettle();

        // Assert: Verifica a mensagem de sucesso.
        expect(find.text(kSuccessSnackbarMsg), findsOneWidget);

        // Assert: Verifica se o formulário foi resetado.
        await tester.pumpAndSettle(
          const Duration(seconds: 4),
        ); // Espera snackbar sumir.
        expect(find.text(kTestName), findsNothing);
        expect(find.text('Selecione a Data de Nascimento'), findsOneWidget);
        final switchWidget = tester.widget<SwitchListTile>(
          find.byKey(FormsPage.subscribeSwitchKey),
        );
        expect(switchWidget.value, isFalse);
      },
    );

    testWidgets('Deve exibir mensagens de validação para campos obrigatórios', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigateToForms(tester);

      // Act: Tenta submeter o formulário vazio.
      await tester.scrollUntilVisible(
        find.byKey(FormsPage.submitButtonKey),
        200,
      );
      await tester.tap(find.byKey(FormsPage.submitButtonKey));
      await tester.pumpAndSettle();

      // Assert: Verifica as mensagens de erro.
      expect(find.text(kEmptyNameMsg), findsOneWidget);
      expect(find.text('Por favor, insira seu email.'), findsOneWidget);
      expect(find.text('Por favor, insira sua idade.'), findsOneWidget);
      expect(find.text('Por favor, selecione uma data.'), findsOneWidget);
      expect(find.text('Selecione ao menos uma habilidade.'), findsOneWidget);
      expect(find.text('Por favor, selecione seu gênero.'), findsOneWidget);
      expect(find.text('Por favor, selecione um país.'), findsOneWidget);
      expect(find.text(kErrorSnackbarMsg), findsOneWidget);
    });

    testWidgets('Deve validar formatos de email e idade incorretos', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigateToForms(tester);

      // Act: Insere dados inválidos.
      await tester.enterText(
        find.byKey(FormsPage.emailFieldKey),
        'email-invalido',
      );
      await tester.enterText(find.byKey(FormsPage.ageFieldKey), 'abc');
      await tester.tap(find.byKey(FormsPage.submitButtonKey));
      await tester.pumpAndSettle();

      // Assert: Verifica as mensagens de validação específicas.
      expect(find.text(kInvalidEmailMsg), findsOneWidget);
      expect(find.text('"abc" não é um número válido.'), findsOneWidget);

      // Act: Insere idade fora do intervalo.
      await tester.enterText(find.byKey(FormsPage.ageFieldKey), '151');
      await tester.tap(find.byKey(FormsPage.submitButtonKey));
      await tester.pumpAndSettle();

      // Assert: Verifica a validação de intervalo de idade.
      expect(find.text(kInvalidAgeMsg), findsOneWidget);
    });
  });
}
