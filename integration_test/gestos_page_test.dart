import 'package:appium_and_flutter_test/pages/home_page.dart';
import 'package:appium_and_flutter_test/pages/login_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/gestos_page.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Testes de Integração da GestosPage', () {
    Future<void> navigateToGestosPage(WidgetTester tester) async {
      app.main(); // Inicia o app
      // Aguarda um tempo para o app estabilizar na tela inicial (LoginPage ou HomePage)
      await tester.pumpAndSettle(const Duration(seconds: 1));

      // Se estiver na LoginPage, realiza o login
      if (tester.any(find.byType(LoginPage))) {
        await tester.enterText(
          find.byKey(LoginPage.usernameFieldKey),
          'admin', // Use um usuário válido, ex: 'admin' ou 'flutter'
        );
        await tester.enterText(
          find.byKey(LoginPage.passwordFieldKey),
          '1234', // Use uma senha válida, ex: '1234' ou '123456'
        );
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
      // Navega para GestosPage
      await tester.tap(find.byKey(HomePage.gesturesButtonKey));
      await tester.pumpAndSettle(); // Aguarda a navegação
      expect(
        find.byType(GestosPage),
        findsOneWidget,
        reason: "A GestosPage não foi carregada.",
      );
    }

    SignaturePainter getSignaturePainter(WidgetTester tester) {
      final customPaintFinder = find.descendant(
        of: find.byKey(GestosPage.drawingAreaKey),
        matching: find.byType(CustomPaint),
      );
      expect(
        customPaintFinder,
        findsOneWidget,
        reason: "CustomPaint não encontrado na área de desenho.",
      );
      final customPaintWidget = tester.widget<CustomPaint>(customPaintFinder);
      expect(
        customPaintWidget.painter,
        isA<SignaturePainter>(),
        reason: "O painter do CustomPaint não é um SignaturePainter.",
      );
      return customPaintWidget.painter as SignaturePainter;
    }

    // Helper para desenhar uma linha na área de desenho
    Future<void> drawLineOnCanvas(
      WidgetTester tester, {
      Offset from = const Offset(50, 50),
      Offset to = const Offset(150, 150),
    }) async {
      final drawingAreaFinder = find.byKey(GestosPage.drawingAreaKey);
      await tester.ensureVisible(drawingAreaFinder);
      await tester.pumpAndSettle();

      final Offset drawingAreaTopLeft = tester.getTopLeft(drawingAreaFinder);
      final Offset globalStartPoint = drawingAreaTopLeft + from;
      final Offset dragVector = to - from;

      await tester.dragFrom(globalStartPoint, dragVector);
      await tester.pumpAndSettle();
    }

    testWidgets('Desenha, muda cor, muda espessura e limpa a área de desenho', (
      WidgetTester tester,
    ) async {
      await navigateToGestosPage(tester);

      // 1. Estado Inicial
      SignaturePainter painter = getSignaturePainter(tester);
      expect(
        painter.lines.isEmpty,
        isTrue,
        reason: "Área de desenho não está vazia inicialmente.",
      );

      // 2. Desenha uma linha (cor padrão: preto, espessura padrão: 5.0)
      await drawLineOnCanvas(
        tester,
        from: const Offset(50, 50),
        to: const Offset(100, 100),
      );
      painter = getSignaturePainter(tester);
      expect(painter.lines.length, 1, reason: "Não desenhou uma linha.");
      expect(painter.lines.first?.points.isNotEmpty, isTrue);
      expect(
        painter.lines.first?.paint.color,
        Colors.black,
        reason: "Cor padrão da linha incorreta.",
      );
      expect(
        painter.lines.first?.paint.strokeWidth,
        5.0,
        reason: "Espessura padrão da linha incorreta.",
      );

      // 3. Muda a cor para Vermelho e desenha outra linha
      await tester.tap(find.byKey(GestosPage.colorDropdownKey));
      await tester.pumpAndSettle(); // Aguarda o dropdown abrir
      await tester.tap(
        find
            .byWidgetPredicate(
              (widget) =>
                  widget is DropdownMenuItem<Color> &&
                  widget.value == Colors.red,
            )
            .last,
      ); // .last é importante
      await tester.pumpAndSettle(); // Aguarda a seleção da cor

      await drawLineOnCanvas(
        tester,
        from: const Offset(60, 60),
        to: const Offset(120, 120),
      );
      painter = getSignaturePainter(tester);
      expect(
        painter.lines.length,
        2,
        reason: "Não desenhou a segunda linha após mudar a cor.",
      );
      expect(
        painter.lines.last?.paint.color,
        Colors.red,
        reason: "Cor da segunda linha (vermelha) incorreta.",
      );
      expect(
        painter.lines.last?.paint.strokeWidth,
        5.0,
        reason: "Espessura da segunda linha incorreta, deveria manter 5.0.",
      );

      // 4. Muda a espessura da linha para 10.0 e desenha outra linha
      final sliderFinder = find.byKey(GestosPage.strokeWidthSliderKey);
      await tester.ensureVisible(sliderFinder);
      await tester.pumpAndSettle();

      final Slider sliderWidget = tester.widget(sliderFinder);
      const double targetStrokeWidth = 10.0;
      final double relativeTapX =
          (targetStrokeWidth - sliderWidget.min) /
          (sliderWidget.max - sliderWidget.min);
      // Garante que relativeTapX esteja dentro do intervalo [0.0, 1.0].
      // Isso é uma proteção caso targetStrokeWidth esteja fora do intervalo min/max do slider.
      final double clampedRelativeTapX = relativeTapX.clamp(0.0, 1.0);

      // Toca no slider na posição relativa calculada
      final sliderRect = tester.getRect(sliderFinder);
      final Offset tapPosition = Offset(
        sliderRect.left + sliderRect.width * clampedRelativeTapX,
        sliderRect.top + sliderRect.height * 0.5,
      );
      await tester.tapAt(tapPosition);
      await tester.pumpAndSettle();

      // Verifica se o valor do slider foi atualizado
      final Slider updatedSliderWidget = tester.widget(sliderFinder);
      expect(
        updatedSliderWidget.value,
        closeTo(targetStrokeWidth, 0.1),
        reason:
            "Valor do slider não atualizado para $targetStrokeWidth como esperado.",
      );

      await drawLineOnCanvas(
        tester,
        from: const Offset(70, 70),
        to: const Offset(140, 140),
      );
      painter = getSignaturePainter(tester);
      expect(
        painter.lines.length,
        3,
        reason: "Não desenhou a terceira linha após mudar a espessura.",
      );
      expect(
        painter.lines.last?.paint.color,
        Colors.red,
        reason:
            "Cor da terceira linha incorreta (deveria ser vermelha, a última selecionada).",
      );
      expect(
        painter.lines.last?.paint.strokeWidth,
        closeTo(targetStrokeWidth, 0.1),
        reason: "Espessura da terceira linha incorreta.",
      );

      // 5. Limpa a área de desenho
      await tester.tap(find.byKey(GestosPage.clearAllButtonKey));
      await tester.pumpAndSettle();
      painter = getSignaturePainter(tester);
      expect(
        painter.lines.isEmpty,
        isTrue,
        reason: "Área de desenho não foi limpa.",
      );
    });
  });
}
