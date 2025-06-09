import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/forms_page.dart';
import 'package:intl/intl.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Testes de Integração da FormsPage', () {
    Future<void> _ensurePageLoaded(WidgetTester tester) async {
      app.main(); // Ou navegue para a FormsPage se não for a inicial
      await tester.pumpAndSettle();
      expect(find.byType(FormsPage), findsOneWidget);
    }

    testWidgets('Preenche e submete o formulário com dados válidos', (
      WidgetTester tester,
    ) async {
      await _ensurePageLoaded(tester);

      // 1. Preencher Nome
      await tester.enterText(find.byKey(FormsPage.nameFieldKey), 'Nome Teste');
      await tester.pumpAndSettle();

      // 2. Preencher Email
      await tester.enterText(
        find.byKey(FormsPage.emailFieldKey),
        'teste@exemplo.com',
      );
      await tester.pumpAndSettle();

      // 3. Preencher Idade
      await tester.enterText(find.byKey(FormsPage.ageFieldKey), '30');
      await tester.pumpAndSettle();

      // 4. Selecionar Data de Nascimento
      await tester.tap(find.byKey(FormsPage.datePickerFieldKey));
      await tester.pumpAndSettle(); // Aguarda o DatePicker aparecer
      await tester.tap(find.text('OK')); // Confirma a data inicial (hoje)
      await tester.pumpAndSettle();
      final todayFormatted = DateFormat('dd/MM/yyyy').format(DateTime.now());
      expect(find.text('Data de Nascimento: $todayFormatted'), findsOneWidget);

      // 5. Ativar Switch de Inscrição
      await tester.tap(find.byKey(FormsPage.subscribeSwitchKey));
      await tester.pumpAndSettle();
      final switchWidget = tester.widget<SwitchListTile>(
        find.byKey(FormsPage.subscribeSwitchKey),
      );
      expect(switchWidget.value, isTrue);

      // 6. Selecionar Habilidades (Checkboxes)
      // Scroll para garantir que o checkbox esteja visível se a lista for longa
      await tester.ensureVisible(
        find.byKey(
          const ValueKey('${FormsPage.skillCheckboxPrefixKey}Flutter'),
        ),
      );
      await tester.pumpAndSettle();
      await tester.tap(
        find.byKey(
          const ValueKey('${FormsPage.skillCheckboxPrefixKey}Flutter'),
        ),
      );
      await tester.pumpAndSettle();

      await tester.ensureVisible(
        find.byKey(const ValueKey('${FormsPage.skillCheckboxPrefixKey}Dart')),
      );
      await tester.pumpAndSettle();
      await tester.tap(
        find.byKey(const ValueKey('${FormsPage.skillCheckboxPrefixKey}Dart')),
      );
      await tester.pumpAndSettle();

      // 7. Selecionar Gênero (Radio Buttons)
      await tester.ensureVisible(
        find.byKey(
          const ValueKey('${FormsPage.genderRadioPrefixKey}Masculino'),
        ),
      );
      await tester.pumpAndSettle();
      await tester.tap(
        find.byKey(
          const ValueKey('${FormsPage.genderRadioPrefixKey}Masculino'),
        ),
      );
      await tester.pumpAndSettle();

      // 8. Selecionar País (Dropdown)
      await tester.ensureVisible(find.byKey(FormsPage.countryDropdownKey));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(FormsPage.countryDropdownKey));
      await tester.pumpAndSettle(); // Aguarda o dropdown abrir
      // Seleciona o primeiro item da lista (Brasil)
      await tester.tap(
        find.text('Brasil').last,
      ); // .last para pegar o item do dropdown
      await tester.pumpAndSettle();
      expect(
        find.text('Brasil'),
        findsWidgets,
      ); // Verifica se o valor foi selecionado

      // 9. Preencher Descrição
      await tester.ensureVisible(find.byKey(FormsPage.descriptionFieldKey));
      await tester.pumpAndSettle();
      await tester.enterText(
        find.byKey(FormsPage.descriptionFieldKey),
        'Descrição de teste.',
      );
      await tester.pumpAndSettle();
      // Esconder o teclado para que o botão de submit fique visível
      FocusManager.instance.primaryFocus?.unfocus();
      await tester.pumpAndSettle();

      // 10. Submeter Formulário
      await tester.ensureVisible(find.byKey(FormsPage.submitButtonKey));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(FormsPage.submitButtonKey));
      await tester.pumpAndSettle(
        const Duration(seconds: 1),
      ); // Aguarda SnackBar

      // Verifica mensagem de sucesso
      expect(find.text('Formulário enviado com sucesso!'), findsOneWidget);
      await tester.pumpAndSettle(
        const Duration(seconds: 2),
      ); // Aguarda SnackBar sumir

      // Verifica se o formulário foi resetado
      expect(find.text('Nome Teste'), findsNothing);
      expect(find.text('teste@exemplo.com'), findsNothing);
      expect(find.text('30'), findsNothing);
      expect(find.text('Selecione a Data de Nascimento'), findsOneWidget);
      final switchWidgetAfterReset = tester.widget<SwitchListTile>(
        find.byKey(FormsPage.subscribeSwitchKey),
      );
      expect(switchWidgetAfterReset.value, isFalse);
      // Verifica se os checkboxes foram desmarcados
      final flutterCheckbox = tester.widget<CheckboxListTile>(
        find.byKey(
          const ValueKey('${FormsPage.skillCheckboxPrefixKey}Flutter'),
        ),
      );
      expect(flutterCheckbox.value, isFalse);
      // Verifica se o radio button foi resetado (nenhum selecionado)
      // A forma de verificar isso depende de como o estado é resetado.
      // Se _selectedGender se torna null, o RadioListTile com value 'Masculino' não estará groupValue.
      final radioMasculino = tester.widget<RadioListTile<String>>(
        find.byKey(
          const ValueKey('${FormsPage.genderRadioPrefixKey}Masculino'),
        ),
      );
      expect(radioMasculino.groupValue, isNull);

      // Verifica se o dropdown foi resetado
      final dropdown = tester.widget<DropdownButtonFormField<String>>(
        find.byKey(FormsPage.countryDropdownKey),
      );
      expect(dropdown.value, isNull);
      expect(find.text('Descrição de teste.'), findsNothing);
    });

    testWidgets('Exibe mensagens de validação para campos obrigatórios', (
      WidgetTester tester,
    ) async {
      await _ensurePageLoaded(tester);

      // Tenta submeter o formulário vazio
      // Scroll até o botão de submit para garantir visibilidade
      await tester.ensureVisible(find.byKey(FormsPage.submitButtonKey));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(FormsPage.submitButtonKey));
      await tester.pumpAndSettle(); // Aguarda as mensagens de validação

      // Verifica mensagens de erro
      expect(find.text('Por favor, insira seu nome.'), findsOneWidget);
      expect(find.text('Por favor, insira seu email.'), findsOneWidget);
      expect(find.text('Por favor, insira sua idade.'), findsOneWidget);
      expect(find.text('Por favor, selecione uma data.'), findsOneWidget);
      // Para checkboxes e radios, a validação é manual e aparece abaixo deles
      expect(find.text('Selecione ao menos uma habilidade.'), findsOneWidget);
      expect(find.text('Por favor, selecione seu gênero.'), findsOneWidget);
      expect(find.text('Por favor, selecione um país.'), findsOneWidget);

      // Verifica SnackBar de erro geral
      expect(
        find.text('Por favor, corrija os erros no formulário.'),
        findsOneWidget,
      );
      await tester.pumpAndSettle(
        const Duration(seconds: 2),
      ); // Aguarda SnackBar sumir
    });

    testWidgets('Validação específica de email e idade', (
      WidgetTester tester,
    ) async {
      await _ensurePageLoaded(tester);

      // Email inválido
      await tester.enterText(
        find.byKey(FormsPage.emailFieldKey),
        'emailinvalido',
      );
      await tester.pumpAndSettle();

      // Idade inválida (não numérica)
      await tester.enterText(find.byKey(FormsPage.ageFieldKey), 'idade');
      await tester.pumpAndSettle();

      // Scroll até o botão de submit para garantir visibilidade
      await tester.ensureVisible(find.byKey(FormsPage.submitButtonKey));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(FormsPage.submitButtonKey));
      await tester.pumpAndSettle();

      expect(find.text('Por favor, insira um email válido.'), findsOneWidget);
      expect(find.text('"idade" não é um número válido.'), findsOneWidget);

      // Idade fora do range
      await tester.enterText(find.byKey(FormsPage.ageFieldKey), '0');
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(FormsPage.submitButtonKey));
      await tester.pumpAndSettle();
      expect(find.text('Por favor, insira uma idade válida.'), findsOneWidget);

      await tester.enterText(find.byKey(FormsPage.ageFieldKey), '150');
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(FormsPage.submitButtonKey));
      await tester.pumpAndSettle();
      expect(find.text('Por favor, insira uma idade válida.'), findsOneWidget);
    });

    testWidgets(
      'Interação com DatePicker, Switch, Checkbox, Radio e Dropdown',
      (WidgetTester tester) async {
        await _ensurePageLoaded(tester);

        // DatePicker
        expect(find.text('Selecione a Data de Nascimento'), findsOneWidget);
        await tester.tap(find.byKey(FormsPage.datePickerFieldKey));
        await tester.pumpAndSettle();
        // Seleciona uma data específica, por exemplo, o dia 15 do mês atual
        await tester.tap(find.text('15'));
        await tester.pumpAndSettle();
        await tester.tap(find.text('OK'));
        await tester.pumpAndSettle();
        final selectedDate = DateTime(
          DateTime.now().year,
          DateTime.now().month,
          15,
        );
        final selectedDateFormatted = DateFormat(
          'dd/MM/yyyy',
        ).format(selectedDate);
        expect(
          find.text('Data de Nascimento: $selectedDateFormatted'),
          findsOneWidget,
        );

        // Switch
        var switchWidget = tester.widget<SwitchListTile>(
          find.byKey(FormsPage.subscribeSwitchKey),
        );
        expect(switchWidget.value, isFalse);
        await tester.tap(find.byKey(FormsPage.subscribeSwitchKey));
        await tester.pumpAndSettle();
        switchWidget = tester.widget<SwitchListTile>(
          find.byKey(FormsPage.subscribeSwitchKey),
        );
        expect(switchWidget.value, isTrue);

        // Checkbox
        var checkboxFirebase = tester.widget<CheckboxListTile>(
          find.byKey(
            const ValueKey('${FormsPage.skillCheckboxPrefixKey}Firebase'),
          ),
        );
        expect(checkboxFirebase.value, isFalse);
        await tester.tap(
          find.byKey(
            const ValueKey('${FormsPage.skillCheckboxPrefixKey}Firebase'),
          ),
        );
        await tester.pumpAndSettle();
        checkboxFirebase = tester.widget<CheckboxListTile>(
          find.byKey(
            const ValueKey('${FormsPage.skillCheckboxPrefixKey}Firebase'),
          ),
        );
        expect(checkboxFirebase.value, isTrue);

        // Radio Button
        var radioFeminino = tester.widget<RadioListTile<String>>(
          find.byKey(
            const ValueKey('${FormsPage.genderRadioPrefixKey}Feminino'),
          ),
        );
        expect(radioFeminino.groupValue, isNull); // Assumindo que começa nulo
        await tester.tap(
          find.byKey(
            const ValueKey('${FormsPage.genderRadioPrefixKey}Feminino'),
          ),
        );
        await tester.pumpAndSettle();
        radioFeminino = tester.widget<RadioListTile<String>>(
          find.byKey(
            const ValueKey('${FormsPage.genderRadioPrefixKey}Feminino'),
          ),
        );
        expect(radioFeminino.groupValue, 'Feminino');

        // Dropdown
        await tester.tap(find.byKey(FormsPage.countryDropdownKey));
        await tester.pumpAndSettle();
        await tester.tap(find.text('Canadá').last);
        await tester.pumpAndSettle();
        expect(
          find.text('Canadá'),
          findsWidgets,
        ); // Verifica se o valor foi selecionado
      },
    );
  });
}
