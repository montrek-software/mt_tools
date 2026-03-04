import factory

from baseclasses.tests.factories.baseclass_factories import ValueDateListFactory
from baseclasses.tests.factories.montrek_factory_schemas import (
    MontrekHubValueDateFactory,
    MontrekHubFactory,
)
from mt_tools.notebook.models.notebook_data_hub_models import NotebookDataHub
from mt_tools.notebook.models.notebook_data_hub_models import NotebookDataHubValueDate


class NotebookDataHubFactory(MontrekHubFactory):
    class Meta:
        model = NotebookDataHub


class NotebookDataHubValueDateFactory(MontrekHubValueDateFactory):
    class Meta:
      model = NotebookDataHubValueDate

    hub = factory.SubFactory(NotebookDataHubFactory)
    value_date_list = factory.SubFactory(ValueDateListFactory)