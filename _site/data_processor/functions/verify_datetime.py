import datetime as dt


def verify_aware_datetime_object(datetime_object_list):
    """
    Verify that the given datetime objects are valid
    :param datetime_object_list: a list of datetime objects
    :return:
    """
    results = []
    for item in datetime_object_list:
        # handle None times for employees
        if item is None:
            results.append(None)
            continue
        elif isinstance(item, dt.datetime):
            if item.tzinfo is not None:
                results.append(True)
            else:
                print("!" * 50)
                print("RECEIVED A DATETIME OBJECT THAT WAS NOT AWARE: ", item)
                print("!" * 50)
                results.append(False)
        # Didn't receive a DT Obj
        else:
            print("!" * 50)
            print("RECEIVED A NON DATETIME OBJ: ", item)
            results.append(False)
    return results
