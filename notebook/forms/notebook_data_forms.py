from baseclasses.forms import MontrekCreateForm
from mt_tools.notebook.repositories.notebook_repositories import NotebookRepository


class NotebookDataCreateForm(MontrekCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_link_choice_field(
            display_field="notebook_name",
            link_name="link_notebook_data_notebook",
            queryset=NotebookRepository({}).receive(),
        )
