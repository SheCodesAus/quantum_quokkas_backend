from django.urls import path
from . import views
from users.views import CustomAuthToken

urlpatterns = [
    path('workshops/', views.WorkshopList.as_view()),
    path('activeworkshops/', views.ActiveWorkshopsList.as_view()),
    path('workshops/<int:pk>/', views.WorkshopDetail.as_view()),
    path('notes/', views.Notelist.as_view()),
    path('recentnotes/', views.RecentNotesList.as_view()),
    path('notes/<int:pk>/', views.NoteDetail.as_view()),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('locations/', views.LocationList.as_view()),
    path('locations/<int:pk>/', views.LocationDetail.as_view()),
    path('organisations/', views.OrganisationList.as_view()),
    path('organisations/<int:pk>/', views.OrganisationDetail.as_view()),
    path('counts/', views.CountsView.as_view()),
    path('workshops/notes-count/', views.WorkshopNotesCountView.as_view()),

]