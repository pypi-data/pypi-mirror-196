from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import AnyUser, SystemProcess


class ThesesPermissionPolicy(RecordPermissionPolicy):
    """nr_metadata.theses.records.api.ThesesRecord permissions."""

    can_search = [SystemProcess(), AnyUser()]
    can_read = [SystemProcess(), AnyUser()]
    can_create = [SystemProcess()]
    can_update = [SystemProcess()]
    can_delete = [SystemProcess()]
    can_manage = [SystemProcess()]
