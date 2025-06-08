import 'dart:io'; // Para usar a classe File
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class RecursosPage extends StatefulWidget {
  const RecursosPage({super.key});

  // Keys for testing
  static const Key imageDisplayAreaKey = ValueKey(
    'recursos_image_display_area',
  );
  static const Key openCameraButtonKey = ValueKey(
    'recursos_open_camera_button',
  );
  static const Key openGalleryButtonKey = ValueKey(
    'recursos_open_gallery_button',
  );
  static const Key removeImageButtonKey = ValueKey(
    'recursos_remove_image_button',
  );
  static const Key selectImageButtonKey = ValueKey(
    'recursos_select_image_button',
  ); // For the alternative button

  // Keys for ModalBottomSheet options
  static const Key imageSourceSheetKey = ValueKey(
    'recursos_image_source_sheet',
  );
  static const Key imageSourceSheetGalleryOptionKey = ValueKey(
    'recursos_image_source_sheet_gallery_option',
  );
  static const Key imageSourceSheetCameraOptionKey = ValueKey(
    'recursos_image_source_sheet_camera_option',
  );

  @override
  State<RecursosPage> createState() => _RecursosPageState();
}

class _RecursosPageState extends State<RecursosPage> {
  File?
  _imageFile; // Variável para armazenar o arquivo da imagem selecionada/tirada
  final ImagePicker _picker = ImagePicker(); // Instância do ImagePicker

  // Função genérica para pegar imagem
  Future<void> _pickImage(ImageSource source) async {
    try {
      final XFile? pickedFile = await _picker.pickImage(
        source: source,
        imageQuality: 80, // Opcional: define a qualidade da imagem (0-100)
        // maxWidth: 800,  // Opcional: define o tamanho máximo da imagem
        // maxHeight: 600,
      );

      if (pickedFile != null) {
        setState(() {
          _imageFile = File(pickedFile.path);
        });
      } else {
        if (mounted) {
          // Verifica se o widget ainda está na árvore
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(
                source == ImageSource.camera
                    ? 'Nenhuma imagem tirada.'
                    : 'Nenhuma imagem selecionada.',
              ),
            ),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        // Verifica se o widget ainda está na árvore
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Erro ao acessar ${source == ImageSource.camera ? "câmera" : "galeria"}: $e',
            ),
          ),
        );
      }
    }
  }

  void _showImageSourceActionSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      builder: (BuildContext bc) {
        return Container(
          // Wrap with a container to assign a key to the sheet itself
          key: RecursosPage.imageSourceSheetKey,
          child: SafeArea(
            child: Wrap(
              children: <Widget>[
                ListTile(
                  key: RecursosPage.imageSourceSheetGalleryOptionKey,
                  leading: const Icon(Icons.photo_library),
                  title: const Text('Abrir Galeria'),
                  onTap: () {
                    Navigator.of(context).pop();
                    _pickImage(ImageSource.gallery);
                  },
                ),
                ListTile(
                  key: RecursosPage.imageSourceSheetCameraOptionKey,
                  leading: const Icon(Icons.photo_camera),
                  title: const Text('Abrir Câmera'),
                  onTap: () {
                    Navigator.of(context).pop();
                    _pickImage(ImageSource.camera);
                  },
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Câmera e Galeria')),
      body: Center(
        child: SingleChildScrollView(
          // Para o caso da imagem ser grande ou a tela pequena
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              // Área para exibir a imagem
              Container(
                key: RecursosPage.imageDisplayAreaKey,
                height: 300, // Altura fixa para o container da imagem
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey.shade400, width: 1),
                  borderRadius: BorderRadius.circular(8.0),
                  color: Colors.grey.shade200,
                ),
                alignment: Alignment.center,
                child: _imageFile == null
                    ? const Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.image_search,
                            size: 60,
                            color: Colors.grey,
                          ),
                          SizedBox(height: 8),
                          Text(
                            'Nenhuma imagem selecionada',
                            style: TextStyle(color: Colors.grey, fontSize: 16),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      )
                    : ClipRRect(
                        // Para garantir que a imagem respeite o borderRadius do container
                        borderRadius: BorderRadius.circular(
                          7.0,
                        ), // Um pouco menor que o container
                        child: Image.file(
                          _imageFile!,
                          fit: BoxFit.cover, // Para cobrir a área do container
                          width: double
                              .infinity, // Para ocupar toda a largura do container
                          height: double
                              .infinity, // Para ocupar toda a altura do container
                        ),
                      ),
              ),
              const SizedBox(height: 24.0),

              // Botão para abrir a câmera
              ElevatedButton.icon(
                key: RecursosPage.openCameraButtonKey,
                icon: const Icon(Icons.camera_alt),
                label: const Text('Abrir Câmera'),
                onPressed: () => _pickImage(ImageSource.camera),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 12.0),
                  textStyle: const TextStyle(fontSize: 16),
                ),
              ),
              const SizedBox(height: 12.0),

              // Botão para abrir a galeria
              ElevatedButton.icon(
                key: RecursosPage.openGalleryButtonKey,
                icon: const Icon(Icons.photo_library),
                label: const Text('Abrir Galeria'),
                onPressed: () => _pickImage(ImageSource.gallery),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 12.0),
                  textStyle: const TextStyle(fontSize: 16),
                ),
              ),
              const SizedBox(height: 24.0),

              // Opcional: Um botão para limpar a imagem selecionada
              if (_imageFile != null)
                TextButton.icon(
                  key: RecursosPage.removeImageButtonKey,
                  icon: const Icon(Icons.delete_outline, color: Colors.red),
                  label: const Text(
                    'Remover Imagem',
                    style: TextStyle(color: Colors.red),
                  ),
                  onPressed: () {
                    setState(() {
                      _imageFile = null;
                    });
                  },
                ),

              // Alternativa: Um botão único que abre um menu de opções (câmera ou galeria)
              const SizedBox(height: 30),
              const Text(
                "Alternativa:",
                textAlign: TextAlign.center,
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              ElevatedButton.icon(
                key: RecursosPage.selectImageButtonKey,
                icon: const Icon(Icons.add_a_photo),
                label: const Text('Selecionar Imagem'),
                onPressed: () => _showImageSourceActionSheet(context),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 12.0),
                  textStyle: const TextStyle(fontSize: 16),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
