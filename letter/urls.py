from django.urls import path
from letter.apps import LetterConfig
from letter.views import LetterListView, LetterCreateView, LetterUpdateView, LetterDeleteView, LetterDetailView


app_name = LetterConfig.name

urlpatterns = [
    path("letter_list/", LetterListView.as_view(template_name='letter/letter_list.html'),name='letter_list'),
    path("create_letter/", LetterCreateView.as_view(), name='letter_create'),
    path("update_letter/<int:pk>/", LetterUpdateView.as_view(), name='letter_update'),
    path("delete_letter/<int:pk>/", LetterDeleteView.as_view(), name='letter_delete'),
    path("detail_letter/<int:pk>/", LetterDetailView.as_view(), name='letter_detail'),
]
