from django.urls import path,include
from store import views

urlpatterns = [
    path('',views.store,name='store'),
    path('cart',views.cart,name='cart'),
    path('checkout',views.checkout,name='checkout'),
    path('update_item',views.updateItem,name='update_item'),
    path('process_order',views.processOrder,name='process_order'),
    path('registration',views.registerUser,name='registration'),
    path('loginUser',views.loginUser,name='loginUser'),
    path('logoutUser',views.logoutUser,name='logoutUser'),
    path('adminpage',views.adminPage,name='adminpage'),
]