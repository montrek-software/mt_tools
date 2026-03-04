import factory

from baseclasses.tests.factories.baseclass_factories import ValueDateListFactory
from baseclasses.tests.factories.montrek_factory_schemas import (
    MontrekHubValueDateFactory,
    MontrekHubFactory,
)
from mt_tools.notebook.models.notebook_fields_hub_models import NotebookFieldsHub
from mt_tools.notebook.models.notebook_fields_hub_models import NotebookFieldsHubValueDate


class NotebookFieldsHubFactory(MontrekHubFactory):
    class Meta:
        model = NotebookFieldsHub


class NotebookFieldsHubValueDateFactory(MontrekHubValueDateFactory):
    class Meta:
      model = NotebookFieldsHubValueDate

    hub = factory.SubFactory(NotebookFieldsHubFactory)
    value_date_list = factory.SubFactory(ValueDateListFactory)