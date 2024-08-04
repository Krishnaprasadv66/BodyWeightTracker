"""
URL configuration for Weight_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from weight_loss import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage,name='home'),
    path('signup',views.signup_page,name='signup'),
    path('login',views.login_page,name='login'),
    path('adddata',views.mark_the_weight,name='adddata'),
    path('logout',views.logout_view,name='logout'),
    path('listview',views.listing,name='listview'),
    path('editdata/<int:id>/', views.edit_datas,name='editdata'),
    path('deletedata/<int:pk>/', views.delete_data, name='deletedata'),
    path('compare_weights/',views.compare_weights,name='compare_weights')
   
]
