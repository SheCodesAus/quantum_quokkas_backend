from django.urls import path
from . import views

urlpatterns = [
    path('workshops/', views.WorkshopList.as_view()),
    path('workshops/<int:pk>/', views.WorkshopDetail.as_view()),
    path('notes/', views.Notelist.as_view()),
   
]