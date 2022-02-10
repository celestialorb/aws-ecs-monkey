import boto3
import configargparse
import random

from loguru import logger


PARSER = configargparse.get_argument_parser()


ECS = boto3.client("ecs")


def stop(aws_ecs_cluster_name, dry_run=True):
    """Selects a random task from the cluster and stops it."""
    logger.info("working on stopping a random task from the cluster")

    tasks = []
    paginator = ECS.get_paginator("list_tasks")
    pages = paginator.paginate(cluster=aws_ecs_cluster_name)
    for page in pages:
        tasks += page["taskArns"]

    task_arn = random.choice(tasks)
    logger.info("ARN of the selected task: {}", task_arn)

    if dry_run:
        logger.info("skipping stopping of AWS ECS task due to dry run")
    else:
        logger.info("stopping selected AWS ECS task")
        ECS.stop_task(
            cluster=aws_ecs_cluster_name,
            task=task_arn,
            reason="AWS ECS Monkey randomly stopped your task."
        )
