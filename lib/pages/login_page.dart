import 'package:flutter/material.dart';

import 'home_page.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key}); // A key do construtor principal já está aqui.
  // --- Keys para Testes ---
  static const Key usernameFieldKey = ValueKey('login_username_field');
  static const Key passwordFieldKey = ValueKey('login_password_field');
  static const Key loginButtonKey = ValueKey('login_button');
  static const Key forgotPasswordButtonKey = ValueKey(
    'login_forgot_password_button',
  );
  static const Key snackbarForgotPasswordButtonKey = ValueKey(
    'login_snackbar_forgot_password_info',
  );
  static const Key alertDialogErrorOkButtonKey = ValueKey(
    'login_alert_error_ok_button',
  );

  // --- Fim das Keys para Testes ---

  @override
  State<LoginPage> createState() => LoginPageState();
}

class LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  final String _defaultUsername = 'admin';
  final String _defaultPassword = '1234';

  void _login() {
    if (_formKey.currentState!.validate()) {
      if (_usernameController.text == _defaultUsername &&
          _passwordController.text == _defaultPassword) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            key: ValueKey('login_snackbar_success'), // Key para o SnackBar
            content: Text(
              'Login bem-sucedido!',
              style: TextStyle(color: Colors.white),
            ),
            backgroundColor: Colors.lightGreen,
          ),
        );
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => const HomePage()),
        );
      } else {
        showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              key: const ValueKey(
                'login_alert_error',
              ), // Key para o AlertDialog
              title: const Text('Erro de Login'),
              content: const Text('Usuário ou senha incorretos.'),
              actions: <Widget>[
                Tooltip(
                  message: 'Confirmar erro de login', // Mensagem do Tooltip
                  child: TextButton(
                    key: LoginPage
                        .alertDialogErrorOkButtonKey, // Usar a const definida acima
                    child: const Text('OK'),
                    onPressed: () {
                      Navigator.of(context).pop();
                    },
                  ),
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
        title: const Text(
          'Login',
        ), // O texto aqui já serve como uma boa referência semântica
        centerTitle: true,
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Form(
            key: _formKey, // GlobalKey para o Form, útil para validação
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: <Widget>[
                Column(
                  children: <Widget>[
                    Semantics(
                      label: 'Logotipo Appium', // Label para acessibilidade
                      child: Image.asset(
                        'assets/images/appium_logo.png',
                        height: 45,
                      ),
                    ),
                    Semantics(
                      label: 'Logotipo Flutter', // Label para acessibilidade
                      child: Image.asset(
                        'assets/images/flutter_logo.png',
                        height: 45,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 32.0),

                // Campo de Usuário
                TextFormField(
                  key: LoginPage.usernameFieldKey, // Key para teste
                  controller: _usernameController,
                  decoration: const InputDecoration(
                    labelText: 'Usuário', // Bom para semântica e Appium
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
                  key: LoginPage.passwordFieldKey, // Key para teste
                  controller: _passwordController,
                  decoration: const InputDecoration(
                    labelText: 'Senha', // Bom para semântica e Appium
                    hintText: 'Digite sua senha',
                    prefixIcon: Icon(Icons.lock_outline),
                    border: OutlineInputBorder(),
                  ),
                  obscureText: true,
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
                  key: LoginPage.loginButtonKey, // Key para teste
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blueAccent,
                    padding: const EdgeInsets.symmetric(vertical: 16.0),
                    textStyle: const TextStyle(fontSize: 18),
                  ),
                  onPressed: _login,
                  // O child Text('Entrar') já é um bom identificador semântico para Appium.
                  child: const Text(
                    'Entrar',
                    style: TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                const SizedBox(height: 16.0),

                // Link para "Esqueceu a senha?"
                Tooltip(
                  message: 'Recuperar senha esquecida', // Mensagem do Tooltip
                  child: TextButton(
                    key: LoginPage.forgotPasswordButtonKey,
                    onPressed: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          key: LoginPage.snackbarForgotPasswordButtonKey,
                          content: Text(
                            'Funcionalidade "Esqueceu a senha?" não implementada.',
                          ),
                        ),
                      );
                    },
                    child: const Text('Esqueceu a senha?'),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
