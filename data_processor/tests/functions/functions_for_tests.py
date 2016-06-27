"""
Functions used to help simplify tests
"""


def find_pop_and_return(looking_for, expected_list):
    """
    Takes in the expected list of items, looks for the item,
    if found returns the found item and the edited list
    :param expected_list: the list of what the expected test results should have
    :param looking_for: string of what should be in the list
    :return: the found item as a string and the edited list
    """

    for index, item in enumerate(expected_list):
        if looking_for == item:
            found_item = item
            expected_list.pop(index)
            return found_item, expected_list


def compare_expect_against_query(expected_employees, employees):
    """
    A comparison test to see if the expected is in the employees query set objects
    :param expected_employees: expected list
    :param employees: A QuerySet object to look through the Employee results
    :return: a list of T/F if the item was found
    """
    # decrement counter
    result_list = []
    for employee in employees:
        found_item, expected_employees = find_pop_and_return(
            looking_for=employee.EMP_ID_TXT,
            expected_list=expected_employees,
        )
        if len(expected_employees) == 0:
            return True
    else:
        return False


