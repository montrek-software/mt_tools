import factory
from baseclasses.tests.factories.montrek_factory_schemas import (
    MontrekSatelliteFactory,
    )

from mt_tools.notebook.tests.factories.notebook_data_hub_factories import NotebookDataHubFactory
from mt_tools.notebook.models.notebook_data_sat_models import NotebookDataSatellite


class NotebookDataSatelliteFactory(MontrekSatelliteFactory):
    class Meta:
        model = NotebookDataSatellite

    hub_entity = factory.SubFactory(NotebookDataHubFactory)
