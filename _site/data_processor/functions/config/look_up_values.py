def get_master_by_dept_dict():
    """
    made this for readability purposes and to have
    one version of the truth for this dict.
    :return: RETURNS a zero'd out dict with lists in it.
    The first items in the list are as follows, in order:
    'mh' = man hours for that dept
    'ne' = number of employees for clocked in
    'hours_per_unit' = hours per vehicle
    """
    master_by_dept_dict = {
        'DEPT1': {
            'mh': 0,
            'ne': 0,
            'hours_per_unit': 0,
        },
        'DEPT2': {
            'mh': 0,
            'ne': 0,
            'hours_per_unit': 0,
        },
        'DEPT3': {
            'mh': 0,
            'ne': 0,
            'hours_per_unit': 0,
        },
        'DEPT4': {
            'mh': 0,
            'ne': 0,
            'hours_per_unit': 0,
        },
        'DEPT5': {
            'mh': 0,
            'ne': 0,
            'hours_per_unit': 0,
        },
        'DEPT6': {
            'mh': 0,
            'ne': 0,
            'hours_per_unit': 0,
        },
        'DEPT7': {
            'mh': 0,
            'ne': 0,
            'hours_per_unit': 0,
        },
        'DEPT8': {
            'mh': 0,
            'ne': 0,
            'hours_per_unit': 0,
        },
        'DEPT9': {
            'mh': 0,
            'ne': 0,
            'hours_per_unit': 0,
        },
        'OTHER': {
            'mh': 0,
            'ne': 0,
            'hours_per_unit': 0,
        },
        'PLANT': {
            'mh': 0,
            'ne': 0,
            'hours_per_unit': 0,
        },
        'claims_for_range': 0
    }

    return master_by_dept_dict


def get_dept_lookup_dict():
    dept_lookup_dict = {
        '1': 'DEPT1',
        '2': 'DEPT2',
        '3': 'DEPT3',
        '4': 'DEPT4',
        '5': 'DEPT5',
        '6': 'DEPT6',
        '7': 'DEPT7',
        '8': 'DEPT8',
        '9': 'DEPT9',
    }
    return dept_lookup_dict
