words_to_numbs = {
    "ноль": 0, "один": 1, "два": 2, "три": 3, "четыре": 4, "пять": 5, "шесть": 6, "семь": 7, "восемь": 8, "девять": 9,
    "десять": 10, "одиннадцать": 11, "двенадцать": 12, "тринадцать": 13, "четырнадцать": 14, "пятнадцать": 15,
    "шестнадцать": 16, "семнадцать": 17, "восемнадцать": 18, "девятнадцать": 19, "двадцать": 20, "тридцать": 30,
    "сорок": 40, "пятьдесят": 50, "шестьдесят": 60, "семьдесят": 70, "восемьдесят": 80, "девяносто": 90
}

#Обратный словарь для преобразования чисел обратно в слова
numbs_to_words = {value: key for key, value in words_to_numbs.items()}

#Словарь для преобразования слов операций в символы операций
operations = {"плюс": "+", "минус": "-", "умножить": "*"}


def perform_operation(number_a, operation, number_b):
    """Выполняет одну из базовых математических операций между двумя числами

    Args:
        number_a (int): Первое число
        operation (str): Операция в виде символа ('+', '-', '*')
        number_b (int): Второе число

    Returns:
        int: Результат операции
    """
    #Выполняем операцию в зависимости от символа
    if operation == "+":
        return number_a + number_b
    elif operation == "-":
        return number_a - number_b
    elif operation == "*":
        return number_a * number_b
    return 0  #Возвращаем 0 по умолчанию (на случай неопределенной операции)


def evaluate_expression(tokens):
    """Вычисляет значение выражения с учетом приоритета операций

    Args:
        tokens (list): Список токенов (чисел и операций), представляющий выражение

    Returns:
        int: Результат вычисления
    """
    #Вспомогательная функция для применения оператора к последним двум числам в стеке
    def apply_operator(operators, values):
        """Применяет оператор к двум последним числам в стеке

        Args:
            operators (list): Список операторов
            values (list): Список чисел
        """
        operator = operators.pop()  #Забираем последний оператор
        right = values.pop()  #Забираем последнее число
        left = values.pop()  #Забираем предпоследнее число
        #Выполняем операцию и добавляем результат обратно в стек
        values.append(perform_operation(left, operator, right))

    values = []  #Стек для хранения чисел
    operators = []  #Стек для хранения операторов
    precedence = {"+": 1, "-": 1, "*": 2}  #Приоритет операций

    for token in tokens:  #Проходим по всем токенам
        if isinstance(token, int):  #Если токен — число
            values.append(token)  #Добавляем его в стек чисел
        elif token in {"+", "-", "*"}:  #Если токен — операция
            #Пока в стеке есть операции с более высоким или равным приоритетом, выполняем их
            while operators and precedence[operators[-1]] >= precedence[token]:
                apply_operator(operators, values)
            operators.append(token)  #Добавляем текущий оператор в стек

    #Выполняем оставшиеся операции
    while operators:
        apply_operator(operators, values)

    return values[0]  #Возвращаем финальное значение


def translate_words(string):
    """Преобразует строку на русском языке в список чисел и операций

    Args:
        string (str): Входная строка, содержащая текстовое представление выражения

    Returns:
        list: Список токенов (чисел и операций)
    """
    words = string.split()  #Разбиваем строку на отдельные слова
    tokens = []  #Список для хранения чисел и операций
    number = 0  #Текущее собираемое число
    is_negative = False  #Флаг для отрицательных чисел

    for word in words:  #Проходим по каждому слову
        if word == "на":  #Игнорируем слово "на"
            continue
        if word == "минус" and not number:  #Обрабатываем начало отрицательного числа
            is_negative = True
        elif word in words_to_numbs:  #Если слово — это число
            number += words_to_numbs[word]
        elif word in operations:  #Если слово — это операция
            if is_negative:  #Если число отрицательное
                number = -number
                is_negative = False
            if number:  #Если есть собранное число, добавляем его
                tokens.append(number)
                number = 0
            tokens.append(operations[word])  #Добавляем операцию
        else:
            raise ValueError(f"Неизвестное слово в выражении: {word}")  #Ошибка, если слово неизвестно
    if is_negative:  #Обрабатываем последнее отрицательное число
        number = -number
    if number:  #Добавляем последнее число, если оно есть
        tokens.append(number)

    return tokens  #Возвращаем список токенов


def translate_number(num):
    """Преобразует число в его текстовое представление на русском языке

    Args:
        num (int): Число для преобразования

    Returns:
        str: Текстовое представление числа
    """
    if num == 0:  #Если число 0
        return "ноль"
    result = []  #Список для хранения слов
    if num < 0:  #Если число отрицательное
        result.append("минус")
        num = -num  #Делаем число положительным для обработки
    if 11 <= num <= 19:  #Для чисел от 11 до 19 используем прямой словарь
        result.append(numbs_to_words[num])
    else:
        tens = (num % 100) // 10 * 10  #Десятки
        ones = num % 10  #Единицы
        if tens:
            result.append(numbs_to_words[tens])  #Добавляем десятки
        if ones:
            result.append(numbs_to_words[ones])  #Добавляем единицы
    return " ".join(result)  #Возвращаем строку


def calc():
    """Основная функция калькулятора
    Ожидает ввода выражений от пользователя, обрабатывает их и выводит результат

    """
    print("Введите выражение (например, 'три плюс пять умножить на два'). Для выхода введите 'выход'.")
    while True:
        string = input("--> ")  #Получаем ввод от пользователя
        if string == "выход":  #Если пользователь вводит "выход", прерываем цикл
            break

        try:
            tokens = translate_words(string)  #Преобразуем строку в токены
            result = evaluate_expression(tokens)  #Вычисляем результат
            print(translate_number(result))  #Преобразуем результат в текст
        except Exception as e:  #Обрабатываем ошибки
            print("Ошибка:", e)

calc()
