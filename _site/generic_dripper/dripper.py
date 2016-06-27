from .models import EmpClockDataModelDripper
from .models import PlantActivityModelDripper, CombinedDripper


class MasterDripper:
    """

    """
    instance = None

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        if self.instance is None:
            self.instance = CombinedDripper(*args, **kwargs)
        else:
            raise AttributeError("A dripper is already defined")


    def __getattr__(self, name):
        """

        :param name:
        :return:
        """
        return getattr(self.instance, name)
