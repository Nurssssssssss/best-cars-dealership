from django.urls import path
from . import views
urlpatterns=[path('csrf/',views.csrf),path('register/',views.register),path('login/',views.login_view),path('logout/',views.logout_view),path('dealers/',views.dealers),path('dealers/<int:pk>/',views.dealer),path('dealers/<int:pk>/reviews/',views.reviews),path('carmakes/',views.carmakes),path('analyze/',views.analyze)]
