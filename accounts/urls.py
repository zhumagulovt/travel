from django.urls import path, include

from . import views

urlpatterns = [
    path('signup/', views.RegistrationView.as_view()),
    path('activate/', views.ActivationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.logout),
    path('change-password/', views.PasswordChangeView.as_view()),
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password-reset')),
    path('saved/', views.SavedView.as_view())
]