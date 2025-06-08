import 'package:appium_and_flutter_test/pages/click_page.dart';
import 'package:appium_and_flutter_test/pages/recursos_page.dart';
import 'package:flutter/material.dart';
import 'chat_page.dart';
import 'forms_page.dart';
import 'gestos_page.dart';
import 'listview_page.dart';
import 'login_page.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  static const Key logoutButtonKey = ValueKey('home_logout_button');
  static const Key logoutDialogKey = ValueKey('home_logout_dialog');
  static const Key logoutDialogCancelButtonKey = ValueKey(
    'home_logout_dialog_cancel_button',
  );
  static const Key logoutDialogConfirmButtonKey = ValueKey(
    'home_logout_dialog_confirm_button',
  );
  static const Key formsButtonKey = ValueKey('home_forms_button');
  static const Key listViewButtonKey = ValueKey('home_listview_button');
  static const Key nativeResourcesButtonKey = ValueKey(
    'home_native_resources_button',
  );
  static const Key gesturesButtonKey = ValueKey('home_gestures_button');
  static const Key clickAndHoldButtonKey = ValueKey(
    'home_click_and_hold_button',
  );
  static const Key chatButtonKey = ValueKey('home_chat_button');

  Widget _buildGridButton(
    BuildContext context,
    String title,
    IconData icon,
    VoidCallback onPressed,
    Key? key,
  ) {
    return Card(
      margin: const EdgeInsets.all(8.0),
      key: key,
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

  void _showLogoutDialog(BuildContext context) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext dialogContext) {
        return AlertDialog(
          key: logoutDialogKey,
          title: const Text('Confirmar Logout'),
          content: const Text('Você tem certeza que deseja sair?'),
          actions: <Widget>[
            Tooltip(
              message: 'Cancelar ação de logout',
              child: TextButton(
                key: logoutDialogCancelButtonKey,
                child: const Text('Cancelar'),
                onPressed: () {
                  Navigator.of(dialogContext).pop();
                },
              ),
            ),
            Tooltip(
              message: 'Confirmar e efetuar logout',
              child: TextButton(
                key: logoutDialogConfirmButtonKey,
                child: const Text('Sair'),
                onPressed: () {
                  Navigator.of(dialogContext).pop();
                  Navigator.pushAndRemoveUntil(
                    context,
                    MaterialPageRoute(builder: (context) => const LoginPage()),
                    (Route<dynamic> route) => false,
                  );
                },
              ),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Menu Principal'),
        centerTitle: true,
        actions: <Widget>[
          Tooltip(
            message: 'Sair do aplicativo',
            child: IconButton(
              key: logoutButtonKey,
              icon: const Icon(Icons.logout),
              onPressed: () {
                _showLogoutDialog(context);
              },
            ),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(5.0),
        child: GridView.count(
          crossAxisCount: 2,
          crossAxisSpacing: 8.0,
          mainAxisSpacing: 8.0,
          children: <Widget>[
            _buildGridButton(context, 'Formulários', Icons.description, () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const FormsPage()),
              );
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Navegar para Formulários')),
              );
            }, formsButtonKey),
            _buildGridButton(context, 'ListView', Icons.list_alt, () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const ListViewPage()),
              );
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Navegar para ListView')),
              );
            }, listViewButtonKey),
            _buildGridButton(context, 'Recursos Nativos', Icons.smartphone, () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const RecursosPage()),
              );
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Navegar para Recursos Nativos')),
              );
            }, nativeResourcesButtonKey),
            _buildGridButton(context, 'Gestos na Tela', Icons.gesture, () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const GestosPage()),
              );
            }, gesturesButtonKey),
            _buildGridButton(context, 'Clicar e Segurar', Icons.touch_app, () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const ClickPage()),
              );
            }, clickAndHoldButtonKey),
            _buildGridButton(
              // ou qualquer outro botão/trigger
              context,
              'Chat Simulado',
              Icons.chat_bubble_outline,
              () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const ChatPage()),
                );
              },
              chatButtonKey,
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
