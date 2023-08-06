from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import RecordServiceConfig
from invenio_records_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_records_resources.services import pagination_links

from nr_metadata.theses.records.api import ThesesRecord
from nr_metadata.theses.services.records.permissions import ThesesPermissionPolicy
from nr_metadata.theses.services.records.schema import NRThesesRecordSchema
from nr_metadata.theses.services.records.search import ThesesSearchOptions


class ThesesServiceConfig(RecordServiceConfig):
    """ThesesRecord service config."""

    url_prefix = "/nr-metadata.theses/"

    permission_policy_cls = ThesesPermissionPolicy

    schema = NRThesesRecordSchema

    search = ThesesSearchOptions

    record_cls = ThesesRecord
    # todo should i leave this here?
    service_id = "theses"

    components = [*RecordServiceConfig.components]

    model = "theses"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{self.url_prefix}{id}"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")
