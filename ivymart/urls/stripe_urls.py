from django.urls import path
from ivymart.views.stripePayment_view import stripeCheckoutView


urlpatterns = [
    path("payment/", stripeCheckoutView, name="stripe-payment"),
]
