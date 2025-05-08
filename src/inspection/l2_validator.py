from typing import Dict, List, Tuple, Any

def validate_l2_entry(entry: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Проверяет корректность одного элемента уровня L2."""
    errors = []

    required_fields = {
        "id": int,
        "name": str,
        "value": float,
        "category": str,
    }

    value_range = (0.0, 100.0)  # допустимый диапазон для value
    valid_categories = {"A", "B", "C"}

    for field, expected_type in required_fields.items():
        if field not in entry:
            errors.append(f"Отсутствует поле: {field}")
        elif not isinstance(entry[field], expected_type):
            errors.append(f"Неверный тип для поля {field}: ожидался {expected_type.__name__}")

    if "value" in entry and isinstance(entry["value"], (int, float)):
        if not (value_range[0] <= entry["value"] <= value_range[1]):
            errors.append(f"Поле 'value' вне допустимого диапазона: {entry['value']}")

    if "category" in entry and isinstance(entry["category"], str):
        if entry["category"] not in valid_categories:
            errors.append(f"Недопустимое значение category: {entry['category']}")

    return (len(errors) == 0, errors)

def validate_l2_dataset(dataset: List[Dict[str, Any]]) -> List[Tuple[int, bool, List[str]]]:
    """Проверяет список элементов уровня L2 и возвращает список результатов."""
    results = []
    for i, entry in enumerate(dataset):
        is_valid, errors = validate_l2_entry(entry)
        results.append((i, is_valid, errors))
    return results
