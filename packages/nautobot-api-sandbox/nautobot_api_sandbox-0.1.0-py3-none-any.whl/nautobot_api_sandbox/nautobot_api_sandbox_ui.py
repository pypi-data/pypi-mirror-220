"""This is the command line interface for the Nautobot API Sandbox."""

import logging
from pynautobot.core.query import RequestError
from nautobot_api_sandbox.nauto_demo_functions import (
    DemoNautobotClient,
    TenantNotFoundError,
    SiteNotFoundError,
)

WELCOME_MSG = """
Welcome to tPayne's nautobot demo API sandbox!
********************************************************************************
Here is a list of available commands:
show_sites.............................Get list of all sites
show_devices [SITE NAME]...............Get count of devices and list device names
create_tenant [TENANT NAME]............Create a new tenant with specified name
get_tenant [TENANT NAME]...............Get specified tenant
delete_tenant [TENANT NAME]............Delete specified tenant
show_tenants...........................Get count and list all tenant names
help...................................Reprint this window
********************************************************************************
"""


def user_interface():
    # Set up logging
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())  # Outputs log messages to the console
    logger.setLevel(logging.INFO)  # Set the desired log level

    # Ask for API token
    while True:
        api_token = input(
            "Please enter your API token. HINT-check readme...(or type 'exit' to quit): "
        )
        if api_token.lower() == "exit":
            return
        try:
            nautobot_client = DemoNautobotClient(api_token=api_token)
            nautobot_client.api.dcim.sites.all()  # Make a simple request to check if the token is valid
            break
        except RequestError:
            logger.error("Invalid API token. Please try again.")

    print(WELCOME_MSG)

    # Commands that need an argument
    commands_with_arg = ["show_devices", "create_tenant", "delete_tenant", "get_tenant"]

    while True:
        command_input = input("Enter a command: ").split()
        command = command_input[0].lower()  # Convert command to lowercase
        arg = " ".join(command_input[1:])  # Join all items after the command with a space

        if command == "create_tenant" or command == "delete_tenant":
            tenant_name = arg  # Store the tenant name without modifying capitalization
        else:
            # Process the argument based on its length
            if len(arg) <= 5:
                arg = arg.upper()  # Convert to uppercase if length is 5 or less
            else:
                arg = arg.title()  # Convert to title case if more than one word

        # Check if the command needs an argument and if it was provided
        if command in commands_with_arg and not arg:
            logger.error("The %s command requires an argument.", command)
            continue

        if command == "show_sites":
            nautobot_client.display_sites()
        elif command == "show_devices":
            try:
                nautobot_client.display_devices(arg)
            except SiteNotFoundError:
                logger.error("Site %s not found. Please enter a valid site name.", arg)
        elif command == "create_tenant":
            tenant = nautobot_client.create_tenant(tenant_name)
            if tenant is None:
                logger.error("A tenant with the name '%s' already exists.", tenant_name)
            else:
                logger.info("Tenant '%s' created successfully.", tenant_name)
        elif command == "delete_tenant":
            try:
                nautobot_client.delete_tenant(arg)
            except TenantNotFoundError:
                logger.error("Tenant '%s' not found. Please enter a valid tenant name.", arg)
        elif command == "show_tenants":
            nautobot_client.display_tenants()
        elif command == "get_tenant":
            try:
                tenant = nautobot_client.get_tenant(arg)
                if tenant is not None:
                    logger.info("Tenant ID: %s\nTenant Name: %s", tenant.id, tenant.name)
            except TenantNotFoundError:
                logger.error("Tenant '%s' not found. Please enter a valid tenant name.", arg)
        elif command == "help":
            print(WELCOME_MSG)
        elif command == "exit":
            break
        else:
            logger.error("Unrecognized command. Type 'help' to see the list of available commands.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    user_interface()
