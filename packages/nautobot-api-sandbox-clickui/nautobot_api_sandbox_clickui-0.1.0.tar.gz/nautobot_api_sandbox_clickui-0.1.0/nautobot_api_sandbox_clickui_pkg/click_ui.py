import logging
import click
import pynautobot

from pynautobot.core.query import RequestError
from nautobot_api_sandbox_ui import (
    INVALID_SITE_MSG,
    INVALID_TENANT_MSG,
    TOKEN_ERROR_MSG,
    COMMAND_ARG_ERROR_MSG,
    TENANT_CREATED_SUCCESS_MSG,
    TENANT_EXISTS_ERROR_MSG,
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
        logging.error(TOKEN_ERROR_MSG)
        ctx.exit()


@cli.command()
@click.pass_context
def show_sites(ctx):
    ctx.obj.display_sites()


@click.command()
@click.argument("site_name")
@click.pass_context
def show_devices(ctx, site_name):
    # Capitalize if the site_name is less than 5 characters
    if len(site_name) <= 5:
        site_name = site_name.upper()
    # Convert to title case if the site_name is more than one word
    elif " " in site_name:
        site_name = site_name.title()

    try:
        ctx.obj.display_devices(site_name)
    except SiteNotFoundError:
        logging.error(INVALID_SITE_MSG, site_name)


cli.add_command(show_devices)


@cli.command()
@click.argument("tenant_name")
@click.pass_context
def create_tenant(ctx, tenant_name):
    tenant = ctx.obj.create_tenant(tenant_name)
    if tenant is None:
        logging.error(TENANT_EXISTS_ERROR_MSG, tenant_name)
    else:
        logging.info(TENANT_CREATED_SUCCESS_MSG, tenant_name)


@cli.command()
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
        logging.error(INVALID_TENANT_MSG, tenant_name)


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
        logging.error(INVALID_TENANT_MSG, tenant_name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cli(obj={})  # Pass an empty context object
