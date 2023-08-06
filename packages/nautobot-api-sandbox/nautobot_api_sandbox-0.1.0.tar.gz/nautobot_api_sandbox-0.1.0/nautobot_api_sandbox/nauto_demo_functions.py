"""Functions module"""

import logging
import pynautobot
from pynautobot.core.query import RequestError


class TenantNotFoundError(Exception):
    """Exception raised when a tenant is not found."""


class SiteNotFoundError(Exception):
    """Exception raised when a site is not found."""


class DemoNautobotClient:
    """A client for interacting with Nautobot."""

    def __init__(self, api_token, api=None):
        """Initialize the client with an API token and an optional pynautobot API object."""
        if api is None:
            self.api = pynautobot.api("https://demo.nautobot.com", token=api_token)
        else:
            self.api = api

        self.logger = logging.getLogger(__name__)
        if not self.logger.hasHandlers():
            self.logger.addHandler(logging.StreamHandler())  # Outputs log messages to the console
            self.logger.setLevel(logging.INFO)  # Set the desired log level

    def get_sites(self):
        """Return a list of all sites."""
        return self.api.dcim.sites.all()

    def display_sites(self):
        """Display the names of all sites."""
        sites = self.get_sites()
        self.logger.info("\nTotal sites: %s\n \n%s", len(sites), [site.name for site in sites])

    def get_devices(self, selected_site_name):
        """Return a list of all devices at the specified site, or raise SiteNotFoundError if the site does not exist."""
        try:
            # First, get the site by name
            site = self.api.dcim.sites.get(name=selected_site_name)
            if site is None:
                raise SiteNotFoundError("Site '%s' not found." % selected_site_name)
            # Then, get the devices for the site using the slug
            devices = self.api.dcim.devices.filter(site=site.slug)
        except RequestError as request_error:
            raise request_error
        return devices

    def display_devices(self, selected_site):
        """Display the names of all devices at the specified site."""
        try:
            devices = self.get_devices(selected_site)
            self.logger.info(
                "\nTotal number of devices in [%s]: %s\n\n%s",
                selected_site,
                len(devices),
                [device.name for device in devices],
            )
        except SiteNotFoundError:
            self.logger.error("Site %s not found. Please enter a valid site name.", selected_site)

    def create_tenant(self, name):
        """Create a new tenant with the specified name and return it."""
        try:
            tenant = self.api.tenancy.tenants.create(name=name)
        except RequestError as request_error:
            if "already exists" in str(request_error):
                return None
            else:
                # If the error is something else, we re-raise the exception
                raise
        return tenant

    def get_tenant(self, name):
        """Return the tenant with the specified name, or raise TenantNotFoundError if the tenant does not exist."""
        tenant = self.api.tenancy.tenants.get(name=name)
        if tenant is None:
            raise TenantNotFoundError("Tenant with name '%s' not found.", name)
        return tenant

    def delete_tenant(self, name):
        """Delete the tenant with the specified name."""
        tenant = self.get_tenant(name)
        if tenant is not None:
            tenant.delete()
            self.logger.info("Tenant '%s' deleted successfully!", name)
        else:
            raise TenantNotFoundError("Tenant with name '%s' not found.", name)

    def get_tenants(self):
        """Return a list of all tenants."""
        return self.api.tenancy.tenants.all()

    def display_tenants(self):
        """Display the names of all tenants."""
        tenants = self.get_tenants()
        self.logger.info(
            "\nTotal tenants: %s\n \n%s",
            len(tenants),
            [tenant.name for tenant in tenants],
        )
