# Nautobot API Sandbox

This is a simple program to test my programming knowledge and learn more about API, Nautobot, and developing in general.

https://demo.nautobot.com/

## Getting Started

1. Install package: `sudo pip install nautobot_api_sandbox`
2. Run package: `nautobot_api_sandbox`
3. Enter Demo token: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`

   This will start the Nautobot API Sandbox command-line interface.
   Follow the instructions in the application to interact with the Nautobot API.
   
   :memo: NOTE: You don't need to add '()' or "" quotes. Simply type the command + name (e.g., create_tenant tpayne, show_devices atl01).

   To update: `pip install --upgrade nautobot_api_sandbox`

## Development Prerequisites

Before getting started, make sure you have the following installed on your machine:

- Python 3.9 or later
- Poetry
## Development

1. Clone the repository: `git clone git@github.com:tPayne0647/nautobot-api-sandbox.git`
2. Navigate to the project directory: `cd nautobot-api-sandbox`
3. Install the project dependencies using Poetry: `poetry install`
4. Install the development dependencies: `poetry install --dev`
4. Activate the virtual environment created by Poetry: `poetry shell`
5. Run the program: `python -m nautobot_api_sandbox.nautobot_api_sandbox_ui`

To run the tests: `poetry run pytest`

Any help or tips would be greatly appreciated!!

## CLick UI command examples 
must be in poetry enviroment
- python nautobot_api_sandbox/click_ui.py show-sites
- python nautobot_api_sandbox/click_ui.py show-devices SITE_NAME
- python nautobot_api_sandbox/click_ui.py create-tenant TENANT_NAME
- python nautobot_api_sandbox/click_ui.py delete-tenant TENANT_NAME
- python nautobot_api_sandbox/click_ui.py show-tenants
- python nautobot_api_sandbox/click_ui.py get-tenant TENANT_NAME
- python nautobot_api_sandbox/click_ui.py COMMAND --help

Remember to replace SITE_NAME or TENANT_NAME with the name of the site or tenant. You dont need to add quotation marks!

## Currently Working On / Want to Add

- [ ] Valid unittest? Need more tests...
- [ ] Make sure using logging correctly
- [x] Integrate click? really want to rework UI
- [x] Exception handling
- [x] Fix delete_tenant RequestError 409
- [x] Update readme instructions
- [x] Poetry integration
- [x] Publish package


This is a work in progress!!!

