from django.urls import path
from . import views

urlpatterns = [
   path('signup/', views.CustomUserList.as_view()), 
   path('login/', views.CustomAuthToken.as_view()),  
   path('users/', views.CustomUserList.as_view()),   
   path('users/<int:pk>/', views.CustomUserDetail.as_view()),
]