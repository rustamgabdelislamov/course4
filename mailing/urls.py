from django.urls import path
from mailing.apps import MailingConfig

from mailing.views import MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingDetailView, \
    send_mailing, AttemptListView

app_name = MailingConfig.name

urlpatterns = [
    path("mailing_list/", MailingListView.as_view(template_name='mailing/mailing_list.html'),name='mailing_list'),
    path("create_mailing/", MailingCreateView.as_view(), name='mailing_create'),
    path("update_mailing/<int:pk>/", MailingUpdateView.as_view(), name='mailing_update'),
    path("delete_mailing/<int:pk>/", MailingDeleteView.as_view(), name='mailing_delete'),
    path("detail_mailing/<int:pk>/", MailingDetailView.as_view(), name='mailing_detail'),
    path("send_mailing/<int:mailing_id>/", send_mailing, name='send_mailing'),
    path("attempt_list/",AttemptListView.as_view(template_name='mailing/attempt_list.html'),name='attempt_list')

]