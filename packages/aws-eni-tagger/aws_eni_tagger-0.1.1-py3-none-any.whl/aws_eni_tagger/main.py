import boto3
import typer
from mypy_boto3_ec2 import EC2Client, type_defs

from aws_eni_tagger.table import show
from aws_eni_tagger.tags import Config, Tags, generate_additional_tags

app = typer.Typer()
AWSTags = list[type_defs.TagTypeDef]


def get_enis(client: EC2Client) -> list[type_defs.NetworkInterfaceTypeDef]:
    return client.describe_network_interfaces()["NetworkInterfaces"]


def get_ec2_client(profile: str, region: str) -> EC2Client:
    if profile:
        boto3.setup_default_session(profile_name=profile, region_name=region)
        return boto3.client("ec2")
    return boto3.client("ec2", region_name=region)


@app.command()
def main(
    profile: str = typer.Option(None, help="AWS profile name", envvar=["AWS_PROFILE", "AWS_VAULT"]),
    region: str = typer.Option(None, help="AWS region name", envvar=["AWS_REGION", "AWS_DEFAULT_REGION"]),
    owner_service_tag_name: str = typer.Option(
        default=Config.owner_service_tag_name,
        help="Key for tag with info about eni owner service ex: {'OwnerService': 'ec2'}",
    ),
    owner_service_name_tag_name: str = typer.Option(
        default=Config.owner_service_name_tag_name,
        help="Key for tag with info about eni owner service name ex: {'OwnerServiceName': 'i-12345'}",
    ),
    overwrite: bool = typer.Option(
        default=Config.overwrite,
        help="If set, the tags with the keys with name specified above/config will be overwritten",
    ),
):
    config = Config(
        overwrite=overwrite,
        owner_service_tag_name=owner_service_tag_name,
        owner_service_name_tag_name=owner_service_name_tag_name,
    )
    ec2_client = get_ec2_client(profile, region)
    enis = get_enis(ec2_client)
    additional_tags_for_enis: dict[str, dict] = {}
    for eni in enis:
        if additional_tags_for_eni := generate_additional_tags(eni, config):
            additional_tags_for_enis[eni["NetworkInterfaceId"]] = additional_tags_for_eni

    if not additional_tags_for_enis:
        typer.echo("Unable to find any additional info. Sorry :(")
        return

    # show
    show([{"eni": eni_id} | additional_tags for eni_id, additional_tags in additional_tags_for_enis.items()])

    # ask
    change_tags = typer.prompt("Add tags? yes/no") == "yes"

    if change_tags:
        for eni_id, aditional_tags in additional_tags_for_enis.items():
            tags_to_create = Tags.dict_to_aws_tags(aditional_tags)
            ec2_client.create_tags(Resources=[eni_id], Tags=tags_to_create)
