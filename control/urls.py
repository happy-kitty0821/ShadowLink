from control import views as controlViews
from django.urls import path

urlpatterns = [
    path('home/', controlViews.dashboard, name='dashboard' ),
]