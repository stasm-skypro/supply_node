# supply/models.py
"""
Модели для приложения 'supply'.

Этот модуль определяет модели Django для представления звеньев сети поставок (Node)
и продуктов (Product), которые они производят или продают.

Ключевые особенности:
- Один класс Node описывает все типы звеньев, а уровень вычисляется через get_level().
- Иерархическая структура сети моделируется через самореферентную связь в модели `Node`.
- Уровень звена в иерархии (завод, розничная сеть и т.д.) вычисляется динамически.
- Продукты связаны с конкретным звеном сети.
- Удаление поставщика не каскадное, а устанавливает связь в `NULL`.
"""

from django.db import models


class Node(models.Model):
    """
    Модель звена сети поставок.

    Представляет собой элемент в иерархической структуре сети, будь то завод,
    розничная сеть или индивидуальный предприниматель.

    :param name: Название звена.
    :type name: str
    :param email: Email-адрес.
    :type email: str
    :param phone: Телефон.
    :type phone: str
    :param country: Страна.
    :type country: str
    :param city: Город.
    :type city: str
    :param street: Улица.
    :type street: str
    :param building_number: Номер дома.
    :type building_number: str
    :param supplier: Ссылка на поставщика (другой узел). Может быть ``None`` для завода (уровень 0).
    :type supplier: Node or None
    :param debt_to_supplier: Задолженность перед поставщиком.
    :type debt_to_supplier: decimal.Decimal
    :param created_at: Дата и время создания записи (устанавливается автоматически).
    :type created_at: datetime.datetime
    """

    # Исключаем ругательства mypy о типизации, добавляя '# type: ignore[var-annotated]'
    name = models.CharField(
        max_length=255, unique=True, verbose_name="Название узла поставки"
    )  # type: ignore[var-annotated]

    # -- Контактная информация --
    email = models.EmailField(unique=True, verbose_name="Электронная почта")  # type: ignore[var-annotated]
    phone = models.CharField(max_length=20, unique=True, verbose_name="Номер телефона")  # type: ignore[var-annotated]
    country = models.CharField(max_length=100, verbose_name="Страна")  # type: ignore[var-annotated]
    city = models.CharField(max_length=100, verbose_name="Город")  # type: ignore[var-annotated]
    street = models.CharField(max_length=100, verbose_name="Улица")  # type: ignore[var-annotated]
    building_number = models.CharField(max_length=20, verbose_name="Номер дома")  # type: ignore[var-annotated]

    # -- Поставщик (самореферентное поле) --
    supplier = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="clients", verbose_name="Поставщик"
    )  # type: ignore[var-annotated]

    # -- Задолженность --
    debt_to_supplier = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Задолженность"
    )  # type: ignore[var-annotated]

    # -- Дата и время создания записи --
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время создания"
    )  # type: ignore[var-annotated]

    def __str__(self) -> str:
        """
        Возвращает строковое представление узла сети поставок.

        :return: Название узла.
        :rtype: str
        """
        return self.name

    @property
    def level(self) -> int:
        """
        Вычисляет уровень звена в иерархии.

        Уровень определяется количеством звеньев в цепочке до завода.
        - 0: Завод (нет поставщика).
        - 1: Поставщик — завод.
        - 2: Поставщик — звено 1-го уровня, и т.д.

        :return: Целочисленное значение уровня.
        :rtype: int
        """
        level = 0
        node = self
        while node.supplier:
            level += 1
            node = node.supplier
        return level

    class Meta:
        """
        Мета-опции для модели Node.

        :ivar verbose_name: Имя модели в единственном числе для отображения в админ-панели.
        :ivar verbose_name_plural: Имя модели во множественном числе.
        :ivar ordering: Порядок сортировки по умолчанию для запросов.
        """

        verbose_name = "Узел сети поставок"
        verbose_name_plural = "Узлы сети поставок"
        ordering = ["name"]


class Product(models.Model):
    """
    Модель продукта.

    Представляет продукт, который производится или продается звеном сети.

    :param name: Название продукта.
    :type name: str
    :param model: Модель продукта.
    :type model: str
    :param release_date: Дата выхода продукта на рынок.
    :type release_date: datetime.date
    :param owner: Звено сети, которому принадлежит продукт.
    :type owner: Node
    """

    # Исключаем ругательства mypy о типизации, добавляя '# type: ignore[var-annotated]'
    name = models.CharField(max_length=255, verbose_name="Название продукта")  # type: ignore[var-annotated]
    model = models.CharField(max_length=100, verbose_name="Модель")  # type: ignore[var-annotated]
    release_date = models.DateField(verbose_name="Дата выхода на рынок")  # type: ignore[var-annotated]

    # Владелец продукта — узел сети
    owner = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="products", verbose_name="Владелец"
    )  # type: ignore[var-annotated]

    def __str__(self) -> str:
        """
        Возвращает строковое представление продукта.

        :return: Строка в формате "Название (Модель)".
        :rtype: str
        """
        return f"{self.name} ({self.model})"

    class Meta:
        """
        Мета-опции для модели Product.

        :ivar verbose_name: Имя модели в единственном числе для отображения в админ-панели.
        :ivar verbose_name_plural: Имя модели во множественном числе.
        :ivar ordering: Порядок сортировки по умолчанию для запросов.
        """

        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]
