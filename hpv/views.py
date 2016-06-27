from django.shortcuts import render
from django.views.generic.base import TemplateView
import datetime as dt
from api.models import hours_per_unitATM
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from collections import OrderedDict


class hours_per_unit(LoginRequiredMixin, TemplateView):
    template_name = "hours_per_unit/hours_per_unit2.html"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        """
        Obtains the most current hours_per_unit object and checks the database for objects
        with shifts 1-3. Sets up an empty dictionary of departments as keys and
        an empty dictionary for the values. Queries the timestamp of the
        current variable object and adds it to the context data. The functions
        for the day and shifts data are called with the departments, context
        and related objects being passed in.
        The departments dictionary order is set (with keyorder and OrderedDict)
        so the departments in the hours_per_unit table are always displayed in the same
        order. The depts dictionary is added to the context.

        :param kwargs: cover all possible imports for the function
        :return: context data
        """

        # Recursive call for context
        context = super().get_context_data(**kwargs)

        # If no data in API
        if hours_per_unitATM.objects.count() == 0:
            return context

        # Obtaining and assigning objects
        current = hours_per_unitATM.objects.latest('timestamp')
        shift1 = hours_per_unitATM.objects.filter(shift=1)
        shift2 = hours_per_unitATM.objects.filter(shift=2)
        shift3 = hours_per_unitATM.objects.filter(shift=3)

        # Seperate into depatrments
        depts = {
            'DEPT1': {},
            'DEPT2': {},
            'DEPT3': {},
            'DEPT4': {},
            'DEPT5': {},
            'DEPT6': {},
            'DEPT7': {},
            'DEPT8': {},
            'DEPT9': {},
            'PLANT': {}
        }

        # For printing out the time of the most recent object
        current_time = current.timestamp
        context.update({'current_time': current_time})

        # Function call for the each portion context data
        self.set_day_data(current, context, depts)
        self.set_shift1_data(current, shift1, context, depts)
        self.set_shift2_data(current, shift2, context, depts)
        self.set_shift3_data(current, shift3, context, depts)

        # Set order of the departments dictionary so the table in the HTML is
        # in order
        keyorder = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8',
                    'DEPT9', 'PLANT']

        context['depts'] = OrderedDict(sorted(depts.items(), key=lambda
                                              i: keyorder.index(i[0])))

        return context

    def set_day_data(self, current, context, depts):
        """
        Using the current object, the function finds and assigns a key and
        value pair for each piece of data for the day column of the hours_per_unit table.
        Each datapoint is collected for the day hours_per_unit for each department.
        The claims (number of finished trucks this day) are queried and added
        to the context.

        :param current: the most recent object added to the api database
        :param context: the current context dataset
        :param depts: the dictionary of dictionaries for the department
        datasets the function is appending to.
        """

        # Catching the data from the API object and putting it in the depts
        # dictionary
        depts['DEPT1']['d_hours_per_unit'] = current.DEPT1_d_hours_per_unit
        depts['DEPT2']['d_hours_per_unit'] = current.DEPT2_d_hours_per_unit
        depts['DEPT3']['d_hours_per_unit'] = current.DEPT3_d_hours_per_unit
        depts['DEPT4']['d_hours_per_unit'] = current.DEPT4_d_hours_per_unit
        depts['DEPT5']['d_hours_per_unit'] = current.DEPT5_d_hours_per_unit
        depts['DEPT6']['d_hours_per_unit'] = current.DEPT6_d_hours_per_unit
        depts['DEPT7']['d_hours_per_unit'] = current.DEPT7_d_hours_per_unit
        depts['DEPT8']['d_hours_per_unit'] = current.DEPT8_d_hours_per_unit
        depts['DEPT9']['d_hours_per_unit'] = current.DEPT9_d_hours_per_unit
        depts['PLANT']['d_hours_per_unit'] = current.PLANT_d_hours_per_unit

        # Catching the days claims data and adding it to the context
        claims_d = current.claims_d
        context.update({'claims_d': claims_d})

    def set_shift1_data(self, current, shift1, context, depts):
        """
        Checks to make sure at least one object with a shift value of 1 is
        passed in. If no object is passed in the function is returned.
        If there are objects, if finds the most recent one by calling
        ".latest('timestamp')". If the timestamp of the most recent shift 1
        object is not within the last 17 hours of the current object, the
        function is returned.
        If the shift object is within 17 hours of the current object, the
        shift's object is used to obtain the shift specific department
        datapoints are assigned as key value pairs in the depts dictionary.
        The claims (number of completed trucks this shift) is queried and added
        to the context.

        :param current: the most recent object added to the api database
        :param shift1: all the objects with a shift value of 1
        :param context: the current context dataset
        :param depts: the dictionary of dictionaries for the department
        datasets the function is appending to.
        """

        # If the most recent API object is not shift 1 it moves onto the next
        # if statement
        if not shift1:
            return

        # Finds most recent API object that is shift 1 between now and 17 hours
        # ago (near end of last shift)
        # If there is no shift 1 within the last 17 hours it returns out of the
        # funtion
        shift1 = shift1.latest('timestamp')
        if not (shift1.timestamp >=
                current.timestamp - dt.timedelta(hours=17)):
            return

        # Catching the data from the API object and putting it in the depts
        # dictionary
        depts['DEPT1']['s1_hours_per_unit'] = shift1.DEPT1_s_hours_per_unit
        depts['DEPT2']['s1_hours_per_unit'] = shift1.DEPT2_s_hours_per_unit
        depts['DEPT3']['s1_hours_per_unit'] = shift1.DEPT3_s_hours_per_unit
        depts['DEPT4']['s1_hours_per_unit'] = shift1.DEPT4_s_hours_per_unit
        depts['DEPT5']['s1_hours_per_unit'] = shift1.DEPT5_s_hours_per_unit
        depts['DEPT6']['s1_hours_per_unit'] = shift1.DEPT6_s_hours_per_unit
        depts['DEPT7']['s1_hours_per_unit'] = shift1.DEPT7_s_hours_per_unit
        depts['DEPT8']['s1_hours_per_unit'] = shift1.DEPT8_s_hours_per_unit
        depts['DEPT9']['s1_hours_per_unit'] = shift1.DEPT9_s_hours_per_unit
        depts['PLANT']['s1_hours_per_unit'] = shift1.PLANT_s_hours_per_unit

        # Catching the shifts claims data and adding it to the context
        s1_claims = shift1.claims_s
        context.update({'s1_claims': s1_claims})

    def set_shift2_data(self, current, shift2, context, depts):
        """
        Checks to make sure at least one object with a shift value of 2 is
        passed in. If no object is passed in the function is returned.
        If there are objects, if finds the most recent one by calling
        ".latest('timestamp')". If the timestamp of the most recent shift 2
        object is not within the last 17 hours of the current object, the
        function is returned.
        If the shift object is within 17 hours of the current object, the
        shift's object is used to obtain the shift specific department
        datapoints are assigned as key value pairs in the depts dictionary.
        The claims (number of completed trucks this shift) is queried and added
        to the context.

        :param current: the most recent object added to the api database
        :param shif2: all the objects with a shift value of 2
        :param context: the current context dataset
        :param depts: the dictionary of dictionaries for the department
        datasets the function is appending to.
        """

        # If the most recent API object is shift 2 function skips to the next
        # step
        if not shift2:
            return

        # Finds most recent API object that is shift 2 between now and 17 hours
        # ago (near end of last shift)
        # If there is no shift 2 within the last 17 hours it returns out of the
        # funtion
        shift2 = shift2.latest('timestamp')
        if not (shift2.timestamp >=
                current.timestamp - dt.timedelta(hours=17)):
            return

        # Catching the data from the API object and putting it in the depts
        # dictionary
        depts['DEPT1']['s2_hours_per_unit'] = shift2.DEPT1_s_hours_per_unit
        depts['DEPT2']['s2_hours_per_unit'] = shift2.DEPT2_s_hours_per_unit
        depts['DEPT3']['s2_hours_per_unit'] = shift2.DEPT3_s_hours_per_unit
        depts['DEPT4']['s2_hours_per_unit'] = shift2.DEPT4_s_hours_per_unit
        depts['DEPT5']['s2_hours_per_unit'] = shift2.DEPT5_s_hours_per_unit
        depts['DEPT6']['s2_hours_per_unit'] = shift2.DEPT6_s_hours_per_unit
        depts['DEPT7']['s2_hours_per_unit'] = shift2.DEPT7_s_hours_per_unit
        depts['DEPT8']['s2_hours_per_unit'] = shift2.DEPT8_s_hours_per_unit
        depts['DEPT9']['s2_hours_per_unit'] = shift2.DEPT9_s_hours_per_unit
        depts['PLANT']['s2_hours_per_unit'] = shift2.PLANT_s_hours_per_unit

        # Catching the shifts claims data and adding it to the context
        s2_claims = shift2.claims_s
        context.update({'s2_claims': s2_claims})

    def set_shift3_data(self, current, shift3, context, depts):
        """
        Checks to make sure at least one object with a shift value of 3 is
        passed in. If no object is passed in, shift_3 is set to False added to
        the context. The if statement then returns out of the function.
        If there are objects, if finds the most recent one by calling
        ".latest('timestamp')". If the timestamp of the most recent shift 3
        object is not within the last 17 hours of the current object, the
        function is returned.
        If the shift object is within 17 hours of the current object, the
        shift's object is used to obtain the shift specific department
        datapoints are assigned as key value pairs in the depts dictionary.
        The claims (number of completed trucks this shift) is queried and
        shift_3 is set to True. Both are added to the context.

        :param current: the most recent object added to the api database
        :param shift3: all the objects with a shift value of 3
        :param context: the current context dataset
        :param depts: the dictionary of dictionaries for the department
        datasets the function is appending to.
        """

        # If the most recent API object is not shift 3, shift 3 is False and is
        # added to the context, passes to the next if statment
        if not shift3:
            shift_3 = False
            context.update({'shift_3': shift_3})
            return

        # Finds most recent API object that is shift 3 between now and 17 hours
        # ago (near end of last shift)
        # If there is no shift 2 within the last 17 hours it returns out of the
        # funtion
        shift3 = shift3.latest('timestamp')
        if not (shift3.timestamp >=
                current.timestamp - dt.timedelta(hours=17)):
            return

        # Catching the data from the API object and putting it in the depts
        # dictionary
        depts['DEPT1']['s3_hours_per_unit'] = shift3.DEPT1_s_hours_per_unit
        depts['DEPT2']['s3_hours_per_unit'] = shift3.DEPT2_s_hours_per_unit
        depts['DEPT3']['s3_hours_per_unit'] = shift3.DEPT3_s_hours_per_unit
        depts['DEPT4']['s3_hours_per_unit'] = shift3.DEPT4_s_hours_per_unit
        depts['DEPT5']['s3_hours_per_unit'] = shift3.DEPT5_s_hours_per_unit
        depts['DEPT6']['s3_hours_per_unit'] = shift3.DEPT6_s_hours_per_unit
        depts['DEPT7']['s3_hours_per_unit'] = shift3.DEPT7_s_hours_per_unit
        depts['DEPT8']['s3_hours_per_unit'] = shift3.DEPT8_s_hours_per_unit
        depts['DEPT9']['s3_hours_per_unit'] = shift3.DEPT9_s_hours_per_unit
        depts['PLANT']['s3_hours_per_unit'] = shift3.PLANT_s_hours_per_unit

        # Catching the shifts claims data, shift 3 is now True, adding both to
        # the context
        s3_claims = shift3.claims_s
        shift_3 = True
        context.update({'s3_claims': s3_claims, 'shift_3': shift_3})


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')


class Detail(LoginRequiredMixin, TemplateView):
    template_name = "hours_per_unit/detail.html"
    login_url = '/login/'

    def detail(request):
        return render(request, self.template_name)
