# Examples of using Public API with Python  
Here we have a selection of Python3 scripts that shows each of the Public APIs being used.  These are not exhaustive and are definitely _not_ for production use.  They are merely here to get you started and, hopefully, to inspire you to come up with interesting ways to use the Public API that we've created.   

## Prerequisites
The following pieces need to be in place before you try the samples :-

* Created by using the Capella UX,  API Access and Secret Keys
* Python 3.9 or greater


## Running 
You will need to download the samples. To do this, either download [the archive](https://github.com/couchbasecloud/rest-api-examples.git) or clone the repository:

```
git clone https://github.com/couchbasecloud/rest-api-examples.git
```

change directory
```
cd rest-api-examples/python
```


There are several Python libraries that will need to be installed and these are listed in _requirements.txt_.  They can be automatically loaded using the _pip_ command:
```
pip install -r requirements.txt
```

Depending on how you have Python installed, you may need to call pip for Python3 like this
```
pip3 install -r requirements.txt
```

Next, set the environment variables for the base URL for Cloud API , access and secret keys.
replace <> by your values for secret and access keys.

```
export CBC_BASE_URL='https://cloudapi.cloud.couchbase.com'
export CBC_SECRET_KEY='<>'
export CBC_ACCESS_KEY='<>'
```

If you don't want use environment variables, you can store these in a file. 

In the capellaAPI folder, create EnvVars.py file and put in the values for access and secret key as indicated below.   

```
# Sets environmental variables used by capella API 

import os

# API URL
os.environ['CBC_BASE_URL'] = 'https://cloudapi.cloud.couchbase.com'


# Access key
os.environ['CBC_ACCESS_KEY'] = ' '

# Secret key
os.environ['CBC_SECRET_KEY'] = ' '

```


Launch a sample by running python with the relevant file e.g
 
```
python getClouds.py
2021-10-29 10:58:20,408 - capellaAPI.CapellaAPI - INFO - /v2/status
2021-10-29 10:58:20,777 - capellaAPI.CapellaAPI - INFO - /v2/clouds?perPage=100
Clouds
-------------------------------------------------------------------------------------------------------------------------------
|                  id                  |  name   | provider |  region   | status | virtualNetworkCIDR |   virtualNetworkID    |
-------------------------------------------------------------------------------------------------------------------------------
| 01a78132-344d-4bd9-a78c-4d57a90eda7c | Cloud01 | aws      | us-east-2 | ready  | 10.0.0.0/16        | vpc-0ab4165ce110e2027 |
-------------------------------------------------------------------------------------------------------------------------------

```
## Documentation
Documentation for the beta APIs can be found at https://docs.couchbase.com/cloud


## Tinkering
If you want to further develop the samples, then please feel free to do so.  The samples make use of the CapellaAPI class which can be found in capellaAPI folder.  That class is also a good starting point for improvements and building from. All of the code here has comments to help explain what's going on and why.
