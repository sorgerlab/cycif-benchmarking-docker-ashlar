# CycIF Benchmarking - ASHLAR

This Docker image is designed for use within AWS BATCH.

## Job configuration YAML

A YAML file containing the configuration for a job must be provided to the
container. Each configuration has the form:

```yaml
inputs:
  - s3://example/dataset1/raw/cycle1.rcpnl
  - s3://example/dataset1/raw/cycle2.rcpnl
output: s3://example/dataset1/ashlar/
arguments:
  - /mnt/input/*.rcpnl
```

All `inputs` are copied into the `/mnt/input` directory in the Docker container.
If an input is suffixed with a `/` it is recursively copied to `/mnt/input` so
that the relative directory structure is maintained.

`arguments` is passed directly to `ashlar` so a series of options can be
specified as a list. No default is provided to `ashlar` for the required
`filepaths` positional argument so this must be specified.

This configuration file's location in S3 is passed to the docker container as
the only argument or can alternatively be passed as a string in the environment
variable `CONFIG`.

## Local usage

This image can be used locally as long as appropriate environment variables
are set when instantiating the docker container.

```bash
# Passing the configuration file's location in S3
docker run \
  -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
  -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
  -e AWS_SESSION_TOKEN="${AWS_SESSION_TOKEN}" \
  cycif-benchmarking-ashlar:latest \
  s3://example/config.yml

# Passing the configuration as an environment variable
docker run \
  -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
  -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
  -e AWS_SESSION_TOKEN="${AWS_SESSION_TOKEN}" \
  -e "CONFIG=$(<config.yml)" \
  cycif-benchmarking-ashlar:latest
```

It is recommended to use a session token inside the Docker container, which can
be generated using the AWS CLI.

```bash
aws sts get-session-token
```
