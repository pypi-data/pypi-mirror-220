from typing import List

from openapi_client import OrmModelServiceGatewayTrafficSplitEntry as TrafficSplitEntry
from openapi_client import ResponseModelServiceGatewayInfo, ResponseModelServiceRevision
from vessl.cli._util import print_data
from vessl.util.exception import InvalidYAMLError


def print_revision(revision: ResponseModelServiceRevision):
    print_data(
        {
            "Number": revision.number,
            "Status": revision.status,
            "Message": revision.message,
        }
    )


def print_gateway(gateway: ResponseModelServiceGatewayInfo):
    def _prettify_traffic_split_entry(entry: TrafficSplitEntry) -> str:
        """
        Returns a pretty representation of given traffic split entry.

        Examples:
        - "########   80%:   3 (port 8000)"
        - "##         20%:  12 (port 3333)"
        """
        gauge_char = "#"
        gauge_width = (entry.traffic_weight + 9) // 10  # round up (e.g. 31%-40% -> 4)
        gauge = gauge_char * gauge_width

        return (
            f"{gauge: <10} {entry.traffic_weight: <3}%: {entry.revision_number: >3} "
            f"(port {entry.port})"
        )

    print_data(
        {
            "Enabled": gateway.enabled,
            "Status": gateway.status,
            "Endpoint": gateway.endpoint or gateway.generated_hostname,
            "Ingress Class": gateway.ingress_class,
            "Annotations": gateway.annotations,
            "Traffic Targets": (
                list(map(_prettify_traffic_split_entry, gateway.rules))
                if gateway.rules
                else "Empty"
            ),
        }
    )


def list_http_ports(yaml_obj) -> List[int]:
    def _check_type(obj, type_: type):
        assert isinstance(obj, type_)
        return obj

    if "ports" not in yaml_obj:
        return []

    http_ports: List[int] = []
    try:
        ports: list = _check_type(yaml_obj["ports"], list)
        for port in ports:
            expose_type = _check_type(port["type"], str)
            if expose_type == "http":
                port_number = _check_type(port["port"], int)
                http_ports.append(port_number)
    except (KeyError, AssertionError) as e:
        raise InvalidYAMLError(message=str(e))

    return http_ports


def validate_port_choice(yaml_obj):
    pass
