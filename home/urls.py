from django.contrib import admin
from django.urls import path, include
from home import views



urlpatterns = [
    path('',views.project, name='home'),
    path('login',views.loginUser, name='login'),
    path('logout',views.logoutUser, name='logout'),
    path('mystock', views.myStock, name='mystock'),
    path('add_to_mystock',views.add_to_mystock,name='add_to_mystock'),
    path('searchs', views.searchStock, name='searchs'),
    path('regularneeds', views.regularNeeds, name="regularneeds"),
    path('globalinventory', views.globalInventory, name="globalinventory"),
    path('medshortage', views.medicineShortage, name='medshortage'),
    path('searchglobal',views.searchGlobal, name='searchglobal'),
    path('searchhome',views.searchHome,name="searchhome"),
    path('contactus', views.contactUs, name="contactus"),
]
