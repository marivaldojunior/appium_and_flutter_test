import 'package:appium_and_flutter_test/pages/click_page.dart';
import 'package:appium_and_flutter_test/pages/recursos_page.dart';
import 'package:flutter/material.dart';
import 'forms_page.dart';
import 'gestos_page.dart';
import 'listview_page.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  Widget _buildGridButton(BuildContext context, String title, IconData icon, VoidCallback onPressed) {
    return Card(
      margin: const EdgeInsets.all(8.0),
      child: InkWell(
        onTap: onPressed,
        splashColor: Theme.of(context).primaryColorLight,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            Icon(icon, size: 48.0, color: Theme.of(context).primaryColor),
            const SizedBox(height: 10.0),
            Text(
              title,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 16.0),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Menu Principal'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(5.0),
        child: GridView.count(
          crossAxisCount: 2,
          crossAxisSpacing: 8.0,
          mainAxisSpacing: 8.0,
          children: <Widget>[
            _buildGridButton(
              context,
              'Formulários',
              Icons.description,
                  () {
                Navigator.push(context, MaterialPageRoute(builder: (context) => const FormsPage()));
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Navegar para Formulários')),
                );
              },
            ),
            _buildGridButton(
              context,
              'ListView',
              Icons.list_alt,
                  () {
                Navigator.push(context, MaterialPageRoute(builder: (context) => const ListViewPage()));
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Navegar para ListView')),
                );
              },
            ),
            _buildGridButton(
              context,
              'Recursos Nativos',
              Icons.smartphone,
                  () {
                Navigator.push(context, MaterialPageRoute(builder: (context) => const RecursosPage()));
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Navegar para Recursos Nativos')),
                );
              },
            ),
            _buildGridButton(
              context,
              'Gestos na Tela',
              Icons.gesture,
                  () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const GestosPage()),
                );
              },
            ),
            _buildGridButton(
              context,
              'Clicar e Segurar',
              Icons.touch_app,
                  () {
                    Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const ClickPage()),
                  );
              },
            ),
            // Você pode adicionar mais botões aqui, se necessário
            // Se o número de botões for ímpar e você quiser manter o layout,
            // você pode adicionar um SizedBox.shrink() ou um Container vazio para ocupar espaço,
            // ou ajustar a lógica de layout.
            // Exemplo:
            // if (numeroDeBotoesForImpar) Container(),
          ],
        ),
      ),
    );
  }
}