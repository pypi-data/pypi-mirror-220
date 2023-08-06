# Nautobot API Sandbox

This is a simple program to test my programming knowledge and learn more about API, Nautobot, and developing in general.

https://demo.nautobot.com/

## Getting Started

1. Install package: `pip install nautobot_api_sandbox`
2. Run package: `nautobot_api_sandbox`
3. Enter Demo token: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`

   This will start the Nautobot API Sandbox command-line interface.
   Follow the instructions in the application to interact with the Nautobot API.
   NOTE: You don't need to add '()' or "" quotes. Simply type the command + the name (e.g., create_tenant tpayne, show_devices atl01).


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
5. Run the program: `nautobot_api_sandbox`

To run the tests: `poetry run pytest`

Any help or tips would be greatly appreciated!!

## Currently Working On / Want to Add

- [ ] Exception handling?
- [ ] Valid unittest? Need more tests...
- [ ] Integrate click? really want to rework UI
- [ ] Make sure using logging correctly
- [x] Fix delete_tenant RequestError 409
- [x] Update readme instructions
- [x] Poetry integration
- [x] Publish package


This is a work in progress!!!

