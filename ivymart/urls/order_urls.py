from django.urls import path
from ivymart.views import order_views as views


urlpatterns = [
    path('all/orders/',views.getOrders,name="allorders"),
    path('add/order/',views.addOrderItems,name="orders-add"),
    path('myorders/',views.getMyOrders,name="myorders"),
    path('payment/success/',views.handlePaymentSuccess,name="payment_success"),

    path('<str:pk>/deliver/',views.updateOrderToDelivered,name="delivered"),
    path('<str:pk>/',views.getOrderById,name="user-order"),
    path('<str:pk>/pay/',views.updateOrderToPaid,name="pay"),
    path('pay/',views.startPayment,name="razor_pay"),
]