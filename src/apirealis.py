from abc import ABC, abstractmethod
import requests


class AbstractAPI(ABC):
    """Абстрактный базовый класс для работы с API."""

    @abstractmethod
    def connect(self) -> bool:
        """Проверяет доступность API."""
        pass

    @abstractmethod
    def get_data(self, **kwargs):
        """Получает данные от API.
        """
        pass


class OpenSkyAPI(AbstractAPI):
    """Класс для работы с OpenSky Network API (данные о самолётах)."""

    def __init__(self):
        self.base_url = "https://opensky-network.org/api/states/all"

    def connect(self) -> bool:
        """Проверяет доступность OpenSky API."""
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False

    def get_data(self, **kwargs) -> dict:
        """Получает данные о самолётах.
        """
        country_code = kwargs.get("country_code")
        params = {}
        if country_code is not None:
            params["icao24"] = country_code.lower()
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()


class NominatimAPI(AbstractAPI):
    """Класс для работы с Nominatim API (геокодирование)."""

    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"

    def connect(self) -> bool:
        """Проверяет доступность Nominatim API."""
        try:
            response = requests.get(self.base_url, params={"q": "Russia", "format": "json"})
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False

    def get_data(self, **kwargs) -> list:
        """Получает координаты страны по её названию.

        """
        country_name = kwargs.get("country_name")
        params = {"q": country_name, "format": "json", "limit": 1}
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()