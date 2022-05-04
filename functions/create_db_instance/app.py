import boto3
import logging
import textwrap

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def describe_db_instance(identifier):
    db_instance_identifier = identifier

    client = boto3.client('rds')

    response = client.describe_db_instances(
        DBInstanceIdentifier=db_instance_identifier,
    )

    logger.info(response)

    instance = response["DBInstances"][0]

    security_groups = instance["VpcSecurityGroups"]

    VpcSecurityGroupIds = [d['VpcSecurityGroupId'] for d in security_groups]

    parameters = {
        "DBInstanceIdentifier": instance["DBInstanceIdentifier"] + "-dtq",
        "DBInstanceClass": instance["DBInstanceClass"],
        "Engine": instance["Engine"],
        "AvailabilityZone": instance["AvailabilityZone"],
        "DBSubnetGroupName": instance["DBSubnetGroup"]["DBSubnetGroupName"],
        "OptionGroupName": instance["OptionGroupMemberships"][0]["OptionGroupName"],
        "DBParameterGroupName": instance["DBParameterGroups"][0]["DBParameterGroupName"],
        "VpcSecurityGroupIds": VpcSecurityGroupIds,
        "DeletionProtection": False
    }

    return parameters

def lambda_handler(event, context):

    db_cluster_identifier = event["DBClusterIdentifier"]
    db_instance_identifier = event["DBInstanceIdentifier"]

    instance = describe_db_instance(db_instance_identifier)

    logger.info(instance)

    client = boto3.client('rds')

    #todo fix instance identifier lenght (max 63)
    response = client.create_db_instance(
        DBClusterIdentifier= db_cluster_identifier,
        DBInstanceIdentifier= instance["DBInstanceIdentifier"],
        DBInstanceClass= instance["DBInstanceClass"],
        Engine= instance["Engine"]
    )

    logger.info(response)

    return {
        "DBClusterIdentifier": db_cluster_identifier,
        "DBInstanceIdentifier": instance["DBInstanceIdentifier"]
    }