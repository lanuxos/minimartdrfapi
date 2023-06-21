from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='home'),
    path('create/', views.addItems, name='add-items'),
    path('all/', views.viewItems, name='view-items'),
    path('update/<int:pk>/', views.updateItems, name='update-items'),
    path('item/<int:pk>/delete/', views.deleteItems, name='delete-items'),
]