import 'package:appium_and_flutter_test/pages/home_page.dart';
import 'package:appium_and_flutter_test/pages/login_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/recursos_page.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  Future<void> _navigateToRecursosPage(WidgetTester tester) async {
    app.main(); // Inicia o app
    await tester.pumpAndSettle(const Duration(seconds: 1));

    if (tester.any(find.byType(LoginPage))) {
      await tester.enterText(find.byKey(LoginPage.usernameFieldKey), 'admin');
      await tester.enterText(find.byKey(LoginPage.passwordFieldKey), '1234');
      await tester.tap(find.byKey(LoginPage.loginButtonKey));
      await tester.pumpAndSettle(const Duration(seconds: 3));
    }

    expect(
      find.byType(HomePage),
      findsOneWidget,
      reason: "Não foi possível alcançar a HomePage.",
    );

    await tester.tap(find.byKey(HomePage.nativeResourcesButtonKey));
    await tester.pumpAndSettle();

    expect(
      find.byType(RecursosPage),
      findsOneWidget,
      reason: "RecursosPage não foi carregada.",
    );
  }

  group('Testes de Integração da RecursosPage', () {
    testWidgets(
      'Verifica UI inicial e interage com seletores de imagem (simulando nenhuma seleção)',
      (WidgetTester tester) async {
        await _navigateToRecursosPage(tester);

        // 1. Verifica estado inicial da UI
        expect(find.byKey(RecursosPage.imageDisplayAreaKey), findsOneWidget);
        expect(find.text('Nenhuma imagem selecionada'), findsOneWidget);
        expect(find.byIcon(Icons.image_search), findsOneWidget);

        expect(find.byKey(RecursosPage.openCameraButtonKey), findsOneWidget);
        expect(find.byKey(RecursosPage.openGalleryButtonKey), findsOneWidget);
        expect(find.byKey(RecursosPage.selectImageButtonKey), findsOneWidget);

        // O botão de remover imagem não deve estar visível inicialmente
        expect(find.byKey(RecursosPage.removeImageButtonKey), findsNothing);

        // 2. Tenta abrir a câmera (ImagePicker retornará null no teste)
        await tester.tap(find.byKey(RecursosPage.openCameraButtonKey));
        // O ImagePicker abre uma UI nativa. Em testes, sem interação manual ou mocks avançados,
        // ele geralmente retorna null rapidamente.
        await tester.pumpAndSettle(
          const Duration(seconds: 2),
        ); // Aguarda possível SnackBar ou atualização de estado

        // Verifica se a SnackBar de "Nenhuma imagem tirada" apareceu
        expect(find.text('Nenhuma imagem tirada.'), findsOneWidget);
        // Aguarda a SnackBar desaparecer
        await tester.pumpAndSettle(const Duration(seconds: 2));
        expect(find.text('Nenhuma imagem tirada.'), findsNothing);

        // 3. Tenta abrir a galeria (ImagePicker retornará null no teste)
        await tester.tap(find.byKey(RecursosPage.openGalleryButtonKey));
        await tester.pumpAndSettle(const Duration(seconds: 2));

        // Verifica se a SnackBar de "Nenhuma imagem selecionada" apareceu
        expect(find.text('Nenhuma imagem selecionada.'), findsOneWidget);
        // Aguarda a SnackBar desaparecer
        await tester.pumpAndSettle(const Duration(seconds: 2));
        expect(find.text('Nenhuma imagem selecionada.'), findsNothing);

        // 4. Tenta selecionar imagem via ActionSheet (Galeria)
        await tester.tap(find.byKey(RecursosPage.selectImageButtonKey));
        await tester.pumpAndSettle(); // Aguarda o ModalBottomSheet aparecer

        expect(find.byKey(RecursosPage.imageSourceSheetKey), findsOneWidget);
        expect(
          find.byKey(RecursosPage.imageSourceSheetGalleryOptionKey),
          findsOneWidget,
        );
        expect(
          find.byKey(RecursosPage.imageSourceSheetCameraOptionKey),
          findsOneWidget,
        );

        // Clica na opção Galeria
        await tester.tap(
          find.byKey(RecursosPage.imageSourceSheetGalleryOptionKey),
        );
        await tester
            .pumpAndSettle(); // ModalBottomSheet fecha, ImagePicker é chamado
        await tester.pumpAndSettle(
          const Duration(seconds: 2),
        ); // Aguarda SnackBar

        expect(find.text('Nenhuma imagem selecionada.'), findsOneWidget);
        await tester.pumpAndSettle(const Duration(seconds: 2));

        // 5. Tenta selecionar imagem via ActionSheet (Câmera)
        await tester.tap(find.byKey(RecursosPage.selectImageButtonKey));
        await tester.pumpAndSettle();

        expect(find.byKey(RecursosPage.imageSourceSheetKey), findsOneWidget);

        // Clica na opção Câmera
        await tester.tap(
          find.byKey(RecursosPage.imageSourceSheetCameraOptionKey),
        );
        await tester.pumpAndSettle();
        await tester.pumpAndSettle(const Duration(seconds: 2));

        expect(find.text('Nenhuma imagem tirada.'), findsOneWidget);
        await tester.pumpAndSettle(const Duration(seconds: 2));

        // Confirma que a área de imagem ainda mostra "Nenhuma imagem selecionada"
        // pois não simulamos o carregamento de uma imagem real.
        expect(find.text('Nenhuma imagem selecionada'), findsOneWidget);
        expect(find.byKey(RecursosPage.removeImageButtonKey), findsNothing);
      },
    );
  });
}
