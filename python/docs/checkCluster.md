 #  checkCluster 

Gets information about a specified cluster

Usage

python checkCluster.py -cid/--clusterID


- clusterID is a valid cluster ID and can be found by using listClusters.py

On success you will see a JSON document that contains various pieces of information about the specified cluster

Example
```
python checkCluster.py -cid fcf7186b-e253-4dd4-b459-0f09c32db539

Cluster information found
{
  "cloudId": "b0bb69c0-c52f-4294-a022-c505fe5641f2",
  "createdAt": "2021-05-19T08:52:41.397446843Z",
  "deployedAt": "2021-05-19T08:52:46.279309087Z",
  "endpointsSrv": "fcf7186b-e253-4dd4-b459-0f09c32db539.dp.cloud.couchbase.com",
  "endpointsURL": [
    "cb-0000.fcf7186b-e253-4dd4-b459-0f09c32db539.dp.cloud.couchbase.com",
    "cb-0001.fcf7186b-e253-4dd4-b459-0f09c32db539.dp.cloud.couchbase.com",
    "cb-0002.fcf7186b-e253-4dd4-b459-0f09c32db539.dp.cloud.couchbase.com"
  ],
  "id": "fcf7186b-e253-4dd4-b459-0f09c32db539",
  "name": "ANewCluster001",
  "privateEndpointURL": [
    "cb-0000.fcf7186b-e253-4dd4-b459-0f09c32db539.internal.dp.cloud.couchbase.com",
    "cb-0001.fcf7186b-e253-4dd4-b459-0f09c32db539.internal.dp.cloud.couchbase.com",
    "cb-0002.fcf7186b-e253-4dd4-b459-0f09c32db539.internal.dp.cloud.couchbase.com"
  ],
  "projectId": "d862216f-0cd5-444e-940a-25ad11ea2584",
  "resourceIdentifier": "couchbase-deviot-anewcluster001-db539",
  "status": "ready",
  "tenantId": "aeb0e100-c511-404d-a025-1bc84b47d5b2",
  "updatedAt": "2021-05-19T09:01:13.552679421Z",
  "version": {
    "components": {
      "cbServerVersion": "enterprise-6.6.0",
      "componentVersion": "8b95ffbe",
      "metricsExporterVersion": "v1.0.0",
      "nodeImageVersion": "amazon-eks-node-1.16-v20200904",
      "operatorVersion": "2.0.3"
    },
    "name": "enterprise-6.6.0"
  }
}

```

 

 
 
 
 
