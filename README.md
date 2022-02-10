# aws-ecs-monkey
A relatively simple project to introduce elements of chaos engineering to an AWS ECS cluster.

_Please keep in mind that this project is in a very early stage and may be subject to breaking changes._

## Usage
This project is very early stages, so usage remains simple and straight-forward. Currently there are only two options
that can be set via the CLI or by environment variables. Usage information can be gathered from the `--help` flag.

The container image uses the Python script as an entrypoint, so adding the appropriate flags should be all that's necessary.

The main argument is the action type. This project currently provides three different ways of injecting chaos into the cluster:
1. `nodes`: termination of a random node
2. `services`: force deployment of a random service
3. `tasks`: stops a random task

```
usage: main.py [-h] [-c CONFIG_FILE] [--cluster-name CLUSTER_NAME] [--action-type {nodes,services,tasks}] [--action-dry-run]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config-file CONFIG_FILE
  --cluster-name CLUSTER_NAME
                        The name of the AWS ECS cluster to inject chaos into. [env var: AWS_ECS_MONKEY_CLUSTER_NAME] (default: None)
  --action-type {nodes,services,tasks}
                        The type of chaos action to inject, only one can be specified. [env var: AWS_ECS_MONKEY_ACTION_TYPE] (default: None)
  --action-dry-run      If provided, no actions will be taken against the cluster. [env var: AWS_ECS_MONKEY_ACTION_DRY_RUN] (default: False)

Args that start with '--' (eg. --cluster-name) can also be set in a config file (specified via -c). Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (for details, see syntax at https://goo.gl/R74nmi). If an arg is specified in more than one place, then commandline values override environment variables which override config file values which override defaults.
```

## Suggestions
If you have any suggestions, feel free to open an issue.

Some random ideas I have in mind:
- Inclusion/exclusion based off of AWS tags on ECS resources.
- Inclusion/exclusion based off of Docker labels in ECS tasks.
- Ability to inject larger amount of chaos (i.e. disrupt more than one resource at a time)

## AWS IAM Permissions
Since this project interacts with the AWS API, it will need to be given the proper AWS IAM permissions. This project makes use of the following actions:
- autoscaling:TerminateInstanceInAutoScalingGroup
- ecs:DescribeContainerInstances
- ecs:DescribeServices
- ecs:ListContainerInstances
- ecs:ListTasks
- ecs:ListServices
- ecs:StopTask
- ecs:UpdateService

## Donate
If you found that this project helped you out, or want to encourage further development feel free to make a small donation!

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate/?hosted_button_id=EA8JUE2CKVPS2)
