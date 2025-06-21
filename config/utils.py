import os

from dotenv import load_dotenv

load_dotenv(override=True)


class ImproperlyConfigured(Exception):
    """
    Кастомное исключение при неправильной настройке переменных окружения проекта.
    """

    def __init__(self, var_name: str):
        super().__init__(f"Обязательная переменная окружения '{var_name}' не установлена.")
        self.var_name = var_name


def get_env(var_name: str, default=None, required=False):
    """
    Получить переменную окружения или выбросить ошибку, если она обязательная.
    :param var_name: Имя переменной
    :param default: Значение по умолчанию
    :param required: Обязательность (если True, то переменная обязательна)
    :return: Значение переменной окружения
    """
    value = os.environ.get(var_name, default)
    if required and value is None:
        raise ImproperlyConfigured(f"Переменная окружения '{var_name}' обязательна, но не установлена.")
    return value
