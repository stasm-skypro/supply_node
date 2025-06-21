# supply/serializers.py
"""
Модуль сериализаторов для приложения 'supply'.

Содержит сериализаторы, используемые для преобразования объектов модели
сети поставок (Node) в формат JSON и обратно, обеспечивая взаимодействие
с API Django REST Framework.
"""
from rest_framework import serializers

from supply.models import Node


class NodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Node.

    Преобразует объекты модели :class:`~supply.models.Node` в JSON и обратно,
    при этом запрещает прямое изменение поля `debt_to_supplier` через API.

    Поля:
        :id: (int) Уникальный идентификатор узла.
        :name: (str) Название узла.
        :email: (str) Email контактного лица.
        :country: (str) Страна расположения узла.
        :city: (str) Город расположения узла.
        :street: (str) Улица расположения узла.
        :house_number: (str) Номер дома расположения узла.
        :supplier: (:class:`~supply.models.Node` or None) Ссылка на поставщика (другой узел сети).
        :debt_to_supplier: (Decimal) Задолженность перед поставщиком (только для чтения).
        :created_at: (datetime) Время создания записи (только для чтения).
    """

    class Meta:
        """
        Мета-класс для настройки сериализатора.

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
        гарантируя, что его нельзя изменить через PATCH или PUT запросы.

        :param instance: :class:`~supply.models.Node` - Экземпляр модели для обновления.
        :param validated_data: dict - Словарь с проверенными данными.
        :returns: :class:`~supply.models.Node` - Обновленный экземпляр модели.
        """
        validated_data.pop("debt_to_supplier", None)
        return super().update(instance, validated_data)
