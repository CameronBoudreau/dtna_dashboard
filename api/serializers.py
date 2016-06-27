from rest_framework import serializers
from .models import hours_per_unitATM


class hours_per_unitSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    shift = serializers.IntegerField()
    claims_s = serializers.IntegerField()
    claims_d = serializers.IntegerField()

    DEPT1_d_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT1_d_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)
    DEPT1_s_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT1_s_ne = serializers.IntegerField()
    DEPT1_s_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)

    DEPT2_d_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT2_d_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)
    DEPT2_s_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT2_s_ne = serializers.IntegerField()
    DEPT2_s_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)

    DEPT3_d_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT3_d_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)
    DEPT3_s_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT3_s_ne = serializers.IntegerField()
    DEPT3_s_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)

    DEPT4_d_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT4_d_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)
    DEPT4_s_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT4_s_ne = serializers.IntegerField()
    DEPT4_s_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)

    DEPT5_d_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT5_d_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)
    DEPT5_s_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT5_s_ne = serializers.IntegerField()
    DEPT5_s_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)

    DEPT6_d_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT6_d_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)
    DEPT6_s_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT6_s_ne = serializers.IntegerField()
    DEPT6_s_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)

    DEPT7_d_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT7_d_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)
    DEPT7_s_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT7_s_ne = serializers.IntegerField()
    DEPT7_s_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)

    DEPT8_d_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT8_d_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)
    DEPT8_s_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT8_s_ne = serializers.IntegerField()
    DEPT8_s_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)

    DEPT9_d_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT9_d_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)
    DEPT9_s_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    DEPT9_s_ne = serializers.IntegerField()
    DEPT9_s_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)

    OTHER_d_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    OTHER_d_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)
    OTHER_s_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    OTHER_s_ne = serializers.IntegerField()
    OTHER_s_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)

    PLANT_d_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    PLANT_d_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)
    PLANT_s_hours_per_unit = serializers.DecimalField(decimal_places=1, max_digits=4)
    PLANT_s_ne = serializers.IntegerField()
    PLANT_s_working_hours = serializers.DecimalField(decimal_places=2, max_digits=6)

    class Meta:
        model = hours_per_unitATM
