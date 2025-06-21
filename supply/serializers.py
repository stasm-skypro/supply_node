# supply/serializers.py
from rest_framework import serializers

from supply.models import Node


class NodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Node

    Преобразует объекты модели Node в JSON и обратно, при этом запрещает
    прямое изменение поля `debt_to_supplier` через API.

    Атрибуты:
    - id (int): Уникальный идентификатор.
    - name (str): Название узла.
    - email (EmailField): Email контактного лица.
    - country (str): Страна.
    - city (str): Город.
    - street (str): Улица.
    - house_number (str): Номер дома.
    - supplier (ForeignKey): Ссылка на поставщика (другой узел сети).
    - debt_to_supplier (Decimal): Задолженность перед поставщиком (только для чтения).
    - created_at (DateTimeField): Время создания (только для чтения).
    """

    class Meta:
        """
        Мета-класс для настройки сериализатора

        Определяет модель, с которой работает сериализатор, и указывает,
        какие поля должны быть включены. Поле `debt_to_supplier`
        устанавливается как "только для чтения".
        """

        model = Node
        fields = "__all__"
        read_only_fields = ["debt_to_supplier"]

    def update(self, instance, validated_data):
        """
        Обновляет экземпляр модели Node.

        Этот метод переопределен для дополнительной защиты поля `debt_to_supplier`.
        Он удаляет это поле из словаря `validated_data` перед обновлением,
        гарантируя, что его нельзя изменить через PATCH или PUT запросы

        :param instance: Экземпляр модели для обновления
        :param validated_data: Словарь с проверенными данными
        :returns Node: Обновленный экземпляр модели
        """
        validated_data.pop("debt_to_supplier", None)
        return super().update(instance, validated_data)
