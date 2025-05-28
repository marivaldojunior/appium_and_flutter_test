import 'package:flutter/material.dart';
import 'dart:math'; // Para gerar IDs aleatórios e durações de áudio

// Modelo para representar uma mensagem
enum MessageType { text, audio }

class Message {
  final String id;
  final String text; // Usado para texto ou como um placeholder para áudio
  final MessageType type;
  final bool isSender; // True se for mensagem do usuário, false caso contrário
  final Duration? audioDuration; // Duração simulada do áudio
  bool isPlaying; // Estado para simular a reprodução do áudio

  Message({
    required this.id,
    required this.text,
    required this.type,
    this.isSender = true,
    this.audioDuration,
    this.isPlaying = false,
  });
}

class ChatPage extends StatefulWidget {
  const ChatPage({super.key});

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final TextEditingController _textController = TextEditingController();
  final List<Message> _messages = [];
  final ScrollController _scrollController = ScrollController();
  final Random _random = Random();


  @override
  void initState() {
    super.initState();
    // Adicionar algumas mensagens de exemplo
    _addInitialMessages();
  }

  void _addInitialMessages() {
    setState(() {
      _messages.addAll([
        Message(id: _generateId(), text: "Olá! Como você está?", type: MessageType.text, isSender: false),
        Message(id: _generateId(), text: "Estou bem, obrigado! E você?", type: MessageType.text, isSender: true),
        Message(id: _generateId(), text: "Ouça isso!", type: MessageType.audio, isSender: false, audioDuration: Duration(seconds: _random.nextInt(50) + 10)),
      ]);
    });
    _scrollToBottom();
  }

  String _generateId() {
    return DateTime.now().millisecondsSinceEpoch.toString() + _random.nextInt(1000).toString();
  }

  void _sendMessage() {
    if (_textController.text.trim().isEmpty) return;

    final newMessage = Message(
      id: _generateId(),
      text: _textController.text.trim(),
      type: MessageType.text,
      isSender: true,
    );
    setState(() {
      _messages.add(newMessage);
      // Simular uma resposta automática após um pequeno atraso
      _simulateReply(newMessage.text);
    });
    _textController.clear();
    _scrollToBottom();
  }

  void _sendAudioMessage() {
    final newAudioMessage = Message(
      id: _generateId(),
      text: "Mensagem de áudio", // Placeholder
      type: MessageType.audio,
      isSender: true,
      audioDuration: Duration(seconds: _random.nextInt(50) + 10), // Duração aleatória de 10-60s
    );
    setState(() {
      _messages.add(newAudioMessage);
      // Simular uma resposta automática após um pequeno atraso
      _simulateReply("Recebi seu áudio!");

    });
    _scrollToBottom();
  }

  void _simulateReply(String originalMessageText) {
    Future.delayed(Duration(milliseconds: _random.nextInt(1500) + 500), () {
      if (!mounted) return; // Verificar se o widget ainda está montado
      setState(() {
        _messages.add(
          Message(
            id: _generateId(),
            text: "Entendido: '$originalMessageText'",
            type: MessageType.text,
            isSender: false,
          ),
        );
        _scrollToBottom();
      });
    });
  }


  void _deleteMessage(String messageId) {
    setState(() {
      _messages.removeWhere((msg) => msg.id == messageId);
    });
  }

