def calc_hours_per_unit(mh, claims):
    """

    :param mh: Integer value - total manhours.
    :param mh: Integer value - total claims.
    :return: Float value - hours_per_unit.
    """
    if claims == 0:
        hours_per_unit = 0
    else:
        hours_per_unit = mh/claims
    return hours_per_unit
