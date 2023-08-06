import base64
from typing import Iterable


def json_normalize_dict(source: dict):
    """
    Turns the values in *source* into values that can be serialized to JSON, avoiding *TypeError*:

    - *bytes* e *bytearray* are changed to *str* in *Base64* format
    - *Iterable* is changed into a *list*
    - all other types kept as they are
    HAZARD: depending on the type of object contained in *source*, the final result may not be serializable.

    :param source: the dict to be made serializable
    """
    for key, value in source.items():
        if isinstance(value, dict):
            json_normalize_dict(value)
        elif isinstance(value, bytes) or isinstance(value, bytearray):
            source[key] = base64.b64encode(value).decode()
        elif isinstance(value, Iterable) and not isinstance(value, str):
            source[key] = json_normalize_iterable(value)


def json_normalize_iterable(source: Iterable) -> list[any]:
    """
    Turns the values in *source* into values that can be serialized to JSON, avoiding *TypeError*:

    - *bytes* e *bytearray* are changed to *str* in *Base64* format
    - *Iterable* is changed into a *list*
    - all other types kept as they are
    HAZARD: depending on the type of object contained in *source*, the final result may not be serializable.

    :param source: the dict to be made serializable
    """
    result: list[any] = []
    for value in source:
        if isinstance(value, dict):
            json_normalize_dict(value)
            result.append(value)
        elif isinstance(value, bytes) or isinstance(value, bytearray):
            result.append(base64.b64encode(value).decode())
        elif isinstance(value, Iterable) and not isinstance(value, str):
            result.append(json_normalize_iterable(value))
        else:
            result.append(value)

    return result
