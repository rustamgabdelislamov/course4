from django.urls import path

from clients.apps import ClientsConfig
from clients.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, ClientDetailView
from users.views import logout_view, RegisterView, UsersContactsView

app_name = ClientsConfig.name

urlpatterns = [
    path("clients_list/", ClientListView.as_view(template_name='clients/clients_list.html'),name='clients_list'),
    path("create_client/", ClientCreateView.as_view(), name='client_create'),
    path("update_client/<int:pk>/", ClientUpdateView.as_view(), name='client_update'),
    path("delete_client/<int:pk>/", ClientDeleteView.as_view(), name='client_delete'),
    path("detail_client/<int:pk>/", ClientDetailView.as_view(), name='client_detail'),

]