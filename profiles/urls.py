from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('', views.list_view, name="profiles"),
    path('bio/<int:item_id>', views.bio_view, name="bio")
]