import json
from inforealis import Airplane
from workclass import JSONStorage
from usercon import fetch_states, display_top_n_by_altitude, display_states


def handle_show_by_country() -> None:
    """Режим 1: показать самолёты по стране."""

    country_code = input("Введите код страны (например US для США): ").strip().upper()
    states = fetch_states(country_code)
    if not states:
        print("Нет данных о самолётах для выбранной страны.")
    else:
        display_states(states)


def handle_top_n() -> None:
    """Режим 2: топ-N самолётов по высоте."""
    try:
        n = int(input("Введите число N для отображения топ-N самолётов: "))
    except ValueError:
        print("Некорректное число.")
        return
    states = fetch_states()
    display_top_n_by_altitude(states, n)


def handle_add(storage: JSONStorage) -> None:
    """Режим 3: сохранить самолёт в базу."""
    reg_country = input("Регистрационная страна: ")
    callsign = input("Позывной: ")
    try:
        vel = float(input("Скорость (км/ч): "))
        alt = float(input("Высота (метры): "))
    except ValueError:
        print("Некорректные числовые значения.")
        return
    plane = Airplane(reg_country, callsign, vel / 3.6, alt)
    storage.add_airplane(plane)
    print("Самолёт успешно сохранён в базу данных.")


def _build_criteria(prefix: str) -> dict:
    """Собирает словарь критериев из ввода пользователя.
    """
    criteria = {}
    rc = input(f"{prefix} по регистрационной стране (пусто — неважно): ")
    cs = input(f"{prefix} по позывному (пусто — неважно): ")
    v = input(f"{prefix} по скорости (пусто — неважно): ")
    a = input(f"{prefix} по высоте (пусто — неважно): ")
    if rc:
        criteria["registration_country"] = rc
    if cs:
        criteria["callsign"] = cs
    if v:
        try:
            criteria["velocity"] = float(v)
        except ValueError:
            pass
    if a:
        try:
            criteria["altitude"] = float(a)
        except ValueError:
            pass
    return criteria


def handle_search(storage: JSONStorage) -> None:
    """Режим 4: поиск самолётов по критериям."""
    criteria = _build_criteria("Критерий")
    results = storage.get_by_criteria(criteria)
    print(json.dumps(results, indent=4))


def handle_delete(storage: JSONStorage) -> None:
    """Режим 5: удаление самолётов по условиям."""
    conditions = _build_criteria("Удалять")
    storage.delete_airplanes(conditions)
    print("Самолёты удалены согласно указанным условиям.")


def main() -> None:
    """Основной цикл приложения."""
    storage = JSONStorage()  # filename по умолчанию "airplanes.json"

    actions = {
        "1": handle_show_by_country,
        "2": handle_top_n,
        "3": lambda: handle_add(storage),
        "4": lambda: handle_search(storage),
        "5": lambda: handle_delete(storage),
    }

    menu = (
        "\nВыберите режим:\n"
        "1. Показать самолёты по стране\n"
        "2. Топ-N самолётов по высоте полёта\n"
        "3. Сохранить самолёт в базу данных\n"
        "4. Найти самолёты по критериям\n"
        "5. Удалить самолёты по условиям\n"
        "6. Выход\n"
    )

    while True:
        choice = input(menu)
        if choice == "6":
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()