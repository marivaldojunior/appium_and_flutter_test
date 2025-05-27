import 'package:flutter/material.dart';

import 'home_page.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  final String _defaultUsername = 'admin';
  final String _defaultPassword = '1234';

  void _login() {
    if (_formKey.currentState!.validate()) {
      // Formulário é válido, verificar credenciais
      if (_usernameController.text == _defaultUsername &&
          _passwordController.text == _defaultPassword) {
        // Credenciais corretas - Navegue para a próxima tela ou mostre sucesso
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Login bem-sucedido!',
            style: TextStyle(
                color: Colors.white),
            ),
            backgroundColor: Colors.lightGreen,
          ),
        );
        // Exemplo: Navegar para uma tela inicial (HomePage)
         Navigator.pushReplacement(
           context,
           MaterialPageRoute(builder: (context) => const HomePage()),
         );
      } else {
        // Credenciais incorretas
        showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: const Text('Erro de Login'),
              content: const Text('Usuário ou senha incorretos.'),
              actions: <Widget>[
                TextButton(
                  child: const Text('OK'),
                  onPressed: () {
                    Navigator.of(context).pop(); // Fecha o diálogo
                  },
                ),
              ],
            );
          },
        );
      }
    }
  }

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
        centerTitle: true,
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: <Widget>[
                // Logos sobrepostos
                Column(
                  children: <Widget>[
                    Image.asset(
                      'assets/images/appium_logo.png',
                      height: 45,
                    ),
                    Image.asset(
                      'assets/images/flutter_logo.png',
                      height: 45,
                    ),
                  ],
                ),
                const SizedBox(height: 32.0),

                // Campo de Usuário
                TextFormField(
                  controller: _usernameController,
                  decoration: const InputDecoration(
                    labelText: 'Usuário',
                    hintText: 'Digite seu usuário',
                    prefixIcon: Icon(Icons.person_outline),
                    border: OutlineInputBorder(),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Por favor, insira o usuário';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16.0),

                // Campo de Senha
                TextFormField(
                  controller: _passwordController,
                  decoration: const InputDecoration(
                    labelText: 'Senha',
                    hintText: 'Digite sua senha',
                    prefixIcon: Icon(Icons.lock_outline),
                    border: OutlineInputBorder(),
                  ),
                  obscureText: true, // Esconde a senha
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Por favor, insira a senha';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 24.0),

                // Botão de Login
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blueAccent,
                    padding: const EdgeInsets.symmetric(vertical: 16.0),
                    textStyle: const TextStyle(fontSize: 18),
                  ),
                  onPressed: _login,
                  child: const Text('Entrar',
                    style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold),
                  ),
                ),
                const SizedBox(height: 16.0),

                // Link para "Esqueceu a senha?" (Opcional)
                TextButton(
                  onPressed: () {
                    // Lógica para esqueceu a senha
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Funcionalidade "Esqueceu a senha?" não implementada.')),
                    );
                  },
                  child: const Text('Esqueceu a senha?'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}