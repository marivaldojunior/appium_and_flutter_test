// test/integration/listview_page_test.dart
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/home_page.dart';
import 'package:appium_and_flutter_test/pages/listview_page.dart';
import 'package:appium_and_flutter_test/pages/login_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

// --- Constantes para os Testes ---
const String kCorrectUsername = 'admin';
const String kCorrectPassword = '1234';
const String kNewItemTitle = 'Novo Item de Teste';
const String kNewItemDesc = 'Descrição do novo item.';
const String kEditedItemTitle = 'Item Editado';
const String kEditedItemDesc = 'Esta descrição foi alterada.';
const String kEmptyListMsg =
    'Nenhum item na lista.\nAdicione alguns itens usando o botão "+".';

// --- Funções Auxiliares de Teste ---

/// Garante um estado limpo, inicializando o app e navegando até a [ListViewPage].
Future<void> _initializeAppAndNavigate(WidgetTester tester) async {
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
  await tester.tap(find.byKey(HomePage.listViewButtonKey));
  await tester.pumpAndSettle();
  expect(find.byType(ListViewPage), findsOneWidget);
}

/// Localiza um item [Dismissible] pelo seu título, rolando a lista se necessário.
Future<Finder> _findItemByTitle(WidgetTester tester, String title) async {
  final itemFinder = find.text(title);
  await tester.scrollUntilVisible(
    itemFinder,
    100.0,
    scrollable: find.byKey(ListViewPage.listViewKey),
  );
  await tester.pumpAndSettle();
  return find.ancestor(of: itemFinder, matching: find.byType(Dismissible));
}

/// Adiciona um novo item através do diálogo.
Future<void> _addItem(
  WidgetTester tester, {
  required String title,
  required String description,
}) async {
  await tester.tap(find.byKey(ListViewPage.addFloatingActionButtonKey));
  await tester.pumpAndSettle();
  expect(find.byKey(ListViewPage.addItemDialogKey), findsOneWidget);

  await tester.enterText(find.byKey(ListViewPage.dialogTitleFieldKey), title);
  await tester.enterText(
    find.byKey(ListViewPage.dialogDescriptionFieldKey),
    description,
  );
  await tester.tap(find.byKey(ListViewPage.dialogAddButtonKey));
  await tester.pumpAndSettle();
}

/// Exclui um item da lista usando um gesto de swipe.
Future<void> _deleteItem(WidgetTester tester, String title) async {
  final itemToDelete = await _findItemByTitle(tester, title);
  await tester.drag(
    itemToDelete,
    const Offset(400.0, 0.0),
  ); // Swipe para direita
  await tester.pumpAndSettle();
  expect(find.byKey(ListViewPage.deleteConfirmDialogKey), findsOneWidget);
  await tester.tap(find.byKey(ListViewPage.deleteConfirmDeleteButtonKey));
  await tester.pumpAndSettle();
}

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Testes de Integração da ListViewPage', () {
    // Garante que cada teste comece em um estado limpo, navegando até a página.
    setUp(() async {
      // A inicialização é feita dentro de cada teste para garantir isolamento total.
    });

    testWidgets('Deve exibir os itens iniciais corretamente', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigate(tester);

      // Assert
      expect(find.text('Item 1'), findsOneWidget);
      expect(find.text('Item 2'), findsOneWidget);
      expect(find.text('Item 3'), findsOneWidget);
      expect(find.text('Item 4'), findsOneWidget);
      expect(find.byKey(ListViewPage.listViewKey), findsOneWidget);
    });

    testWidgets('Deve adicionar um novo item à lista', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigate(tester);

      // Act
      await _addItem(tester, title: kNewItemTitle, description: kNewItemDesc);

      // Assert
      expect(find.text('Novo item adicionado!'), findsOneWidget);
      expect(find.text(kNewItemTitle), findsOneWidget);
    });

    testWidgets('Deve editar um item existente', (WidgetTester tester) async {
      // Arrange
      await _initializeAppAndNavigate(tester);
      const originalTitle = 'Item 1';
      final itemToEdit = await _findItemByTitle(tester, originalTitle);

      // Act: Abre o diálogo de edição.
      await tester.drag(
        itemToEdit,
        const Offset(-400.0, 0.0),
      ); // Swipe para esquerda
      await tester.pumpAndSettle();
      expect(find.byKey(ListViewPage.editItemDialogKey), findsOneWidget);

      // Act: Edita e salva as alterações.
      await tester.enterText(
        find.byKey(ListViewPage.dialogTitleFieldKey),
        kEditedItemTitle,
      );
      await tester.enterText(
        find.byKey(ListViewPage.dialogDescriptionFieldKey),
        kEditedItemDesc,
      );
      await tester.tap(find.byKey(ListViewPage.dialogSaveButtonKey));
      await tester.pumpAndSettle();

      // Assert
      expect(find.text('Item atualizado!'), findsOneWidget);
      expect(find.text(kEditedItemTitle), findsOneWidget);
      expect(find.text(originalTitle), findsNothing);
    });

    testWidgets('Deve excluir um item após confirmação', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigate(tester);
      const titleToDelete = 'Item 2';

      // Act
      await _deleteItem(tester, titleToDelete);

      // Assert
      expect(find.text('Item removido!'), findsOneWidget);
      expect(find.text(titleToDelete), findsNothing);
    });

    testWidgets('Deve exibir SnackBar ao tocar em um item', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigate(tester);
      const titleToTap = 'Item 3';
      final itemToTap = await _findItemByTitle(tester, titleToTap);

      // Act
      await tester.tap(
        find.descendant(of: itemToTap, matching: find.byType(ListTile)),
      );
      await tester.pumpAndSettle();

      // Assert
      expect(find.text('Item selecionado: $titleToTap'), findsOneWidget);
    });

    testWidgets(
      'Deve exibir mensagem de lista vazia após excluir todos os itens',
      (WidgetTester tester) async {
        // Arrange
        await _initializeAppAndNavigate(tester);
        final initialItems = ['Item 1', 'Item 2', 'Item 3', 'Item 4'];

        // Act: Deleta todos os itens iniciais.
        for (final title in initialItems) {
          await _deleteItem(tester, title);
          await tester.pumpAndSettle(
            const Duration(seconds: 2),
          ); // Espera SnackBar sumir
        }

        // Assert
        expect(find.byKey(ListViewPage.emptyListTextKey), findsOneWidget);
        expect(find.text(kEmptyListMsg), findsOneWidget);
        expect(find.byKey(ListViewPage.listViewKey), findsNothing);
      },
    );
  });
}
