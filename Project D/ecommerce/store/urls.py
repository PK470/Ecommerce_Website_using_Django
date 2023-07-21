from django.urls import path
from .import views

urlpatterns = [
    path('',views.store,name='store'),
    path('carts/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('updateItem/',views.updateItem,name='updateItem'),
    path('processOrder/',views.processorder,name='processOrder'),
    path('register/',views.register,name='register'),
    path('login/',views.ulogin,name='login'),
    path('logout/',views.uLogout,name='logout'),
    path('pview/<int:pk>',views.pView,name='pview'),
    path('search/',views.search,name='search'),
    path('forgetpassword/',views.forgotpassword,name='forgetpassword'),
    path('changepass/',views.chgpass,name='changepass')
]
