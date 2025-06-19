# supply/models.py
"""
✅ Особенности:
Один класс Node описывает все типы звеньев, а уровень вычисляется через get_level()
Продукты (Product) привязаны к узлу
Можно легко фильтровать узлы по уровню, поставщику и т.д.
Удаление поставщика не приводит к удалению клиентов — просто supplier = NULL
"""

from django.db import models


class Node(models.Model):
    """
    Модель звена сети поставок.

    Атрибуты:
    - id (int): Уникальный идентификатор
    - name (str): Название звена
    - email (str): Email-адрес
    - phone (str): Телефон
    - country (str): Страна
    - city (str): Город
    - street (str): Улица
    - building_number (str): Номер дома
    - supplier (Node): Ссылка на другого узла (поставщика); может быть null только у завода
    - debt_to_supplier (Decimal): Задолженность перед поставщиком (с точностью до копеек)
    - created_at (datetime): Дата и время создания записи (заполняется автоматически)

    Связи:
    - supplier — self-relation (ForeignKey на Node)
    Один NetworkNode может иметь много клиентов (дочерних узлов), но только одного поставщика
    """

    # Исключаем ругательства mypy о типизации, добавляя '# type: ignore[var-annotated]'
    name = models.CharField(max_length=255, unique=True)  # type: ignore[var-annotated]

    # -- Контактная информация --
    email = models.EmailField(unique=True)  # type: ignore[var-annotated]
    phone = models.CharField(max_length=20, unique=True)  # type: ignore[var-annotated]
    country = models.CharField(max_length=100)  # type: ignore[var-annotated]
    city = models.CharField(max_length=100)  # type: ignore[var-annotated]
    street = models.CharField(max_length=100)  # type: ignore[var-annotated]
    building_number = models.CharField(max_length=20)  # type: ignore[var-annotated]

    # -- Поставщик (самореференсное поле) --
    supplier = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="clients"
    )  # type: ignore[var-annotated]

    # -- Задолженность --
    debt_to_supplier = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # type: ignore[var-annotated]

    # -- Дата и время создания записи --
    created_at = models.DateTimeField(auto_now_add=True)  # type: ignore[var-annotated]

    def __str__(self):
        """
        Возвращает строковое представление узла сети поставок.
        :return: Строка, содержащая имя узла.
        """
        return self.name

    def get_level(self):
        """
        Вычисляет уровень звена в иерархии:
        0 — если нет поставщика (завод)
        1 — если поставщик — завод
        2 — и т.д.
        """
        level = 0
        node = self
        while node.supplier:
            level += 1
            node = node.supplier
        return level

    class Meta:
        """
        Класс метаданных для модели NetworkNode.

        Атрибуты:
        - verbose_name: Имя модели в единственном числе.
        - verbose_name_plural: Имя модели во множественном числе.
        - ordering: Порядок сортировки узлов по имени.
        """

        verbose_name = "Узел сети поставок"
        verbose_name_plural = "Узлы сети поставок"
        ordering = ["name"]


class Product(models.Model):
    """
    Модель продукта.

    Атрибуты:
    - id (int): Уникальный идентификатор
    - name (str): Название продукта
    - model (str): Модель
    - release_date (datetime): Дата выхода на рынок
    """

    # Исключаем ругательства mypy о типизации, добавляя '# type: ignore[var-annotated]'
    name = models.CharField(max_length=255)  # type: ignore[var-annotated]
    model = models.CharField(max_length=100)  # type: ignore[var-annotated]
    release_date = models.DateField()  # type: ignore[var-annotated]

    # Владелец продукта — узел сети
    owner = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="products")  # type: ignore[var-annotated]

    def __str__(self):
        """
        Возвращает строковое представление продукта.
        :return: Строка, содержащая имя и модель продукта.
        """
        return f"{self.name} ({self.model})"

    class Meta:
        """
        Класс метаданных для модели Product.

        Атрибуты:
        - verbose_name: Имя модели в единственном числе.
        - verbose_name_plural: Имя модели во множественном числе.
        - ordering: Порядок сортировки продуктов по имени.
        """

        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]
