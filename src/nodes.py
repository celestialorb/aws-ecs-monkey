import boto3
import configargparse
import random

from loguru import logger


PARSER = configargparse.get_argument_parser()


AUTOSCALING = boto3.client("autoscaling")
ECS = boto3.client("ecs")


def terminate(aws_ecs_cluster_name, dry_run=True):
    """Selects a random node from the cluster and terminates it."""
    logger.info("working on terminating a random node from the cluster")

    nodes = []
    paginator = ECS.get_paginator("list_container_instances")
    pages = paginator.paginate(cluster=aws_ecs_cluster_name)
    for page in pages:
        nodes += page["containerInstanceArns"]

    container_instance_arn = random.choice(nodes)
    logger.info("container instance ARN of the selected node: {}",
                container_instance_arn)
    response = ECS.describe_container_instances(
        cluster=aws_ecs_cluster_name,
        containerInstances=[container_instance_arn]
    )

    # Assumes one result.
    # TODO: implement system to terminate a certain percentage of nodes instead.
    ec2_instance_id = response["containerInstances"][0]["ec2InstanceId"]
    logger.info("EC2 instance id of the selected node: {}", ec2_instance_id)

    if dry_run:
        logger.info("skipping node termination due to dry run")
    else:
        logger.info("terminating selected instance")
        AUTOSCALING.terminate_instance_in_auto_scaling_group(
            InstanceId=ec2_instance_id,
            ShouldDecrementDesiredCapacity=False
        )
