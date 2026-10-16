import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from main import TimeValidator


class TestTimeValidator(unittest.TestCase):
    """Модульные тесты (unit-тесты) для проверки класса TimeValidator."""

    def test_valid_times(self) -> None:
        """Проверка корректных значений времени (включая граничные)."""
        valid_samples = [
            "00:00:00",  # Нижняя граница
            "23:59:59",  # Верхняя граница
            "12:30:45",  # Обычное дневное время
            "09:05:01",  # Ведущие нули
            "19:59:00",  # Граница первого десятка часов
            "20:00:00",  # Начало двадцатых часов
            "  08:15:30  "  # С пробелами по краям
        ]
        for sample in valid_samples:
            with self.subTest(sample=sample):
                self.assertTrue(TimeValidator.is_valid_time(sample))

    def test_invalid_times(self) -> None:
        """Проверка некорректных значений времени и неверных форматов."""
        invalid_samples = [
            "24:00:00",  # Часы больше 23
            "23:60:00",  # Минуты больше 59
            "23:59:60",  # Секунды больше 59
            "99:99:99",  # Полностью неверные числа
            "1:20:30",   # Нет ведущего нуля в часах
            "12:5:30",   # Нет ведущего нуля в минутах
            "12:30:5",   # Нет ведущего нуля в секундах
            "12:30",     # Отсутствуют секунды (ЧЧ:ММ)
            "12-30-45",  # Неверный разделитель
            "ab:cd:ef",  # Буквы вместо цифр
            "",          # Пустая строка
        ]
        for sample in invalid_samples:
            with self.subTest(sample=sample):
                self.assertFalse(TimeValidator.is_valid_time(sample))

    def test_non_string_input(self) -> None:
        """Проверка устойчивости к передаче нестроковых типов данных."""
        self.assertFalse(TimeValidator.is_valid_time(None))  # type: ignore
        self.assertFalse(TimeValidator.is_valid_time(123456))  # type: ignore
        self.assertEqual(TimeValidator.find_times_in_text(None), [])  # type: ignore

    def test_find_times_in_text(self) -> None:
        """Проверка поиска корректного времени в тексте и игнорирования ошибочного."""
        text = (
            "Поезд отправляется в 08:30:00, прибывает в 18:45:15. "
            "Ошибочные записи лога: 25:10:00, 12:65:00, 10:10:99, 123:45:00, 8:00:00. "
            "Полночь — 00:00:00."
        )
        expected = ["08:30:00", "18:45:15", "00:00:00"]
        self.assertEqual(TimeValidator.find_times_in_text(text), expected)

    def test_find_times_in_file(self) -> None:
        """Проверка поиска времени в локальном файле."""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
            tmp.write("Старт сервера в 01:02:03, стоп в 23:59:59. Ошибка: 24:01:01.")
            tmp_path = tmp.name

        try:
            result = TimeValidator.find_times_in_file(tmp_path)
            self.assertEqual(result, ["01:02:03", "23:59:59"])
        finally:
            os.remove(tmp_path)

    @patch("main.requests.get")
    def test_find_times_in_url(self, mock_get: MagicMock) -> None:
        """Проверка поиска времени на веб-странице по URL (с использованием mock)."""
        mock_response = MagicMock()
        mock_response.text = "<html><body>Время обновления: 14:22:10 и 22:00:55</body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = TimeValidator.find_times_in_url("https://example.com")
        self.assertEqual(result, ["14:22:10", "22:00:55"])
        mock_get.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)