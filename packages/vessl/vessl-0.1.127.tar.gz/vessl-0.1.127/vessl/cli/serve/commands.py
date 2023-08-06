import sys
from typing import Optional, TextIO

import click
import yaml

from openapi_client import ResponseModelServiceInfo
from vessl import vessl_api
from vessl.cli._base import VesslGroup
from vessl.serving import (
    create_revision_from_yaml,
    read_gateway,
    update_gateway_for_revision,
    update_gateway_from_yaml,
)
from vessl.util.exception import VesslApiException

from .util import list_http_ports, print_gateway, print_revision, validate_port_choice

cli = VesslGroup("serve")


def serving_name_callback(
    ctx: click.Context, param: click.Parameter, serving_name: Optional[str]
) -> str:
    if vessl_api.organization is None:
        vessl_api.set_organization()

    try:
        serving: ResponseModelServiceInfo = vessl_api.model_service_read_api(
            serving_name, vessl_api.organization.name
        )
    except VesslApiException as e:
        print(f"Invalid serving {serving_name}: {e.message}")
        sys.exit(1)

    ctx.meta["serving"] = serving


serving_name_option = click.option(
    "--serving",
    "serving_name",
    type=click.STRING,
    required=True,
    callback=serving_name_callback,
    expose_value=False,
    help="Name of serving.",
)

update_gateway_option = click.option(
    "--update-gateway/--no-update-gateway",
    "-g/-G",
    is_flag=True,
    default=False,
    help="Whether to update gateway so that it points to this revision.",
)

enable_gateway_if_off_option = click.option(
    "--enable-gateway-if-off/--no-enable-gateway-if-off",
    "-e/-E",
    is_flag=True,
    default=False,
    help="When updating gateway, whether to enable the gateway if it is currently off.",
)

update_gateway_weight_option = click.option(
    "--update-gateway-weight",
    type=click.INT,
    required=False,
    help=(
        "When updating gateway, the amount of traffic that should be "
        "directed to this revision (in percentage)."
    ),
)

update_gateway_port_option = click.option(
    "--update-gateway-port",
    type=click.INT,
    required=False,
    help=(
        "When updating gateway, the port to receive the traffic; "
        "this port must be defined in serving spec."
    ),
)


@cli.vessl_command(name="revision")
@click.pass_context
@serving_name_option
@click.option(
    "-f",
    "--file",
    type=click.File("r"),
    required=True,
    help="Path to YAML file for serving revision definition.",
)
@update_gateway_option
@enable_gateway_if_off_option
@update_gateway_weight_option
@update_gateway_port_option
def import_revision(
    ctx: click.Context,
    file: TextIO,
    update_gateway: bool,
    enable_gateway_if_off: bool,
    update_gateway_weight: Optional[int] = None,
    update_gateway_port: Optional[int] = None,
):
    if not update_gateway and (
        update_gateway_weight is not None or update_gateway_port is not None
    ):
        print("Cannot specify traffic weight or port when not updating gateway.")
        sys.exit(1)

    serving: ResponseModelServiceInfo = ctx.meta["serving"]

    yaml_body = file.read()
    yaml_obj = yaml.safe_load(yaml_body)

    if update_gateway:
        # Do as much validation as possible before actually creating revision.
        # weight check
        if update_gateway_weight is None:
            update_gateway_weight = 100
        elif not 1 <= update_gateway_weight <= 100:
            print(f"Invalid weight: {update_gateway_weight}% (must be between 1 and 100)")
            sys.exit(1)

        # port check
        if update_gateway_port is None:
            http_ports = list_http_ports(yaml_obj)
            if len(http_ports) != 1:
                print(
                    "Error: port for gateway was not specified, and could not automatically "
                    "determine which port to use.\n"
                    f"{len(http_ports)} port(s) was found: " + ", ".join(map(str, http_ports))
                )
                sys.exit(1)
            update_gateway_port = http_ports[0]
            print(f"Automatically choosing port {update_gateway_port} for gateway.")
        elif not 1 <= update_gateway_port <= 65535:
            print(f"Invalid port: {update_gateway_port}")
            sys.exit(1)
        else:
            validate_port_choice(yaml_obj, update_gateway_port)

        # gateway status check
        if not enable_gateway_if_off:
            gateway_current = read_gateway(
                organization=vessl_api.organization.name, serving_name=serving.name
            )
            if not gateway_current.enabled:
                print("Cannot update gateway because it is not enabled. Please enable it first.")
                print("NOTE (current status of gateway):")
                print_gateway(gateway_current)
                sys.exit(1)

    revision = create_revision_from_yaml(
        organization=vessl_api.organization.name, serving_name=serving.name, yaml_body=yaml_body
    )
    print(f"Successfully created revision in serving {serving.name}.\n")
    print_revision(revision)

    if update_gateway:
        gateway_updated = update_gateway_for_revision(
            vessl_api.organization.name,
            serving_name=serving.name,
            revision_number=revision.number,
            port=update_gateway_port,
            weight=update_gateway_weight,
        )
        print(f"Successfully updated gateway for revision #{revision.number}.\n")
        print_gateway(gateway_updated)
    else:
        print(
            "NOTE: Since --update-gateway option was not given, "
            "you cannot currently access this revision via gateway.\n\n"
            "Either use --update-gateway when creating revision, or update gateway manually."
        )


@cli.vessl_command(name="gateway")
@click.pass_context
@serving_name_option
@click.option(
    "-f",
    "--file",
    type=click.File("r"),
    required=True,
    help="Path to YAML file for serving revision definition.",
)
def import_gateway(ctx: click.Context, file: TextIO):
    serving: ResponseModelServiceInfo = ctx.meta["serving"]
    yaml_body = file.read()

    gateway = update_gateway_from_yaml(
        organization=vessl_api.organization.name, serving_name=serving.name, yaml_body=yaml_body
    )
    print(f"Successfully update gateway of serving {serving.name}.\n")
    print_gateway(gateway)
