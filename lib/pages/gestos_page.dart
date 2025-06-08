import 'package:flutter/material.dart';

// Classe para armazenar os pontos e a pintura de um traço
class DrawingPoint {
  List<Offset> points;
  Paint paint;

  DrawingPoint({required this.points, required this.paint});
}

// CustomPainter para desenhar os traços na tela
class SignaturePainter extends CustomPainter {
  final List<DrawingPoint?> lines;

  SignaturePainter({required this.lines});

  @override
  void paint(Canvas canvas, Size size) {
    // print('DEBUG: SignaturePainter.paint called - Size: $size, Lines count: ${lines.length}');

    // Opcional: Desenhe um retângulo de borda para ver a área do canvas do CustomPaint
    // Paint debugBorderPaint = Paint()
    //   ..color = Colors.red
    //   ..style = PaintingStyle.stroke
    //   ..strokeWidth = 1.0; // Linha fina para não atrapalhar
    // canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), debugBorderPaint);

    for (var line in lines) {
      if (line != null && line.points.isNotEmpty) {
        // print('DEBUG: SignaturePainter - Drawing line with ${line.points.length} points. Color: ${line.paint.color}, StrokeWidth: ${line.paint.strokeWidth}');
        for (int i = 0; i < line.points.length - 1; i++) {
          final p1 = line.points[i];
          final p2 = line.points[i + 1];
          canvas.drawLine(p1, p2, line.paint);
        }
        if (line.points.length == 1) {
          canvas.drawCircle(
            line.points.first,
            line.paint.strokeWidth / 2,
            line.paint,
          );
        }
      }
    }
  }

  @override
  bool shouldRepaint(covariant SignaturePainter oldDelegate) {
    // Esta lógica é crucial e parece estar funcionando com as mudanças anteriores
    return oldDelegate.lines != lines;
  }
}

class GestosPage extends StatefulWidget {
  const GestosPage({super.key});
  // Keys for testing
  static const Key clearAllButtonKey = ValueKey('gestos_clear_all_button');
  static const Key drawingAreaKey = ValueKey('gestos_drawing_area');
  static const Key colorDropdownKey = ValueKey('gestos_color_dropdown');
  static const Key strokeWidthSliderKey = ValueKey(
    'gestos_stroke_width_slider',
  );

  @override
  State<GestosPage> createState() => _GestosPageState();
}

class _GestosPageState extends State<GestosPage> {
  // Removido 'final' para permitir reatribuição
  List<DrawingPoint?> _drawingLines = <DrawingPoint?>[];
  Color _selectedColor = Colors.black;
  double _strokeWidth = 5.0; // Certifique-se que este valor é razoável

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Desenho / Assinatura'),
        actions: [
          IconButton(
            key: GestosPage.clearAllButtonKey,
            icon: const Icon(Icons.clear_all),
            tooltip: 'Limpar Tudo',
            onPressed: () {
              setState(() {
                _drawingLines.clear(); // Limpar a lista existente
                // Opcional: para forçar a mudança de referência se _drawingLines.clear() não for suficiente
                // _drawingLines = [];
              });
            },
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Área de Desenho Refatorada
            Expanded(
              child: GestureDetector(
                key: GestosPage.drawingAreaKey,
                behavior: HitTestBehavior.opaque, // Mantém, é importante
                onPanStart: (details) {
                  setState(() {
                    _drawingLines = List.from(_drawingLines)
                      ..add(
                        DrawingPoint(
                          points: [details.localPosition],
                          paint: Paint()
                            ..color = _selectedColor
                            ..strokeWidth = _strokeWidth
                            ..strokeCap = StrokeCap.round
                            ..style = PaintingStyle.stroke,
                        ),
                      );
                  });
                },
                onPanUpdate: (details) {
                  if (_drawingLines.isNotEmpty && _drawingLines.last != null) {
                    setState(() {
                      DrawingPoint lastLine = _drawingLines.last!;
                      List<Offset> updatedPoints = List.from(lastLine.points)
                        ..add(details.localPosition);
                      DrawingPoint updatedLastLine = DrawingPoint(
                        points: updatedPoints,
                        paint: lastLine.paint,
                      );
                      _drawingLines = List.from(
                        _drawingLines.sublist(0, _drawingLines.length - 1),
                      )..add(updatedLastLine);
                    });
                  }
                },
                onPanEnd: (details) {
                  // Nenhum comportamento especial no final do traço por enquanto
                },
                child: CustomPaint(
                  painter: SignaturePainter(lines: _drawingLines),
                  // O child do CustomPaint define a área que ele tentará cobrir.
                  // Usar um Container com constraints.expand() garante que ele preencha o Expanded.
                  // A cor foi removida para garantir que o CustomPaint desenhe "direto" no que está abaixo.
                  child: Container(
                    constraints: const BoxConstraints.expand(),
                    // REMOVIDO: color: Colors.grey[200],
                  ),
                ),
              ),
            ),
            // Controles de Desenho
            _buildDrawingControls(),
          ],
        ),
      ),
    );
  }

  Widget _buildDrawingControls() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 12.0),
      color: Theme.of(context).colorScheme.surfaceVariant,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: <Widget>[
          DropdownButtonHideUnderline(
            child: DropdownButton<Color>(
              key: GestosPage.colorDropdownKey,
              value: _selectedColor,
              items: [
                DropdownMenuItem(
                  value: Colors.black,
                  child: _buildColorSwatch(Colors.black),
                ),
                DropdownMenuItem(
                  value: Colors.red,
                  child: _buildColorSwatch(Colors.red),
                ),
                DropdownMenuItem(
                  value: Colors.green,
                  child: _buildColorSwatch(Colors.green),
                ),
                DropdownMenuItem(
                  value: Colors.blue,
                  child: _buildColorSwatch(Colors.blue),
                ),
                DropdownMenuItem(
                  value: Colors.yellow,
                  child: _buildColorSwatch(Colors.yellow),
                ),
              ],
              onChanged: (Color? newColor) {
                if (newColor != null) {
                  setState(() {
                    _selectedColor = newColor;
                  });
                }
              },
            ),
          ),
          Expanded(
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text('Espessura:'),
                Expanded(
                  child: Slider(
                    key: GestosPage.strokeWidthSliderKey,
                    value: _strokeWidth,
                    min: 1.0, // Mínimo de 1.0 para garantir visibilidade
                    max: 20.0,
                    divisions: 19,
                    label: _strokeWidth.round().toString(),
                    onChanged: (double value) {
                      setState(() {
                        // Certifique-se que a espessura não seja zero ou muito pequena
                        _strokeWidth = value < 1.0 ? 1.0 : value;
                      });
                    },
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildColorSwatch(Color color) {
    return Container(
      width: 24,
      height: 24,
      decoration: BoxDecoration(
        color: color,
        shape: BoxShape.circle,
        border: Border.all(
          color: _selectedColor == color
              ? Theme.of(context).colorScheme.outline
              : Colors.transparent,
          width: 2,
        ),
      ),
    );
  }
}
