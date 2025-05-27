import 'package:flutter/material.dart';

import 'forms_page.dart';
import 'listview_page.dart';

// Importe as páginas para as quais você irá navegar
// Exemplo:
// import 'forms_page.dart';
// import 'list_view_page.dart';
// import 'native_features_page.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  // Função auxiliar para criar os botões da grade
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
          crossAxisCount: 2, // Define dois itens por linha
          crossAxisSpacing: 8.0, // Espaçamento horizontal entre os itens
          mainAxisSpacing: 8.0, // Espaçamento vertical entre os itens
          children: <Widget>[
            _buildGridButton(
              context,
              'Formulários',
              Icons.description, // Ícone para formulários
                  () {
                // Navegar para a página de Formulários
                Navigator.push(context, MaterialPageRoute(builder: (context) => const FormsPage()));
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Navegar para Formulários')),
                );
              },
            ),
            _buildGridButton(
              context,
              'ListView',
              Icons.list_alt, // Ícone para ListView
                  () {
                // Navegar para a página de ListView
                Navigator.push(context, MaterialPageRoute(builder: (context) => const ListViewPage()));
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Navegar para ListView')),
                );
              },
            ),
            _buildGridButton(
              context,
              'Recursos Nativos',
              Icons.smartphone, // Ícone para Recursos Nativos
                  () {
                // Navegar para a página de Recursos Nativos
                // Exemplo:
                // Navigator.push(context, MaterialPageRoute(builder: (context) => const NativeFeaturesPage()));
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Navegar para Recursos Nativos')),
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