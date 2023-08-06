import importlib_metadata
from flask_resources import ResponseHandler
from invenio_records_resources.resources import RecordResourceConfig

from nr_metadata.theses.resources.records.ui import ThesesUIJSONSerializer


class ThesesResourceConfig(RecordResourceConfig):
    """ThesesRecord resource config."""

    blueprint_name = "Theses"
    url_prefix = "/nr-metadata.theses/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.nr_metadata.theses.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                ThesesUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }
