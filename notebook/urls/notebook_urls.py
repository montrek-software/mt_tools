from mt_tools.notebook.views.notebook_views import NotebookNotebookDatasListView
from mt_tools.notebook.views.notebook_views import NotebookNotebookDataCreateView
from django.shortcuts import redirect
from django.urls import path

from mt_tools.notebook.views.notebook_views import (
    NotebookCreateView,
    NotebookDeleteView,
    NotebookDetailView,
    NotebookHistoryView,
    NotebookListView,
    NotebookNotebookFieldsCreateView,
    NotebookNotebookFieldssListView,
    NotebookUpdateView,
)

urlpatterns = [
    path("notebook", lambda _: redirect("notebook_list"), name="notebook"),
    path(
        "notebook/list",
        NotebookListView.as_view(),
        name="notebook_list",
    ),
    path(
        "notebook/create",
        NotebookCreateView.as_view(),
        name="notebook_create",
    ),
    path(
        "notebook/<int:pk>/delete",
        NotebookDeleteView.as_view(),
        name="notebook_delete",
    ),
    path(
        "notebook/<int:pk>/update",
        NotebookUpdateView.as_view(),
        name="notebook_update",
    ),
    path(
        "notebook/<int:pk>/details",
        NotebookDetailView.as_view(),
        name="notebook_details",
    ),
    path(
        "notebook/<int:pk>/history",
        NotebookHistoryView.as_view(),
        name="notebook_history",
    ),
    path(
        "notebook/<int:pk>/notebook_fieldss/list",
        NotebookNotebookFieldssListView.as_view(),
        name="notebook_notebook_fieldss_list",
    ),
    path(
        "notebook/<int:pk>/notebook_fields/create",
        NotebookNotebookFieldsCreateView.as_view(),
        name="notebook_notebook_fields_create",
    ),
    path(
        "notebook/<int:pk>/notebook_datas/list",
        NotebookNotebookDatasListView.as_view(),
        name="notebook_notebook_datas_list",
    ),
    path(
        "notebook/<int:pk>/notebook_data/create",
        NotebookNotebookDataCreateView.as_view(),
        name="notebook_notebook_data_create",
    ),
]
