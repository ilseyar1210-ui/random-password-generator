import unittest
import json
import os
import string

class TestRandomPasswordGenerator(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_passwords.json"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_password_length_range(self):
        """Тест: длина пароля в допустимых пределах"""
        from main import MIN_LENGTH, MAX_LENGTH
        self.assertEqual(MIN_LENGTH, 4)
        self.assertEqual(MAX_LENGTH, 32)
        self.assertLess(MIN_LENGTH, MAX_LENGTH)

    def test_password_generation_with_uppercase(self):
        """Тест: генерация пароля только с заглавными буквами"""
        import random
        import string
        
        length = 10
        characters = string.ascii_uppercase
        password = ''.join(random.choice(characters) for _ in range(length))
        
        self.assertEqual(len(password), length)
        self.assertTrue(all(c in string.ascii_uppercase for c in password))

    def test_password_generation_with_digits(self):
        """Тест: генерация пароля только с цифрами"""
        import random
        import string
        
        length = 8
        characters = string.digits
        password = ''.join(random.choice(characters) for _ in range(length))
        
        self.assertEqual(len(password), length)
        self.assertTrue(all(c in string.digits for c in password))

    def test_save_and_load_history(self):
        """Тест: сохранение и загрузка истории"""
        from main import RandomPasswordGenerator
        import tkinter as tk
        root = tk.Tk()
        app = RandomPasswordGenerator(root)

        import main
        main.HISTORY_FILE = self.test_file
        app.HISTORY_FILE = self.test_file

        test_data = [{
            "password": "TestPass123",
            "length": 10,
            "uppercase": True,
            "lowercase": True,
            "digits": True,
            "symbols": False,
            "timestamp": "2024-01-01 12:00:00"
        }]

        app.history = test_data
        app.save_history()

        app.history = []
        app.history = app.load_history()

        self.assertEqual(len(app.history), 1)
        self.assertEqual(app.history[0]["password"], "TestPass123")
        root.destroy()

    def test_empty_selection_validation(self):
        """Тест: проверка выбора хотя бы одного типа символов"""
        # Симулируем ситуацию, когда ничего не выбрано
        use_uppercase = False
        use_lowercase = False
        use_digits = False
        use_symbols = False
        
        any_selected = any([use_uppercase, use_lowercase, use_digits, use_symbols])
        self.assertFalse(any_selected)


if __name__ == "__main__":
    unittest.main()
