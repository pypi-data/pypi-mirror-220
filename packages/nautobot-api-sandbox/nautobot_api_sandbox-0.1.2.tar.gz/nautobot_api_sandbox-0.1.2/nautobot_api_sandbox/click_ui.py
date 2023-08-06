import logging
import click
from pynautobot.core.query import RequestError
from nautobot_api_sandbox.nauto_demo_functions import (
    DemoNautobotClient,
    TenantNotFoundError,
    SiteNotFoundError,
)


@click.group()
@click.pass_context
def cli(ctx):
    api_token = click.prompt("Please enter your API token. HINT-check readme...", type=str)
    try:
        ctx.obj = DemoNautobotClient(api_token=api_token)
        ctx.obj.api.dcim.sites.all()  # Make a simple request to check if the token is valid
    except RequestError:
        logging.error("Invalid API token. Please try again.")
        ctx.exit()


@cli.command()
@click.pass_context
def show_sites(ctx):
    ctx.obj.display_sites()


@cli.command()
@click.argument("site_name")
@click.pass_context
def show_devices(ctx, site_name):
    try:
        ctx.obj.display_devices(site_name)
    except SiteNotFoundError:
        logging.error("Site %s not found. Please enter a valid site name.", site_name)


@cli.command()
@click.argument("tenant_name")
@click.pass_context
def create_tenant(ctx, tenant_name):
    tenant = ctx.obj.create_tenant(tenant_name)
    if tenant is None:
        logging.error("A tenant with the name '%s' already exists.", tenant_name)
    else:
        logging.info("Tenant '%s' created successfully.", tenant_name)


@click.command()
@click.argument("tenant_name")
@click.pass_context
def delete_tenant(ctx, tenant_name):
    try:
        result = ctx.obj.delete_tenant(tenant_name)
        if result is not None:  # if result is None, it means an error has occurred
            success, message = result
            if success:
                logging.info(message)
            else:
                logging.error(message)
    except TenantNotFoundError as e:
        logging.error(str(e))


cli.add_command(delete_tenant)


@cli.command()
@click.pass_context
def show_tenants(ctx):
    ctx.obj.display_tenants()


@cli.command()
@click.argument("tenant_name")
@click.pass_context
def get_tenant(ctx, tenant_name):
    try:
        tenant = ctx.obj.get_tenant(tenant_name)
        if tenant is not None:
            logging.info("Tenant ID: %s\nTenant Name: %s", tenant.id, tenant.name)
    except TenantNotFoundError:
        logging.error("Tenant '%s' not found. Please enter a valid tenant name.", tenant_name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cli(obj={})  # Pass an empty context object
