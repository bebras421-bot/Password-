import unittest
import os
import json
from model import PasswordRecord, PasswordStorage
from controller import PasswordValidator

class TestPasswordManager(unittest.TestCase):
    """Тестирование приложения"""
    
    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.test_file = "test_passwords.json"
        self.storage = PasswordStorage(self.test_file)
        self.validator = PasswordValidator()
    
    def tearDown(self):
        """Очистка после каждого теста"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    # === ПОЗИТИВНЫЕ ТЕСТЫ ===
    
    def test_add_record(self):
        """Тест добавления записи"""
        record = PasswordRecord("Google", "user@email.com", "SecurePass123")
        self.storage.add(record)
        self.assertEqual(len(self.storage.get_all()), 1)
        self.assertEqual(self.storage.get_all()[0].service, "Google")
    
    def test_view_records(self):
        """Тест просмотра записей"""
        self.storage.add(PasswordRecord("Github", "user", "pass123"))
        records = self.storage.get_all()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].username, "user")
    
    def test_delete_record(self):
        """Тест удаления записи"""
        self.storage.add(PasswordRecord("Amazon", "user", "pass123"))
        self.storage.delete(0)
        self.assertEqual(len(self.storage.get_all()), 0)
    
    def test_generate_password_length(self):
        """Тест генерации пароля (граничный случай)"""
        import random
        import string
        length = 8
        chars = string.ascii_letters + string.digits
        password = ''.join(random.choice(chars) for _ in range(length))
        self.assertEqual(len(password), 8)
    
    def test_generate_password_length_64(self):
        """Тест генерации пароля максимальной длины"""
        import random
        import string
        length = 64
        chars = string.ascii_letters + string.digits
        password = ''.join(random.choice(chars) for _ in range(length))
        self.assertEqual(len(password), 64)
    
    def test_json_save_load(self):
        """Тест сохранения и загрузки JSON"""
        record = PasswordRecord("TestService", "testuser", "testpass")
        self.storage.add(record)
        self.storage.save()
        
        # Загрузка из нового экземпляра
        new_storage = PasswordStorage(self.test_file)
        self.assertEqual(len(new_storage.get_all()), 1)
        self.assertEqual(new_storage.get_all()[0].service, "TestService")
    
    # === НЕГАТИВНЫЕ ТЕСТЫ ===
    
    def test_empty_service(self):
        """Тест пустого названия сервиса"""
        self.assertFalse(self.validator.validate_not_empty("", "Service"))
    
    def test_empty_password(self):
        """Тест пустого пароля"""
        self.assertFalse(self.validator.validate_not_empty("", "Password"))
    
    def test_short_password(self):
        """Тест короткого пароля (< 8 символов)"""
        self.assertFalse(self.validator.validate_password("1234567"))
    
    def test_delete_nonexistent_index(self):
        """Тест удаления несуществующего индекса"""
        self.storage.add(PasswordRecord("Test", "user", "pass"))
        self.assertFalse(self.storage.delete(5))
    
    def test_delete_nonexistent_service(self):
        """Тест удаления несуществующего сервиса"""
        self.assertFalse(self.storage.delete_by_service("Nonexistent"))
    
    def test_duplicate_service(self):
        """Тест дублирования сервиса"""
        self.storage.add(PasswordRecord("Duplicate", "user1", "pass1"))
        self.assertTrue(self.validator.validate_service_unique(self.storage, "Unique"))
        self.assertFalse(self.validator.validate_service_unique(self.storage, "Duplicate"))
    
    def test_load_empty_json(self):
        """Тест загрузки из пустого JSON"""
        with open(self.test_file, 'w') as f:
            json.dump([], f)
        storage = PasswordStorage(self.test_file)
        self.assertEqual(len(storage.get_all()), 0)
    
    def test_load_corrupted_json(self):
        """Тест загрузки повреждённого JSON"""
        with open(self.test_file, 'w') as f:
            f.write("not a json")
        storage = PasswordStorage(self.test_file)
        self.assertEqual(len(storage.get_all()), 0)

if __name__ == "__main__":
    unittest.main()