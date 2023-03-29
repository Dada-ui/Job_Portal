from django.shortcuts import render,redirect
from app.forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import *
from django.contrib import messages, auth
from django.views.generic import *
from app.models import User
from django.shortcuts import HttpResponseRedirect
from django.db.models import Q
from django.views.generic import UpdateView
from app.forms import SearcherProfileUpdateForm
from app.models import User
from django.http import HttpResponseRedirect

# Create your views here.

############### -  INDEX  - ###############

def indexview(request):
    if request.user.is_authenticated and request.user.role == "searcher":
        return redirect('dashboard')
    elif request.user.is_authenticated and request.user.role == "employee":
        return redirect('home')
    else:
        return render(request,'index.html')


def jobs(request):
    if request.user.is_authenticated: 
        applied = list(Applicant.objects.filter(user=request.user).values_list('job_id', flat=True))
        j = Job.objects.exclude(id__in=applied)
    else:
        j = Job.objects.all()
    return render(request,'jobs.html',{'j':j})
    
    
def search(request):
    query = request.GET['query']
    s = Job.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
    return render(request, 'search.html', {'s':s})
    

def companies(request):
    return render(request,'companies.html')


def services(request):
    return render(request,'services.html')


def about(request):
    return render(request,'about.html')


def contact(request):
    return render(request,'contact.html')


def chatbot(request):
    return render(request,'chatbot.html')



###############  -  USER  -  ###############


@login_required(login_url='login')
def dashboard(request):
    if request.user.is_authenticated and request.user.role == "searcher":
        return render(request,'dashboard.html')
    else:
        return render(request,'index.html')


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        profile_photo = request.FILES['profile_photo']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        resume = request.FILES['resume']
        p = Profile.objects.create(profile_photo=profile_photo,first_name=first_name,last_name=last_name,email=email,resume=resume)
        p.user = request.user
        p.save()
        messages.success(request,'Profile added successfully...!')
        return render(request, 'show_profile.html',{'p': p})
    return render(request, 'profile.html')


@login_required(login_url='login')
def show_profile(request):
    sp = Profile.objects.get(user_id=request.user.id)    
    return render(request, 'show_profile.html', {'sp': sp})


########### - STAFF - ###########

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated and request.user.role == "employee":
        return render(request,'home.html')
    else:
        return render(request,'index.html')


@login_required(login_url='login')
def add_jobs(request):
    if request.method == 'POST':
            title = request.POST['title']
            Experience = request.POST['Experience']
            company_name = request.POST['company_name']
            location = request.POST['location']
            package = request.POST['package']
            benefits = request.POST['benefits']
            job_type = request.POST['job_type']
            qualifications = request.POST['qualifications']
            description = request.POST['description']
            last_date = request.POST['last_date']
            company_description = request.POST['company_description']
            website = request.POST['website']
            created_at = request.POST['created_at']
            a = Job.objects.create(title=title,Experience=Experience,company_name=company_name,location=location,package=package,benefits=benefits,job_type=job_type,qualifications=qualifications,description=description,last_date=last_date,company_description=company_description,website=website,created_at=created_at)
            a.save()
            messages.success(request,'New job add successfully..!')
            return redirect('jobs')
    return render(request,'add_jobs.html')


def employee(request):
    return render(request,'employee.html')


class RegistersearcherView(CreateView):
    model = User
    form_class = SearcherRegistrationForm
    template_name = 'searcher_register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            messages.success(request,'Signup done successfully...!')
            return redirect('login')
        else:
            return render(request, 'searcher_register.html', {'form': form})


class RegisterEmployeeView(CreateView):
    model = User
    form_class = EmployeeRegistrationForm
    template_name = 'employee_register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            messages.success(request,'Signup done successfully...!')
            return redirect('login')
        else:
            return render(request, 'employee_register.html', {'form': form})


class LoginView(FormView):
    """
        Provides the ability to login as a user with an email and password
    """
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)


@login_required(login_url='login')
def apply_jobs(request, id):
    aj = Job.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST['title']
        location = request.POST['location']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        resume = request.FILES['resume']
        a = Applicant.objects.create(title=title, location=location, first_name=first_name, last_name=last_name, phone=phone, email=email, resume=resume)
        a.user = request.user
        a.save()
        messages.success(request,'You have applied for a job successfully..! shortly you will get a mail')
        return render(request, 'success_page.html', {'a': a , 'aj': aj })
    return render(request, 'apply_jobs.html', {'aj': aj})


@login_required(login_url='login')
def success_page(request, id):
    s = Applicant.objects.get(id=id)
    return render(request, 'success_page.html', {'s': s})


def applicants(request):
    aj = Applicant.objects.all()
    return render(request,'applicants.html', {'aj': aj})


@login_required(login_url='login')
def find_resume(request):
    profiles = Profile.objects.all()
    a = ProfileRating.objects.aggregate(Avg('rating'))
    return render(request, 'find.html',{'profiles':profiles , 'a': a})


@login_required(login_url='login')
def rating_details(request,id): 
    p = Profile.objects.get(id=id)
    if request.method == 'POST':
        rating = request.POST['rating']
        review = request.POST['review']
        a = ProfileRating.objects.create(rating=rating, review=review)
        a.user = request.user
        a.save()
        messages.success(request,'You have given a Rating & Review to this profile')
        return render(request, 'rating_details.html', {'p': p , 'a': a })
    pr = ProfileRating.objects.all().last()
    return render(request, 'rating_details.html', {'p': p , 'pr': pr})