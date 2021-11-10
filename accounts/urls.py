from django.urls import path
from .views import LoginView, SignupView, ForgotPasswordEmail, ForgotPasswordReset
urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', SignupView.as_view()),
    path('forgot-password-email/', ForgotPasswordEmail.as_view()),  #Send email with link to reset password
    path('forgot-password-reset/', ForgotPasswordReset.as_view()),
]