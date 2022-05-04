import os
import boto3
from operator import itemgetter

def lambda_handler(event, context):

  DBClusterIdentifier = event["DBClusterIdentifier"]

  client = boto3.client('rds')

  response = client.describe_db_cluster_snapshots(
    DBClusterIdentifier=DBClusterIdentifier,
    IncludePublic=False,
    IncludeShared=True,
  )
  
  list = response["DBClusterSnapshots"]
  
  sorted_list = sorted(list, key=itemgetter('SnapshotCreateTime'), reverse=True)

  latest_snapshot_id = {
    "DBClusterSnapshotIdentifier": sorted_list[0]["DBClusterSnapshotIdentifier"],
    "DBClusterIdentifier": DBClusterIdentifier
  }

  return latest_snapshot_id