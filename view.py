class ConsoleView:
    """Класс для отображения данных в консоли"""
    
    @staticmethod
    def show_menu() -> None:
        """Отображает главное меню"""
        print("\n" + "="*50)
        print("          PASSWORD MANAGER")
        print("="*50)
        print("1. Add new password")
        print("2. View all passwords")
        print("3. Delete password")
        print("4. Generate password")
        print("5. Exit")
        print("="*50)
    
    @staticmethod
    def show_passwords(records: list) -> None:
        """Отображает список паролей"""
        if not records:
            print("\n📭 No passwords saved yet.")
            return
        
        print("\n" + "-"*60)
        print(f"{'#':<3} {'Service':<20} {'Username':<20} {'Created':<15}")
        print("-"*60)
        for i, record in enumerate(records):
            print(f"{i+1:<3} {record.service:<20} {record.username:<20} {record.created_at[:10]}")
        print("-"*60)
    
    @staticmethod
    def show_message(message: str) -> None:
        """Отображает сообщение"""
        print(f"\n{message}")
    
    @staticmethod
    def get_input(prompt: str) -> str:
        """Получает ввод от пользователя"""
        return input(prompt).strip()
    
    @staticmethod
    def show_password_generation_settings() -> tuple:
        """Запрашивает настройки генерации пароля"""
        print("\n🔐 Password Generation Settings:")
        while True:
            try:
                length = int(input("Length (8-64): "))
                if 8 <= length <= 64:
                    break
                print("Length must be between 8 and 64")
            except ValueError:
                print("Please enter a valid number")
        
        use_digits = input("Include digits? (y/n): ").lower() == 'y'
        use_letters = input("Include letters? (y/n): ").lower() == 'y'
        use_symbols = input("Include special symbols? (y/n): ").lower() == 'y'
        
        return length, use_digits, use_letters, use_symbols