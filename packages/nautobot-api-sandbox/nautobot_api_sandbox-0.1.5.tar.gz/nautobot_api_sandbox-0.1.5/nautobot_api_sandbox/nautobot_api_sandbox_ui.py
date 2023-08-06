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

INVALID_SITE_MSG = "Site %s not found. Please enter a valid site name."
INVALID_TENANT_MSG = "Tenant '%s' not found. Please enter a valid tenant name."
TOKEN_ERROR_MSG = "Invalid API token. Please try again."
COMMAND_ARG_ERROR_MSG = "The %s command requires an argument."
TENANT_EXISTS_ERROR_MSG = "A tenant with the name '%s' already exists."
TENANT_CREATED_SUCCESS_MSG = "Tenant '%s' created successfully."


def user_interface():
    # Set up logging
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())  # Outputs log messages to the console
    logger.setLevel(logging.INFO)  # Set the desired log level
    logger.propagate = False  # Prevents the logger from passing messages to the root logger

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
            logger.error(TOKEN_ERROR_MSG)

    logger.info(WELCOME_MSG)  # Use logger.info instead of print

    # Commands that need an argument
    commands_with_arg = ["show_devices", "create_tenant", "delete_tenant", "get_tenant"]

    while True:
        command_input = input("Enter a command: ").split()
        command = command_input[0].lower()  # Convert command to lowercase
        arg = " ".join(command_input[1:])  # Join all items after the command with a space

        if command == "exit":
            break

        if command == "create_tenant" or command == "delete_tenant" or command == "get_tenant":
            tenant_name = arg  # Store the tenant name without modifying capitalization
        else:
            # Process the argument based on its length
            if len(arg) <= 5:
                arg = arg.upper()  # Convert to uppercase if length is 5 or less
            else:
                arg = arg.title()  # Convert to title case if more than one word

        # Check if the command needs an argument and if it was provided
        if command in commands_with_arg and not arg:
            logger.error(COMMAND_ARG_ERROR_MSG, command)
            continue

        if command == "show_sites":
            nautobot_client.display_sites()
        elif command == "show_devices":
            try:
                nautobot_client.display_devices(arg)
            except SiteNotFoundError:
                logger.error(INVALID_SITE_MSG, arg)
        elif command == "create_tenant":
            tenant = nautobot_client.create_tenant(tenant_name)
            if tenant is None:
                logger.error(TENANT_EXISTS_ERROR_MSG, tenant_name)
            else:
                logger.info(TENANT_CREATED_SUCCESS_MSG, tenant_name)
        elif command == "delete_tenant":
            try:
                success, message = nautobot_client.delete_tenant(arg)
                if success:
                    logger.info(message)
                else:
                    logger.error(message)
            except TenantNotFoundError:
                logger.error("Tenant with name '%s' not found.", arg)

        elif command == "show_tenants":
            nautobot_client.display_tenants()
        elif command == "get_tenant":
            try:
                nautobot_client.display_tenant(arg)
            except TenantNotFoundError:
                logger.error(INVALID_TENANT_MSG, arg)
        elif command == "help":
            logger.info(WELCOME_MSG)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    user_interface()
