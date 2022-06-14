from django.urls import path, include

from . import views
from .routers import router

urlpatterns = [
    path('tours/', views.TourListView.as_view()),
    path('tours/<int:pk>/', views.TourDetail.as_view()),
    path('tours/<int:pk>/saved/', views.SavedView.as_view()),
    path('tours/', include(router.urls)),
    path('tours/<int:pk>/rating/', views.SavedView.as_view()),
]