from django.urls import path
from .views import assign_role, create_user, login_view, logout_view, user_list

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("users/", user_list, name="user_list"),
    path("assign-role/<int:id>/", assign_role, name="assign_role"),
    path("create-user/", create_user, name="create_user")
]