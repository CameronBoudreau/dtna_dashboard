from .man_hours_calculations import get_emp_man_hours, get_emp_dept


def iterate_over_employees(by_dept_dict, employees, start, stop):
    """
    Iterates over the employees queryset and adds the inforDEPT9ion to the dict
    :param by_dept_dict: instance of the master dept dict
    :param employees: employees query set
    :param start: DATETIME TIMEZONE AWARE object
    :param stop: DATETIME TIMEZONE AWARE object
    :return: the instance of the department dict
    """
    # defining only the plant portion of the dict
    plant_dict = by_dept_dict['PLANT']
    claims = by_dept_dict['claims_for_range']
    for employee in employees:
        # getting emp's department
        emp_dept = get_emp_dept(
            employee.EMP_DEPT_TXT
        )

        if emp_dept in by_dept_dict:
            # referencing only that emp dept
            dept = by_dept_dict[emp_dept]
            # increasing num of emp by one
            dept['ne'] += 1
            # calculate emp man hours
            emp_man_hours = get_emp_man_hours(employee, start, stop)
            dept['mh'] += emp_man_hours

            # incrementing plant man hours
            plant_dict['ne'] += 1
            plant_dict['mh'] += emp_man_hours

            dept, plant_dict = calc_hours_per_unit(claims, dept, plant_dict)
    return by_dept_dict


def calc_hours_per_unit(claims, dept, plant_dict):
    """
    Calculates the hours_per_unit for each department and the plant.
    Yes it does this every cycle. Haven't timed it if it is
    :param claims:
    :param dept:
    :param plant_dict:
    :return:
    """
    print(dept)
    if claims != 0:
        dept['hours_per_unit'] = dept['mh'] / claims
        plant_dict['hours_per_unit'] = plant_dict['mh'] / claims
    return dept, plant_dict
