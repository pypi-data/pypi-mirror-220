import subprocess
import traceback

from e2e_cli.auto_scaling.autoscaling_routing import AutoscalingRouting
from e2e_cli.bucket_store.bucket_routing import BucketRouting
from e2e_cli.cdn.cdn_routing import CdnRouting
from e2e_cli.config.config_routing import ConfigRouting
from e2e_cli.core import show_messages, constants
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.dbaas.dbaas_routing import DBaaSRouting
from e2e_cli.image.image_routing import ImageRouting
from e2e_cli.loadbalancer.lb_routing import LBRouting
from e2e_cli.logs.logs_routing import LogRouting
from e2e_cli.man_display import man_page
from e2e_cli.node.node_routing import NodeRouting
from e2e_cli.security_groups.security_group_routing import SecurityGroupRouting
from e2e_cli.volumes.volumes_routing import VolumesRouting
from e2e_cli.vpc.vpc_routing import VpcRouting


class CommandsRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, parsing_errors):

        if (self.arguments.args.version):
            show_messages.e2e_version_info()

        elif (self.arguments.args.info):
            show_messages.e2e_pakage_info()

        elif self.arguments.args.command is None:
            show_messages.show_parsing_error(parsing_errors)
            subprocess.call([constants.E2E_CLI, constants._HELP])

        elif self.arguments.args.command == "help":
            man_page()

        elif (self.arguments.args.command == constants.CONFIG):

            if self.arguments.args.config_commands in ["add", "view", "add_file", "delete", "set"]:
                try:
                    ConfigRouting(self.arguments).route(parsing_errors)
                except Exception as e:
                    if ("debug" in self.arguments.inputs):
                        trace = traceback.format_exc()
                        Checks.manage_exception(e, self.arguments, trace)
            else:
                show_messages.show_parsing_error(parsing_errors)
                subprocess.call([constants.E2E_CLI, constants.CONFIG, constants._HELP])

        else:
            print(f"Using alias : {self.arguments.args.alias}")
            route_set = {constants.NODE: NodeRouting,
                         constants.LB: LBRouting,
                         constants.BUCKET: BucketRouting,
                         constants.DBAAS: DBaaSRouting,
                         constants.IMAGE: ImageRouting,
                         constants.AUTOSCALING: AutoscalingRouting,
                         constants.CDN: CdnRouting,
                         constants.VPC: VpcRouting,
                         constants.VOLUME: VolumesRouting,
                         constants.SECURITY_GROUPS: SecurityGroupRouting,
                         constants.LOGS: LogRouting
                         }
            service_route = route_set.get(self.arguments.args.command)

            if service_route:
                try:
                    service_route(self.arguments).route(parsing_errors)
                except Exception as e:
                    if ("debug" in self.arguments.inputs):
                        trace = traceback.format_exc()
                        Checks.manage_exception(e, self.arguments, trace)

            else:
                print("Command not found!! for more help type e2e_cli help")
                show_messages.show_parsing_error(parsing_errors)
