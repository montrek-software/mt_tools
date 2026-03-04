import factory
from baseclasses.tests.factories.montrek_factory_schemas import (
    MontrekSatelliteFactory,
    )

from mt_tools.notebook.tests.factories.notebook_fields_hub_factories import NotebookFieldsHubFactory
from mt_tools.notebook.models.notebook_fields_sat_models import NotebookFieldsSatellite


class NotebookFieldsSatelliteFactory(MontrekSatelliteFactory):
    class Meta:
        model = NotebookFieldsSatellite

    hub_entity = factory.SubFactory(NotebookFieldsHubFactory)
