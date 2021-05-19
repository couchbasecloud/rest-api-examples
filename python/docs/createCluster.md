 #  createCluster 
Creates a new cluster to the configuration specified in the Python script

Usage

python createCluster.py -cid/--cloudID, -pid/--projectID, -cn/--clusterName

Requires a cloudID, projectID and name for the cluster.   

- cloudID is a valid cloud ID and can be found by using listClouds.py
- projectID is a valid project ID and can be found by using listProjects.py
- cluster name is an alphanumeric string, without any special characters

To change the configuration of the cluster that is to be created, the Python script will need editing.  Modify "servers" in the cluster_configuration JSON.  This found in create_cluster function, as shown below 

```
def create_cluster(cloud_id, project_id, cluster_name):

    # This is the configuration of the cluster that will be created
    cluster_configuration = {
        "cloudId": cloud_id,
        "name": cluster_name,
        "projectId": project_id,
        "servers": [
            {
                "services": [
                    "data"
                ],
                "size": 3,
                "aws": {
                    "ebsSizeGib": 128,
                    "instanceSize": "m5.xlarge"
                }
            }
        ]
    }
```
On success you will see returned the endpoint to use to check the status of the new clusters deployment; this will include the new clusters ID.  Deployment can take several minutes and you can use the endpoint to see where it is at.  Alternatively, take the cluster ID and use it with checkCluster.py to obtain this information.


Example
```
python createCluster.py -cid b0bb69c0-c52f-4294-a022-c505fe5641f2 -pid d862216f-0cd5-444e-940a-25ad11ea2584 -cn ANewCluster001

Success. Resource status can be checked here:- /v2/clusters/fcf7186b-e253-4dd4-b459-0f09c32db539

```

 

 
 
 
 
