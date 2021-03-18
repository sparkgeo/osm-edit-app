import os
from aws_cdk import (
    core,
    aws_ec2 as ec2,
)

from types import SimpleNamespace

CommonConfig = {
    "env":
        core.Environment(
            account=os.getenv("AWS_ACCT_ID"),
            region=os.getenv("AWS_REGION", "us-east-1")
        ),
}

ProdConfig = SimpleNamespace(
    env_id="prod",
    cidr_block="10.0.0.0/16",
    # TODO update the below to match Dev.
    # rds_multi_az=True,
    # rds_instance_type=ec2.InstanceType.of(
    #     ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM
    # ),
    # Put additional config above here.
    **CommonConfig
)

DevConfig = SimpleNamespace(
    env_id="dev",
    cidr_block="10.10.0.0/16",
    private_dns_name="securemaps-dev",
    rds=SimpleNamespace(
        multi_az=False,
        instance_type=ec2.InstanceType.of(
            ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO
        ),
    ),
    osm_web=SimpleNamespace(
        cpu=512,
        memory=1024,
        count=1,
    ),
    # Put additional config above here.
    **CommonConfig
)

# TODO refactor if more envs are added.
EnvConfig = ProdConfig if os.getenv("ENVIRONMENT").lower() in [
    "production", "prod"
] else DevConfig
