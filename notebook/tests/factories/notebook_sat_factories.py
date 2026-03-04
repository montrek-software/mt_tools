import factory
from baseclasses.tests.factories.montrek_factory_schemas import (
    MontrekSatelliteFactory,
)

from mt_tools.notebook.tests.factories.notebook_hub_factories import NotebookHubFactory
from mt_tools.notebook.models.notebook_sat_models import NotebookSatellite


class NotebookSatelliteFactory(MontrekSatelliteFactory):
    class Meta:
        model = NotebookSatellite

    hub_entity = factory.SubFactory(NotebookHubFactory)
