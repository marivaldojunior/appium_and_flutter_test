class ListItemData {
  String id; // Único identificador
  String title;
  String? description; // Opcional
  bool isCompleted;
  DateTime createdAt;

  ListItemData({
    required this.id,
    required this.title,
    this.description,
    this.isCompleted = false,
    DateTime? createdAt,
  }) : createdAt = createdAt ?? DateTime.now(); // Define um valor padrão se não fornecido

  // Você pode adicionar métodos aqui, como copyWith para facilitar a edição
  ListItemData copyWith({
    String? id,
    String? title,
    String? description,
    bool? isCompleted,
    DateTime? createdAt,
  }) {
    return ListItemData(
      id: id ?? this.id,
      title: title ?? this.title,
      description: description ?? this.description,
      isCompleted: isCompleted ?? this.isCompleted,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  @override
  bool operator ==(Object other) => // Necessário se você quiser comparar objetos
  identical(this, other) ||
      other is ListItemData &&
          runtimeType == other.runtimeType &&
          id == other.id;

  @override
  int get hashCode => id.hashCode; // Necessário se você sobrescrever ==
}