"""
Main is what orchestrates all of the sub functions.
"""

from .claims_calculations import get_range_of_claims
from .man_hours_calculations import get_employees
from .hours_per_unit_calcuations import iterate_over_employees
from .config.look_up_values import get_master_by_dept_dict





def main(start, stop):
    """
    Main function that queries the DB to return hours_per_unit by dept.
    :param start: DATETIME TIMEZONE AWARE object
    :param stop:  DATETIME TIMEZONE AWARE object
    :return: completed_by_dept_dict that is based on master by dept dict fully calculated.
    """
    print("!*"*50)
    print("PROCESS DATA MAIN FUNCTION")
    print("!*"*50)
    print("START= ",start,"STOP =", stop)

    # create instance of master dept dict
    by_dept_dict = get_master_by_dept_dict()

    # populate claims for range
    by_dept_dict['claims_for_range'] = get_range_of_claims(start, stop)
    print("CLAIMS FOR RANGE: ", by_dept_dict['claims_for_range'])

    # get employees
    employees = get_employees(start, stop)
    # iterate over the list employee queries
    by_dept_dict = iterate_over_employees(by_dept_dict, employees, start, stop)

    return by_dept_dict






