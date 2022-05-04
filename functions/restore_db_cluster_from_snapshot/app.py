import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    client = boto3.client('rds')

    response = client.restore_db_cluster_from_snapshot(
        SnapshotIdentifier= event["DBClusterSnapshotIdentifier"],
        DBClusterIdentifier= event["DBClusterIdentifier"],
        Engine= event["Engine"],
        EngineVersion= event["EngineVersion"],
        DBSubnetGroupName= event["DBSubnetGroup"],
        VpcSecurityGroupIds= event["VpcSecurityGroupIds"],
        DeletionProtection= False
    )

    logger.info(response)

    return {
        "DBClusterIdentifier": response["DBCluster"]["DBClusterIdentifier"],
        "DBInstanceIdentifier": event["DBInstanceIdentifier"]
    }