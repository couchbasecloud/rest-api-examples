# Sample Python apps  
Here you will find a number of a sample Python applications that demonstrate using various features of the Couchbase Cloud Public API to automate operations. 

To use any of these samples, follow the instructions below


## Prerequisites
The following pieces need to be in place

* Created Access and Secret Keys for the API
* Python 3.8 or greater


## Running 
You will need to download the samples. To do this, either download [the archive](https://github.com/couchbasecloud/rest-api-examples.git) or clone the repository:

```
$ git clone https://github.com/couchbasecloud/rest-api-examples.git
```

change directory
```
$ cd rest-api-examples/python
```


There are several Python libraries that will need to be installed and these are listed in _requirements.txt_.  They can be automatically loaded using the _pip_ command:
```
$ pip install -r requirements.txt
```

Next, set the environment variables for the base URL for Cloud API , access and secret keys.
replace <> by your values for secret and access keys.

```
$ export cbc_base_url='https://cloudapi.cloud.couchbase.com'
$ export cbc_secret_key='<>'
$ export cbc_access_key='<>'
```

Launch the application by running the relevant file from a terminal e.g
 
```
$ python listClouds.py
```
## Documentation

Documentation for each of the samples can be found in the docs folder. 

Documentation for the beta APIs can be found at https://docs.couchbase.com/cloud/public-api-guide/introducing-public-api.html 
