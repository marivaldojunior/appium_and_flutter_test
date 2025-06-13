import 'package:appium_and_flutter_test/pages/home_page.dart';
import 'package:appium_and_flutter_test/pages/login_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/listview_page.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  Future<void> _navigateToListViewPage(WidgetTester tester) async {
    app.main(); // Inicia o app
    // Aguarda um tempo para o app estabilizar na tela inicial (LoginPage ou HomePage)
    await tester.pumpAndSettle(const Duration(seconds: 1));

    // Se estiver na LoginPage, realiza o login
    if (tester.any(find.byType(LoginPage))) {
      await tester.enterText(find.byKey(LoginPage.usernameFieldKey), 'admin');
      await tester.enterText(find.byKey(LoginPage.passwordFieldKey), '1234');
      await tester.tap(find.byKey(LoginPage.loginButtonKey));
      // Aguarda o login, navegação para HomePage e desaparecimento do SnackBar
      await tester.pumpAndSettle(const Duration(seconds: 3));
    }

    // Garante que está na HomePage
    expect(
      find.byType(HomePage),
      findsOneWidget,
      reason: "Não foi possível alcançar a HomePage.",
    );

    // Navega para ListViewPage
    await tester.tap(find.byKey(HomePage.listViewButtonKey));
    await tester.pumpAndSettle(); // Aguarda a navegação

    // Garante que está na ListViewPage
    expect(
      find.byType(ListViewPage),
      findsOneWidget,
      reason: "ListViewPage não foi carregada.",
    );
  }

  // Helper para encontrar um item Dismissible pelo título
  // Garante que o item esteja visível antes de tentar interagir
  Future<Finder> findDismissibleItemByTitle(
    WidgetTester tester,
    String title,
  ) async {
    final itemTextFinder = find.text(title);

    // Verifica se a lista em si existe antes de tentar rolar
    if (tester.any(find.byKey(ListViewPage.listViewKey))) {
      await tester.scrollUntilVisible(
        itemTextFinder,
        100.0, // Incremento de scroll
        scrollable: find.byKey(ListViewPage.listViewKey),
        maxScrolls:
            10, // Limita o número de scrolls para evitar loops infinitos
      );
    }
    await tester.pumpAndSettle();

    // Encontra o widget Dismissible que é ancestral do texto do título
    final dismissibleFinder = find.ancestor(
      of: itemTextFinder,
      matching: find.byType(Dismissible),
    );
    expect(
      dismissibleFinder,
      findsOneWidget,
      reason: "Não foi possível encontrar o item Dismissible para '$title'.",
    );
    return dismissibleFinder;
  }

  group('Testes de Integração da ListViewPage', () {
    testWidgets('Adiciona, edita, exclui itens e verifica interações da lista', (
      WidgetTester tester,
    ) async {
      await _navigateToListViewPage(tester);

      // 1. Verifica itens iniciais
      expect(find.text('Item 1'), findsOneWidget);
      expect(find.text('Item 2'), findsOneWidget);
      expect(find.text('Item 3'), findsOneWidget);
      expect(find.text('Item 4'), findsOneWidget);
      expect(find.byKey(ListViewPage.listViewKey), findsOneWidget);

      // 2. Adiciona um novo item
      const String novoTitulo = 'Novo Item Teste';
      const String novaDescricao = 'Descrição do novo item.';

      await tester.tap(find.byKey(ListViewPage.addFloatingActionButtonKey));
      await tester.pumpAndSettle();
      expect(find.byKey(ListViewPage.addItemDialogKey), findsOneWidget);

      // Testa validação (campos vazios)
      await tester.tap(find.byKey(ListViewPage.dialogAddButtonKey));
      await tester.pumpAndSettle();
      expect(find.text('O título não pode estar vazio.'), findsOneWidget);
      expect(find.text('A descrição não pode estar vazia.'), findsOneWidget);

      // Preenche e adiciona
      await tester.enterText(
        find.byKey(ListViewPage.dialogTitleFieldKey),
        novoTitulo,
      );
      await tester.enterText(
        find.byKey(ListViewPage.dialogDescriptionFieldKey),
        novaDescricao,
      );
      await tester.tap(find.byKey(ListViewPage.dialogAddButtonKey));
      await tester.pumpAndSettle(); // Dialog fecha, SnackBar aparece

      expect(find.text('Novo item adicionado!'), findsOneWidget);
      expect(find.text(novoTitulo), findsOneWidget);
      await tester.pumpAndSettle(
        const Duration(seconds: 2),
      ); // Espera SnackBar sumir

      // 3. Edita um item existente (Item 1)
      const String tituloEditado = 'Item 1 Editado';
      const String descricaoEditada = 'Descrição do Item 1 foi alterada.';
      Finder itemParaEditarFinder = await findDismissibleItemByTitle(
        tester,
        'Item 1',
      );

      await tester.drag(
        itemParaEditarFinder,
        const Offset(-400.0, 0.0),
      ); // Swipe para esquerda
      await tester.pumpAndSettle();
      expect(find.byKey(ListViewPage.editItemDialogKey), findsOneWidget);

      // Verifica se campos estão pré-preenchidos
      expect(find.widgetWithText(TextFormField, 'Item 1'), findsOneWidget);

      // Testa validação
      await tester.enterText(find.byKey(ListViewPage.dialogTitleFieldKey), '');
      await tester.tap(find.byKey(ListViewPage.dialogSaveButtonKey));
      await tester.pumpAndSettle();
      expect(find.text('O título não pode estar vazio.'), findsOneWidget);

      // Preenche e salva
      await tester.enterText(
        find.byKey(ListViewPage.dialogTitleFieldKey),
        tituloEditado,
      );
      await tester.enterText(
        find.byKey(ListViewPage.dialogDescriptionFieldKey),
        descricaoEditada,
      );
      await tester.tap(find.byKey(ListViewPage.dialogSaveButtonKey));
      await tester.pumpAndSettle();

      expect(find.text('Item atualizado!'), findsOneWidget);
      expect(find.text(tituloEditado), findsOneWidget);
      expect(find.text('Item 1'), findsNothing); // Original não deve existir
      await tester.pumpAndSettle(
        const Duration(seconds: 2),
      ); // Espera SnackBar sumir

      // 4. Exclui um item (Item 2)
      Finder itemParaExcluirFinder = await findDismissibleItemByTitle(
        tester,
        'Item 2',
      );

      // Tenta excluir e cancela
      await tester.drag(
        itemParaExcluirFinder,
        const Offset(400.0, 0.0),
      ); // Swipe para direita
      await tester.pumpAndSettle();
      expect(find.byKey(ListViewPage.deleteConfirmDialogKey), findsOneWidget);
      await tester.tap(find.byKey(ListViewPage.deleteConfirmCancelButtonKey));
      await tester.pumpAndSettle();
      expect(find.text('Item 2'), findsOneWidget); // Item ainda existe

      // Exclui de verdade
      itemParaExcluirFinder = await findDismissibleItemByTitle(
        tester,
        'Item 2',
      ); // Re-encontra
      await tester.drag(itemParaExcluirFinder, const Offset(400.0, 0.0));
      await tester.pumpAndSettle();
      expect(find.byKey(ListViewPage.deleteConfirmDialogKey), findsOneWidget);
      await tester.tap(find.byKey(ListViewPage.deleteConfirmDeleteButtonKey));
      await tester.pumpAndSettle();

      expect(find.text('Item removido!'), findsOneWidget);
      expect(find.text('Item 2'), findsNothing);
      await tester.pumpAndSettle(
        const Duration(seconds: 2),
      ); // Espera SnackBar sumir

      // 5. Toca em um item para ver SnackBar de seleção (Item 3)
      // Encontra o ListTile dentro do Dismissible para tocar
      final item3Dismissible = await findDismissibleItemByTitle(
        tester,
        'Item 3',
      );
      final item3ListTile = find.descendant(
        of: item3Dismissible,
        matching: find.byType(ListTile),
      );
      expect(item3ListTile, findsOneWidget);
      await tester.tap(item3ListTile);
      await tester.pumpAndSettle(); // SnackBar aparece
      expect(find.text('Item selecionado: Item 3'), findsOneWidget);
      await tester.pumpAndSettle(
        const Duration(seconds: 2),
      ); // Espera SnackBar sumir

      // 6. Exclui todos os itens restantes para verificar o estado de lista vazia
      // Itens restantes: "Item 1 Editado", "Item 3", "Item 4", "Novo Item Teste"
      final titulosParaExcluir = [
        tituloEditado,
        'Item 3',
        'Item 4',
        novoTitulo,
      ];

      for (final titulo in titulosParaExcluir) {
        Finder itemFinder = await findDismissibleItemByTitle(tester, titulo);
        await tester.drag(
          itemFinder,
          const Offset(400.0, 0.0),
        ); // Swipe para direita
        await tester.pumpAndSettle();
        expect(
          find.byKey(ListViewPage.deleteConfirmDialogKey),
          findsOneWidget,
          reason: "Dialog de confirmação para '$titulo' não apareceu.",
        );
        await tester.tap(find.byKey(ListViewPage.deleteConfirmDeleteButtonKey));
        await tester.pumpAndSettle(); // Item removido, SnackBar
        expect(
          find.text('Item removido!'),
          findsOneWidget,
          reason: "SnackBar de remoção para '$titulo' não apareceu.",
        );
        await tester.pumpAndSettle(const Duration(seconds: 2)); // SnackBar some
        expect(
          find.text(titulo),
          findsNothing,
          reason: "'$titulo' não foi removido.",
        );
      }

      // Verifica estado de lista vazia
      expect(find.byKey(ListViewPage.emptyListTextKey), findsOneWidget);
      expect(
        find.text(
          'Nenhum item na lista.\nAdicione alguns itens usando o botão "+".',
        ),
        findsOneWidget,
      );
      expect(find.byKey(ListViewPage.listViewKey), findsNothing);

      // 7. Adiciona um item novamente para garantir que a lista vazia some
      await tester.tap(find.byKey(ListViewPage.addFloatingActionButtonKey));
      await tester.pumpAndSettle();
      await tester.enterText(
        find.byKey(ListViewPage.dialogTitleFieldKey),
        "Outro Item",
      );
      await tester.enterText(
        find.byKey(ListViewPage.dialogDescriptionFieldKey),
        "Outra Desc",
      );
      await tester.tap(find.byKey(ListViewPage.dialogAddButtonKey));
      await tester.pumpAndSettle();

      expect(find.text("Outro Item"), findsOneWidget);
      expect(find.byKey(ListViewPage.listViewKey), findsOneWidget);
      expect(find.byKey(ListViewPage.emptyListTextKey), findsNothing);
    });
  });
}