  void _togglePlayAudio(String messageId) {
    setState(() {
      final messageIndex = _messages.indexWhere((msg) => msg.id == messageId);
      if (messageIndex != -1 && _messages[messageIndex].type == MessageType.audio) {
        // Simular parar outros áudios se algum estiver tocando
        for (var msg in _messages) {
          if (msg.id != messageId && msg.isPlaying) {
            msg.isPlaying = false;
          }
        }
        _messages[messageIndex].isPlaying = !_messages[messageIndex].isPlaying;
      }
    });
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Chat Simulado'),
      ),
      body: SafeArea(child: Column(
        children: <Widget>[
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(8.0),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                return _buildMessageItem(message);
              },
            ),
          ),
          _buildMessageInputArea(),
        ],
      )),
    );
  }

  Widget _buildMessageItem(Message message) {
    final isSender = message.isSender;
    final messageAlignment = isSender ? CrossAxisAlignment.end : CrossAxisAlignment.start;
    final bubbleColor = isSender ? Theme.of(context).colorScheme.primaryContainer : Theme.of(context).colorScheme.secondaryContainer;
    final textColor = isSender ? Theme.of(context).colorScheme.onPrimaryContainer : Theme.of(context).colorScheme.onSecondaryContainer;

    return Container(
      margin: const EdgeInsets.symmetric(vertical: 4.0),
      child: Column(
        crossAxisAlignment: messageAlignment,
        children: <Widget>[
          Row(
            mainAxisAlignment: isSender ? MainAxisAlignment.end : MainAxisAlignment.start,
            children: <Widget>[
              // Botão de excluir (sempre à esquerda do balão para o remetente, ou à direita para o destinatário - opcional)
              if (isSender) _buildDeleteButton(message.id),

              Flexible( // Garante que o balão não exceda os limites
                child: Container(
                  constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75), // Limita a largura do balão
                  padding: const EdgeInsets.symmetric(horizontal: 14.0, vertical: 10.0),
                  decoration: BoxDecoration(
                    color: bubbleColor,
                    borderRadius: BorderRadius.only(
                      topLeft: const Radius.circular(16.0),
                      topRight: const Radius.circular(16.0),
                      bottomLeft: isSender ? const Radius.circular(16.0) : const Radius.circular(0.0),
                      bottomRight: isSender ? const Radius.circular(0.0) : const Radius.circular(16.0),
                    ),
                  ),
                  child: message.type == MessageType.text
                      ? Text(message.text, style: TextStyle(color: textColor))
                      : _buildAudioMessageContent(message, textColor),
                ),
              ),
              if (!isSender) _buildDeleteButton(message.id), // Botão de excluir para mensagens recebidas
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildDeleteButton(String messageId) {
    return IconButton(
      icon: Icon(Icons.delete_outline, size: 18.0, color: Colors.grey[600]),
      padding: EdgeInsets.zero,
      constraints: const BoxConstraints(),
      tooltip: "Excluir mensagem",
      onPressed: () => _deleteMessage(messageId),
    );
  }


  Widget _buildAudioMessageContent(Message message, Color textColor) {
    return Row(
      mainAxisSize: MainAxisSize.min, // Para não ocupar espaço desnecessário
      children: <Widget>[
        IconButton(
          icon: Icon(
            message.isPlaying ? Icons.pause_circle_filled : Icons.play_circle_filled,
            color: textColor,
            size: 30.0,
          ),
          onPressed: () => _togglePlayAudio(message.id),
          padding: EdgeInsets.zero,
          constraints: const BoxConstraints(),
        ),
        const SizedBox(width: 8.0),
        // Simulação de barra de progresso (visual apenas)
        Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  "Áudio", // Ou message.text se você quiser exibir o placeholder
                  style: TextStyle(color: textColor, fontWeight: FontWeight.bold),
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 2),
                Container(
                  height: 5.0,
                  width: 100.0, // Largura fixa para a barra de "progresso"
                  decoration: BoxDecoration(
                    color: textColor.withOpacity(0.3),
                    borderRadius: BorderRadius.circular(10.0),
                  ),
                  child: message.isPlaying ? Align( // Simula progresso quando tocando
                    alignment: Alignment.centerLeft,
                    child: Container(
                      width: 50.0, // Metade da barra
                      decoration: BoxDecoration(
                        color: textColor,
                        borderRadius: BorderRadius.circular(10.0),
                      ),
                    ),
                  ) : null,
                ),
              ],
            )
        ),
        const SizedBox(width: 8.0),
        Text(
          _formatDuration(message.audioDuration ?? Duration.zero),
          style: TextStyle(color: textColor.withOpacity(0.8), fontSize: 12.0),
        ),
      ],
    );
  }

  String _formatDuration(Duration d) {
    final minutes = d.inMinutes.remainder(60).toString().padLeft(2, '0');
    final seconds = d.inSeconds.remainder(60).toString().padLeft(2, '0');
    return "$minutes:$seconds";
  }

  Widget _buildMessageInputArea() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 8.0),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        boxShadow: const [
          BoxShadow(
            offset: Offset(0, -1),
            blurRadius: 1.0,
            color: Colors.black12,
          ),
        ],
      ),
      child: Row(
        children: <Widget>[
          Expanded(
            child: TextField(
              controller: _textController,
              decoration: InputDecoration(
                hintText: 'Digite uma mensagem...',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(25.0),
                  borderSide: BorderSide.none,
                ),
                filled: true,
                fillColor: Colors.grey[200],
                contentPadding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 10.0),
              ),
              onSubmitted: (_) => _sendMessage(),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.mic),
            onPressed: _sendAudioMessage,
            tooltip: "Enviar mensagem de áudio",
          ),
          IconButton(
            icon: const Icon(Icons.send),
            onPressed: _sendMessage,
            tooltip: "Enviar mensagem de texto",
          ),
        ],
      ),
    );
  }
}