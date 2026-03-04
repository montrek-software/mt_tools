from django.shortcuts import redirect
from django.urls import path
from mt_tools.notebook.views.notebook_views import NotebookListView
from mt_tools.notebook.views.notebook_views import NotebookCreateView
from mt_tools.notebook.views.notebook_views import NotebookUpdateView
from mt_tools.notebook.views.notebook_views import NotebookDeleteView
from mt_tools.notebook.views.notebook_views import NotebookDetailView
from mt_tools.notebook.views.notebook_views import NotebookHistoryView

urlpatterns = [
    path(
        "notebook",
        lambda _: redirect("notebook_list"),
        name="notebook"
    ),
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
]