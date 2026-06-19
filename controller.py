import random
import string
from model import PasswordStorage, PasswordRecord
from view import ConsoleView

class BaseValidator:
    """Базовый класс для валидации"""
    
    @staticmethod
    def validate_not_empty(value: str, field_name: str) -> bool:
        if not value or value.strip() == "":
            print(f"❌ {field_name} cannot be empty")
            return False
        return True

class PasswordValidator(BaseValidator):
    """Класс для валидации паролей (наследует BaseValidator)"""
    
    @staticmethod
    def validate_password(password: str) -> bool:
        if len(password) < 8:
            print("❌ Password must be at least 8 characters long")
            return False
        return True
    
    @staticmethod
    def validate_service_unique(storage: PasswordStorage, service: str) -> bool:
        if storage.get_by_service(service):
            print(f"❌ Service '{service}' already exists")
            return False
        return True

class PasswordController:
    """Контроллер для управления паролями"""
    
    def __init__(self):
        self.storage = PasswordStorage()
        self.view = ConsoleView()
        self.validator = PasswordValidator()
    
    def add_password(self) -> None:
        """Добавляет новый пароль"""
        service = self.view.get_input("Enter service name: ")
        if not self.validator.validate_not_empty(service, "Service"):
            return
        if not self.validator.validate_service_unique(self.storage, service):
            return
        
        username = self.view.get_input("Enter username: ")
        if not self.validator.validate_not_empty(username, "Username"):
            return
        
        password = self.view.get_input("Enter password: ")
        if not self.validator.validate_not_empty(password, "Password"):
            return
        if not self.validator.validate_password(password):
            return
        
        record = PasswordRecord(service, username, password)
        self.storage.add(record)
        self.view.show_message(f"✅ Password for '{service}' added successfully!")
    
    def view_passwords(self) -> None:
        """Показывает все пароли"""
        records = self.storage.get_all()
        self.view.show_passwords(records)
    
    def delete_password(self) -> None:
        """Удаляет пароль"""
        records = self.storage.get_all()
        if not records:
            self.view.show_message("📭 No passwords to delete.")
            return
        
        self.view.show_passwords(records)
        choice = self.view.get_input("\nEnter service name or record number to delete: ")
        
        if choice.isdigit():
            index = int(choice) - 1
            if self.storage.delete(index):
                self.view.show_message("✅ Password deleted successfully!")
            else:
                self.view.show_message("❌ Invalid record number")
        else:
            if self.storage.delete_by_service(choice):
                self.view.show_message(f"✅ Password for '{choice}' deleted successfully!")
            else:
                self.view.show_message(f"❌ Service '{choice}' not found")
    
    def generate_password(self) -> None:
        """Генерирует случайный пароль"""
        length, use_digits, use_letters, use_symbols = self.view.show_password_generation_settings()
        
        if not (use_digits or use_letters or use_symbols):
            self.view.show_message("❌ At least one character type must be selected")
            return
        
        chars = ""
        if use_digits:
            chars += string.digits
        if use_letters:
            chars += string.ascii_letters
        if use_symbols:
            chars += string.punctuation
        
        password = ''.join(random.choice(chars) for _ in range(length))
        self.view.show_message(f"🔑 Generated password: {password}")
    
    def run(self) -> None:
        """Запускает главный цикл приложения"""
        while True:
            self.view.show_menu()
            choice = self.view.get_input("Select option: ")
            
            if choice == "1":
                self.add_password()
            elif choice == "2":
                self.view_passwords()
            elif choice == "3":
                self.delete_password()
            elif choice == "4":
                self.generate_password()
            elif choice == "5":
                self.view.show_message("👋 Goodbye!")
                break
            else:
                self.view.show_message("❌ Invalid option. Please try again.")