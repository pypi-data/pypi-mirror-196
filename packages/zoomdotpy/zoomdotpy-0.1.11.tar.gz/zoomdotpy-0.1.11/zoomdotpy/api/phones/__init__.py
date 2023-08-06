from .sites import SitesAPI
from .site_settings import SiteSettingsAPI

from .devices import DevicesAPI
from .auto_receptionists import AutoReceptionistsAPI
from .emergency_addresses import EmergencyAddressesAPI
from .call_queues import CallQueuesAPI

from zoomdotpy.api.base import _BaseAPI

class PhonesAPI(_BaseAPI):
    devices: DevicesAPI

    sites: SitesAPI
    site_settings: SiteSettingsAPI

    auto_receptionists: AutoReceptionistsAPI
    emergency_addresses: EmergencyAddressesAPI
    call_queues: CallQueuesAPI

    def __post_init__(self):        
        self.call_queues    = CallQueuesAPI(self._s)
        self.devices        = DevicesAPI(self._s)
        
        self.sites          = SitesAPI(self._s)
        self.site_settings  = SiteSettingsAPI(self._s)

        self.auto_receptionists     = AutoReceptionistsAPI(self._s)
        self.emergency_addresses    = EmergencyAddressesAPI(self._s)