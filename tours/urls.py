from django.urls import path

from . import views

urlpatterns = [
    path('tours/', views.TourListView.as_view()),
    path('tours/<int:pk>/', views.TourDetail.as_view()),
]