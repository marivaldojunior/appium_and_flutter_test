import 'package:flutter/material.dart';
import 'dart:math';
import '../model/list_item_data.dart'; // Para gerar IDs aleatórios

// --- Página ListView ---
class ListViewPage extends StatefulWidget {
  const ListViewPage({super.key});

  // Keys for testing
  static const Key addFloatingActionButtonKey = ValueKey('listview_add_fab');
  static const Key emptyListTextKey = ValueKey('listview_empty_text');
  static const Key listViewKey = ValueKey('listview_list');

  // Keys for Add/Edit Dialog
  static const Key addItemDialogKey = ValueKey('listview_add_item_dialog');
  static const Key editItemDialogKey = ValueKey('listview_edit_item_dialog');
  static const Key dialogTitleFieldKey = ValueKey(
    'listview_dialog_title_field',
  );
  static const Key dialogDescriptionFieldKey = ValueKey(
    'listview_dialog_description_field',
  );
  static const Key dialogCancelButtonKey = ValueKey(
    'listview_dialog_cancel_button',
  );
  static const Key dialogAddButtonKey = ValueKey('listview_dialog_add_button');
  static const Key dialogSaveButtonKey = ValueKey(
    'listview_dialog_save_button',
  );

  // Keys for Delete Confirmation Dialog
  static const Key deleteConfirmDialogKey = ValueKey(
    'listview_delete_confirm_dialog',
  );
  static const Key deleteConfirmCancelButtonKey = ValueKey(
    'listview_delete_confirm_cancel_button',
  );
  static const Key deleteConfirmDeleteButtonKey = ValueKey(
    'listview_delete_confirm_delete_button',
  );

  @override
  State<ListViewPage> createState() => _ListViewPageState();
}

class _ListViewPageState extends State<ListViewPage> {
  final List<ListItemData> _items = [];
  final Random _random = Random();

  @override
  void initState() {
    super.initState();
    // Adicionar alguns itens iniciais para demonstração
    _items.addAll([
      ListItemData(
        id: _generateId(),
        title: 'Item 1',
        description: 'Descrição detalhada do Item 1',
      ),
      ListItemData(
        id: _generateId(),
        title: 'Item 2',
        description: 'Explicação sobre o Item 2',
      ),
      ListItemData(
        id: _generateId(),
        title: 'Item 3',
        description: 'Mais informações do Item 3',
      ),
      ListItemData(
        id: _generateId(),
        title: 'Item 4',
        description: 'Detalhes extras para o Item 4',
      ),
    ]);
  }

  String _generateId() {
    return DateTime.now().millisecondsSinceEpoch.toString() +
        _random.nextInt(1000).toString();
  }

  void _addItem() {
    _showAddItemDialog();
  }

