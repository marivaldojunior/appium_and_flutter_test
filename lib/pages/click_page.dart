import 'package:flutter/material.dart';

class ClickPage extends StatelessWidget {
  const ClickPage({super.key});

  void _showAlertDialog(BuildContext context, String title, String message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text(title),
          content: Text(message),
          actions: <Widget>[
            TextButton(
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
              onDoubleTap: () {
                print('Duplo clique detectado!');
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
              onLongPress: () {
                print('Clique longo detectado!');
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
