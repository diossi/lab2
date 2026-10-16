import re
from typing import List
import requests


class TimeValidator:
    """
    Класс для проверки и поиска синтаксически корректного времени
    в формате ЧЧ:ММ:СС (24-часовой формат: от 00:00:00 до 23:59:59).
    """

    # Паттерн для поиска времени в тексте (с границами слов \b)
    SEARCH_PATTERN: str = r"\b(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d\b"
    # Паттерн для строгой проверки одной строки от начала (^) до конца ($)
    EXACT_PATTERN: str = r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$"

    @classmethod
    def is_valid_time(cls, time_str: str) -> bool:
        """
        Проверяет, является ли переданная строка корректным временем ЧЧ:ММ:СС.
        """
        if not isinstance(time_str, str):
            return False
        return bool(re.fullmatch(cls.EXACT_PATTERN, time_str.strip()))

    @classmethod
    def find_times_in_text(cls, text: str) -> List[str]:
        """
        Находит все вхождения корректного времени ЧЧ:ММ:СС в произвольном тексте.
        """
        if not isinstance(text, str):
            return []
        return re.findall(cls.SEARCH_PATTERN, text)

    @classmethod
    def find_times_in_file(cls, filepath: str) -> List[str]:
        """
        Считывает текстовый файл и находит в нем все вхождения времени ЧЧ:ММ:СС.
        """
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        return cls.find_times_in_text(content)

    @classmethod
    def find_times_in_url(cls, url: str, timeout: int = 10) -> List[str]:
        """
        Загружает веб-страницу по URL с помощью requests и ищет время ЧЧ:ММ:СС.
        """
        headers = {"User-Agent": "Mozilla/5.0 (Educational Python Lab)"}
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Вызовет исключение при ошибке HTTP (404, 500 и т.д.)
        return cls.find_times_in_text(response.text)


def main() -> None:
    """Пользовательское консольное меню программы."""
    validator = TimeValidator()

    while True:
        print("\n" + "=" * 55)
        print("Лабораторная работа: Поиск и проверка времени (ЧЧ:ММ:СС)")
        print("=" * 55)
        print("1. Проверить одну строку со временем (пользовательский ввод)")
        print("2. Найти все значения времени в введенном тексте")
        print("3. Найти время в локальном файле")
        print("4. Найти время на веб-странице по URL")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        try:
            if choice == "1":
                user_input = input("Введите время в формате ЧЧ:ММ:СС: ")
                if validator.is_valid_time(user_input):
                    print(f"[УСПЕХ]: '{user_input.strip()}' — корректное время!")
                else:
                    print(f"[ОШИБКА]: '{user_input}' НЕ является корректным временем.")

            elif choice == "2":
                text = input("Введите текст для поиска: ")
                found = validator.find_times_in_text(text)
                print(f"Найдено совпадений ({len(found)}): {found}")

            elif choice == "3":
                filepath = input("Введите путь к файлу (например, sample.txt): ").strip()
                found = validator.find_times_in_file(filepath)
                print(f"В файле '{filepath}' найдено совпадений ({len(found)}): {found}")

            elif choice == "4":
                url = input("Введите URL (например, https://time.is/): ").strip()
                found = validator.find_times_in_url(url)
                print(f"На странице найдено совпадений ({len(found)}): {found[:20]}")
                if len(found) > 20:
                    print(f"...и еще {len(found) - 20} совпадений.")

            elif choice == "0":
                print("Выход из программы.")
                break
            else:
                print("Неизвестная команда. Выберите пункт от 0 до 4.")

        except FileNotFoundError:
            print("[ОШИБКА ФАЙЛА]: Указанный файл не найден. Проверьте путь.")
        except requests.exceptions.RequestException as e:
            print(f"[ОШИБКА СЕТИ]: Не удалось загрузить страницу ({e}).")
        except Exception as e:
            print(f"[НЕПРЕДВИДЕННАЯ ОШИБКА]: {e}")


if __name__ == "__main__":
    main()