  void _showAddItemDialog() {
    final titleController = TextEditingController();
    final descriptionController = TextEditingController();
    final _formKey =
        GlobalKey<FormState>(); // Chave para validar o formulário do popup

    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          key: ListViewPage.addItemDialogKey,
          title: const Text('Adicionar Novo Item'),
          content: SingleChildScrollView(
            child: Form(
              // Adiciona um Form para validação
              key: _formKey,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  TextFormField(
                    key: ListViewPage.dialogTitleFieldKey,
                    // Usa TextFormField para validação
                    controller: titleController,
                    decoration: const InputDecoration(
                      labelText: 'Título',
                      hintText: 'Digite o título do item',
                    ),
                    autofocus: true,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'O título não pode estar vazio.';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    key: ListViewPage.dialogDescriptionFieldKey,
                    // Usa TextFormField para validação
                    controller: descriptionController,
                    decoration: const InputDecoration(
                      labelText: 'Descrição',
                      hintText: 'Digite a descrição do item',
                    ),
                    maxLines: 3,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'A descrição não pode estar vazia.';
                      }
                      return null;
                    },
                  ),
                ],
              ),
            ),
          ),
          actions: <Widget>[
            TextButton(
              key: ListViewPage.dialogCancelButtonKey,
              child: const Text('Cancelar'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
            TextButton(
              key: ListViewPage.dialogAddButtonKey,
              child: const Text('Adicionar'),
              onPressed: () {
                // Valida o formulário antes de adicionar
                if (_formKey.currentState!.validate()) {
                  final newItem = ListItemData(
                    id: _generateId(),
                    title: titleController.text,
                    description: descriptionController.text,
                  );
                  setState(() {
                    _items.add(newItem);
                  });
                  Navigator.of(context).pop(); // Fecha o popup
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Novo item adicionado!'),
                      duration: Duration(seconds: 1),
                    ),
                  );
                }
              },
            ),
          ],
        );
      },
    );
  }

  void _removeItem(String id) {
    setState(() {
      _items.removeWhere((item) => item.id == id);
    });
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Item removido!'),
        duration: Duration(seconds: 1),
      ),
    );
  }

  void _editItem(ListItemData itemToEdit) {
    final titleController = TextEditingController(text: itemToEdit.title);
    final descriptionController = TextEditingController(
      text: itemToEdit.description,
    );
    final formKey =
        GlobalKey<FormState>(); // Chave para validar o formulário do popup

    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          key: ListViewPage.editItemDialogKey,
          title: const Text('Editar Item'),
          content: SingleChildScrollView(
            child: Form(
              // Adiciona um Form para validação
              key: formKey,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  TextFormField(
                    key: ListViewPage.dialogTitleFieldKey,
                    // Usa TextFormField para validação
                    controller: titleController,
                    decoration: const InputDecoration(labelText: 'Título'),
                    autofocus: true,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'O título não pode estar vazio.';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    key: ListViewPage.dialogDescriptionFieldKey,
                    // Usa TextFormField para validação
                    controller: descriptionController,
                    decoration: const InputDecoration(labelText: 'Descrição'),
                    maxLines: 3,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'A descrição não pode estar vazia.';
                      }
                      return null;
                    },
                  ),
                ],
              ),
            ),
          ),
          actions: <Widget>[
            TextButton(
              key: ListViewPage.dialogCancelButtonKey,
              child: const Text('Cancelar'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
            TextButton(
              key: ListViewPage.dialogSaveButtonKey,
              child: const Text('Salvar'),
              onPressed: () {
                // Valida o formulário antes de salvar
                if (formKey.currentState!.validate()) {
                  setState(() {
                    final index = _items.indexWhere(
                      (item) => item.id == itemToEdit.id,
                    );
                    if (index != -1) {
                      _items[index] = itemToEdit.copyWith(
                        title: titleController.text,
                        description: descriptionController.text,
                      );
                    }
                  });
                  Navigator.of(context).pop();
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Item atualizado!'),
                      duration: Duration(seconds: 1),
                    ),
                  );
                }
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
      appBar: AppBar(title: const Text('Lista com Swipe')),
      body: _items.isEmpty
          ? const Center(
              key: ListViewPage.emptyListTextKey,
              child: Text(
                'Nenhum item na lista.\nAdicione alguns itens usando o botão "+".',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 16, color: Colors.grey),
              ),
            )
          : ListView.builder(
              key: ListViewPage.listViewKey,
              itemCount: _items.length,
              itemBuilder: (context, index) {
                final item = _items[index];
                return Dismissible(
                  // A chave do Dismissible já é única por item, o que é bom.
                  // Para interagir com o conteúdo do item (ListTile), podemos adicionar uma chave a ele.
                  key: Key(item.id), // Chave única para cada item Dismissible
                  // --- Swipe para Direita (Excluir) ---
                  background: Container(
                    color: Colors.red,
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    alignment: Alignment.centerLeft,
                    child: const Row(
                      mainAxisAlignment: MainAxisAlignment.start,
                      children: <Widget>[
                        Icon(Icons.delete, color: Colors.white),
                        SizedBox(width: 8),
                        Text(
                          'Excluir',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ),
                  // --- Swipe para Esquerda (Editar) ---
                  secondaryBackground: Container(
                    color: Colors.blue,
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    alignment: Alignment.centerRight,
                    child: const Row(
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: <Widget>[
                        Text(
                          'Editar',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        SizedBox(width: 8),
                        Icon(Icons.edit, color: Colors.white),
                      ],
                    ),
                  ),
                  confirmDismiss: (DismissDirection direction) async {
                    if (direction == DismissDirection.startToEnd) {
                      // Direita (Excluir)
                      // Mostrar diálogo de confirmação para excluir
                      return await showDialog(
                        context: context,
                        builder: (BuildContext context) {
                          return AlertDialog(
                            key: ListViewPage.deleteConfirmDialogKey,
                            title: const Text("Confirmar Exclusão"),
                            content: Text(
                              "Você tem certeza que deseja excluir '${item.title}'?",
                            ),
                            actions: <Widget>[
                              TextButton(
                                onPressed: () => Navigator.of(
                                  context,
                                ).pop(false), // Não exclui
                                key: ListViewPage.deleteConfirmCancelButtonKey,
                                child: const Text("Cancelar"),
                              ),
                              TextButton(
                                style: TextButton.styleFrom(
                                  foregroundColor: Colors.red,
                                ),
                                onPressed: () =>
                                    Navigator.of(context).pop(true), // Exclui
                                key: ListViewPage.deleteConfirmDeleteButtonKey,
                                child: const Text("Excluir"),
                              ),
                            ],
                          );
                        },
                      );
                    } else if (direction == DismissDirection.endToStart) {
                      // Esquerda (Editar)
                      _editItem(item);
                      return false; // Não remove o item da lista, apenas abre o popup
                    }
                    return false;
                  },
                  onDismissed: (DismissDirection direction) {
                    // Esta função só será chamada se confirmDismiss retornar true (para exclusão)
                    if (direction == DismissDirection.startToEnd) {
                      _removeItem(item.id);
                    }
                    // Ação de editar já foi tratada no confirmDismiss
                  },
                  child: Card(
                    margin: const EdgeInsets.symmetric(
                      horizontal: 8.0,
                      vertical: 4.0,
                    ),
                    child: ListTile(
                      // Adicionar uma chave ao ListTile se precisar interagir diretamente com ele (além do swipe)
                      key: ValueKey('list_item_${item.id}'),
                      title: Text(
                        item.title,
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: Text(item.description ?? ''),
                      leading: CircleAvatar(
                        child: Text(
                          item.title.isNotEmpty ? item.title[0] : '?',
                        ),
                      ),
                      onTap: () {
                        // Opcional: Ação ao tocar no item (ex: ver detalhes)
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text('Item selecionado: ${item.title}'),
                          ),
                        );
                      },
                    ),
                  ),
                );
              },
            ),
      floatingActionButton: FloatingActionButton(
        key: ListViewPage.addFloatingActionButtonKey,
        onPressed: _addItem,
        tooltip: 'Adicionar Item',
        child: const Icon(Icons.add),
      ),
    );
  }
}
