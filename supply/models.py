# supply/models.py
from django.db import models


class Node(models.Model):
    """
    Модель звена сети поставок.

    Атрибуты:
    - id (int): Уникальный идентификатор.
    - name (str): Название звена.
    - email (str): Email-адрес.
    - phone (str): Телефон.
    - country (str): Страна.
    - city (str): Город.
    - street (str): Улица.
    - building_number (str): Номер дома.
    - supplier (Node): Ссылка на другого узла (поставщика); может быть null только у завода.
    - debt_to_supplier (Decimal): Задолженность перед поставщиком (с точностью до копеек).
    - created_at (datetime): Дата и время создания записи (заполняется автоматически).

    Связи:
    - supplier — self-relation (ForeignKey на Node)
    Один NetworkNode может иметь много клиентов (дочерних узлов), но только одного поставщика
    """

    # Исключаем ругательства mypy о типизации, добавляя '# type: ignore[var-annotated]'
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)  # type: ignore[var-annotated]

    # -- Контактная информация --
    email = models.EmailField(unique=True, null=False, blank=False)  # type: ignore[var-annotated]
    phone = models.CharField(max_length=20, unique=True, null=False, blank=False)  # type: ignore[var-annotated]
    country = models.CharField(max_length=100, null=False, blank=False)  # type: ignore[var-annotated]
    city = models.CharField(max_length=100, null=False, blank=False)  # type: ignore[var-annotated]
    street = models.CharField(max_length=100, null=False, blank=False)  # type: ignore[var-annotated]
    building_number = models.CharField(max_length=20, null=False, blank=False)  # type: ignore[var-annotated]

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
