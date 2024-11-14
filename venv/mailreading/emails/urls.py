from django.urls import path
from .views import login_view,messages_view

urlpatterns = [
    path("login/", login_view),
    path("messages/", messages_view),

]
