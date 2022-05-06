from django.urls import path
from .views import CustomLoginView, RegisterView, CreatePackTypeView, PackListView
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', PackListView.as_view(), name='pack_list'),
    path('create_pack_type', CreatePackTypeView.as_view(), name='create_pack_type'),
]
