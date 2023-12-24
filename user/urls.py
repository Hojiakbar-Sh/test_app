from django.contrib.auth.views import LoginView
from django.urls import path

from user.forms import CustomAuthenticationForm
from user.views import RegisterView, DetailProfileView, logout_view, EditProfileView, DeleteProfileView

app_name = 'account'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path(
        'login/',
        LoginView.as_view(authentication_form=CustomAuthenticationForm, template_name='pages/login_page.html'),
        name='login'
    ),
    path('logout/', logout_view, name='logout'),
    path('profile/detail/<int:pk>/', DetailProfileView.as_view(), name='profile_detail'),
    path('profile/edit/<int:pk>/', EditProfileView.as_view(), name='profile_edit'),
    path('profile/delete/<int:pk>/', DeleteProfileView.as_view(), name='profile_delete'),
]
