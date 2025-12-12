import hashlib

def generate_4digit_hash(*args):
    """
    Генерирует 4-значный хеш на основе переменного количества аргументов (строк),
    учитывая их порядок.
    """
    # args здесь — это кортеж (tuple) всех переданных аргументов.

    # Объединяем все аргументы (которые должны быть строками) в одну строку
    combined_string = "".join(args)

    # Кодируем объединенную строку в байты с UTF-8
    encoded_string = combined_string.encode('utf-8')

    # Используем алгоритм MD5
    hash_object = hashlib.md5(encoded_string)
    hex_digest = hash_object.hexdigest()

    # Преобразуем шестнадцатеричный хеш в целое число
    hash_int = int(hex_digest[:8], 16)

    # Ограничиваем результат 4 цифрами (0000 до 9999)
    four_digit_hash = hash_int % 10000

    # Форматируем результат в 4-значную строку с ведущими нулями
    return f"{four_digit_hash:04d}"


def generate_5digit_hash(*args):
    """
    Генерирует 5-значный хеш на основе переменного количества аргументов (строк),
    учитывая их порядок.
    """
    # Объединяем все аргументы в одну строку
    combined_string = "".join(args)

    # Кодируем объединенную строку в байты с UTF-8
    encoded_string = combined_string.encode('utf-8')

    # Используем алгоритм MD5
    hash_object = hashlib.md5(encoded_string)
    hex_digest = hash_object.hexdigest()

    # Преобразуем шестнадцатеричный хеш в целое число
    # Берем достаточно символов (10) чтобы обеспечить равномерное распределение 5 цифр
    hash_int = int(hex_digest[:10], 16)

    # !!! Ключевое изменение: Ограничиваем результат 5 цифрами путем операции по модулю !!!
    # Диапазон будет от 00000 до 99999
    five_digit_hash = hash_int % 100000

    # Форматируем результат в 5-значную строку с ведущими нулями
    return f"{five_digit_hash:05d}"  # Изменили '04d' на '05d'