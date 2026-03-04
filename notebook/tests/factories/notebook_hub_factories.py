import factory

from baseclasses.tests.factories.baseclass_factories import ValueDateListFactory
from baseclasses.tests.factories.montrek_factory_schemas import (
    MontrekHubValueDateFactory,
    MontrekHubFactory,
)
from mt_tools.notebook.models.notebook_hub_models import NotebookHub
from mt_tools.notebook.models.notebook_hub_models import NotebookHubValueDate


class NotebookHubFactory(MontrekHubFactory):
    class Meta:
        model = NotebookHub


class NotebookHubValueDateFactory(MontrekHubValueDateFactory):
    class Meta:
        model = NotebookHubValueDate

    hub = factory.SubFactory(NotebookHubFactory)
    value_date_list = factory.SubFactory(ValueDateListFactory)
