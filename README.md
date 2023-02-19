# COUCHBASE DOCUMENT COPIER
Copies your Couchbase documents from one bucket to another.

## Requirements
- Docker or Python 3.9
- Couchbase 6.6+ (ref. https://docs.couchbase.com/python-sdk/current/project-docs/compatibility.html#couchbase-versionsdk-version-matrix)

## Usage
Create `.env` file in main directory and set your environment properties. Then just simply run the `python3 main.py`.
To run with docker see instructions bellow.

### Configuration
Use environment variables.

| variable_name    | default_value | description                                                         |
|------------------|---------------|---------------------------------------------------------------------|
| SOURCE_HOST      |               | host address                                                        |
| SOURCE_BUCKET    |               | bucket name                                                         |
| SOURCE_USER      |               | username                                                            |
| SOURCE_PASS      |               | password                                                            |
| ID_QUERY         |               | query to select document ids to be transfered                       |
| TARGET_HOST      |               | host address                                                        |
| TARGET_BUCKET    |               | bucket name                                                         |
| TARGET_USER      |               | username                                                            |
| TARGET_PASS      |               | password                                                            |
| TARGET_OVERWRITE | 'false'       | set to 'true' if you do not want to skip already existing documents |
| BATCH_SIZE       | 10            | the batch for get / upsert multiple documents                       |


### LDAP Authentication
Add `?sasl_mech_force=PLAIN` to you connection string.

### Build docker image
```sh
docker build -t drajnic/couchbase-copier .
```

### Run with docker
```sh
docker run --rm -it --env SOURCE_HOST='localhost' --env SOURCE_BUCKET='source_bucket' --env SOURCE_USER='admin' --env SOURCE_PASS='password' --env ID_QUERY="SELECT META().id FROM source_bucket" --env TARGET_HOST='localhost' --env TARGET_BUCKET='target_bucket' --env TARGET_USER='admin' --env TARGET_PASS='password' --network host drajnic/couchbase-copier
```

## Development

### Init virtualenv
```sh
python3 -m venv ./virtualenv
```

### Activate virtualenv
```sh
source ./virtualenv/bin/activate
```

### Install new package with
```sh
pip install couchbase && pip freeze > requirements.txt
```
