import json
from typing import List, Dict
from abc import ABC, abstractmethod
from inforealis import Airplane


class AbstractStorage(ABC):
    """Абстрактный базовый класс для хранилища самолётов."""

    @abstractmethod
    def add_airplane(self, airplane: Airplane) -> None:
        """Добавляет самолёт в хранилище."""
        pass

    @abstractmethod
    def get_by_criteria(self, criteria: Dict) -> List[Dict]:
        """Возвращает самолёты, соответствующие критериям."""
        pass

    @abstractmethod
    def delete_airplanes(self, conditions: Dict) -> None:
        """Удаляет самолёты, соответствующие условиям."""
        pass


class JSONStorage(AbstractStorage):
    """Хранилище самолётов на основе JSON-файла."""

    def __init__(self, filename: str = "airplanes.json"):
        self.__filename = filename
        try:
            with open(self.__filename, "r") as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = []

    def __save(self) -> None:
        """Приватный метод сохранения данных в файл."""
        with open(self.__filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def add_airplane(self, airplane: Airplane) -> None:
        """Добавляет самолёт в JSON-файл.
        """
        self.data.append(
            {
                "registration_country": airplane.registration_country,
                "callsign": airplane.callsign,
                "velocity": airplane.velocity,
                "altitude": airplane.altitude,
            }
        )
        self.__save()

    def get_by_criteria(self, criteria: Dict) -> List[Dict]:
        """Ищет самолёты по критериям.
        """
        return [
            item for item in self.data
            if all(item.get(k) == v for k, v in criteria.items())
        ]

    def delete_airplanes(self, conditions: Dict) -> None:
        """Удаляет самолёты по условиям.
        """
        self.data = [
            item for item in self.data
            if not all(item.get(k) == v for k, v in conditions.items())
        ]
        self.__save()