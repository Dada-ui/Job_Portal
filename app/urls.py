from app import views
from django.urls import path


urlpatterns = [
    
    # Index #
    path('',views.indexview,name='index'),
    path('search',views.search,name='search'),
    path('jobs',views.jobs,name='jobs'),
    path('companies',views.companies,name='companies'),
    path('services',views.services,name='services'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('chatbot',views.chatbot,name='chatbot'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('login', views.LoginView.as_view(), name='login'),

    # User #
    path('dashboard',views.dashboard,name='dashboard'),
    path('searcher_register', views.RegistersearcherView.as_view(), name='searcher-register'),
    path('apply_jobs/<int:id>',views.apply_jobs,name='apply_jobs'),
    path('success_page',views.success_page,name='success_page'),
    
    # Profile #
    path('profile',views.profile,name='profile'),
    path('show_profile',views.show_profile,name='show_profile'),
    
    # Staff #
    path('home',views.home,name='home'),
    path('employee_register', views.RegisterEmployeeView.as_view(), name='employee-register'),
    path('employee',views.employee,name='employee'),
    path('add_jobs',views.add_jobs,name='add_jobs'),
    path('applicants',views.applicants,name='applicants'),
    path('find',views.find_resume,name='find'),
    path('rating_details/<int:id>',views.rating_details,name='rating'),
]