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

    @factory.post_generation
    def notebook(self, create, extracted, **kwargs):
        if not create:
            return
        if not extracted:
            return
        self.hub_entity.link_notebook_fields_notebook.add(extracted.hub_entity)
