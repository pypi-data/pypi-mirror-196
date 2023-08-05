from collections import UserDict
from dataclasses import dataclass

import aws_eni_identifier
from mypy_boto3_ec2 import type_defs

AWSTags = list[type_defs.TagTypeDef]


@dataclass
class Config:
    overwrite: bool = False
    owner_service_tag_name: str = "OwnerService"
    owner_service_name_tag_name: str = "OwnerServiceName"


class Tags(UserDict):
    def __init__(self, aws_tags: AWSTags):
        self.data = self.aws_tags_to_dict(aws_tags)

    @staticmethod
    def aws_tags_to_dict(aws_tags: AWSTags) -> dict[str, str]:
        return {tag["Key"]: tag["Value"] for tag in aws_tags}

    @staticmethod
    def dict_to_aws_tags(tags: dict[str, str]) -> AWSTags:
        return [{"Key": k, "Value": v} for k, v in tags.items()]


def generate_additional_tags(eni: type_defs.NetworkInterfaceTypeDef, config: Config) -> dict[str, str]:
    original_tags = Tags(eni.get("TagSet", []))
    eni_info = aws_eni_identifier.identify_eni(eni)

    service = eni_info.get("svc")
    service_name = eni_info.get("name")

    generated_tags: dict[str, str] = {}
    if service and ((config.owner_service_tag_name not in original_tags) or config.overwrite):
        generated_tags[config.owner_service_tag_name] = service
    if service_name and ((config.owner_service_name_tag_name not in original_tags) or config.overwrite):
        generated_tags[config.owner_service_name_tag_name] = service_name
    return generated_tags
