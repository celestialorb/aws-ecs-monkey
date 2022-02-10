import configargparse

from loguru import logger

import nodes
import services
import tasks

# Read in the configuration.
p = configargparse.get_argument_parser()
p.add("-c", "--config-file", required=False, is_config_file=True)
p.add("--cluster-name", env_var="AWS_ECS_MONKEY_CLUSTER_NAME")
p.add("--action-type", env_var="AWS_ECS_MONKEY_ACTION_TYPE")
p.add("--action-dry-run", env_var="AWS_ECS_MONKEY_ACTION_DRY_RUN", action="store_true")

config = p.parse_args()
logger.info(config)

if config.action_type == "nodes":
    nodes.terminate(aws_ecs_cluster_name=config.cluster_name,
                    dry_run=config.action_dry_run)
if config.action_type == "services":
    services.roll(aws_ecs_cluster_name=config.cluster_name,
                  dry_run=config.action_dry_run)
if config.action_type == "tasks":
    tasks.stop(aws_ecs_cluster_name=config.cluster_name,
               dry_run=config.action_dry_run)
