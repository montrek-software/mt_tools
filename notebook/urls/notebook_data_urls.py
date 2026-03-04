from django.shortcuts import redirect
from django.urls import path
from mt_tools.notebook.views.notebook_data_views import NotebookDataListView
from mt_tools.notebook.views.notebook_data_views import NotebookDataCreateView
from mt_tools.notebook.views.notebook_data_views import NotebookDataUpdateView
from mt_tools.notebook.views.notebook_data_views import NotebookDataDeleteView
from mt_tools.notebook.views.notebook_data_views import NotebookDataDetailView
from mt_tools.notebook.views.notebook_data_views import NotebookDataHistoryView

urlpatterns = [
    path(
        "notebook_data",
        lambda _: redirect("notebook_data_list"),
        name="notebook_data"
    ),
    path(
        "notebook_data/list",
        NotebookDataListView.as_view(),
        name="notebook_data_list",
    ),
    path(
        "notebook_data/create",
        NotebookDataCreateView.as_view(),
        name="notebook_data_create",
    ),
    path(
        "notebook_data/<int:pk>/delete",
        NotebookDataDeleteView.as_view(),
        name="notebook_data_delete",
    ),
    path(
        "notebook_data/<int:pk>/update",
        NotebookDataUpdateView.as_view(),
        name="notebook_data_update",
    ),
    path(
        "notebook_data/<int:pk>/details",
        NotebookDataDetailView.as_view(),
        name="notebook_data_details",
    ),
    path(
        "notebook_data/<int:pk>/history",
        NotebookDataHistoryView.as_view(),
        name="notebook_data_history",
    ),
]