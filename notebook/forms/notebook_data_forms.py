from baseclasses.forms import MontrekCreateForm
from mt_tools.notebook.repositories.notebook_repositories import NotebookRepository


class NotebookDataCreateForm(MontrekCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # notebook = NotebookRepository(self.session_data).receive().get(pk=initial)
        # fields = notebook.field_name
        # breakpoint()
        self.add_link_choice_field(
            display_field="notebook_name",
            link_name="link_notebook_data_notebook",
            queryset=NotebookRepository({}).receive(),
        )
