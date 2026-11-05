class Airplane:
    """Класс, представляющий самолёт."""

    __slots__ = ("registration_country", "callsign", "velocity", "altitude")

    def __init__(self, registration_country: str, callsign: str, velocity, altitude):
        self.registration_country = registration_country
        self.callsign = callsign.strip() if callsign else "N/A"
        self.velocity = self.__validate_float(velocity)
        self.altitude = self.__validate_float(altitude)

    @staticmethod
    def __validate_float(value) -> float:
        """Приватный метод валидации числа."""
        try:
            return float(value) if value is not None else 0.0
        except (ValueError, TypeError):
            return 0.0

    def __lt__(self, other: object) -> bool:
        """Сравнение по высоте."""
        if not isinstance(other, Airplane):
            return NotImplemented
        return self.altitude < other.altitude

    def __eq__(self, other: object) -> bool:
        """Сравнение по скорости и высоте."""
        if not isinstance(other, Airplane):
            return NotImplemented
        return (self.velocity == other.velocity) and (self.altitude == other.altitude)

    def __gt__(self, other: object) -> bool:
        """Сравнение по скорости."""
        if not isinstance(other, Airplane):
            return NotImplemented
        return self.velocity > other.velocity

    def __repr__(self) -> str:
        return f"<Airplane {self.callsign} from {self.registration_country} Alt:{self.altitude} Vel:{self.velocity}>"