[![FivexL](https://releases.fivexl.io/fivexlbannergit.jpg)](https://fivexl.io/)
# AWS ENI Tagger
This CLI tool adds meaningful tags to your AWS Elastic Network Interfaces (ENIs) based on information obtained from aws-eni-idetifier.
#### Before:
![before.png](https://github.com/fivexl/aws-eni-tagger/raw/master/docs/before.jpg?raw=true)

#### After:
![after.png](https://github.com/fivexl/aws-eni-tagger/raw/master/docs/after.png?raw=true)

# Installation

```bash
pip install aws-eni-tagger
```

# Usage
```bash
aws-eni-tagger --profile my-aws-profile
```
## Arguments:

The CLI takes the following arguments:

  * **--profile**: AWS profile name. Required.
    
  * **--owner-service-tag-name**: Key for tag with information about the ENI owner service. Default is 'OwnerService'.
    
  * **--owner-service-name-tag-name**: Key for tag with information about the ENI owner service name. Default is 'OwnerServiceName'.
  
  * **--overwrite**: If set, the tags with the keys with name specified above/config will be overwritten. Default is False.

For example:

```bash
aws-eni-tagger --profile my_aws_profile --overwrite
```

This will run the aws-eni-tagger with the specified AWS profile and will overwrite existing tags.

# Developing

Install the package:
```bash
poetry install
```
Run tests:
```bash
poetry run pytest
```
