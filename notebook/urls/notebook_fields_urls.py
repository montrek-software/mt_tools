from django.shortcuts import redirect
from django.urls import path
from mt_tools.notebook.views.notebook_fields_views import NotebookFieldsListView
from mt_tools.notebook.views.notebook_fields_views import NotebookFieldsCreateView
from mt_tools.notebook.views.notebook_fields_views import NotebookFieldsUpdateView
from mt_tools.notebook.views.notebook_fields_views import NotebookFieldsDeleteView
from mt_tools.notebook.views.notebook_fields_views import NotebookFieldsDetailView
from mt_tools.notebook.views.notebook_fields_views import NotebookFieldsHistoryView

urlpatterns = [
    path(
        "notebook_fields",
        lambda _: redirect("notebook_fields_list"),
        name="notebook_fields",
    ),
    path(
        "notebook_fields/list",
        NotebookFieldsListView.as_view(),
        name="notebook_fields_list",
    ),
    path(
        "notebook_fields/create",
        NotebookFieldsCreateView.as_view(),
        name="notebook_fields_create",
    ),
    path(
        "notebook_fields/<int:pk>/delete",
        NotebookFieldsDeleteView.as_view(),
        name="notebook_fields_delete",
    ),
    path(
        "notebook_fields/<int:pk>/update",
        NotebookFieldsUpdateView.as_view(),
        name="notebook_fields_update",
    ),
    path(
        "notebook_fields/<int:pk>/details",
        NotebookFieldsDetailView.as_view(),
        name="notebook_fields_details",
    ),
    path(
        "notebook_fields/<int:pk>/history",
        NotebookFieldsHistoryView.as_view(),
        name="notebook_fields_history",
    ),
]
