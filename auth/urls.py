from django.urls import path
from django.contrib.auth.views import LogoutView

from auth.views import LoginView, SignupView

app_name = 'auth'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]