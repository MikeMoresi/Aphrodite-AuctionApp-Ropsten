from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('',views.mainpage,name='mainpage'),
    path('sell',views.sellView,name='sell'),
    path('bid/<int:pk>',views.bidView,name='bid'),
]