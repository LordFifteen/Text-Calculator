from translate import Translator
from num2words import *
from word2number import w2n
def calc():
    try:
        translator = Translator(from_lang='ru', to_lang='en')
        number_a = w2n.word_to_num(translator.translate(input("Введите число a: ")))
        print(number_a)
        number_b = w2n.word_to_num(translator.translate(input("Введите число b: ")))
        print(number_b)
        action = input("Введите действие(-, +, *, /): ")
        if action == "+":
            result = number_a + number_b
        elif action == "-":
            result = number_a - number_b
        elif action == "*":
            result = number_a * number_b
        elif action == "/":
            if action == 0:
                print("Ошибка: Деление на ноль!")
                return
            result = number_a / number_b
        else:
            print("Ошибка: Неверная операция!")
            return

        print("Результат: ", result)
    except ValueError:
        print("Ошибка: Введите корректные числа!")
calc()
