from django.contrib.auth.views import LoginView
from django.urls import path


from users.apps import UsersConfig
from users.views import logout_view, RegisterView, UsersListView, UsersContactsView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/', logout_view,name='logout'),
    path('register/', RegisterView.as_view(),name='register'),
    path("list/", UsersListView.as_view(), name="users_list"),
    path("contacts/", UsersContactsView.as_view(), name="contacts"),
]