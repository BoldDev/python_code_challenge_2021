from django.urls import path

from show import views

urlpatterns = [
    path('',views.index,name="index")
]
