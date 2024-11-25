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