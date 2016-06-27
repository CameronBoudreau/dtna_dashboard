from get_data.models import PlantActivityModel


def get_claimed_objects_in_range(start, stop):
    """
    returns filtered objects within a range of start, stop
    :param start: Datetime object that points to the start of the query
    :param stop: Datetime object to slice the view
    :return: PlantActivityModel, 'claim', objects

    """
    return PlantActivityModel.objects.filter(
        UNIT_LOADED_TIME__gte=start,
        UNIT_LOADED_TIME__lte=stop,
        UNIT_COMPLETED_DEPT__exact='03',
    )


def get_range_of_claims(start, stop):
    """
    gets trucks claimed in system from start to stop
    :param start: Datetime object that points to the start of the query
    :param stop: Datetime object or None to slice the view or just get from start to current time
    :return: int of number of trucks produced from start to stop
    """
    num_trucks = get_claimed_objects_in_range(start, stop)
    print('('*50)
    print('NUM TRUCKS FROM CLAIMS', num_trucks.count())
    print('(' * 50)

    return num_trucks.count()
