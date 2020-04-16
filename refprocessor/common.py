from typing import Union, Tuple

SIGN_GT = ">"
SIGN_GTE = ">="
SIGN_LT = "<"
SIGN_LTE = "<="

# Знаки больше
SIGNS_GT = (
    ">",
    "&gt;",
    "старше",
    "больше",
    "более",
)
# Знаки больше или равно
SIGNS_GTE = (
    ">=",
    "≥",
    "&ge;",
    "от",
    "с",
)

# Знаки меньше
SIGNS_LT = (
    "<",
    "&lt;",
    "младше",
    "меньше",
    "менее",
    "до",
)
# Знаки меньше или равно
SIGNS_LTE = (
    "<=",
    "≤",
    "&le;",
    "по",
)

SIGNS_ORIG_TO_SIGN = (
    (SIGNS_GT, SIGN_GT),
    (SIGNS_GTE, SIGN_GTE),
    (SIGNS_LT, SIGN_LT),
    (SIGNS_LTE, SIGN_LTE),
)

RANGE_REGEXP = r"^(от |с )?(\d+)( )?([\w.]+)* ([-–] |до |по )(\d+)( )?([\w.]+)*$"

POINT_STRICT = ")"
POINT_NON_STRICT = "]"


def get_sign_by_string(s: str) -> Union[None, str]:
    for signs in SIGNS_ORIG_TO_SIGN:
        if s in signs[0]:
            return signs[1]
    return None


class Value:
    def __init__(self, value: Union[int, float, Tuple[Union[int, float], str]], mode=POINT_NON_STRICT):
        if isinstance(value, tuple):
            self.value = value[0]
            self.mode = value[1]
        else:
            self.value = value
            self.mode = mode

    def __eq__(self, other: 'Value'):
        return self.value == other.value and self.mode == other.mode

    def __str__(self):
        return f"{self.mode}{self.value}"


class ValueRange:
    def __init__(self, val_from: Union[Value, int, float, Tuple[Union[int, float], str]], val_to: Union[Value, int, float]):
        if isinstance(val_from, Value):
            self.val_from = val_from
        else:
            self.val_from = Value(val_from)

        if isinstance(val_to, Value):
            self.val_to = val_to
        else:
            self.val_to = Value(val_to)

    def in_range(self, val: int):
        if self.val_from.mode == POINT_STRICT and val <= self.val_from.value:
            return False
        if self.val_from.mode == POINT_NON_STRICT and val < self.val_from.value:
            return False

        if self.val_to.mode == POINT_STRICT and val >= self.val_to.value:
            return False
        if self.val_to.mode == POINT_NON_STRICT and val > self.val_to.value:
            return False

        return True

    def __eq__(self, other: 'ValueRange'):
        return self.val_from == other.val_from and self.val_to == other.val_to

    def __str__(self):
        return f"{self.val_from} – {self.val_to}"
