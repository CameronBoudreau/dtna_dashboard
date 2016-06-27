from django.contrib.auth.forms import AuthenticationForm


def default(request):
    form = AuthenticationForm()
    context = {'form': form}
    return context
