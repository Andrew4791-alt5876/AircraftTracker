import json
from typing import List, Dict, Any, Optional

from src.aircrafts import Aircraft
from src.saver import Saver


class JSONSaver(Saver):
    """Реализация хранилища на основе JSON-файла."""

    def __init__(self, filename: str):
        self.filename = filename

    def _load_data(self) -> List[Dict[str, Any]]:
        """Загружает данные из JSON-файла. Если файла нет, возвращает пустой список."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            # Если файл повреждён, можно вернуть пустой список или выбросить исключение
            return []

    def _save_data(self, data: List[Dict[str, Any]]) -> None:
        """Сохраняет данные в JSON-файл."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_aircraft(self, aircraft: Aircraft) -> None:
        data = self._load_data()
        # Добавляем новый самолёт в виде словаря
        data.append(aircraft.to_dict())
        self._save_data(data)

    def get_aircraft(self, criteria: Optional[Dict[str, Any]] = None) -> List[Aircraft]:
        data = self._load_data()
        if criteria is None:
            # Возвращаем все записи
            return [Aircraft.from_dict(item) for item in data]

        # Фильтруем записи по точному совпадению значений
        filtered = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                filtered.append(Aircraft.from_dict(item))
        return filtered

    def delete_aircraft(self, criteria: Optional[Dict[str, Any]] = None) -> None:
        data = self._load_data()
        if criteria is None:
            # Удаляем всё
            self._save_data([])
            return

        # Оставляем только те записи, которые НЕ удовлетворяют критериям
        new_data = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if not match:
                new_data.append(item)
        self._save_data(new_data)
