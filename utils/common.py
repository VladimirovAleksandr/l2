from typing import Union, Dict, Iterable, Any

from laboratory.settings import SYSTEM_AS_VI


def one_of_includes(check_value: Union[str, Iterable[str], Dict[str, Any]], values_to_check: Iterable[str]):
    return any(x in check_value for x in values_to_check)


def select_key_by_one_of_values_includes(value: str, values_to_check: Dict[str, Iterable]):
    for key in values_to_check:
        if one_of_includes(value, values_to_check[key]):
            return key
    return None


def replace_values_by_keys(value: str, to_replace: Dict[str, str]):
    for key in to_replace:
        value = value.replace(f"{{{{{key}}}}}", to_replace[key])
    return value


def non_selected_visible_type(orig, more_filters=None):
    if not more_filters:
        more_filters = {}
    return list_non_selected_visible_type(orig.objects.filter(hide=False, **more_filters).values("pk", "title").order_by("pk"))


def list_non_selected_visible_type(orig):
    return [{"pk": -1, "title": "Не выбрано"}, *list(orig)]


def none_if_minus_1(v):
    if v == -1 or v == "-1":
        return None
    return v


def get_system_name():
    return 'VI' if SYSTEM_AS_VI else 'L2'
