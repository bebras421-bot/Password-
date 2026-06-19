import json
import datetime
from typing import List, Optional

class PasswordRecord:
    """Модель данных для записи пароля"""
    
    def __init__(self, service: str, username: str, password: str, created_at: str = None):
        self.service = service
        self.username = username
        self.password = password
        self.created_at = created_at or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> dict:
        """Преобразует объект в словарь для JSON"""
        return {
            "service": self.service,
            "username": self.username,
            "password": self.password,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PasswordRecord':
        """Создаёт объект из словаря"""
        return cls(
            service=data["service"],
            username=data["username"],
            password=data["password"],
            created_at=data.get("created_at")
        )
    
    def __str__(self) -> str:
        return f"Service: {self.service} | Username: {self.username} | Created: {self.created_at}"


class PasswordStorage:
    """Класс для работы с хранилищем паролей в JSON"""
    
    def __init__(self, filename: str = "passwords.json"):
        self.filename = filename
        self.records: List[PasswordRecord] = []
        self.load()
    
    def add(self, record: PasswordRecord) -> None:
        """Добавляет новую запись"""
        self.records.append(record)
        self.save()
    
    def delete(self, index: int) -> bool:
        """Удаляет запись по индексу"""
        if 0 <= index < len(self.records):
            del self.records[index]
            self.save()
            return True
        return False
    
    def delete_by_service(self, service: str) -> bool:
        """Удаляет запись по названию сервиса"""
        for i, record in enumerate(self.records):
            if record.service.lower() == service.lower():
                del self.records[i]
                self.save()
                return True
        return False
    
    def get_all(self) -> List[PasswordRecord]:
        """Возвращает все записи"""
        return self.records
    
    def get_by_service(self, service: str) -> Optional[PasswordRecord]:
        """Ищет запись по сервису"""
        for record in self.records:
            if record.service.lower() == service.lower():
                return record
        return None
    
    def save(self) -> None:
        """Сохраняет данные в JSON-файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([r.to_dict() for r in self.records], f, ensure_ascii=False, indent=2)
    
    def load(self) -> None:
        """Загружает данные из JSON-файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.records = [PasswordRecord.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.records = []