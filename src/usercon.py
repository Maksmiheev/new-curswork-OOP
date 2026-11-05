from tabulate import tabulate
from apirealis import OpenSkyAPI


def fetch_states(country_code: str = None):
    """Получает список состояний самолётов через OpenSkyAPI.
    """
    api = OpenSkyAPI()
    data = api.get_data(country_code=country_code)
    return data.get("states") or []


def display_top_n_by_altitude(states: list, n: int) -> None:
    """Отображает топ-N самолётов по высоте.
    """
    sorted_states = sorted(states, key=lambda x: x[7] or 0, reverse=True)[:n]
    headers = ["Callsign", "Country", "Altitude (m)", "Velocity (km/h)"]
    rows = [
        [s[1], s[2], s[7], round((s[9] or 0) * 3.6)]
        for s in sorted_states
    ]
    print(tabulate(rows, headers=headers))


def display_states(states: list) -> None:
    """Отображает все самолёты из списка состояний.
    """
    headers = ["Callsign", "Country", "Altitude (m)", "Velocity (km/h)"]
    rows = [
        [s[1], s[2], s[7], round((s[9] or 0) * 3.6)]
        for s in states
    ]
    print(tabulate(rows, headers=headers))