# Cloud Public API Go Examples

A list of examples written in Go to interact with Couchbase Cloud Public API.
More details about the API:

https://docs.couchbase.com/cloud/public-api-guide/introducing-public-api.html

Basically this repository provides a tiny http client wrapper which generates
request headers using access/secret keys. Generated headers are requires to
interact with the API.

## Usage

### Environment variables

Environment variables provided below must be set in order to use API Client. You
can use `godotenv` (https://github.com/joho/godotenv) package to temporary
populate it using `.env` file. `.env` is located in `./examples` directory.

In order to get ACCESS/SECRET (or in other words api-key) you need to have
access to the Couchbase Cloud UI and have an admin user who has access to manage
the tenant.

```shell
ACCESS_KEY=
SECRET_KEY=
BASE_URL=https://cloudapi.cloud.couchbase.com
```

### Usage

Executing the command from `./examples` directory should list all tenant
projects.

```shell
godotenv -f .env go run ./get '/v2/projects' 
```

The response of each example consists of response `status code` and `body`

### Examples

#### addip

Adds an ip to a cluster's allowlist.

```shell
godotenv -f .env go run ./addip <cluster-id> <ip>
```

#### createbucket

Creates a bucket with `<bucket-name>` for a cluster.

```shell
godotenv -f .env go run ./createbucket <cluster-id> <bucket-name>
``` 

#### createproject

Creates a project with `<project-name>`

```shell
godotenv -f .env go run ./createproject <project-name>
``` 

#### createuser

Creates a Database User for a Cluster. Created user going to have full access to
a provided `<bucket>`

```shell
godotenv -f .env go run ./createuser <cluster-id> <username> <password> <bucket>
``` 

#### deploycluster

Initiates new Cluster deployment in connect Cloud. It creates a new project for
with a given `<project-name>`

```shell
godotenv -f .env go run ./deploycluster <cloud-id> <project-name> <cluster-name>
``` 

#### get

Send `GET` request to a given uri `<endpoint>`. For example: `./get '
/v2/projects' returns a list of projects.

```shell
godotenv -f .env go run ./get <endpoint>
``` 

#### getcertificate

Get Cluster's self-signed certificate

```shell
godotenv -f .env go run ./getcertificate <cluster-id>
``` 

#### health

Get Cluster's health stats. It includes bucket and node stats.

```shell
godotenv -f .env go run ./health <cluster-id>
``` 

#### pollbuckethealth

It checks bucket status for every 5 seconds till it becomes `healthy`

```shell
godotenv -f .env go run ./pollbuckethealth <cluster-id> <bucket-name>
``` 

#### pollclusterstatus

It checks cluster status for every 5 seconds till it becomes `ready`

```shell
godotenv -f .env go run ./pollclusterstatus <cluster-id>
``` 

#### status

Returns Public API Status. The endpoint does not require authentication.

```shell
godotenv -f .env go run ./status
``` 
