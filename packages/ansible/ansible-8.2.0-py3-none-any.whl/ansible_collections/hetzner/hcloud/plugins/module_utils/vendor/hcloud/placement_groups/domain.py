try:
    from dateutil.parser import isoparse
except ImportError:
    isoparse = None

from ..core.domain import BaseDomain


class PlacementGroup(BaseDomain):
    """Placement Group Domain

    :param id: int
           ID of the Placement Group
    :param name: str
           Name of the Placement Group
    :param labels: dict
           User-defined labels (key-value pairs)
    :param servers: List[ int ]
           List of server IDs assigned to the Placement Group
    :param type: str
           Type of the Placement Group
    :param created: datetime
           Point in time when the image was created
    """

    __slots__ = ("id", "name", "labels", "servers", "type", "created")

    """Placement Group type spread
       spreads all servers in the group on different vhosts
    """
    TYPE_SPREAD = "spread"

    def __init__(
        self, id=None, name=None, labels=None, servers=None, type=None, created=None
    ):
        self.id = id
        self.name = name
        self.labels = labels
        self.servers = servers
        self.type = type
        self.created = isoparse(created) if created else None


class CreatePlacementGroupResponse(BaseDomain):
    """Create Placement Group Response Domain

    :param placement_group: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>`
           The Placement Group which was created
    :param action: :class:`BoundAction <hcloud.actions.client.BoundAction>`
           The Action which shows the progress of the Placement Group Creation
    """

    __slots__ = ("placement_group", "action")

    def __init__(
        self,
        placement_group,  # type: BoundPlacementGroup
        action,  # type: BoundAction
    ):
        self.placement_group = placement_group
        self.action = action
