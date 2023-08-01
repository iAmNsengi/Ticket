from django.urls import path
from .views import *

urlpatterns = [
    path("", home),
    path("login/", Login),
    path("logout/", Logout),
    path("buy/", BuyTicket, name="buy"),
    path("buy/step2", BuyTicketStepTwo),
    path("buy/step3", BuyTicketStep3),
    path("buy/step4", BuyTicketStep4),
    path("profile/", MyProfile, name="profile"),
    path("confirmation/", Confirmation, name="confirmation"),
]
