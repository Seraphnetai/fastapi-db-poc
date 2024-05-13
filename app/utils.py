"""Utilsy używane w ramach usługi"""

from app.models import EndpointInputModel


def validate_input(input_: EndpointInputModel):
    """
    Funkcja sprawdzająca czy input do enpointa ma poprawną strukturę

    Args:
        input_ (EndpointInputModel): JSON stanowiący request body

    Returns:
        (bool): wartość logiczna mówiąca o tym czy podany JSON jest poprawny
    """
    if input_:
        return True
    else:
        return False
