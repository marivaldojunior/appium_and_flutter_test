import 'package:flutter/material.dart';

class ClickPage extends StatelessWidget {
  const ClickPage({super.key});

  // Keys for testing
  static const Key doubleTapCardKey = ValueKey('click_page_double_tap_card');
  static const Key longPressCardKey = ValueKey('click_page_long_press_card');
  static const Key alertDialogKey = ValueKey('click_page_alert_dialog');
  static const Key alertDialogOkButtonKey = ValueKey(
    'click_page_alert_dialog_ok_button',
  );

  void _showAlertDialog(BuildContext context, String title, String message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          key: alertDialogKey,
          title: Text(title),
          content: Text(message),
          actions: <Widget>[
            TextButton(
              key: alertDialogOkButtonKey,
              child: const Text('OK'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Interações de Clique')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            // Card para Duplo Clique
            GestureDetector(
              key: doubleTapCardKey,
              onDoubleTap: () {
                _showAlertDialog(
                  context,
                  'Duplo Clique!',
                  'Você clicou duas vezes neste card.',
                );
              },
              child: Card(
                elevation: 4.0,
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: <Widget>[
                      Icon(
                        Icons.touch_app,
                        size: 40.0,
                        color: Theme.of(context).colorScheme.primary,
                      ),
                      const SizedBox(height: 16.0),
                      const Text(
                        'Card de Duplo Clique',
                        style: TextStyle(
                          fontSize: 18.0,
                          fontWeight: FontWeight.bold,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 8.0),
                      const Text(
                        'Toque duas vezes rapidamente aqui.',
                        textAlign: TextAlign.center,
                      ),
                    ],
                  ),
                ),
              ),
            ),

            const SizedBox(height: 32.0), // Espaçamento entre os cards
            // Card para Clique Longo
            GestureDetector(
              key: longPressCardKey,
              onLongPress: () {
                _showAlertDialog(
                  context,
                  'Clique Longo!',
                  'Você pressionou e segurou este card.',
                );
              },
              child: Card(
                elevation: 4.0,
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: <Widget>[
                      Icon(
                        Icons.timer_outlined,
                        size: 40.0,
                        color: Theme.of(context).colorScheme.secondary,
                      ),
                      const SizedBox(height: 16.0),
                      const Text(
                        'Card de Clique Longo',
                        style: TextStyle(
                          fontSize: 18.0,
                          fontWeight: FontWeight.bold,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 8.0),
                      const Text(
                        'Pressione e segure aqui.',
                        textAlign: TextAlign.center,
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
