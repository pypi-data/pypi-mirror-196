from .sites import SitesAPI
from .devices import DevicesAPI
from .auto_receptionists import AutoReceptionistsAPI
from .emergency_addresses import EmergencyAddressesAPI

from zoomdotpy.api.base import _BaseAPI

class PhonesAPI(_BaseAPI):
    devices: DevicesAPI
    sites: SitesAPI
    auto_receptionists: AutoReceptionistsAPI
    emergency_addresses: EmergencyAddressesAPI

    def __post_init__(self):
        self.devices    = DevicesAPI(self._s)
        self.sites      = SitesAPI(self._s)
        self.auto_receptionists     = AutoReceptionistsAPI(self._s)
        self.emergency_addresses    = EmergencyAddressesAPI(self._s)