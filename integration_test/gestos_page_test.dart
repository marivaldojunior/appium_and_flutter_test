// test/integration/gestos_page_test.dart
import 'package:appium_and_flutter_test/main.dart' as app;
import 'package:appium_and_flutter_test/pages/gestos_page.dart';
import 'package:appium_and_flutter_test/pages/home_page.dart';
import 'package:appium_and_flutter_test/pages/login_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

// --- Constantes para os Testes ---
const String kCorrectUsername = 'admin';
const String kCorrectPassword = '1234';
const double kDefaultStrokeWidth = 5.0;
const double kTargetStrokeWidth = 10.0;
const Color kDefaultColor = Colors.black;
const Color kTargetColor = Colors.red;

// --- Funções Auxiliares de Teste ---

/// Garante um estado limpo, inicializando o app e navegando até a [GestosPage].
Future<void> _initializeAppAndNavigateToGestos(WidgetTester tester) async {
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
  await tester.tap(find.byKey(HomePage.gesturesButtonKey));
  await tester.pumpAndSettle();
  expect(find.byType(GestosPage), findsOneWidget);
}

/// Obtém o estado atual do painter da área de desenho.
SignaturePainter _getPainterState(WidgetTester tester) {
  final customPaintFinder = find.descendant(
    of: find.byKey(GestosPage.drawingAreaKey),
    matching: find.byType(CustomPaint),
  );
  expect(customPaintFinder, findsOneWidget);
  final customPaintWidget = tester.widget<CustomPaint>(customPaintFinder);
  expect(customPaintWidget.painter, isA<SignaturePainter>());
  return customPaintWidget.painter as SignaturePainter;
}

/// Desenha uma linha na área de desenho.
Future<void> _drawLine(WidgetTester tester) async {
  final drawingAreaFinder = find.byKey(GestosPage.drawingAreaKey);
  await tester.drag(drawingAreaFinder, const Offset(100, 100));
  await tester.pumpAndSettle();
}

/// Altera a cor no dropdown.
Future<void> _changeColor(WidgetTester tester, Color color) async {
  await tester.tap(find.byKey(GestosPage.colorDropdownKey));
  await tester.pumpAndSettle();
  // .last é usado para garantir que estamos tocando no item do menu, não no item já selecionado.
  await tester.tap(
    find
        .byWidgetPredicate(
          (w) => w is DropdownMenuItem<Color> && w.value == color,
        )
        .last,
  );
  await tester.pumpAndSettle();
}

/// Altera o valor do slider de espessura.
Future<void> _changeStrokeWidth(WidgetTester tester, double value) async {
  final sliderFinder = find.byKey(GestosPage.strokeWidthSliderKey);
  final sliderWidget = tester.widget<Slider>(sliderFinder);
  final relativePosition =
      (value - sliderWidget.min) / (sliderWidget.max - sliderWidget.min);
  // Calculate the position to tap on the slider based on its RenderBox.
  final sliderBox = tester.renderObject<RenderBox>(sliderFinder);
  final sliderOffset = sliderBox.localToGlobal(Offset.zero);
  final tapPosition =
      sliderOffset +
      Offset(
        sliderBox.size.width * relativePosition,
        sliderBox.size.height / 2,
      );
  await tester.tapAt(tapPosition);
  await tester.pumpAndSettle();
}

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Testes de Integração da GestosPage', () {
    testWidgets('Deve iniciar com a área de desenho vazia', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigateToGestos(tester);

      // Act
      final painter = _getPainterState(tester);

      // Assert
      expect(
        painter.lines.isEmpty,
        isTrue,
        reason: "A área de desenho deveria estar vazia inicialmente.",
      );
    });

    testWidgets('Deve desenhar uma linha com as configurações padrão', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigateToGestos(tester);

      // Act
      await _drawLine(tester);
      final painter = _getPainterState(tester);

      // Assert
      expect(
        painter.lines.length,
        1,
        reason: "Uma linha deveria ser desenhada.",
      );
      final line = painter.lines.first;
      expect(line, isNotNull);
      expect(
        line?.paint.color,
        kDefaultColor,
        reason: "A cor padrão da linha está incorreta.",
      );
      expect(
        line?.paint.strokeWidth,
        kDefaultStrokeWidth,
        reason: "A espessura padrão da linha está incorreta.",
      );
    });

    testWidgets('Deve alterar a cor da linha e desenhar novamente', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigateToGestos(tester);

      // Act: Muda a cor e desenha.
      await _changeColor(tester, kTargetColor);
      await _drawLine(tester);
      final painter = _getPainterState(tester);

      // Assert
      expect(
        painter.lines.length,
        1,
        reason: "Deveria ter apenas uma linha após a mudança de cor.",
      );
      expect(
        painter.lines.last?.paint.color,
        kTargetColor,
        reason: "A cor da linha não foi alterada para a cor alvo.",
      );
    });

    testWidgets('Deve alterar a espessura da linha e desenhar novamente', (
      WidgetTester tester,
    ) async {
      // Arrange
      await _initializeAppAndNavigateToGestos(tester);

      // Act: Muda a espessura e desenha.
      await _changeStrokeWidth(tester, kTargetStrokeWidth);
      await _drawLine(tester);
      final painter = _getPainterState(tester);

      // Assert
      expect(
        painter.lines.length,
        1,
        reason: "Deveria ter apenas uma linha após a mudança de espessura.",
      );
      expect(
        painter.lines.last?.paint.strokeWidth,
        closeTo(kTargetStrokeWidth, 0.1),
        reason: "A espessura da linha não foi alterada corretamente.",
      );
    });

    testWidgets('Deve limpar a área de desenho após clicar no botão "Limpar"', (
      WidgetTester tester,
    ) async {
      // Arrange: Desenha algo para que haja o que limpar.
      await _initializeAppAndNavigateToGestos(tester);
      await _drawLine(tester);
      var painter = _getPainterState(tester);
      expect(painter.lines.isNotEmpty, isTrue);

      // Act: Clica no botão de limpar.
      await tester.tap(find.byKey(GestosPage.clearAllButtonKey));
      await tester.pumpAndSettle();
      painter = _getPainterState(tester);

      // Assert
      expect(
        painter.lines.isEmpty,
        isTrue,
        reason: "A área de desenho não foi limpa após o clique no botão.",
      );
    });
  });
}
