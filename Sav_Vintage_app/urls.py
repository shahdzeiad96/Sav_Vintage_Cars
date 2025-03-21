from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
path('',views.login,name='login'),
path('register',views.register, name='register'),
path('login',views.login, name='login'),
path('success',views.success,name='success'),
path('logout',views.logout,name='logout'),
path('addCar',views.addCar,name='addCar'),
path('details/<int:id>',views.details,name='details'),
path('delete/<int:id>',views.deleteCar,name='delete'),
path('cancel/<int:id>',views.cancelOrder,name='cancel'),
path('update/<int:id>',views.update,name='update'),
path('successPurchase/<int:car_id>',views.makePurchase,name='successPurchase'),
path('viewOrders',views.viewOrders,name='viewOrders'),
path('cancel',views.cancelAdd,name='cancel')
]