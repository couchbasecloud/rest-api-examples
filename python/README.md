# CloudPublicAPISample
This is a sample application to demonstrate using Couchbase Cloud Public API to automate operations.  
The application lists the cloud connections


## Prerequisites
The following pieces need to be in place in order to run the application.

* Admission into the Restricted Beta
* Access and Secret Keys for authentication to the API
* Python 3.0 or greater


## Running the application
To download the application you can either download [the archive](https://github.com/couchbaselabs/cloud_public_api_sample) or clone the repository:

```
$ git clone https://github.com/couchbaselabs/cloud_public_api_sample
```

change directory
```
$ cloud_public_api_sample
```


The application uses several Python libraries that need to be installed, this are listed in _requirements.txt_ and can be automatically loaded using the _pip_ command:
```
$ pip install -r requirements.txt
```

set environment variables for the base URL , access and secret keys.
replace <> by your values for secret and access keys.

```
$ export cbc_base_url='https://cloudapi.cloud.couchbase.com'
$ export cbc_secret_key='<>'
$ export cbc_access_key='<>'
```

Launch the application by running the _cloud_public_api_sample.py_ file from a terminal.
 
```
$ python cloud_public_api_sample.py
```
## Documentation
Documentation for the beta APIs can be found at https://docs.couchbase.com/cloud/public-api-guide/introducing-public-api.html 
