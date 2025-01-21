from django.urls import path
from . import views
from users.views import CustomAuthToken

urlpatterns = [
    path('workshops/', views.WorkshopList.as_view()),
    path('workshops/<int:pk>/', views.WorkshopDetail.as_view()),
    path('notes/', views.Notelist.as_view()),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),  
]