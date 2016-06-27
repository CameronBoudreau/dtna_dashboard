from django.db import models

class hours_per_unitATM(models.Model):
    """
    Keeps track of all data related to hours_per_unit (Man Hours per Vehicle) for graphing and historical viewing. All values are ATM (At This Moment) referring to the timestamp.

    :param timestamp: When processed data was added
    :param num_clocked_in: Currently working employees
    :param num_claims_to_time: Number of trucks completed so far that day
    """
    timestamp = models.DateTimeField()
    shift = models.IntegerField()
    claims_s = models.IntegerField()
    claims_d = models.IntegerField()

    DEPT1_d_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT1_d_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    DEPT1_s_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT1_s_ne = models.IntegerField()
    DEPT1_s_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    DEPT2_d_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT2_d_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    DEPT2_s_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT2_s_ne = models.IntegerField()
    DEPT2_s_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    DEPT3_d_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT3_d_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    DEPT3_s_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT3_s_ne = models.IntegerField()
    DEPT3_s_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    DEPT4_d_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT4_d_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    DEPT4_s_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT4_s_ne = models.IntegerField()
    DEPT4_s_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    DEPT5_d_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT5_d_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    DEPT5_s_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT5_s_ne = models.IntegerField()
    DEPT5_s_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    DEPT6_d_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT6_d_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    DEPT6_s_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT6_s_ne = models.IntegerField()
    DEPT6_s_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    DEPT7_d_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT7_d_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    DEPT7_s_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT7_s_ne = models.IntegerField()
    DEPT7_s_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    DEPT8_d_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT8_d_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    DEPT8_s_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT8_s_ne = models.IntegerField()
    DEPT8_s_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    DEPT9_d_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT9_d_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    DEPT9_s_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DEPT9_s_ne = models.IntegerField()
    DEPT9_s_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    OTHER_d_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    OTHER_d_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    OTHER_s_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    OTHER_s_ne = models.IntegerField()
    OTHER_s_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    PLANT_d_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    PLANT_d_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    PLANT_s_hours_per_unit = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    PLANT_s_ne = models.IntegerField()
    PLANT_s_working_hours = models.DecimalField(decimal_places=2, max_digits=6, null=True)

### To Add
# calculated tables hours_per_unit atm
# attendance table atm
# api call to serve hours_per_unit y and time as x
