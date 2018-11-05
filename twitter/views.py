from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .forms import userinput
from . apicall import getdata
from chartjs.views.lines import BaseLineChartView

# Importations for PDF report processing
from django.views.generic import View
from django.utils import timezone
from .models import *
from .render import Render
# End of importations for PDF

from .models import *
from .forms import RegistrationForm, EditProfileForm
from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404


# Create your views here.

def index(request):

    return render(request,'index.html')

def query(request):
    # hall = 'trump'
    # random = getdata(hall)
    # print(random)
    word = "word of the home"
    return render(request, 'home.html', {"word": word})


# class LineChartJSONView(BaseLineChartView):
#     template_name = 'home.html'

#     def get_labels(self):
#         """Return 7 labels for the x-axis."""
#         return ["January", "February", "March", "April", "May", "June", "July"]

#     def get_providers(self):
#         """Return names of datasets."""
#         return ["Central", "Eastside", "Westside"]

#     def get_data(self):
#         """Return 3 datasets to plot."""

#         return [[75, 44, 92, 11, 44, 95, 35],
#                 [41, 92, 18, 3, 73, 87, 92],
#                 [87, 21, 94, 3, 90, 13, 65]]


def analyse(request):
    user_input = userinput(request.GET or None)
    if request.GET and user_input.is_valid():
        input_hastag = user_input.cleaned_data['q']
        # print(input_hastag)
        data = getdata(input_hastag)
        positive = data['Positive']
        neutral = data['Neutral']
        negative = data['Negative']
        print(data['Positive'])
        print(data)
        return render(request, "results.html", {'data': data, 'positive': positive, 'neutral': neutral, 'negative': negative})
    return render(request, "home.html", {'input_hastag': user_input})




# View for converting the template to PDF
class Pdf(View):

    def get(self, request):
        report = Report.objects.all()
        today = timezone.now()
        params = {
            'today': today,
            'sentiments': report,
            'request': request
        }
        return Render.render('pdf.html', params)


# Authentication views
def register(request):
    if request.user.is_authenticated():
        return redirect('index')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # user.is_active = False
                user.save()
                # current_site = get_current_site(request)
                # to_email = form.cleaned_data.get('email')
                # activation_email(user, current_site, to_email)
                # return HttpResponse('Please confirm your email')
            return redirect('auth_login')

        else:
            form = RegistrationForm()
        return render(request, 'registration/signup.html',{'form':form})

def profile(request,username):
    profile = User.objects.get(username=username)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    sentiments = Reports.get_profile_reports(profile.id)
    title = f'@{profile.username} Projects'


    return render(request, 'profile/profile.html', {'title':title, 'profile':profile, 'sentiments':sentiments, 'profile_details':profile_details})



def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('profile',username=request.user)
    else:
        form = EditProfileForm()

    return render(request, 'profile/edit_profile.html', {'form':form})
