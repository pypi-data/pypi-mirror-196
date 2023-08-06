from invenio_db import db
from invenio_records.models import RecordMetadataBase


class ThesesMetadata(db.Model, RecordMetadataBase):
    """Model for ThesesRecord metadata."""

    __tablename__ = "theses_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
