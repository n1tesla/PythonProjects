def calculate_pressure(temp: float, temp_coeff_1=-4, temp_coeff_2=122) -> float:
    """
    calculate pressure with given params
    :param temp: a generated float number
    :return: a float
    """
    return -temp_coeff_1 * temp + temp_coeff_2


def calculate_velocity(acceleration: float, sec_coeff=0.5) -> float:
    """
    calculate velocity with given params
    :param acceleration: a generated float number
    :return: a float
    """
    return acceleration * sec_coeff


def derive_feature(**kwargs):
    pass


