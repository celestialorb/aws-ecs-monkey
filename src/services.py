import boto3
import configargparse
import random

from loguru import logger


PARSER = configargparse.get_argument_parser()


ECS = boto3.client("ecs")


def roll(aws_ecs_cluster_name, dry_run=True):
    """Selects a random service from the cluster and forces a new deployment (rolls)."""
    logger.info("working on rolling a random service from the cluster")

    services = []
    paginator = ECS.get_paginator("list_services")
    pages = paginator.paginate(cluster=aws_ecs_cluster_name)
    for page in pages:
        services += page["serviceArns"]

    service_arn = random.choice(services)
    logger.info("ARN of the selected service: {}", service_arn)

    # Describe the service to obtain its name.
    response = ECS.describe_services(
        cluster=aws_ecs_cluster_name, services=[service_arn])

    # Assumes one result.
    service_name = response["services"][0]["serviceName"]
    logger.info("selected service name: {}", service_name)

    if dry_run:
        logger.info("skipping rolling of AWS ECS service due to dry run")
    else:
        logger.info("rolling selected AWS ECS service")
        ECS.update_service(
            cluster=aws_ecs_cluster_name,
            service=service_name,
            forceNewDeployment=True
        )
