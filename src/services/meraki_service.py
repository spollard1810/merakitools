import meraki

class MerakiService:
    def __init__(self):
        self.dashboard = None
        self.organization_id = None

    def set_api_key(self, api_key):
        self.dashboard = meraki.DashboardAPI(
            api_key,
            output_log=False,
            print_console=False
        )
        # Get first organization ID
        organizations = self.dashboard.organizations.getOrganizations()
        if organizations:
            self.organization_id = organizations[0]['id']

    def get_networks(self):
        if not self.dashboard or not self.organization_id:
            return []
        try:
            return self.dashboard.organizations.getOrganizationNetworks(
                self.organization_id
            )
        except:
            return []

    def get_devices(self, network_id):
        if not self.dashboard:
            return []
        try:
            return self.dashboard.networks.getNetworkDevices(network_id)
        except:
            return []

    def get_clients(self, network_id, timespan=2592000):  # Default to 30 days
        if not self.dashboard:
            return []
        try:
            return self.dashboard.networks.getNetworkClients(
                network_id,
                timespan=timespan,
                perPage=1000,  # Adjust as needed
                total_pages='all'
            )
        except:
            return [] 