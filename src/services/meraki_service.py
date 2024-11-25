import asyncio
import meraki.aio

class MerakiService:
    def __init__(self):
        self.dashboard = None
        self.async_dashboard = None
        self.organization_id = None

    async def set_api_key(self, api_key):
        self.async_dashboard = meraki.aio.AsyncDashboardAPI(
            api_key,
            output_log=False,
            print_console=False
        )
        # Get first organization ID
        organizations = await self.async_dashboard.organizations.getOrganizations()
        if organizations:
            self.organization_id = organizations[0]['id']

    async def get_networks(self):
        if not self.async_dashboard or not self.organization_id:
            return []
        try:
            return await self.async_dashboard.organizations.getOrganizationNetworks(
                self.organization_id
            )
        except:
            return []

    async def get_devices_async(self, network_id):
        if not self.async_dashboard:
            return []
        try:
            return await self.async_dashboard.networks.getNetworkDevices(network_id)
        except:
            return []

    async def get_clients_async(self, network_id, timespan=2592000):
        if not self.async_dashboard:
            return []
        try:
            return await self.async_dashboard.networks.getNetworkClients(
                network_id,
                timespan=timespan,
                perPage=1000,
                total_pages='all'
            )
        except:
            return [] 