// test/integration/recursos_page_test.dart
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/home_page.dart';
import 'package:appium_and_flutter_test/pages/login_page.dart';
import 'package:appium_and_flutter_test/pages/recursos_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

// --- Constantes para os Testes ---
const String kInitialImageText = 'Nenhuma imagem selecionada';
const String kNoImageTakenSnackbarMsg = 'Nenhuma imagem tirada.';
const String kNoImageSelectedSnackbarMsg = 'Nenhuma imagem selecionada.';
const String kCorrectUsername = 'admin';
const String kCorrectPassword = '1234';

// --- Funções Auxiliares de Teste ---

/// Inicializa o app, faz login e navega até a [RecursosPage].
/// Garante um estado limpo e consistente para o início de cada teste.
Future<void> _initializeAppAndNavigateToRecursos(WidgetTester tester) async {
  // Arrange: Inicia o app do zero.
  app.main();
  await tester.pumpAndSettle();

  // Act: Faz login se estiver na LoginPage.
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

  // Assert: Garante que chegou na HomePage.
  expect(
    find.byType(HomePage),
    findsOneWidget,
    reason: "Deveria estar na HomePage após o login.",
  );

  // Act: Navega para a RecursosPage.
  await tester.tap(find.byKey(HomePage.nativeResourcesButtonKey));
  await tester.pumpAndSettle();

  // Assert: Confirma que a RecursosPage foi carregada.
  expect(
    find.byType(RecursosPage),
    findsOneWidget,
    reason: "Deveria ter navegado para a RecursosPage.",
  );
}

/// Testa a seleção de uma fonte de imagem (Câmera ou Galeria) e verifica o SnackBar esperado,
/// simulando o cancelamento da seleção (retorno nulo do ImagePicker).
Future<void> _testImageSelectionSourceAndCancel(
  WidgetTester tester, {
  required Key sourceOptionKey,
  required String expectedSnackbarMsg,
}) async {
  // Act: Abre o seletor de fonte de imagem.
  await tester.tap(find.byKey(RecursosPage.selectImageButtonKey));
  await tester.pumpAndSettle();

  // Assert: Verifica se o ModalBottomSheet com as opções está visível.
  expect(find.byKey(RecursosPage.imageSourceSheetKey), findsOneWidget);
  expect(find.byKey(sourceOptionKey), findsOneWidget);

  // Act: Toca na opção desejada (Câmera ou Galeria).
  await tester.tap(find.byKey(sourceOptionKey));
  // Aguarda o fechamento do sheet e a chamada do ImagePicker (que retornará null).
  await tester.pumpAndSettle();

  // Assert: Verifica se a SnackBar correta foi exibida.
  expect(find.text(expectedSnackbarMsg), findsOneWidget);

  // Act: Aguarda a SnackBar desaparecer.
  await tester.pumpAndSettle(
    const Duration(seconds: 4),
  ); // Duração padrão de uma SnackBar.

  // Assert: Confirma que a SnackBar desapareceu.
  expect(find.text(expectedSnackbarMsg), findsNothing);
}

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Testes de Integração da RecursosPage', () {
    // O setUp é executado ANTES de cada teste no grupo, garantindo isolamento.
    setUp((() async {
      // Como a navegação é o ponto de partida para todos os testes,
      // a inicialização é feita dentro de cada teste para garantir um
      // ambiente completamente novo e evitar estados compartilhados.
    }));

    testWidgets(
      'Deve exibir a UI inicial corretamente, sem imagem selecionada',
      (WidgetTester tester) async {
        // Arrange
        await _initializeAppAndNavigateToRecursos(tester);

        // Assert: Verifica os elementos visíveis no estado inicial.
        expect(find.byKey(RecursosPage.imageDisplayAreaKey), findsOneWidget);
        expect(find.text(kInitialImageText), findsOneWidget);
        expect(find.byIcon(Icons.image_search), findsOneWidget);
        expect(find.byKey(RecursosPage.selectImageButtonKey), findsOneWidget);

        // Assert: Verifica que o botão de remover não está visível.
        expect(find.byKey(RecursosPage.removeImageButtonKey), findsNothing);
      },
    );

    testWidgets(
      'Deve exibir SnackBar ao simular cancelamento da seleção da galeria',
      (WidgetTester tester) async {
        // Arrange
        await _initializeAppAndNavigateToRecursos(tester);

        // Act & Assert
        await _testImageSelectionSourceAndCancel(
          tester,
          sourceOptionKey: RecursosPage.imageSourceSheetGalleryOptionKey,
          expectedSnackbarMsg: kNoImageSelectedSnackbarMsg,
        );

        // Assert final: Confirma que o estado da página não mudou.
        expect(find.text(kInitialImageText), findsOneWidget);
        expect(find.byKey(RecursosPage.removeImageButtonKey), findsNothing);
      },
    );

    testWidgets(
      'Deve exibir SnackBar ao simular cancelamento da captura da câmera',
      (WidgetTester tester) async {
        // Arrange
        await _initializeAppAndNavigateToRecursos(tester);

        // Act & Assert
        await _testImageSelectionSourceAndCancel(
          tester,
          sourceOptionKey: RecursosPage.imageSourceSheetCameraOptionKey,
          expectedSnackbarMsg: kNoImageTakenSnackbarMsg,
        );

        // Assert final: Confirma que o estado da página não mudou.
        expect(find.text(kInitialImageText), findsOneWidget);
        expect(find.byKey(RecursosPage.removeImageButtonKey), findsNothing);
      },
    );
  });
}
