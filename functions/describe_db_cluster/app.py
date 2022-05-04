import os
import boto3
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
  
  db_cluster_snapshot_identifier = event["DBClusterSnapshotIdentifier"]
  db_cluster_identifier = event['DBClusterIdentifier']

  client = boto3.client('rds')

  response = client.describe_db_clusters(
    DBClusterIdentifier=db_cluster_identifier,
  )

  logger.info(response)

  instance = response["DBClusters"][0]

  security_groups = instance["VpcSecurityGroups"]

  VpcSecurityGroupIds = [d['VpcSecurityGroupId'] for d in security_groups]

  db_instance_identifier = instance["DBClusterMembers"][0]["DBInstanceIdentifier"]

  parameters = {
    "DBClusterSnapshotIdentifier": db_cluster_snapshot_identifier,
    "DBClusterIdentifier": instance["DBClusterIdentifier"] + "-datamasque",
    "Engine": instance["Engine"],
    "EngineVersion": instance["EngineVersion"],
    "DBSubnetGroup": instance["DBSubnetGroup"],
    "VpcSecurityGroupIds": VpcSecurityGroupIds,
    "DeletionProtection": False,
    "DBInstanceIdentifier": db_instance_identifier
  }

  return parameters