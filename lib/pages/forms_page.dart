import 'package:flutter/material.dart';
import 'package:intl/intl.dart'; // Para formatação de data

class FormsPage extends StatefulWidget {
  const FormsPage({super.key});

  @override
  State<FormsPage> createState() => _FormsPageState();
}

class _FormsPageState extends State<FormsPage> {
// Chave global para o formulário para validação e salvamento
  final _formKey = GlobalKey<FormState>();

// Controladores para campos de texto
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _ageController = TextEditingController();
  final TextEditingController _descriptionController = TextEditingController();

// Variáveis para outros tipos de input
  DateTime? _selectedDate;
  bool _isSubscribed = false;
  final Set<String> _selectedSkills = {}; // Usar Set para evitar duplicatas
  String? _selectedGender;
  String? _selectedCountry;

  final List<String> _availableSkills = ['Flutter', 'Dart', 'Firebase', 'Testing'];
  final List<String> _availableGenders = ['Masculino', 'Feminino', 'Outro'];
  final List<String> _availableCountries = ['Brasil', 'Portugal', 'EUA', 'Canadá'];

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate ?? DateTime.now(),
      firstDate: DateTime(1900),
      lastDate: DateTime.now().add(const Duration(days: 365 * 5)), // Permite selecionar até 5 anos no futuro
    );
    if (picked != null && picked != _selectedDate) {
      setState(() {
        _selectedDate = picked;
      });
    }
  }

  void _submitForm() {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save(); // Chama onSaved em cada FormField

// Aqui você teria a lógica para processar os dados do formulário
// Por exemplo, enviar para um backend ou salvar localmente
      print('Nome: ${_nameController.text}');
      print('Email: ${_emailController.text}');
      print('Idade: ${_ageController.text}');
      print('Data Selecionada: ${_selectedDate != null ? DateFormat('dd/MM/yyyy').format(_selectedDate!) : 'Não selecionada'}');
      print('Inscrito: $_isSubscribed');
      print('Habilidades: $_selectedSkills');
      print('Gênero: $_selectedGender');
      print('País: $_selectedCountry');
      print('Descrição: ${_descriptionController.text}');

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Formulário enviado com sucesso!')),
      );

  // Opcional: Limpar o formulário após o envio
  // _formKey.currentState!.reset();
  // _nameController.clear();
  // _emailController.clear();
  // _ageController.clear();
  // _descriptionController.clear();
  // setState(() {
  //   _selectedDate = null;
  //   _isSubscribed = false;
  //   _selectedSkills.clear();
  //   _selectedGender = null;
  //   _selectedCountry = null;
  // });

    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Por favor, corrija os erros no formulário.')),
      );
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _ageController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Formulários Diversos'),
      ),
      body: SafeArea(
        child: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Form(
          key: _formKey,
          child: ListView( // Usar ListView para permitir rolagem se o conteúdo for grande
            children: <Widget>[
              // Campo de Texto Simples (Nome)
              const SizedBox(height: 10.0),
              TextFormField(
                controller: _nameController,
                decoration: const InputDecoration(
                  labelText: 'Nome Completo',
                  hintText: 'Digite seu nome',
                  icon: Icon(Icons.person),
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor, insira seu nome.';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16.0),

              // Campo de Email
              TextFormField(
                controller: _emailController,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  hintText: 'exemplo@dominio.com',
                  icon: Icon(Icons.email),
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.emailAddress,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor, insira seu email.';
                  }
                  if (!RegExp(r"^[a-zA-Z0-9.a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9]+\.[a-zA-Z]+").hasMatch(value)) {
                    return 'Por favor, insira um email válido.';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16.0),

              // Campo Numérico (Idade)
              TextFormField(
                controller: _ageController,
                decoration: const InputDecoration(
                  labelText: 'Idade',
                  hintText: 'Sua idade',
                  icon: Icon(Icons.cake),
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor, insira sua idade.';
                  }
                  final n = num.tryParse(value);
                  if (n == null) {
                    return '"$value" não é um número válido.';
                  }
                  if (n <= 0 || n > 120) {
                    return 'Por favor, insira uma idade válida.';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16.0),

              // Seletor de Data
              ListTile(
                leading: const Icon(Icons.calendar_today, color: Colors.grey),
                title: Text(
                  _selectedDate == null
                      ? 'Selecione a Data de Nascimento'
                      : 'Data de Nascimento: ${DateFormat('dd/MM/yyyy').format(_selectedDate!)}',
                ),
                trailing: const Icon(Icons.arrow_drop_down),
                onTap: () => _selectDate(context),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(4.0),
                  side: BorderSide(color: Theme.of(context).colorScheme.onSurface.withOpacity(0.38)),
                ),
              ),
              // Adicionando um validador "manual" para o seletor de data
              FormField<DateTime>(
                builder: (FormFieldState<DateTime> state) {
                  return state.hasError
                      ? Padding(
                    padding: const EdgeInsets.only(top: 8.0, left: 16.0),
                    child: Text(
                      state.errorText!,
                      style: TextStyle(color: Theme.of(context).colorScheme.error, fontSize: 12),
                    ),
                  )
                      : Container(); // Sem erro, não mostra nada
                },
                validator: (value) {
                  if (_selectedDate == null) { // Usamos a variável de estado aqui
                    return 'Por favor, selecione uma data.';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16.0),

              // Switch (Inscrição)
              SwitchListTile(
                title: const Text('Receber notificações?'),
                secondary: Icon(_isSubscribed ? Icons.notifications_active : Icons.notifications_off),
                value: _isSubscribed,
                onChanged: (bool value) {
                  setState(() {
                    _isSubscribed = value;
                  });
                },
              ),
              const SizedBox(height: 16.0),

              // Checkboxes (Habilidades)
              const Text('Quais suas habilidades?', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              Column(
                children: _availableSkills.map((skill) {
                  return CheckboxListTile(
                    title: Text(skill),
                    value: _selectedSkills.contains(skill),
                    onChanged: (bool? selected) {
                      setState(() {
                        if (selected == true) {
                          _selectedSkills.add(skill);
                        } else {
                          _selectedSkills.remove(skill);
                        }
                      });
                    },
                  );
                }).toList(),
              ),
              // Adicionando um validador "manual" para checkboxes
              FormField<Set<String>>(
                builder: (FormFieldState<Set<String>> state) {
                  return state.hasError
                      ? Padding(
                    padding: const EdgeInsets.only(top: 0.0, left: 16.0),
                    child: Text(
                      state.errorText!,
                      style: TextStyle(color: Theme.of(context).colorScheme.error, fontSize: 12),
                    ),
                  )
                      : Container();
                },
                validator: (value) {
                  if (_selectedSkills.isEmpty) {
                    return 'Selecione ao menos uma habilidade.';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16.0),

              // Radio Buttons (Gênero)
              const Text('Gênero:', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              Column(
                children: _availableGenders.map((gender) {
                  return RadioListTile<String>(
                    title: Text(gender),
                    value: gender,
                    groupValue: _selectedGender,
                    onChanged: (String? value) {
                      setState(() {
                        _selectedGender = value;
                      });
                    },
                  );
                }).toList(),
              ),
              // Adicionando um validador "manual" para radio buttons
              FormField<String>(
                builder: (FormFieldState<String> state) {
                  return state.hasError
                      ? Padding(
                    padding: const EdgeInsets.only(top: 0.0, left: 16.0),
                    child: Text(
                      state.errorText!,
                      style: TextStyle(color: Theme.of(context).colorScheme.error, fontSize: 12),
                    ),
                  )
                      : Container();
                },
                validator: (value) {
                  if (_selectedGender == null) {
                    return 'Por favor, selecione seu gênero.';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16.0),
              // DropdownButton (País)
              DropdownButtonFormField<String>(
                decoration: const InputDecoration(
                  labelText: 'País de Origem',
                  icon: Icon(Icons.flag),
                  border: OutlineInputBorder(),
                ),
                value: _selectedCountry,
                hint: const Text('Selecione seu país'),
                isExpanded: true,
                items: _availableCountries.map((String country) {
                  return DropdownMenuItem<String>(
                    value: country,
                    child: Text(country),
                  );
                }).toList(),
                onChanged: (String? newValue) {
                  setState(() {
                    _selectedCountry = newValue;
                  });
                },
                validator: (value) => value == null ? 'Por favor, selecione um país.' : null,
              ),
              const SizedBox(height: 16.0),

              // Campo de Texto Multilinha (Descrição)
              TextFormField(
                controller: _descriptionController,
                decoration: const InputDecoration(
                  labelText: 'Sobre você (opcional)',
                  hintText: 'Conte-nos um pouco sobre você...',
                  icon: Icon(Icons.notes),
                  border: OutlineInputBorder(),
                ),
                maxLines: 3, // Permite múltiplas linhas
                keyboardType: TextInputType.multiline,
              ),
              const SizedBox(height: 24.0),

              // Botão de Envio
              ElevatedButton(
                onPressed: _submitForm,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16.0),
                  textStyle: const TextStyle(fontSize: 18),
                ),
                child: const Text('Enviar Formulário'),
              ),
              const SizedBox(height: 10.0),
            ],
          ),
        ),
      ),)
    );
  }
}